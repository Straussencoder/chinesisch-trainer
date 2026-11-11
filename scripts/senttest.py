# Prüft das Satz-Training: Lückensätze, »Welcher Satz ist richtig?«, Satz bauen mit getauschter Zeitangabe,
# nur gelernte Wörter, Einbau in Wiederholen und Lektionen, ganze Runde richtig und mit Fehlern, Karten.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
src = open(ROOT + "/scripts/fulltest.py").read()
STEP = src[src.index('STEP = """')+10:src.index('"""', src.index('STEP = """')+10)]
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
MARK = """(n) => { const T = window.__t, s = T.state(), t = T.today(); s.learn.done = {}; s.words = {}; T.LESSONS.slice(0, n).forEach(l => { s.learn.done[l.id] = {at:t, best:90}; l.W.forEach(w => s.words[w.zh] = {b:1, d:t, iv:1, e:2.5}); }); }"""
CUR = """() => { const S = window.__t.getS(); if(!S || S.finished) return null; const e = S.queue[0]; return {type:e.type, right: e.type==='gap' ? e.opts.indexOf(e.gw) : e.type==='judge' ? e.opts.findIndex(o => o.ok) : -1}; }"""
def play(pg, wrong_every=0):
    n = 0; types = []
    for _ in range(200):
        st = pg.evaluate(STEP)
        if st.get("finished") or st.get("none"): break
        c = pg.evaluate(CUR); t = st["type"]; types.append(t); n += 1
        wrong = wrong_every and n % wrong_every == 0 and not st.get("retry")
        if t in ("gap", "judge"):
            r = c["right"]; pg.click(f'#session [data-opt="{(r+1) % (3 if t=="gap" else 2) if wrong else r}"]')
        elif t == "sentmean": pg.click(f'#session [data-opt="{(st["right"]+1)%3 if wrong else st["right"]}"]')
        elif t == "build":
            for i in (list(reversed(st["order"])) if wrong else st["order"]): pg.click(f'#session [data-bank="{i}"]')
            pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }")
        pg.wait_for_timeout(25); pg.click("#s-next"); pg.wait_for_timeout(25)
    return types
with sync_playwright() as p:
    b = p.chromium.launch()
    for view, (w, h) in (("mobile", (390, 844)), ("desktop", (1366, 900))):
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); fontroute.setup(pg)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
        d = pg.evaluate("() => { const T = window.__t; return {n:T.DRILL.length, gap:T.DRILL.filter(s => s.gap).length, bad:T.DRILL.filter(s => s.bad).length, nolesson:T.DRILL.filter(s => !s.lesson).length, alt:T.DRILL.filter(s => s.alt.length).length}; }")
        ok(d["n"] == 210 and d["gap"] == 210 and d["bad"] >= 30 and d["nolesson"] == 0, f"{view}: Übungssätze geladen {d}")
        # --- nur gelernte Wörter, nach 10 Lektionen ---
        pg.evaluate(MARK, 10)
        aud = pg.evaluate("""() => { const T = window.__t, s = T.state(), bad = [], types = {};
          for(let r=0;r<40;r++){ T.startSentences(); const q = T.getS().queue;
            q.forEach(e => { types[e.type] = (types[e.type]||0)+1;
              const zs = (e.s ? e.s.toks.map(t => t.zh) : []).concat(e.type==='gap' ? e.opts.map(o => o.zh) : []).concat(e.type==='judge' ? e.s.bad.toks.map(t => t.zh) : []).concat(e.bank ? e.bank.map(b => b.zh) : []);
              if(e.type==='sentmean') e.opts.forEach(o => o.toks.forEach(t => zs.push(t.zh)));
              zs.forEach(z => { if(!s.words[z]) bad.push(e.type + ':' + z); }); });
            if(r===0) types.len = q.length; }
          return {bad:[...new Set(bad)], types}; }""")
        ok(not aud["bad"], f"{view}: nach 10 Lektionen nur gelernte Wörter in 40 Runden {aud['bad'][:8]}")
        tp = aud["types"]
        ok(tp.get("gap", 0) > 0 and tp.get("build", 0) > 0 and tp.get("judge", 0) > 0 and tp.get("sentmean", 0) > 0, f"{view}: alle vier Aufgabenarten kommen vor {tp}")
        ok(tp["len"] == 10, f"{view}: eine Runde hat 10 Sätze ({tp['len']})")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        # --- Lückensatz anzeigen ---
        pg.evaluate("""() => { const T = window.__t, s = T.DRILL.find(x => x.de === 'Ich trinke keinen Kaffee.'); const S = T.getS();
          T.startSentences(); const SS = T.getS(); SS.queue = [T.makeGap(s), T.makeJudge(T.DRILL.find(x => x.de === 'Ich habe keinen Kaffee.'))]; T.renderSession(); }""")
        pg.wait_for_timeout(100)
        ok(pg.locator("#session .gapslot").count() == 1 and pg.locator("#session .opts.g3 .opt").count() == 3, f"{view}: Lücke und drei Wörter zur Auswahl")
        txt = pg.inner_text("#session .gapsent")
        ok("不" not in txt and "我" in txt and "咖啡" in txt, f"{view}: das fehlende Wort steht nicht schon da ({txt!r})")
        ok(pg.inner_text("#session .prompt").find("Ich trinke keinen Kaffee") >= 0, f"{view}: deutscher Satz als Hilfe")
        c = pg.evaluate(CUR); pg.click(f'#session [data-opt="{(c["right"]+1)%3}"]'); pg.wait_for_timeout(80)
        ok(pg.locator("#session .s-foot.bad").count() == 1 and pg.locator("#session .gapfill").count() == 1, f"{view}: falsch: rot, Lücke zeigt das richtige Wort")
        ok(pg.locator("#session .satzbox .sw").count() == 4, f"{view}: Zerlegung mit allen 4 Wörtern")
        ov = pg.evaluate("() => { const s = document.getElementById('s-main'); return [document.scrollingElement.scrollWidth - innerWidth, s ? s.scrollWidth - s.clientWidth : 0]; }")
        ok(ov[0] <= 1 and ov[1] <= 1, f"{view}: kein seitlicher Überlauf {ov}")
        pg.click("#s-next"); pg.wait_for_timeout(80)
        # --- Welcher Satz ist richtig ---
        ok(pg.locator("#session .jopt").count() == 2, f"{view}: zwei Sätze zur Wahl")
        jt = pg.locator("#session .jopt .jhz").all_inner_texts()
        ok(sorted(jt) == sorted(["我没有咖啡。", "我不有咖啡。"]), f"{view}: richtiger und typischer falscher Satz {jt}")
        c = pg.evaluate(CUR); pg.click(f'#session [data-opt="{c["right"]}"]'); pg.wait_for_timeout(80)
        why = pg.inner_text("#session .jwhy")
        ok(pg.locator("#session .s-foot.ok").count() == 1 and "没" in why, f"{view}: richtig, mit Erklärung ({why[:50]!r})")
        pg.click("#s-next"); pg.wait_for_timeout(80)
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        # --- Satz bauen: getauschte Zeitangabe zählt ---
        alt = pg.evaluate("""() => { const T = window.__t, s = T.DRILL.find(x => x.de === 'Heute trinke ich keinen Kaffee.'); return [s.key, s.alt]; }""")
        ok(alt[1] == ["今天我不喝咖啡"], f"{view}: 我今天… darf auch 今天我… sein {alt}")
        no = pg.evaluate("() => { const T = window.__t; return T.DRILL.filter(s => s.alt.length).map(s => s.alt[0]).filter(a => /^(几|什么|哪)/.test(a)).length; }")
        ok(True, f"{view}: Tausch-Varianten, die mit einem Fragewort beginnen: {no}")
        # --- ganze Runde, alles richtig, dann mit Fehlern ---
        pg.evaluate(MARK, 20); pg.evaluate("() => window.__t.startSentences()"); pg.wait_for_timeout(100)
        types = play(pg)
        fin = pg.evaluate("() => { const S = window.__t.getS(); return S && S.finished; }")
        ok(fin and fin["pct"] == 100 and fin["xp"] == 10 and len(types) == 10, f"{view}: Runde ohne Fehler: 10 Aufgaben, 100 % {fin} {types}")
        ok("Satz-Training geschafft" in pg.inner_text("#session"), f"{view}: Abschluss-Text")
        pg.click('#session [data-act="exit"]'); pg.wait_for_timeout(150)
        pg.evaluate("() => window.__t.startSentences()"); pg.wait_for_timeout(100)
        types = play(pg, wrong_every=3)
        fin = pg.evaluate("() => { const S = window.__t.getS(); return S && S.finished; }")
        ok(fin and fin["pct"] < 100 and len(types) > 10, f"{view}: Runde mit Fehlern: falsche kommen nochmal ({len(types)} Aufgaben, {fin})")
        pg.click('#session [data-act="exit"]'); pg.wait_for_timeout(150)
        # --- Wiederholen hat drei Satz-Aufgaben ---
        rv = pg.evaluate("""() => { const T = window.__t; T.startReview(false); const q = T.getS().queue; return q.filter(e => ['gap','build','judge','sentmean'].includes(e.type)).map(e => e.type); }""")
        ok(len(rv) == 3 and "gap" in rv, f"{view}: Wiederholen: drei Sätze dabei {rv}")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        # --- Lektion: Lückensatz am Ende ---
        lg = pg.evaluate("""() => { const T = window.__t; let n = 0, last = 0; T.LESSONS.forEach(l => { const q = T.buildLesson(l); const g = q.filter(e => e.type === 'gap'); if(g.length){ n++; if(q[q.length-1].type === 'gap') last++; } }); return [n, last]; }""")
        ok(lg[0] >= 28 and lg[0] == lg[1], f"{view}: Lektionen mit Lückensatz am Schluss {lg}")
        # --- Karten ---
        pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(250)
        ok(pg.locator('#view-wiederholen [data-act="sentprac"]').count() == 1 and not pg.locator('#view-wiederholen [data-act="sentprac"]').is_disabled(), f"{view}: Karte Satz-Training in Wiederholen")
        pg.click('#view-wiederholen [data-act="sentprac"]'); pg.wait_for_timeout(150)
        ok(pg.evaluate("() => window.__t.getS() && window.__t.getS().kind === 'sent'"), f"{view}: Knopf startet das Satz-Training")
        ok("Satz-Training" in pg.inner_text("#session .s-ctx"), f"{view}: Kopfzeile »Satz-Training«")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        pg.evaluate("() => { const T = window.__t, s = T.state(); s.learn.done = {}; s.words = {}; location.hash = 'lernen'; }"); pg.wait_for_timeout(150)
        pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(250)
        ok(pg.locator('#view-wiederholen [data-act="sentprac"]').count() == 0 or pg.locator('#view-wiederholen [data-act="sentprac"]').is_disabled(), f"{view}: ohne gelernte Lektionen ist das Satz-Training gesperrt")
        ok(not errs, f"{view}: keine JS-Fehler {errs[:3]}")
        ctx.close()
    b.close()
print("\n".join(res)); print(sum(1 for r in res if r.startswith("OK")), "/", len(res))
