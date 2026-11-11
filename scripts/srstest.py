# Prüft den neuen Wiederholplan: Abstände und Faktor, alte Spielstände, Schreiben ab Fach 2,
# Lernschleife (kurz danach und am Ende nochmal), Freies Üben mit schwachen Wörtern, Merkhilfen.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
src = open(ROOT + "/scripts/fulltest.py").read()
STEP = src[src.index('STEP = """')+10:src.index('"""', src.index('STEP = """')+10)]
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
MARK = """(n) => { const T = window.__t, s = T.state(), t = T.today(); T.LESSONS.slice(0, n).forEach(l => { s.learn.done[l.id] = {at:t, best:90}; l.W.forEach(w => s.words[w.zh] = {b:1, d:t}); }); }"""
def answer(pg, st, wrong):
    t = st["type"]
    if t in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'#session [data-opt="{(st["right"]+1)%st.get("nopt",3) if wrong else st["right"]}"]')
    elif t == "write": pg.fill("#w-in", "xx" if wrong else st["typed"]); pg.keyboard.press("Enter")
    elif t == "tone": pg.click(f'[data-stone="{(st["tone"]%4)+1 if wrong else st["tone"]}"]')
    elif t == "pairs":
        for li, ri in enumerate(st["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
    elif t == "build":
        for i in (list(reversed(st["order"])) if wrong else st["order"]): pg.click(f'[data-bank="{i}"]')
        pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }")
    pg.wait_for_timeout(30)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}); pg = ctx.new_page(); fontroute.setup(pg)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
    # --- Rechnung ---
    r = pg.evaluate("""() => { const T = window.__t, t = T.today(), A = T.addDays, out = {};
      out.new1 = T.srsNext({b:1, d:t, iv:1, e:2.5}, 'ok');
      out.three = T.srsNext({b:2, d:t, iv:3, e:2.5}, 'ok');
      out.old2 = T.srsNext({b:2, d:t}, 'ok');
      out.old5 = T.srsNext({b:5, d:t}, 'ok');
      out.cap = T.srsNext({b:5, d:t, iv:150, e:2.5}, 'ok');
      out.notdue = T.srsNext({b:3, d:A(t, 4), iv:7, e:2.5}, 'ok');
      out.lapse = T.srsNext({b:4, d:t, iv:20, e:2.5}, 'lapse');
      out.fail = T.srsNext({b:4, d:t, iv:20, e:2.5}, 'fail');
      out.ndlapse = T.srsNext({b:4, d:A(t, 9), iv:20, e:2.5}, 'lapse');
      out.floor = T.srsNext({b:1, d:t, iv:1, e:1.35}, 'lapse');
      out.box = [0,1,2,3,6,7,13,14,29,30,180].map(T.boxOf);
      out.t1 = A(t, 1); out.t3 = A(t, 3); out.t8 = A(t, 8); out.t18 = A(t, 18); out.t75 = A(t, 75); out.t180 = A(t, 180); out.t = t; out.t4 = A(t, 4);
      return out; }""")
    ok(r["new1"]["iv"] == 3 and r["new1"]["d"] == r["t3"] and r["new1"]["b"] == 2, f"neues Wort richtig: 3 Tage, Fach 2 ({r['new1']})")
    ok(r["three"]["iv"] == 8 and r["three"]["d"] == r["t8"] and r["three"]["b"] == 3, f"3 Tage richtig: 3 × 2,5 = 8 Tage ({r['three']})")
    ok(r["old2"]["iv"] == 8 and r["old2"]["e"] == 2.5, f"alter Spielstand Fach 2 ohne iv: weiter wie 3 Tage ({r['old2']})")
    ok(r["old5"]["iv"] == 75 and r["old5"]["d"] == r["t75"] and r["old5"]["b"] == 5, f"alter Spielstand Fach 5: 30 × 2,5 = 75 Tage ({r['old5']})")
    ok(r["cap"]["iv"] == 180 and r["cap"]["d"] == r["t180"], f"höchstens 180 Tage ({r['cap']})")
    ok(r["notdue"]["d"] == r["t4"] and r["notdue"]["iv"] == 7, f"nicht fällig und richtig: Plan bleibt ({r['notdue']})")
    ok(r["lapse"]["iv"] == 1 and r["lapse"]["d"] == r["t1"] and abs(r["lapse"]["e"] - 2.3) < 1e-9 and r["lapse"]["b"] == 1, f"fällig, Fehler, dann richtig: morgen wieder, Faktor 2,3 ({r['lapse']})")
    ok(r["fail"]["iv"] == 0 and r["fail"]["d"] == r["t"] and r["fail"]["b"] == 0, f"fällig, zuletzt falsch: heute nochmal ({r['fail']})")
    ok(r["ndlapse"]["d"] == r["t1"] and r["ndlapse"]["iv"] == 8 and abs(r["ndlapse"]["e"] - 2.4) < 1e-9, f"nicht fällig, Fehler: morgen, Abstand verkleinert ({r['ndlapse']})")
    ok(abs(r["floor"]["e"] - 1.3) < 1e-9, f"Faktor nie unter 1,3 ({r['floor']})")
    ok(r["box"] == [0,1,1,2,2,3,3,4,4,5,5], f"Fach aus Abstand {r['box']}")
    # Folge: immer richtig ergibt 1, 3, 8, 20, 50, 125, 180
    seq = pg.evaluate("""() => { const T = window.__t; let rec = {b:1, d:T.today(), iv:1, e:2.5}, out = [1];
      for(let i=0;i<6;i++){ rec = T.srsNext(Object.assign({}, rec, {d:T.today()}), 'ok'); out.push(rec.iv); } return out; }""")
    ok(seq == [1,3,8,20,50,125,180], f"immer richtig: {seq}")
    # applyResults (Lektion, Spiel)
    ar = pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today();
      s.words['你'] = {b:2, d:t, iv:3, e:2.5}; s.words['好'] = {b:2, d:t, iv:3, e:2.5}; s.words['我'] = {b:2, d:t, iv:3, e:2.5};
      T.applyResults({'你':{ok:2, bad:0}, '好':{ok:1, bad:1}, '我':{ok:0, bad:1}}); return [s.words['你'], s.words['好'], s.words['我'], T.addDays(t,1), t]; }""")
    ok(ar[0]["iv"] == 8 and ar[1]["d"] == ar[3] and ar[2]["d"] == ar[4] and ar[2]["b"] == 0, f"Lektion/Spiel: richtig, Fehler mit Korrektur, nur falsch {ar[:3]}")
    # --- Wiederholen: Schreiben ab Fach 2 ---
    pg.evaluate(MARK, 8)
    rv = pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(), pool = T.learnedWords();
      pool.forEach((w, i) => s.words[w.zh] = i % 2 ? {b:3, d:t, iv:8, e:2.5} : {b:1, d:t, iv:1, e:2.5});
      let hi = 0, hiW = 0, lo = 0, loW = 0;
      for(let k=0;k<20;k++){ T.buildReview(pool.slice(0,15), pool).forEach(e => { if(!e.w || e.type==='pairs' || e.conf) return; const b = s.words[e.w.zh].b;
        if(b>=2){ hi++; if(e.type==='write') hiW++; } else { lo++; if(e.type==='write') loW++; } }); }
      return {hi, hiW, lo, loW}; }""")
    ok(rv["hi"] > 0 and rv["hi"] == rv["hiW"], f"ab Fach 2 immer selbst schreiben ({rv['hiW']}/{rv['hi']})")
    ok(rv["lo"] > 0 and rv["loW"] < rv["lo"], f"Fach 0 und 1 gemischt, nicht nur Schreiben ({rv['loW']}/{rv['lo']})")
    # --- Lernschleife in einer echten Runde ---
    pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(); T.learnedWords().forEach(w => s.words[w.zh] = {b:1, d:t, iv:1, e:2.5}); T.startReview(false); }""")
    pg.wait_for_timeout(150)
    dbg = []; first = None; idx = 0; seen_at = []; wrong_done = False; n = 0
    for _ in range(80):
        st = pg.evaluate(STEP)
        if st.get("finished") or st.get("none"): break
        w = pg.evaluate("() => { const e = window.__t.getS().queue[0]; return e.w && !e.conf ? e.w.zh : null; }")
        idx += 1
        if st["type"] != "pairs" and w and not wrong_done:
            first = w; wrong_done = True; seen_at.append(idx)
            answer(pg, st, True)
            fb = pg.locator("#session .fb-mnemo").count()
            ok(fb == 1, f"nach Fehler steht die Merkhilfe da ({first})")
            q = pg.evaluate("() => window.__t.getS().queue.length")
            pg.click("#s-next"); pg.wait_for_timeout(30)
            pos = pg.evaluate(f"() => window.__t.getS().queue.map((e, i) => e.w && !e.conf && e.w.zh === {first!r} ? i : -1).filter(i => i >= 0)")
            ok(len(pos) == 2 and pos[0] == 2 and pos[1] == q, f"Fehler kommt nach 2 anderen und am Ende nochmal (Plätze {pos}, Länge vorher {q})")
            continue
        if w and w == first: seen_at.append(idx); dbg.append((idx, st["type"], st.get("retry")))
        answer(pg, st, False); pg.click("#s-next"); pg.wait_for_timeout(30); n += 1
    ok(len(seen_at) == 3, f"Wort kam insgesamt dreimal ({seen_at} {dbg})")
    st_after = pg.evaluate(f"() => {{ const T = window.__t; return [T.state().words[{first!r}], T.addDays(T.today(), 1)]; }}")
    ok(st_after[0]["d"] == st_after[1] and abs(st_after[0]["e"] - 2.3) < 1e-9, f"danach: morgen wieder, Faktor gesunken {st_after[0]}")
    other = pg.evaluate(f"() => {{ const T = window.__t, s = T.state(); return T.learnedWords().filter(w => w.zh !== {first!r}).map(w => s.words[w.zh]).filter(r => r.d === T.addDays(T.today(), 3)).length; }}")
    ok(other >= 5, f"die anderen Wörter: in 3 Tagen ({other})")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
    if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
    pg.wait_for_timeout(150)
    # --- Freies Üben: schwache Wörter ---
    fp = pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(), pool = T.learnedWords(), A = T.addDays;
      pool.forEach(w => s.words[w.zh] = {b:5, d:A(t, 40), iv:40, e:2.5});
      const weak = pool.slice(0, 5).map(w => w.zh); weak.forEach(zh => s.words[zh] = {b:1, d:A(t, 1), iv:1, e:1.5});
      let hit = 0; for(let k=0;k<20;k++){ T.startReview(true); const q = T.getS().queue; const zs = new Set(q.filter(e => e.w).map(e => e.w.zh)); hit += weak.filter(z => zs.has(z)).length; }
      const plan = JSON.stringify(s.words);
      return {hit, plan}; }""")
    ok(fp["hit"] == 100, f"Freies Üben nimmt die 5 schwächsten Wörter jedes Mal mit ({fp['hit']}/100)")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    # Freies Üben: richtig ändert nichts, falsch bringt morgen
    pg.evaluate("() => window.__t.startReview(true)"); pg.wait_for_timeout(100)
    before = pg.evaluate("() => JSON.stringify(window.__t.state().words)")
    st = pg.evaluate(STEP)
    if st["type"] == "pairs":
        answer(pg, st, False); pg.click("#s-next"); pg.wait_for_timeout(30); st = pg.evaluate(STEP)
    answer(pg, st, False)
    same = pg.evaluate("() => JSON.stringify(window.__t.state().words)") == before
    ok(same, "Freies Üben: richtig ändert den Plan nicht")
    pg.click("#s-next"); pg.wait_for_timeout(30); st = pg.evaluate(STEP)
    if st["type"] == "pairs":
        answer(pg, st, False); pg.click("#s-next"); pg.wait_for_timeout(30); st = pg.evaluate(STEP)
    wzh = pg.evaluate("() => window.__t.getS().queue[0].w.zh")
    answer(pg, st, True)
    rec = pg.evaluate(f"() => {{ const T = window.__t; return [T.state().words[{wzh!r}], T.today()]; }}")
    ok(rec[0]["d"] == rec[1], f"Freies Üben: falsch und noch nicht korrigiert = heute nochmal {rec[0]}")
    pg.click("#s-next"); pg.wait_for_timeout(30)
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
    # --- Merkhilfen ---
    mm = pg.evaluate("() => { const T = window.__t; return {n:Object.keys(T.MNEMO).length, miss:T.WORDS.filter(w => !T.MNEMO[w.zh]).map(w => w.zh)}; }")
    ok(mm["n"] == 167 and not mm["miss"], f"Merkhilfe für alle Wörter ({mm})")
    pg.evaluate("() => { const T = window.__t, s = T.state(); s.learn.done = {}; s.words = {}; T.startLesson('l1'); }"); pg.wait_for_timeout(150)
    ok(pg.locator("#session .wordcard .mnemo").count() == 1, "neues Wort zeigt die Merkhilfe")
    txt = pg.locator("#session .wordcard .mnemo").inner_text()
    ok("merkhilfe" in txt.lower() and "Mensch" in txt, f"Text der Merkhilfe für 你: {txt[:60]!r}")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    # --- Karteikasten ---
    pg.evaluate("() => { location.hash='lernen'; }"); pg.wait_for_timeout(100)
    pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(), A = T.addDays; s.words = {};
      [['你',{b:5, d:A(t,40), iv:40, e:2.5}], ['好',{b:2, d:t}], ['我',{b:1, d:A(t,1), iv:9, e:2.5}]].forEach(([k, v]) => s.words[k] = v);
      s.learn.done = {l1:{at:t, best:90}}; location.hash='wiederholen'; }""")
    pg.wait_for_timeout(250)
    counts = pg.evaluate("() => Array.from(document.querySelectorAll('.kasten .fach b')).map(b => +b.textContent)")
    ok(counts == [0,0,1,1,0,1], f"Karteikasten zählt nach Abstand {counts}")
    labs = pg.evaluate("() => Array.from(document.querySelectorAll('.kasten .fach small')).map(b => b.textContent)")
    ok(labs[1] == "morgen" and "Monat" in labs[5], f"Beschriftung {labs}")
    ok(not errs, f"keine JS-Fehler {errs[:3]}")
    b.close()
print("\n".join(res)); print(sum(1 for r in res if r.startswith("OK")), "/", len(res))
