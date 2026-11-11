import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, shutil
sys.path.insert(0, ROOT + "/scripts")
import fontroute
STEP = """() => { const S = window.__t.getS(); if(!S) return {t:'none'}; if(S.finished) return {t:'fin'}; const ex = S.queue[0]; const r = {t:ex.type};
  if(ex.opts) r.right = ex.type==='sentmean' ? ex.opts.indexOf(ex.s) : ex.opts.indexOf(ex.w);
  if(ex.type==='build'){ const used = []; r.order = ex.s.toks.map(t => { const i = ex.bank.findIndex((b,k) => b.zh===t.zh && used.indexOf(k)<0); used.push(i); return i; }); }
  if(ex.type==='pairs' && ex.left) r.pairs = ex.left.map(l => ex.right.findIndex(x => x.zh===l.zh));
  if(ex.type==='tone') r.tone = window.__t.toneOf(ex.w.py); return r; }"""
def play(pg, shot=None):
    k = 0
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
        k += 1
        if shot and k == 4: pg.wait_for_timeout(250); pg.screenshot(path=shot)
        pg.click("#s-next")
QA = """() => { const G = window.__t.getG(); if(!G || G.phase!=='race' || !G.q || G.answered) return null; const q = G.q;
  return q.type==='tone' ? {i: window.__t.toneOf(q.w.py), tone:true} : {i: q.opts.indexOf(q.w)}; }"""
def race(pg, rid, wrong_at=-1, shots=None, max_q=40):
    pg.click(f'[data-race="{rid}"]')
    pg.wait_for_timeout(3300)
    n = 0
    while n < max_q:
        g = pg.evaluate("() => { const G = window.__t.getG(); return G ? G.phase : 'none'; }")
        if g != "race": break
        a = pg.evaluate(QA)
        if not a: pg.wait_for_timeout(120); continue
        i = a["i"]
        if n == wrong_at: i = (i % 4) + 1 if a.get("tone") else (i + 1) % 4
        try: pg.click(f"[data-gopt=\"{i}\"]", timeout=2000)
        except Exception: continue
        n += 1
        if shots and n in shots: pg.wait_for_timeout(260); pg.screenshot(path=shots[n])
        pg.wait_for_timeout(700 if n != wrong_at + 1 else 1700)
    pg.wait_for_timeout(1400)
view = sys.argv[1]; dark = len(sys.argv) > 2 and sys.argv[2] == "dark"
w, h = (390, 844) if view == "mobile" else (1366, 900)
tag = view + ("_dark" if dark else "")
O = ROOT + "/shots/v5/"
shutil.copy(ROOT + "/zh-app/test.html", ROOT + "/test2/index.html"); shutil.copy(ROOT + "/zh-app/audio.js", ROOT + "/test2/audio.js")
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme="dark" if dark else "light")
    pg = ctx.new_page(); fontroute.setup(pg)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto("file://" + ROOT + "/test2/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(1500)
    pg.screenshot(path=O+f"{tag}_lernen0.png")
    pg.screenshot(path=O+f"{tag}_lernen0_full.png", full_page=True)
    for lid in ["l1", "l2", "l3"]:
        pg.click(f'#view-lernen button.btn[data-lesson="{lid}"]')
        play(pg, O+f"{tag}_session.png" if lid == "l1" else None)
        if lid == "l2": pg.wait_for_timeout(900); pg.screenshot(path=O+f"{tag}_ceremony.png")
        pg.click('[data-act="exit"]')
    # einige Wörter fällig machen
    pg.evaluate("() => { const s = window.__t.state(), t = window.__t.today(); Object.keys(s.words).slice(0, 6).forEach(k => s.words[k].d = t); }")
    pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(300)
    pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(900)
    pg.screenshot(path=O+f"{tag}_lernen3.png")
    pg.screenshot(path=O+f"{tag}_lernen3_full.png", full_page=True)
    over1 = pg.evaluate("() => document.scrollingElement.scrollWidth - innerWidth")
    pg.evaluate("() => window.scrollTo(0, 300)"); pg.wait_for_timeout(300); pg.screenshot(path=O+f"{tag}_lernen3_scrolled.png")
    for v in ["wiederholen", "toene", "saetze", "einstellungen"]:
        pg.evaluate(f"() => {{ location.hash = '{v}'; }}"); pg.wait_for_timeout(500); pg.screenshot(path=O+f"{tag}_{v}.png")
    pg.evaluate("() => { location.hash = 'spiel'; }"); pg.wait_for_timeout(1200)
    pg.screenshot(path=O+f"{tag}_lobby.png"); pg.screenshot(path=O+f"{tag}_lobby_full.png", full_page=True)
    over2 = pg.evaluate("() => document.scrollingElement.scrollWidth - innerWidth")
    race(pg, "wang", wrong_at=2, shots={1: O+f"{tag}_race1.png", 3: O+f"{tag}_race_wrong.png", 7: O+f"{tag}_race7.png"})
    pg.screenshot(path=O+f"{tag}_race_result.png")
    res = pg.evaluate("() => { const G = window.__t.getG(); return G && {phase:G.phase, won:G.won, ok:G.ok, n:G.n, xp:G.xp, time:G.time}; }")
    st = pg.evaluate("() => { const s = window.__t.state(); return {game:s.game, day:s.days[window.__t.today()], words:s.words}; }")
    b.close()
print("Ergebnis:", res)
print("Spielstand:", st["game"], "Tag:", st["day"])
print("Überlauf:", over1, over2, "Fehler:", errs or "keine")
