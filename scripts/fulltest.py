# Spielt alle Lektionen durch, prüft Fortschritt, Audio-Zuordnung, Überlauf, Fehler.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import json, sys
VIEW = sys.argv[1] if len(sys.argv) > 1 else "mobile"
SIZE = {"mobile": (390, 844), "desktop": (1366, 900)}[VIEW]
INSTR = """
(() => {
  window.__log = [];
  const rev = () => { const m = {}; const bc = window.__t.blobCache; Object.keys(bc).forEach(k => m[bc[k]] = k); return m; };
  const op = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ window.__log.push({a: rev()[this.src] || this.src.slice(0,30)}); return op.call(this).catch(()=>{}); };
  if (window.speechSynthesis) { const sp = window.speechSynthesis.speak.bind(window.speechSynthesis); window.speechSynthesis.speak = function(u){ window.__log.push({tts: u.text}); try{ sp(u); }catch(e){} }; }
})();
"""
STEP = """() => { const S = window.__t.getS(); if(!S) return {none:true}; if(S.finished) return {finished:true, f:S.finished, prog:S.prog};
  const ex = S.queue[0]; const r = {type:ex.type, answered:S.answered, retry:!!ex.retry, prog:S.prog, zh: ex.w ? ex.w.zh : (ex.s ? ex.s.zh : '')};
  if(ex.opts){ r.right = ex.type==='sentmean' ? ex.opts.indexOf(ex.s) : ex.type==='gap' ? ex.opts.indexOf(ex.gw) : ex.type==='judge' ? ex.opts.findIndex(o => o.ok) : ex.opts.indexOf(ex.w); r.nopt = ex.opts.length; }
  if(ex.type==='tone') r.tone = window.__t.toneOf(ex.w.py);
  if(ex.type==='write'){ const num = (py) => py.split(/[_ ]/).map(sy => { const m = {'ā':['a',1],'á':['a',2],'ǎ':['a',3],'à':['a',4],'ē':['e',1],'é':['e',2],'ě':['e',3],'è':['e',4],'ī':['i',1],'í':['i',2],'ǐ':['i',3],'ì':['i',4],'ō':['o',1],'ó':['o',2],'ǒ':['o',3],'ò':['o',4],'ū':['u',1],'ú':['u',2],'ǔ':['u',3],'ù':['u',4],'ǖ':['v',1],'ǘ':['v',2],'ǚ':['v',3],'ǜ':['v',4]}; let t = 0, o = ''; for(const c of sy.toLowerCase()){ if(m[c]){ o += m[c][0]; t = m[c][1]; } else if(/[a-zü]/.test(c)) o += c==='ü' ? 'v' : c; } return o + (t || ''); }).join(''); r.typed = num(ex.w.py); }
  if(ex.type==='pairs' && ex.left) r.pairs = ex.left.map(l => ex.right.findIndex(x => x.zh===l.zh));
  if(ex.type==='build'){ const used = ex.slot ? ex.built.filter(x => x!=null) : []; r.order = ex.s.toks.map((t, j) => { if(ex.slot && ex.built[j]!=null) return null; const i = ex.bank.findIndex((b,k) => b.zh===t.zh && used.indexOf(k)<0); used.push(i); return i; }).filter(x => x!==null); }
  return r; }"""
OVER = "() => { const e = document.scrollingElement; const s = document.getElementById('s-main'); return {doc: e.scrollWidth - window.innerWidth, sess: s ? s.scrollWidth - s.clientWidth : 0}; }"
errs, issues, audio_map, progs = [], [], {}, []
def take_log(pg): return pg.evaluate("() => { const l = window.__log; window.__log = []; return l; }")
def run_session(pg, wrong_every=0, tag=""):
    n = 0; last_prog = -1; types = []
    while n < 400:
        n += 1
        st = pg.evaluate(STEP)
        if st.get("finished"):
            if abs(st["prog"] - 1) > 1e-9: issues.append(f"{tag}: Fortschritt endet bei {st['prog']}")
            return st, types
        if st["prog"] < last_prog - 1e-9: issues.append(f"{tag}: Fortschritt geht zurück {last_prog} -> {st['prog']}")
        last_prog = st["prog"]
        o = pg.evaluate(OVER)
        if o["doc"] > 1 or o["sess"] > 1: issues.append(f"{tag}: seitlicher Überlauf bei {st['type']} {st['zh']} {o}")
        t = st["type"]; types.append(t + ("*" if st["retry"] else ""))
        log = take_log(pg)
        if t == "intro":
            audio_map[st["zh"]] = log
            pg.click("#s-next"); continue
        if t == "rule":
            pg.click("#s-next"); continue
        if t == "draw":
            pg.wait_for_timeout(150); pg.click('[data-act="drawskip"]'); pg.wait_for_timeout(60); continue
        wrong = wrong_every and (n % wrong_every == 0) and not st["retry"]
        if t in ("mean","hear","char","sentmean","gap","judge"):
            i = st["right"]
            if wrong: i = (i + 1) % st.get("nopt", 3)
            pg.click(f'[data-opt="{i}"]')
        elif t == "write":
            pg.fill("#w-in", "xx" if wrong else st["typed"]); pg.keyboard.press("Enter")
        elif t == "tone":
            k = st["tone"] if not wrong else (st["tone"] % 4) + 1
            pg.click(f'[data-stone="{k}"]')
        elif t == "pairs":
            st = pg.evaluate(STEP)
            for li, ri in enumerate(st["pairs"]):
                pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        elif t == "build":
            order = st["order"] if not wrong else list(reversed(st["order"]))
            for i in order: pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }")
        take_log(pg)
        pg.click("#s-next")
    issues.append(f"{tag}: zu viele Schritte"); return None, types

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": SIZE[0], "height": SIZE[1]})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto("file://" + ROOT + "/test/index.html")
    pg.wait_for_function("!!window.ZH_AUDIO")
    pg.evaluate(INSTR)
    pg.screenshot(path=f"{ROOT}/shots/v3_{VIEW}_lernen.png", full_page=False)
    for li in range(pg.evaluate('() => window.__t.LESSONS.length')):
        lid = pg.evaluate(f"() => window.__t.LESSONS[{li}].id")
        pg.evaluate("location.hash='lernen'"); pg.wait_for_timeout(50)
        pg.click(f'button.btn[data-lesson="{lid}"]')
        if li == 1: pg.screenshot(path=f"{ROOT}/shots/v3_{VIEW}_intro.png")
        st, types = run_session(pg, wrong_every=(7 if li % 3 == 0 else 0), tag=f"L{li+1}")
        if li == 0: pg.screenshot(path=f"{ROOT}/shots/v3_{VIEW}_finish.png")
        print(f"L{li+1}: {len(types)} Schritte, {st['f'] if st else '-'}")
        pg.click('[data-act="exit"]')
    done = pg.evaluate("() => Object.keys(window.__t.state().learn.done).length")
    print("Lektionen erledigt:", done, "Wörter gelernt:", pg.evaluate("() => Object.keys(window.__t.state().words).length"))
    # Wiederholung: alles fällig setzen
    pg.evaluate("() => { const s = window.__t.state(); const t = new Date(); const ds = t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0'); Object.keys(s.words).forEach(k => s.words[k].d = ds); location.hash='wiederholen'; }")
    pg.wait_for_timeout(100)
    pg.screenshot(path=f"{ROOT}/shots/v3_{VIEW}_wdh.png")
    pg.click('#view-wiederholen [data-act="review"]')
    st, types = run_session(pg, wrong_every=5, tag="Wiederholung")
    print("Wiederholung:", len(types), "Schritte", st["f"] if st else "-")
    pg.click('[data-act="exit"]')
    stages = pg.evaluate("() => { const w = window.__t.state().words; const c = {}; Object.values(w).forEach(x => c[x.b] = (c[x.b]||0)+1); return c; }")
    print("Stufen nach Wiederholung:", stages)
    json.dump(audio_map, open(f"{ROOT}/audit/audio_map_{VIEW}.json", "w"), ensure_ascii=False, indent=0)
    b.close()
print("Probleme:", issues or "keine")
print("JS-Fehler:", [e for e in errs if "fonts.g" not in e and "net::" not in e] or "keine")
