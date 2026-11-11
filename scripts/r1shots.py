import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, os
sys.path.insert(0, ROOT + "/scripts"); import fontroute
O = ROOT + "/shots/r1/"; os.makedirs(O, exist_ok=True)
view = sys.argv[1] if len(sys.argv) > 1 else "m"; scheme = sys.argv[2] if len(sys.argv) > 2 else "light"
w, h = (390, 844) if view == "m" else (1366, 900)
tag = view + "_" + scheme
STEP = """() => { const S = window.__t.getS(); if(!S) return {t:'none'}; if(S.finished) return {t:'fin'}; const ex = S.queue[0]; const r = {t:ex.type, old:!!ex.old, ans:S.answered};
  if(ex.opts){ r.right = ex.type==='sentmean' ? ex.opts.indexOf(ex.s) : ex.type==='gap' ? ex.opts.indexOf(ex.gw) : ex.type==='judge' ? ex.opts.findIndex(o => o.ok) : ex.opts.indexOf(ex.w); r.nopt = ex.opts.length; }
  if(ex.type==='build'){ const used = ex.slot ? ex.built.filter(x => x!=null) : []; r.order = ex.s.toks.map((t, j) => { if(ex.slot && ex.built[j]!=null) return null; const i = ex.bank.findIndex((b,k) => b.zh===t.zh && used.indexOf(k)<0); used.push(i); return i; }).filter(x => x!==null); }
  if(ex.type==='pairs' && ex.left) r.pairs = ex.left.map(l => ex.right.findIndex(x => x.zh===l.zh));
  if(ex.type==='tone') r.tone = window.__t.toneOf(ex.w.py); if(ex.type==='write'){ const num = (py) => py.split(/[_ ]/).map(sy => { const m = {'ā':['a',1],'á':['a',2],'ǎ':['a',3],'à':['a',4],'ē':['e',1],'é':['e',2],'ě':['e',3],'è':['e',4],'ī':['i',1],'í':['i',2],'ǐ':['i',3],'ì':['i',4],'ō':['o',1],'ó':['o',2],'ǒ':['o',3],'ò':['o',4],'ū':['u',1],'ú':['u',2],'ǔ':['u',3],'ù':['u',4],'ǖ':['v',1],'ǘ':['v',2],'ǚ':['v',3],'ǜ':['v',4]}; let t = 0, o = ''; for(const c of sy.toLowerCase()){ if(m[c]){ o += m[c][0]; t = m[c][1]; } else if(/[a-zü]/.test(c)) o += c==='ü' ? 'v' : c; } return o + (t || ''); }).join(''); r.typed = num(ex.w.py); } return r; }"""
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = ctx.new_page(); fontroute.setup(pg)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(900)
    pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today();
      T.LESSONS.slice(0, 2).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:t}); }); location.hash = 'wiederholen'; }""")
    pg.wait_for_timeout(200); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(500)
    pg.click('#view-lernen .hr-go'); pg.wait_for_timeout(400)
    nw = 0; intro = 0
    for _ in range(90):
        st = pg.evaluate(STEP); t = st["t"]
        if t == "fin": break
        if t == "intro":
            if not intro: pg.wait_for_timeout(250); pg.screenshot(path=O+f"{tag}_intro.png"); intro = 1
            pg.click("#s-next"); continue
        if t == "rule": pg.click("#s-next"); continue
        if t in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'[data-opt="{st["right"]}"]')
        elif t == "write":
            nw += 1
            if nw == 1:
                pg.wait_for_timeout(200); pg.screenshot(path=O+f"{tag}_write0.png")
                # Tonfehler in der letzten Silbe
                typed = st["typed"]; bad = typed[:-1] + ("1" if typed[-1] != "1" else "2")
                pg.fill("#w-in", bad); pg.keyboard.press("Enter"); pg.wait_for_timeout(500); pg.screenshot(path=O+f"{tag}_write_bad.png")
            elif nw == 2:
                pg.fill("#w-in", st["typed"]); pg.keyboard.press("Enter"); pg.wait_for_timeout(500); pg.screenshot(path=O+f"{tag}_write_ok.png")
            else:
                pg.fill("#w-in", st["typed"]); pg.keyboard.press("Enter")
        elif t == "tone": pg.click(f'[data-stone="{st["tone"]}"]')
        elif t == "pairs":
            st = pg.evaluate(STEP)
            for li, ri in enumerate(st["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        elif t == "build":
            for i in st["order"]: pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check")
        pg.click("#s-next")
    pg.wait_for_timeout(1200); pg.screenshot(path=O+f"{tag}_finish.png", full_page=True)
    pg.click('[data-act="exit"]'); pg.wait_for_timeout(300)
    pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today();
      T.LESSONS.slice(0, 9).forEach((l, i) => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach((w, j) => s.words[w.zh] = {b:(i+j)%6, d:T.addDays(t, (i+j)%3)}); });
      s.err = s.err || {}; ['谢谢','多少','对不起','喜欢','什么'].forEach((z, i) => { if (T.WORD[z]) s.err[z] = {n:5-i, ok:i%2, last:t}; }); location.hash = 'saetze'; }""")
    pg.wait_for_timeout(300); pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(600)
    pg.screenshot(path=O+f"{tag}_review.png", full_page=True)
    pg.evaluate("() => { location.hash = 'toene'; }"); pg.wait_for_timeout(400)
    pg.evaluate("() => window.__t.toneSet('毛')"); pg.click('[data-tone="2"]'); pg.wait_for_timeout(1500)
    pg.screenshot(path=O+f"{tag}_tone_ans.png", full_page=True)
    pg.set_input_files("#own-file", "/tmp/own/low_mao2.m4a"); pg.wait_for_timeout(2500)
    pg.locator("#t-own").scroll_into_view_if_needed(); pg.wait_for_timeout(200); pg.screenshot(path=O+f"{tag}_own_ok.png")
    pg.set_input_files("#own-file", "/tmp/pitchref/raw/s_kan4.mp3"); pg.wait_for_timeout(2500)
    pg.locator("#t-own").scroll_into_view_if_needed(); pg.wait_for_timeout(200); pg.screenshot(path=O+f"{tag}_own_bad.png")
    b.close()
print("Fehler:", errs or "keine", "| write:", nw)
