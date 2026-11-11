import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import json
errs = []
STEP = """() => { const S = window.__t.getS(); if(!S) return {none:true}; if(S.finished) return {finished:true, f:S.finished};
  const ex = S.queue[0]; const r = {type:ex.type, answered:S.answered, retry:!!ex.retry};
  if(ex.opts){ r.right = ex.type==='sentmean' ? ex.opts.indexOf(ex.s) : ex.type==='gap' ? ex.opts.indexOf(ex.gw) : ex.type==='judge' ? ex.opts.findIndex(o => o.ok) : ex.opts.indexOf(ex.w); r.nopt = ex.opts.length; }
  if(ex.type==='tone') r.tone = window.__t.toneOf(ex.w.py);
  if(ex.type==='pairs'){ if(!ex.left) return {type:'pairs', notReady:true}; r.pairs = ex.left.map(l => ex.right.findIndex(x => x.zh===l.zh)); }
  if(ex.type==='build'){ const used = ex.slot ? ex.built.filter(x => x!=null) : []; r.order = ex.s.toks.map((t, j) => { if(ex.slot && ex.built[j]!=null) return null; const i = ex.bank.findIndex((b,k) => b.zh===t.zh && used.indexOf(k)<0); used.push(i); return i; }).filter(x => x!==null); }
  return r; }"""
def run_lesson(pg, wrong_first=True, log=None):
    n = 0; wrong_done = not wrong_first; types = []
    while n < 200:
        n += 1
        st = pg.evaluate(STEP)
        if st.get("finished"): return st, types
        t = st["type"]; types.append(t + ("*" if st.get("retry") else ""))
        if t == "intro":
            pg.click("#s-next"); continue
        if t in ("mean","hear","char","sentmean","gap","judge"):
            i = st["right"]
            if not wrong_done: i = (i + 1) % 2 if st["right"] in (0,1) else 0; wrong_done = True
            pg.click(f'[data-opt="{i}"]')
        elif t == "tone":
            pg.click(f'[data-stone="{st["tone"]}"]')
        elif t == "pairs":
            for li, ri in enumerate(st["pairs"]):
                pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        elif t == "build":
            for i in st["order"]: pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check")
        pg.click("#s-next")
    raise Exception("zu viele Schritte")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto("file://" + ROOT + "/test/index.html")
    pg.wait_for_function("!!window.ZH_AUDIO")
    pg.screenshot(path=ROOT + "/shots/a_path.png")
    pg.click('#next-card [data-lesson]')
    pg.screenshot(path=ROOT + "/shots/b_intro.png")
    st, types = run_lesson(pg)
    print("L1:", len(types), "Schritte", " ".join(types)); print("Ergebnis:", st["f"])
    pg.screenshot(path=ROOT + "/shots/c_finish.png")
    pg.click("#fin-go")   # nächste Lektion
    # in L2 bis zur ersten Satz-Übung spielen und Screenshot machen
    for _ in range(60):
        s = pg.evaluate(STEP)
        if s["type"] == "build" and not s["answered"]:
            pg.click(f'[data-bank="{s["order"][0]}"]'); pg.screenshot(path=ROOT + "/shots/d_build.png"); pg.click('[data-ans="0"]'); break
        if s["type"] == "intro": pg.click("#s-next"); continue
        if s["type"] in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'[data-opt="{s["right"]}"]')
        elif s["type"] == "tone": pg.click(f'[data-stone="{s["tone"]}"]')
        elif s["type"] == "pairs":
            if s.get("notReady"): break
            for li, ri in enumerate(s["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        pg.click("#s-next")
    st2, types2 = run_lesson(pg, wrong_first=False)
    print("L2 Rest:", " ".join(types2), st2["f"])
    pg.click('[data-act="exit"]')
    # Wiederholung: Wörter auf heute fällig setzen
    pg.evaluate("() => { const s = window.__t.state(); const t = new Date(); const ds = t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0'); Object.keys(s.words).forEach(k => s.words[k].d = ds); location.hash='wiederholen'; }")
    pg.wait_for_timeout(200)
    pg.click('[data-act="review"]')
    st3, types3 = run_lesson(pg, wrong_first=True)
    print("Review:", " ".join(types3), st3["f"])
    words = pg.evaluate("() => window.__t.state().words")
    print("SRS-Stufen:", sorted(set((v['b'], v['d']) for v in words.values())))
    pg.click('[data-act="exit"]')
    pg.evaluate("location.hash='lernen'"); pg.wait_for_timeout(200)
    pg.screenshot(path=ROOT + "/shots/e_path2.png", full_page=False)
    nos = pg.evaluate("() => window.__t.SENTS.filter(s => !window.__t.sentClips(s.toks)).map(s => s.zh)")
    print("Sätze ohne Wort-für-Wort-Aufnahme:", nos)
    nw = pg.evaluate("() => window.__t.WORDS.filter(w => !window.__t.clipsFor(w)).map(w => w.zh)")
    print("Wörter ohne Aufnahme:", nw)
    b.close()
print("errors:", [e for e in errs if "fonts.g" not in e and "net::" not in e])
