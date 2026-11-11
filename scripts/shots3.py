import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys
from PIL import Image
STEP = """() => { const S = window.__t.getS(); const ex = S.queue[0]; const r = {type:ex.type};
  if(ex.opts){ r.right = ex.type==='sentmean' ? ex.opts.indexOf(ex.s) : ex.type==='gap' ? ex.opts.indexOf(ex.gw) : ex.type==='judge' ? ex.opts.findIndex(o => o.ok) : ex.opts.indexOf(ex.w); r.nopt = ex.opts.length; }
  if(ex.type==='build'){ const used = ex.slot ? ex.built.filter(x => x!=null) : []; r.order = ex.s.toks.map((t, j) => { if(ex.slot && ex.built[j]!=null) return null; const i = ex.bank.findIndex((b,k) => b.zh===t.zh && used.indexOf(k)<0); used.push(i); return i; }).filter(x => x!==null); }
  if(ex.type==='pairs' && ex.left) r.pairs = ex.left.map(l => ex.right.findIndex(x => x.zh===l.zh));
  if(ex.type==='tone') r.tone = window.__t.toneOf(ex.w.py);
  return r; }"""
def advance_to(pg, want, answer_wrong=False, limit=60):
    for _ in range(limit):
        st = pg.evaluate(STEP)
        if st["type"] == want: return st
        t = st["type"]
        if t == "intro": pg.click("#s-next"); continue
        if t in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'[data-opt="{st["right"]}"]')
        elif t == "tone": pg.click(f'[data-stone="{st["tone"]}"]')
        elif t == "pairs":
            for li, ri in enumerate(st["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        elif t == "build":
            for i in st["order"]: pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check")
        pg.click("#s-next")
def shoot(view, w, h, dark=False):
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, color_scheme="dark" if dark else "light")
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
        def snap(name): f = f"{ROOT}/shots/s3_{view}_{name}.png"; pg.screenshot(path=f); out.append(f)
        # zwei Lektionen erledigen, damit der Pfad Zustände zeigt
        for lid in ["l1"]:
            pg.click(f'button.btn[data-lesson="{lid}"]')
            advance_to(pg, "__none__", limit=40) if False else None
            for _ in range(80):
                s = pg.evaluate("() => { const S = window.__t.getS(); return S && S.finished ? 'fin' : 'run'; }")
                if s == "fin": break
                st = pg.evaluate(STEP); t = st["type"]
                if t == "intro": pg.click("#s-next"); continue
                if t in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'[data-opt="{st["right"]}"]')
                elif t == "tone": pg.click(f'[data-stone="{st["tone"]}"]')
                elif t == "pairs":
                    for li, ri in enumerate(st["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
                elif t == "build":
                    for i in st["order"]: pg.click(f'[data-bank="{i}"]')
                    pg.click("#s-check")
                pg.click("#s-next")
            pg.click('[data-act="exit"]')
        pg.wait_for_timeout(200); snap("1_lernen")
        pg.click('button.btn[data-lesson="l2"]'); pg.wait_for_timeout(200); snap("2_intro")
        st = advance_to(pg, "char"); pg.click(f'[data-opt="{(st["right"]+1)%4}"]'); pg.wait_for_timeout(350); snap("3_char_falsch")
        pg.click("#s-next")
        st = advance_to(pg, "pairs"); pg.click('[data-pl="0"]'); snap("4_paare")
        pg.evaluate("() => { const S = window.__t.getS(); S.queue = S.queue.filter(e => e.type==='build' || e.type==='sentmean'); }"); pg.evaluate("() => {}")
        pg.click('[data-act="close"]'); pg.click('[data-act="close"]')
        pg.click('button.btn[data-lesson="l2"]')
        pg.evaluate("() => { const S = window.__t.getS(); S.queue = S.queue.filter(e => e.type==='build'); S.prog = 0.7; }")
        pg.click('[data-act="close"]'); pg.click('[data-act="close"]')
        pg.click('button.btn[data-lesson="l2"]')
        st = advance_to(pg, "build"); pg.click(f'[data-bank="{st["order"][0]}"]'); pg.click(f'[data-bank="{st["order"][1]}"]'); snap("5_satz")
        for i in st["order"][2:]: pg.click(f'[data-bank="{i}"]')
        pg.click("#s-check"); pg.wait_for_timeout(350); snap("6_satz_richtig")
        pg.click('[data-act="close"]'); pg.click('[data-act="close"]')
        for hsh in ["wiederholen", "toene", "saetze", "einstellungen"]:
            pg.evaluate(f"location.hash='{hsh}'"); pg.wait_for_timeout(250)
            if hsh == "toene": pg.click('[data-tone="2"]'); pg.wait_for_timeout(200)
            if hsh == "saetze": pg.click('#c-reveal'); pg.wait_for_timeout(200)
            snap("7_" + hsh)
        b.close()
    return out
view = sys.argv[1]; w, h = (390, 844) if view.startswith("mobile") else (1366, 900)
files = shoot(view, w, h, dark=view.endswith("dark"))
ims = [Image.open(f) for f in files]
cols = 5 if w < 600 else 2
scale = 1 if w < 600 else 0.5
ims = [i.resize((int(i.width*scale), int(i.height*scale))) for i in ims]
rows = (len(ims)+cols-1)//cols
W = max(i.width for i in ims); H = max(i.height for i in ims)
m = Image.new("RGB", (cols*W + (cols-1)*8, rows*H + (rows-1)*8), "white")
for k, im in enumerate(ims): m.paste(im, ((k%cols)*(W+8), (k//cols)*(H+8)))
m.save(f"{ROOT}/shots/m3_{view}.png"); print(m.size, len(files))
