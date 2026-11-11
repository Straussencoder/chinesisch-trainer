# Prüft die Gespräche: alle 17 durchspielen (falsch, dann richtig), Sperre, Tastatur, Banner, Abschluss, Speicherstand.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0, ROOT + "/scripts"); import fontroute
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
STATE = "() => { const S = window.__t.getS(); return S ? {w:S.waiting, i:S.i, shown:S.shown, n:S.d.lines.length, fin:!!S.finished, opts:S.opts && S.opts.map(o => !!o.ok)} : null; }"
OVER = "() => { const m = document.querySelector('#session'); return m ? [...m.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + 1 || r.left < -1); }).map(e => e.className).slice(0, 4) : []; }"
def mark(pg, upto, dlg=None):
    pg.evaluate("""([upto, dlg]) => { const T = window.__t, s = T.state(), t = T.today(); s.learn.done = {}; s.learn.dlg = dlg || {};
      T.LESSONS.slice(0, upto).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t, 1)}); }); location.hash = 'saetze'; }""", [upto, dlg or {}])
    pg.wait_for_timeout(150); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(350)
with sync_playwright() as p:
    b = p.chromium.launch()
    for view, (w, h) in (("mobile", (390, 844)), ("desktop", (1366, 900))):
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); fontroute.setup(pg)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(600)
        # gesperrt vor der Etappe
        mark(pg, 1)
        ok(pg.locator('[data-dlg="u1"]').first.is_disabled(), f"{view}: Gespräch 1 gesperrt, solange Etappe 1 offen ist")
        pg.evaluate("() => window.__t.startDialog('u1')"); ok(pg.evaluate("() => !window.__t.getS()"), f"{view}: gesperrtes Gespräch startet nicht")
        ok(pg.locator(".dl-banner:not(.day-banner)").count() == 0, f"{view}: kein Banner ohne geschaffte Etappe")
        units = pg.evaluate("() => window.__t.UNITS.map(u => [u.id, u.lessons[u.lessons.length-1].n])")
        todo = units if view == "mobile" else units[8:10]
        for uid, lastn in todo:
            prior = {u: {"at": "2026-11-01", "best": 100} for u, _ in units[:[x for x, _ in units].index(uid)]}
            mark(pg, lastn, prior)
            node = pg.locator(f'.node.dl[data-dlg="{uid}"]')
            cls = node.get_attribute("class") or ""
            banner = pg.locator(f'.dl-banner[data-dlg="{uid}"]').count()
            if uid in ("u1", "u9"): ok("avail" in cls and banner == 1, f"{view} {uid}: Knoten bereit ({cls}), Banner da ({banner})")
            node.scroll_into_view_if_needed(); node.click(); pg.wait_for_timeout(250)
            wrong_seen = why_ok = True; steps = 0
            while steps < 40:
                steps += 1
                st = pg.evaluate(STATE)
                if not st or st["fin"]: break
                if st["w"]:
                    bad = st["opts"].index(False)
                    pg.keyboard.press(str(bad + 1)); pg.wait_for_timeout(120)
                    if not pg.is_visible(".dl-why") or not pg.locator(f'[data-dopt="{bad}"]').is_disabled(): why_ok = False
                    s2 = pg.evaluate(STATE)
                    if not s2["w"]: wrong_seen = False
                    pg.click(f'[data-dopt="{st["opts"].index(True)}"]'); pg.wait_for_timeout(150)
                    if pg.locator(".dl-why").count(): why_ok = False
                else:
                    if uid == "u5" and steps == 3: pg.keyboard.press(" ")
                    pg.keyboard.press("Enter"); pg.wait_for_timeout(120)
            if view == "mobile" and uid in ("u2", "u11"):
                pg.screenshot(path=f"{ROOT}/shots/r2/dt_{uid}_fin.png")
            st = pg.evaluate("() => { const S = window.__t.getS(); return S && S.finished ? {pct:S.finished.pct, xp:S.finished.xp} : null; }")
            nrows = pg.locator(".dl-sum .dl-row").count(); nlines = pg.evaluate(f"() => window.__t.DIALOGS['{uid}'].lines.length")
            saved = pg.evaluate(f"() => window.__t.state().learn.dlg['{uid}']")
            ok(st and st["pct"] == 0 and nrows == nlines and saved and wrong_seen and why_ok, f"{view} {uid}: durchgespielt, Fehler erklärt, {nrows}/{nlines} Zeilen im Rückblick, gespeichert {saved}")
            ov = pg.evaluate(OVER); ok(not ov, f"{view} {uid}: nichts ragt über den Rand {ov}")
            pg.click('[data-act="exit"]') if pg.locator('[data-act="exit"]').count() else pg.keyboard.press("Escape")
            pg.wait_for_timeout(200)
            cls2 = pg.locator(f'.node.dl[data-dlg="{uid}"]').get_attribute("class") or ""
            if uid in ("u1", "u9"): ok("done" in cls2 and pg.locator(f'.dl-banner[data-dlg="{uid}"]').count() == 0, f"{view} {uid}: danach als geschafft markiert ({cls2})")
        # alles richtig auf Anhieb -> 100 % und Bonus
        mark(pg, 2)
        pg.evaluate("() => window.__t.startDialog('u1')"); pg.wait_for_timeout(200)
        for _ in range(20):
            st = pg.evaluate(STATE)
            if not st or st["fin"]: break
            if st["w"]: pg.click(f'[data-dopt="{st["opts"].index(True)}"]')
            else: pg.click("#s-next")
            pg.wait_for_timeout(100)
        fin = pg.evaluate("() => window.__t.getS().finished")
        ok(fin and fin["pct"] == 100 and fin["xp"] == 15, f"{view}: ohne Fehler 100 % und 15 Punkte {fin}")
        if view == "mobile": pg.screenshot(path=ROOT + "/shots/r2/dt_fin100.png")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(200)
        # Abschluss der letzten Lektion einer Etappe bietet das Gespräch an
        mark(pg, 17)
        pg.evaluate("() => window.__t.startLesson('l18')"); pg.wait_for_timeout(200)
        pg.evaluate("() => { const S = window.__t.getS(); S.queue = [S.queue.find(e => e.type==='intro') || S.queue[0]]; window.__t.renderSession(); }")
        pg.click("#s-next"); pg.wait_for_timeout(500)
        ok(pg.locator('#session [data-dlg="u9"]').count() == 1, f"{view}: nach Etappe 9 wird das Gespräch angeboten")
        pg.click('#session [data-dlg="u9"]'); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => { const S = window.__t.getS(); return !!S && S.kind==='dialog' && S.unit.id==='u9'; }"), f"{view}: Knopf startet das Gespräch")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => !window.__t.getS()"), f"{view}: Abbrechen mit Escape (zweimal) schließt")
        ok(not errs, f"{view}: keine JS-Fehler {errs[:3]}")
        ctx.close()
    # alter Speicherstand ohne Gespräche
    ctx = b.new_context(); pg = ctx.new_page()
    pg.add_init_script("localStorage.setItem('zh-trainer-v1', JSON.stringify({v:3, learn:{done:{l1:{at:'2026-10-01', best:90}, l2:{at:'2026-10-02', best:80}}}, words:{}, prefs:{}}))")
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(400)
    ok(pg.evaluate("() => JSON.stringify(window.__t.state().learn.dlg)") == "{}" and pg.locator('.dl-banner[data-dlg="u1"]').count() == 1, "alter Stand: Gespräche leer, Gespräch 1 angeboten")
    ok(not errs, f"alter Stand: keine JS-Fehler {errs}")
    b.close()
print("\n".join(res))
