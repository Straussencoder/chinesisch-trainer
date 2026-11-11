import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, shutil
sys.path.insert(0, ROOT + "/scripts"); import fontroute
O = ROOT + "/shots/v5/"
shutil.copy(ROOT + "/zh-app/test.html", ROOT + "/test/index.html")
views = sys.argv[1].split(",") if len(sys.argv) > 1 else ["lernen"]
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for dev, (w, h) in [("m", (390, 844)), ("d", (1366, 900))]:
        for scheme in ["light", "dark"]:
            ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = ctx.new_page(); fontroute.setup(pg)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(900)
            pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today();
              T.LESSONS.slice(0, 5).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t, 1)}); });
              Object.keys(s.words).slice(0, 7).forEach(k => s.words[k].d = t);
              s.days[t] = {tones:0, toneOk:0, cards:0, neu:0, xp:12, lessons:3, reviews:0, games:0}; location.hash = 'wiederholen'; }""")
            pg.wait_for_timeout(300)
            for v in views:
                pg.evaluate(f"() => {{ location.hash = '{v}'; }}"); pg.wait_for_timeout(1300)
                pg.screenshot(path=O+f"q_{dev}_{scheme}_{v}.png")
            ov = pg.evaluate("() => document.scrollingElement.scrollWidth - innerWidth")
            if ov: errs.append(f"overflow {dev} {scheme} {ov}")
            ctx.close()
    b.close()
print("Fehler:", errs or "keine")
