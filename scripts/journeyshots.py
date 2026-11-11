import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys
STEP = """() => { const S = window.__t.getS(); if(!S) return {t:'none'}; if(S.finished) return {t:'fin'}; const ex = S.queue[0]; const r = {t:ex.type};
  if(ex.opts){ r.right = ex.type==='sentmean' ? ex.opts.indexOf(ex.s) : ex.type==='gap' ? ex.opts.indexOf(ex.gw) : ex.type==='judge' ? ex.opts.findIndex(o => o.ok) : ex.opts.indexOf(ex.w); r.nopt = ex.opts.length; }
  if(ex.type==='build'){ const used = ex.slot ? ex.built.filter(x => x!=null) : []; r.order = ex.s.toks.map((t, j) => { if(ex.slot && ex.built[j]!=null) return null; const i = ex.bank.findIndex((b,k) => b.zh===t.zh && used.indexOf(k)<0); used.push(i); return i; }).filter(x => x!==null); }
  if(ex.type==='pairs' && ex.left) r.pairs = ex.left.map(l => ex.right.findIndex(x => x.zh===l.zh));
  if(ex.type==='tone') r.tone = window.__t.toneOf(ex.w.py); return r; }"""
def play(pg):
    for _ in range(90):
        st = pg.evaluate(STEP); t = st["t"]
        if t == "fin": return
        if t == "intro": pg.click("#s-next"); continue
        if t in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'[data-opt="{st["right"]}"]')
        elif t == "tone": pg.click(f'[data-stone="{st["tone"]}"]')
        elif t == "pairs":
            for li, ri in enumerate(st["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        elif t == "build":
            for i in st["order"]: pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check")
        pg.click("#s-next")
errs = []
view = sys.argv[1]; w, h = (390, 844) if view == "mobile" else (1366, 900)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(600)
    pg.screenshot(path=f"{ROOT}/shots/j_{view}_start.png", full_page=True)
    for lid in ["l1", "l2"]:
        pg.click(f'#view-lernen button.btn[data-lesson="{lid}"]'); play(pg)
        if lid == "l2":
            pg.wait_for_timeout(900); pg.screenshot(path=f"{ROOT}/shots/j_{view}_ceremony.png")
        pg.click('[data-act="exit"]')
    pg.click('#view-lernen button.btn[data-lesson="l3"]'); play(pg); pg.click('[data-act="exit"]')
    pg.wait_for_timeout(700)
    pg.screenshot(path=f"{ROOT}/shots/j_{view}_progress.png", full_page=True)
    over = pg.evaluate("() => document.scrollingElement.scrollWidth - innerWidth")
    b.close()
print("Überlauf:", over, "Fehler:", errs or "keine")
