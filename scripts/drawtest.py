# Prüft "Zeichen schreiben": Übung in Lektionen, Einstellung, Übungsrunde mit nachgezogenen Strichen, Fehlversuche, Überspringen, fehlende Datei.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, os, shutil
sys.path.insert(0, ROOT + "/scripts"); import fontroute
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
def trace(pg, ch, k, bad=False):
    med = pg.evaluate("([c,k]) => window.ZH_STROKES[c].medians[k]", [ch, k])
    box = pg.locator("#draw-pad").bounding_box(); size = box["width"]; pad = round(size*0.06); sc = (size - 2*pad)/1024
    pts = [(box["x"] + pad + x*sc, box["y"] + pad + (900 - y)*sc) for x, y in med]
    if bad: pts = pts[::-1]
    pg.mouse.move(*pts[0]); pg.mouse.down()
    for a, b2 in zip(pts, pts[1:]):
        for t in range(1, 6): pg.mouse.move(a[0] + (b2[0]-a[0])*t/5, a[1] + (b2[1]-a[1])*t/5)
    pg.mouse.up(); pg.wait_for_timeout(110)
SETUP = """(n) => { const T = window.__t, s = T.state(), t = T.today(); T.LESSONS.slice(0, n).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t,1)}); }); location.hash='wiederholen'; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for view, (w, h) in (("mobile", (390, 844)), ("desktop", (1366, 900))):
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); fontroute.setup(pg)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(500)
        # Lektionen: genau eine Schreibübung, mit einem neuen Zeichen
        bad = pg.evaluate("() => window.__t.LESSONS.filter(l => { const q = window.__t.buildLesson(l).filter(e => e.type==='draw'); return q.length !== 1 || !q[0].outline || Array.from(q[0].w.zh).indexOf(q[0].ch) < 0 || q[0].w.lesson !== l || !window.ZH_STROKES || false; }).map(l => l.id)")
        ok(pg.evaluate("() => window.__t.LESSONS.every(l => window.__t.buildLesson(l).filter(e => e.type==='draw').length === 1)"), f"{view}: jede Lektion hat genau ein Zeichen zum Nachziehen")
        pg.evaluate("() => { window.__t.state().prefs.draw = false; }")
        ok(pg.evaluate("() => window.__t.LESSONS.every(l => window.__t.buildLesson(l).filter(e => e.type==='draw').length === 0)"), f"{view}: Einstellung aus = keine Schreibübung")
        pg.evaluate("() => { window.__t.state().prefs.draw = true; }")
        pg.evaluate(SETUP, 6); pg.wait_for_timeout(300)
        ok(pg.locator(".drawcard:not(.testcard):not(.sentcard):not(.numcard):not(.hskcard):not(.saycard):not(.txtcard):not(.lsncard)").count() == 1, f"{view}: Karte »Zeichen schreiben« unter Wiederholen")
        pg.click('[data-act="drawprac"]'); pg.wait_for_timeout(300)
        nq = pg.evaluate("() => window.__t.getS().queue.length")
        ok(nq == 6, f"{view}: Übungsrunde mit 6 Zeichen ({nq})")
        done = 0
        for i in range(6):
            pg.wait_for_function("() => { const e = window.__t.getS().queue[0]; return e && e.strokes > 0 && e.writer; }", timeout=8000)
            e = pg.evaluate("() => { const e = window.__t.getS().queue[0]; return {ch:e.ch, n:e.strokes, outline:e.outline}; }")
            if i == 2:
                pg.click('[data-act="drawskip"]'); pg.wait_for_timeout(250); continue
            if e["outline"]: pg.wait_for_timeout(e["n"]*900 + 1400)
            else: pg.wait_for_timeout(300)
            if i == 0: trace(pg, e["ch"], 0, bad=True)
            for k in range(e["n"]): trace(pg, e["ch"], k)
            pg.wait_for_timeout(1100)
            st = pg.evaluate("() => { const S = window.__t.getS(); return {ans:S.answered, miss:S.queue[0].miss}; }")
            ok(st["ans"] and (st["miss"] == (1 if i == 0 else 0)), f"{view}: {e['ch']} ({e['n']} Striche) nachgezogen, Fehlstriche {st['miss']}")
            done += 1
            pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
        fin = pg.evaluate("() => { const S = window.__t.getS(); return S && S.finished ? {xp:S.finished.xp, drawn:S.drawn} : null; }")
        ok(fin and fin["drawn"] == 5 and fin["xp"] == 10, f"{view}: Abschluss zählt 5 geschriebene Zeichen, 10 Punkte {fin}")
        saved = pg.evaluate("() => Object.keys(window.__t.state().draw).length")
        ok(saved == 5, f"{view}: 5 Zeichen gespeichert, übersprungenes nicht ({saved})")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(200)
        # zweite Runde: geübte Zeichen ohne Vorlage, ungeübte zuerst
        pg.click('[data-act="drawprac"]'); pg.wait_for_timeout(200)
        first = pg.evaluate("() => { const S = window.__t.getS(); return S.queue.map(e => e.outline); }")
        ok(first[0] is True, f"{view}: ungeübte Zeichen kommen zuerst ({first})")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
        ok(not errs, f"{view}: keine JS-Fehler {errs[:3]}")
        ctx.close()
    # Datei fehlt
    ctx = b.new_context(); pg = ctx.new_page()
    pg.route("**/schreiben.js", lambda r: r.abort())
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(300)
    pg.evaluate(SETUP, 2); pg.wait_for_timeout(200); pg.click('[data-act="drawprac"]'); pg.wait_for_timeout(800)
    ok("nicht geladen" in pg.inner_text("#draw-pad"), "Datei fehlt: verständlicher Hinweis")
    pg.click('[data-act="drawskip"]'); pg.wait_for_timeout(300)
    ok(pg.evaluate("() => window.__t.getS().queue.length") == 5, "Datei fehlt: Überspringen geht weiter")
    ok(not errs, f"Datei fehlt: keine JS-Fehler {errs}")
    b.close()
print("\n".join(res))
