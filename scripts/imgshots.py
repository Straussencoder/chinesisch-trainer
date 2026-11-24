# Bildschirmfotos aller Etappen-Bilder: Startbild (hero) je Etappe und Lernpfad, Handy und Mac
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
from playwright.sync_api import sync_playwright
O = ROOT + "/shots/img/"; _os.makedirs(O, exist_ok=True)
scheme = sys.argv[1] if len(sys.argv) > 1 else "light"
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(375, 740), (1280, 800)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = ctx.new_page(); fontroute.setup(pg)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("fehlt: " + r.url) if "/img/" in r.url else None)
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(500)
        n = pg.evaluate("() => window.__t.LESSONS.length")
        seen = set()
        for i in range(n):
            sc = pg.evaluate("""(i) => { const T = window.__t, s = T.state(), t = T.today();
              s.learn.done = {}; T.LESSONS.slice(0, i).forEach(l => s.learn.done[l.id] = {at:t, best:100});
              const sc = (T.LESSONS[i].scene || ''); location.hash = 'x'; location.hash = 'lernen'; return document.querySelector('#hero-art img') ? document.querySelector('#hero-art img').getAttribute('src') : 'svg'; }""", i)
            pg.wait_for_timeout(400)
            src = pg.evaluate("() => { const im = document.querySelector('#hero-art img'); return im ? im.getAttribute('src') : 'svg'; }")
            if src in seen: continue
            seen.add(src)
            pg.wait_for_function("() => { const im = document.querySelector('#hero-art img'); return !im || (im.complete && im.naturalWidth > 0); }", timeout=5000)
            pg.locator("#hero").screenshot(path=O + f"{scheme}_{w}_hero_{_os.path.basename(src).split('.')[0]}.png")
        print(w, "Startbilder:", sorted(seen))
        pg.evaluate("() => { location.hash = 'x'; location.hash = 'lernen'; }"); pg.wait_for_timeout(500)
        pg.evaluate("async () => { for (const im of document.querySelectorAll('img')) { im.loading = 'eager'; } }")
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(1500)
        bad = pg.evaluate("() => [...document.querySelectorAll('img.scene-img')].filter(im => !(im.complete && im.naturalWidth)).map(im => im.src)")
        cnt = pg.evaluate("() => [document.querySelectorAll('.st-art img.scene-img').length, document.querySelectorAll('.st-art svg').length]")
        print(w, "Lernpfad Bilder/SVG:", cnt, "nicht geladen:", bad)
        pg.screenshot(path=O + f"{scheme}_{w}_pfad.png", full_page=True)
        ctx.close()
print("Fehler:", errs)
