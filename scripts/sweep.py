# Darstellung auf vielen Breiten: Startseite, Spielhalle, Rennen, Ergebnis, Übung; prüft Überlauf
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0, ROOT + "/scripts"); import fontroute
O = ROOT + "/shots/v5/"
SIZES = [(320, 640), (375, 667), (768, 1024), (1024, 768), (1920, 1080)]
scheme = sys.argv[1] if len(sys.argv) > 1 else "light"
hz = len(sys.argv) > 2 and sys.argv[2] == "gross"
issues = []
OVER = """() => { const W = innerWidth, out = [];
  document.querySelectorAll('#app *, #session *, #game *').forEach(e => { const b = e.getBoundingClientRect(); if(!b.width || e.closest('svg') || e.closest('.hero') || e.closest('.vbanner') || e.closest('.lobby-hero')) return;
    const cs = getComputedStyle(e); if(cs.position === 'fixed') return;
    if(b.right > W + 1 || b.left < -1) out.push(e.tagName + '.' + e.className + ' [' + Math.round(b.left) + ',' + Math.round(b.right) + ']'); });
  return {doc: document.scrollingElement.scrollWidth - W, els: out.slice(0, 6)}; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in SIZES:
        ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = ctx.new_page(); fontroute.setup(pg)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(700)
        pg.evaluate("""(hz) => { const T = window.__t, s = T.state(), t = T.today();
          T.LESSONS.slice(0, 7).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t, 1)}); });
          Object.keys(s.words).slice(0, 9).forEach(k => s.words[k].d = t); if(hz) s.prefs.hz = 'gross';
          s.days[t] = {tones:0, toneOk:0, cards:0, neu:0, xp:8, lessons:0, reviews:0, games:0}; location.hash = 'wiederholen'; }""", hz)
        pg.wait_for_timeout(200)
        tag = f"sw_{scheme}{'_gross' if hz else ''}_{w}"
        def check(name):
            r = pg.evaluate(OVER)
            if r["doc"] > 0 or r["els"]: issues.append(f"{w}px {name}: Überlauf {r}")
        for v in ["lernen", "spiel", "wiederholen", "toene", "saetze", "einstellungen"]:
            pg.evaluate(f"() => {{ location.hash = '{v}'; }}"); pg.wait_for_timeout(700 if v in ("lernen", "spiel") else 300)
            check(v)
            if v in ("lernen", "spiel"): pg.screenshot(path=O + f"{tag}_{v}.png")
        # Übung
        pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(300)
        pg.click('#view-wiederholen [data-act="review"]'); pg.wait_for_timeout(400)
        for k in range(3):
            st = pg.evaluate("() => { const S = window.__t.getS(); const ex = S.queue[0]; return {t:ex.type, r: ex.opts ? ex.opts.indexOf(ex.w) : -1, tone: ex.type==='tone' ? window.__t.toneOf(ex.w.py) : 0}; }")
            if st["t"] == "pairs" or st["t"] == "build": break
            pg.screenshot(path=O + f"{tag}_sess{k}.png") if k == 0 else None
            check("Übung " + st["t"])
            if st["t"] == "tone": pg.click(f'[data-stone="{st["tone"]}"]')
            elif st["r"] >= 0: pg.click(f'[data-opt="{st["r"]}"]')
            else: break
            pg.wait_for_timeout(200); check("Übung beantwortet"); pg.click("#s-next"); pg.wait_for_timeout(200)
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        # Rennen
        pg.evaluate("() => { location.hash = 'spiel'; }"); pg.wait_for_timeout(400)
        pg.click('[data-race="li"]'); pg.wait_for_timeout(3300)
        pg.screenshot(path=O + f"{tag}_race.png"); check("Rennen")
        for k in range(40):
            st = pg.evaluate("() => { const G = window.__t.getG(); if(!G || G.phase!=='race') return null; if(G.answered || !G.q) return {wait:1}; const q = G.q; return {i: q.type==='tone' ? window.__t.toneOf(q.w.py) : q.opts.indexOf(q.w)}; }")
            if st is None: break
            if "wait" in st: pg.wait_for_timeout(120); continue
            try: pg.click(f'[data-gopt="{st["i"]}"]', timeout=1500)
            except Exception: pass
            pg.wait_for_timeout(300)
        pg.wait_for_timeout(1500)
        pg.screenshot(path=O + f"{tag}_result.png"); check("Ergebnis")
        if errs: issues.append(f"{w}px JS: {errs[:2]}")
        ctx.close()
    b.close()
print("\n".join(issues) or "keine Probleme")
