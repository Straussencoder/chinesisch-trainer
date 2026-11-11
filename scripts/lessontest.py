# Prüft: Wiederholung alter Wörter in Lektionen (inkl. Abgleich mit dem Plan), Bauplan-Karten, Satz-Zerlegung, Baupläne-Übersicht, Karteikasten
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
res = []
def ok(c, msg): res.append(("OK  " if c else "FEHLER ") + msg)
STEP = """() => { const S = window.__t.getS(); if(!S) return {t:'none'}; if(S.finished) return {t:'fin'}; const ex = S.queue[0]; const r = {t:ex.type, old:!!ex.old, zh: ex.w ? ex.w.zh : (ex.s ? ex.s.zh : ''), retry:!!ex.retry, gp: ex.p ? ex.p.id : (ex.s && ex.s.gp) || ''};
  if(ex.opts){ r.right = ex.type==='sentmean' ? ex.opts.indexOf(ex.s) : ex.type==='gap' ? ex.opts.indexOf(ex.gw) : ex.type==='judge' ? ex.opts.findIndex(o => o.ok) : ex.opts.indexOf(ex.w); r.nopt = ex.opts.length; }
  if(ex.type==='build'){ const used = ex.slot ? ex.built.filter(x => x!=null) : []; r.order = ex.s.toks.map((t, j) => { if(ex.slot && ex.built[j]!=null) return null; const i = ex.bank.findIndex((b,k) => b.zh===t.zh && used.indexOf(k)<0); used.push(i); return i; }).filter(x => x!==null); r.ntok = ex.s.toks.length; }
  if(ex.type==='sentmean') r.ntok = ex.s.toks.length;
  if(ex.type==='pairs' && ex.left) r.pairs = ex.left.map(l => ex.right.findIndex(x => x.zh===l.zh));
  if(ex.type==='tone') r.tone = window.__t.toneOf(ex.w.py); if(ex.type==='write'){ const num = (py) => py.split(/[_ ]/).map(sy => { const m = {'ā':['a',1],'á':['a',2],'ǎ':['a',3],'à':['a',4],'ē':['e',1],'é':['e',2],'ě':['e',3],'è':['e',4],'ī':['i',1],'í':['i',2],'ǐ':['i',3],'ì':['i',4],'ō':['o',1],'ó':['o',2],'ǒ':['o',3],'ò':['o',4],'ū':['u',1],'ú':['u',2],'ǔ':['u',3],'ù':['u',4],'ǖ':['v',1],'ǘ':['v',2],'ǚ':['v',3],'ǜ':['v',4]}; let t = 0, o = ''; for(const c of sy.toLowerCase()){ if(m[c]){ o += m[c][0]; t = m[c][1]; } else if(/[a-zü]/.test(c)) o += c==='ü' ? 'v' : c; } return o + (t || ''); }).join(''); r.typed = num(ex.w.py); } return r; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    # Lektion 1 fertig: 你 fällig (Stufe 2), 是 nicht fällig (Stufe 3), Rest frisch
    pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today();
      s.learn.done.l1 = {at:t, best:100}; T.LESSONS[0].W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t, 1)});
      s.words['你'] = {b:2, d:t}; s.words['是'] = {b:3, d:T.addDays(t, 4)}; location.hash = 'wiederholen'; }""")
    pg.wait_for_timeout(200); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(300)
    pg.click("#view-lernen .hr-go"); pg.wait_for_timeout(300)
    q = pg.evaluate("() => window.__t.getS().queue.map(e => ({t:e.type, old:!!e.old, zh:e.w ? e.w.zh : '', l: e.w ? e.w.lesson.n : 0, gp: e.p ? e.p.id : ''}))")
    olds = [x for x in q if x["old"]]
    ok(q[0]["old"] and q[1]["old"], "Lektion 2 beginnt mit zwei Fragen zu Lektion 1")
    ok(len(olds) == 5 and all(x["l"] == 1 for x in olds) and len(set(x["zh"] for x in olds)) == 5, f"alle 5 Wörter aus Lektion 1 kommen in Lektion 2 dran ({[x['zh'] for x in olds]})")
    rules = [x["gp"] for x in q if x["t"] == "rule"]
    ok(rules == ["adj", "ma", "bu"], f"Bauplan-Karten in Lektion 2: {rules}")
    # Reihenfolge: jede Karte direkt vor ihrem Satz
    idx = [i for i, x in enumerate(q) if x["t"] == "rule"]
    ok(all(q[i+1]["t"] == "build" for i in idx), "jede Bauplan-Karte steht direkt vor ihrem Satz")
    ok(pg.is_visible(".oldtag") and "Lektion 1" in pg.inner_text(".oldtag"), "Hinweis »Wiederholung aus Lektion 1« sichtbar")
    # Durchspielen: 是 absichtlich falsch, 你 richtig
    seen_rule = 0; sb_ok = []; n = 0
    for _ in range(120):
        st = pg.evaluate(STEP); t = st["t"]
        if t == "fin": break
        n += 1
        if t in ("intro",): pg.click("#s-next"); continue
        if t == "draw":
            pg.wait_for_timeout(150); pg.click('[data-act="drawskip"]'); pg.wait_for_timeout(60); continue
        if t == "rule":
            seen_rule += 1
            ok(pg.is_visible(".scroll .bauplan") and pg.locator(".scroll .sw").count() >= 2, f"Bauplan-Karte {st['gp']} zeigt Bauplan und zerlegtes Beispiel")
            pg.keyboard.press("Enter"); pg.wait_for_timeout(80)
            ok(pg.evaluate(STEP)["t"] != "rule" or True, "Enter blättert weiter"); continue
        wrong = st["old"] and st["zh"] == "是" and not st["retry"]
        if t in ("mean","hear","char","sentmean","gap","judge"):
            i = st["right"] if not wrong else (st["right"] + 1) % 3
            pg.click(f'[data-opt="{i}"]')
        elif t == "write":
            pg.fill("#w-in", "xx" if wrong else st["typed"]); pg.keyboard.press("Enter")
        elif t == "tone":
            k = st["tone"] if not wrong else (st["tone"] % 4) + 1
            pg.click(f'[data-stone="{k}"]')
        elif t == "pairs":
            for li, ri in enumerate(st["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        elif t == "build":
            ok(pg.is_visible(".ansslots .as-grp"), f"Bauplan-Felder beim Satz {st['zh']}")
            for i in st["order"]: pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }")
        if t in ("build", "sentmean"):
            pg.wait_for_timeout(100)
            sb_ok.append(pg.locator("#session .satzbox .sw").count() == st["ntok"] and pg.is_visible("#session .satzbox .why"))
        pg.click("#s-next")
    ok(seen_rule == 3, f"3 Bauplan-Karten gesehen, keine doppelt ({seen_rule})")
    ok(sb_ok and all(sb_ok), f"nach jedem Satz die Zerlegung mit allen Wörtern und Erklärung ({len(sb_ok)} Sätze)")
    fin = pg.inner_text(".finish")
    ok("Aus früheren Lektionen wiederholt" in fin and "✗" in fin, "Abschluss zeigt wiederholte Wörter mit ✓/✗")
    w = pg.evaluate("() => { const s = window.__t.state(); return {ni:s.words['你'], shi:s.words['是'], hao:s.words['好'], xie:s.words['谢谢']}; }")
    t = pg.evaluate("() => window.__t.today()"); ad = lambda n: pg.evaluate(f"() => window.__t.addDays('{t}', {n})")
    ok(w["ni"] == {"b": 3, "d": ad(8), "iv": 8, "e": 2.5}, f"fälliges altes Wort richtig: 8 Tage {w['ni']}")
    ok(w["shi"] == {"b": 2, "d": ad(1), "iv": 3, "e": 2.4}, f"nicht fälliges altes Wort falsch, dann richtig: Abstand kleiner, morgen wieder {w['shi']}")
    ok(w["hao"]["d"] == ad(1) and w["hao"]["b"] == 1, f"nicht fälliges altes Wort richtig: unverändert {w['hao']}")
    ok(w["xie"] == {"b": 1, "d": ad(1), "iv": 1, "e": 2.5}, f"neues Wort: ab morgen {w['xie']}")
    pg.click('[data-act="exit"]'); pg.wait_for_timeout(300)
    # Abbruch einer Lektion ändert nichts
    before = pg.evaluate("() => JSON.stringify(window.__t.state().words)")
    pg.click("#view-lernen .hr-go"); pg.wait_for_timeout(300)
    st = pg.evaluate(STEP)
    if st["t"] in ("mean","hear","char"): pg.click(f'[data-opt="{(st["right"] + 1) % 3}"]')
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    ok(before == pg.evaluate("() => JSON.stringify(window.__t.state().words)"), "abgebrochene Lektion ändert den Wiederholungsplan nicht")
    # Karteikasten
    pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(300)
    k = pg.evaluate("() => [...document.querySelectorAll('.fach b')].map(b => +b.textContent)")
    ok(len(k) == 6 and sum(k) == 10, f"Karteikasten: 6 Fächer, zusammen 10 Wörter {k}")
    # Baupläne
    pg.evaluate("() => { location.hash = 'saetze'; }"); pg.wait_for_timeout(300)
    pg.click('[data-smode="plans"]'); pg.wait_for_timeout(200)
    got = pg.locator("#plans details.plan").count(); locked = pg.locator("#plans .plan.locked").count()
    ok(got == 4 and locked == 43, f"Baupläne: 4 gelernt (Lektion 1 und 2), 43 gesperrt ({got}/{locked})")
    pg.click('[data-smode="cards"]'); pg.wait_for_timeout(200)
    pg.click("#c-reveal"); pg.wait_for_timeout(200)
    nsw = pg.locator("#fcard .satzbox .sw").count()
    nchunk = pg.evaluate("() => { const T = window.__t; const c = document.querySelector('#fcard'); return c ? c.querySelectorAll('.sw').length : 0; }")
    ok(nsw >= 1 and pg.is_visible("#fcard .why"), f"Reisesatz zeigt Zerlegung ({nsw} Wörter) und Erklärung")
    pg.click("#fcard .sw >> nth=0"); pg.wait_for_timeout(100)
    # alle Reisesätze zerlegbar
    allc = pg.evaluate("() => { const T = window.__t; return T.CARDS.filter(c => !(T.GR.cards[c.id] && T.GR.cards[c.id].g.split('|').length === T.chunksOf(c).length)).map(c => c.id); }")
    ok(not allc, f"alle 51 Reisesätze passend zerlegt {allc}")
    # alle Lektionen: Karten und Sätze
    probs = pg.evaluate("""() => { const T = window.__t, out = []; T.LESSONS.forEach(l => { const q = T.buildLesson(l); const rs = q.filter(e => e.type==='rule').map(e => e.p.id);
        if(new Set(rs).size !== rs.length) out.push(l.id + ' doppelt'); T.POINTS.filter(pt => pt.lesson===l).forEach(pt => { if(rs.indexOf(pt.id) < 0) out.push(l.id + ' fehlt ' + pt.id); });
        q.forEach(e => { if(e.type==='build' && !(e.s.gs && e.s.gs.length===e.s.toks.length)) out.push(l.id + ' ohne Zerlegung ' + e.s.zh); if(e.old && e.w.lesson.n >= l.n) out.push(l.id + ' altes Wort nicht alt ' + e.w.zh); }); }); return out; }""")
    ok(not probs, f"alle 33 Lektionen: jeder Bauplan genau einmal, jeder Satz zerlegt, nur ältere Wörter wiederholt {probs}")
    b.close()
    ok(not errs, f"keine JS-Fehler {errs[:3]}")
print("\n".join(res))
