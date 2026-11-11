# Prüft den Wochen-Test: Zusammenstellung, keine zweite Chance, Speichern, Verlauf, Hinweis auf der Startseite.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
STEP = open(ROOT + "/scripts/fulltest.py").read()
STEP = STEP[STEP.index('STEP = """')+10:STEP.index('"""', STEP.index('STEP = """')+10)]
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
def play(pg, wrong_every=0):
    n = 0
    for _ in range(40):
        st = pg.evaluate(STEP)
        if st.get("finished") or st.get("none"): break
        t = st["type"]
        n += 1; wrong = wrong_every and n % wrong_every == 0
        if t in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'[data-opt="{(st["right"]+1)%st.get("nopt",3) if wrong else st["right"]}"]')
        elif t == "write": pg.fill("#w-in", "xx" if wrong else st["typed"]); pg.keyboard.press("Enter")
        elif t == "tone": pg.click(f'[data-stone="{(st["tone"]%4)+1 if wrong else st["tone"]}"]')
        elif t == "build":
            for i in (list(reversed(st["order"])) if wrong else st["order"]): pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }")
        pg.wait_for_timeout(60); pg.click("#s-next"); pg.wait_for_timeout(60)
    return n
with sync_playwright() as p:
    b = p.chromium.launch()
    for view, (w, h) in (("mobile", (390, 844)), ("desktop", (1366, 900))):
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); fontroute.setup(pg)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(500)
        pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(); T.LESSONS.slice(0, 1).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:t}); }); location.hash='wiederholen'; }""")
        pg.wait_for_timeout(300)
        ok(pg.locator('.testcard [data-act="test"]').is_disabled(), f"{view}: Test gesperrt unter 10 Wörtern")
        pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(); T.LESSONS.slice(0, 12).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t,1)}); }); s.learn.dlg = {}; T.UNITS.forEach(u => s.learn.dlg[u.id] = {at:t, best:100}); location.hash='saetze'; }""")
        pg.wait_for_timeout(200); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(400)
        ok(pg.locator('.dl-banner[data-act="test"]').count() == 1, f"{view}: Startseite weist auf den Test hin")
        pg.click('.dl-banner[data-act="test"]'); pg.wait_for_timeout(300)
        q = pg.evaluate("() => window.__t.getS().queue.map(e => e.type)")
        ok(len(q) == 15 and q.count("build") == 3 and q.count("tone") == 2, f"{view}: 15 Fragen, 3 Sätze, 2 Töne {q}")
        n = play(pg, wrong_every=5)
        fin = pg.evaluate("() => window.__t.getS().finished")
        ok(n == 15 and fin and fin["pct"] == 80, f"{view}: keine zweite Chance ({n} Fragen), 3 Fehler = 80 % {fin}")
        ok(pg.locator(".finish .rr-w.bad").count() == 3, f"{view}: drei Fehler im Rückblick")
        if view == "mobile": pg.screenshot(path=ROOT + "/shots/r2/wtest_fin1.png")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(200)
        ok(pg.evaluate("() => !window.__t.testDue()") and pg.locator('.dl-banner[data-act="test"]').count() == 0, f"{view}: nach dem Test kein Hinweis mehr")
        pg.evaluate("() => { location.hash='wiederholen'; }"); pg.wait_for_timeout(300)
        ok("80 %" in pg.inner_text(".testcard"), f"{view}: Karte zeigt letztes Ergebnis")
        pg.click('.testcard [data-act="test"]'); pg.wait_for_timeout(200); play(pg)
        ok(pg.locator(".tbars .tbar").count() == 2 and "Besser" in pg.inner_text(".finish"), f"{view}: Verlauf mit 2 Tests, Vergleich zum letzten Mal")
        if view == "mobile": pg.screenshot(path=ROOT + "/shots/r2/wtest_fin2.png")
        ok(len(pg.evaluate("() => window.__t.state().tests")) == 2, f"{view}: zwei Ergebnisse gespeichert")
        pg.click('[data-act="exit"]'); ok(not errs, f"{view}: keine JS-Fehler {errs[:3]}")
        ctx.close()
    b.close()
print("\n".join(res))
