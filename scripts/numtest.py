# Prüft das Zahlen-Training: Zahlen richtig gebaut (1 bis 99), typische Verwechslungen als Auswahl,
# keine 2 bei Uhrzeit und Mengen, Preis/Uhrzeit/Datum erst nach den passenden Lektionen, ganze Runde, Ohne Ton, Handzeichen.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import os, sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
URL = os.environ.get("ZH_URL", "file://" + ROOT + "/test/index.html")
src = open(ROOT + "/scripts/fulltest.py").read()
STEP = src[src.index('STEP = """')+10:src.index('"""', src.index('STEP = """')+10)]
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
MARK = """(n) => { const T = window.__t, s = T.state(), t = T.today(); s.learn.done = {}; s.words = {}; T.LESSONS.slice(0, n).forEach(l => { s.learn.done[l.id] = {at:t, best:90}; l.W.forEach(w => s.words[w.zh] = {b:1, d:t, iv:1, e:2.5}); }); }"""
CUR = """() => { const S = window.__t.getS(); if(!S || S.finished) return null; const e = S.queue[0]; return {type:e.type, right: e.opts && e.opts[0] && 'ok' in e.opts[0] ? e.opts.findIndex(o => o.ok) : -1, n:e.opts ? e.opts.length : 0}; }"""
CN = {1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九",10:"十"}
def cn(n):
    if n <= 10: return CN[n]
    if n < 20: return "十" + CN[n-10]
    return CN[n//10] + "十" + (CN[n%10] if n % 10 else "")
def play(pg, wrong_every=0):
    n = 0; types = []
    for _ in range(200):
        st = pg.evaluate(STEP)
        if st.get("finished") or st.get("none"): break
        c = pg.evaluate(CUR); t = st["type"]; types.append(t); n += 1
        wrong = wrong_every and n % wrong_every == 0 and not st.get("retry")
        if t in ("nread", "nhear", "nctx"): pg.click(f'#session [data-opt="{(c["right"]+1) % c["n"] if wrong else c["right"]}"]')
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
        pg.goto(URL); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
        # --- Zahlen bauen ---
        built = pg.evaluate("() => { const T = window.__t, o = {}; for(let n=1;n<100;n++) o[n] = T.numToks(n).map(t => t.zh).join(''); return o; }")
        wrongs = [n for n in range(1, 100) if built[str(n)] != cn(n)]
        ok(not wrongs, f"{view}: 1 bis 99 richtig zusammengesetzt (Fehler bei {wrongs[:5]})")
        py = pg.evaluate("() => window.__t.numToks(11).map(t => t.py).join(' ')")
        ok(py == "shí yī", f"{view}: 11 = shí yī ({py})")
        cf = pg.evaluate("() => { const T = window.__t; return {a:T.numConfusers(18, 1, 99), b:T.numConfusers(80, 1, 99), c:T.numConfusers(4, 1, 99), d:T.numConfusers(37, 1, 99), e:T.numConfusers(3, 1, 12, x => x===2)}; }")
        ok(80 in cf["a"] and 18 in cf["b"] and 10 in cf["c"] and 73 in cf["d"], f"{view}: typische Verwechslungen 18/80, 4/10, 37/73 {cf}")
        ok(2 not in cf["e"] and len(cf["e"]) == 3, f"{view}: keine 2 Uhr in der Auswahl {cf['e']}")
        # --- gesperrt vor Lektion 6 ---
        pg.evaluate(MARK, 5); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(100); pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(250)
        ok(pg.locator('#view-wiederholen [data-act="numprac"]').is_disabled(), f"{view}: vor Lektion 6 gesperrt")
        pg.evaluate("() => window.__t.startNumbers()")
        ok(pg.evaluate("() => !window.__t.getS()"), f"{view}: Start vor Lektion 6 wird verhindert")
        # --- nach Lektion 6: nur reine Zahlen ---
        pg.evaluate(MARK, 6)
        a = pg.evaluate("""() => { const T = window.__t, s = T.state(), types = {}, bad = [];
          for(let r=0;r<40;r++){ T.startNumbers(); T.getS().queue.forEach(e => { types[e.type] = (types[e.type]||0)+1;
            const zs = (e.s ? e.s.toks.map(t => t.zh) : []).concat(e.bank ? e.bank.map(b => b.zh) : []); zs.forEach(z => { if(!s.words[z]) bad.push(z); }); }); }
          return {types, bad:[...new Set(bad)], len:T.getS().queue.length}; }""")
        ok(not a["bad"] and "nctx" not in a["types"], f"{view}: nach Lektion 6 nur Zahlen, keine fremden Wörter {a['types']} {a['bad']}")
        ok(a["len"] == 10 and a["types"].get("nread") and a["types"].get("build") and a["types"].get("nhear"), f"{view}: 10 Aufgaben, lesen, bauen, hören {a['types']}")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        # --- Preis, Uhrzeit, Datum nach den Lektionen ---
        pg.evaluate(MARK, 33)
        cx = pg.evaluate("""() => { const T = window.__t, out = {price:[], time:[], date:[]}, bad = [];
          for(let r=0;r<200;r++){ ['price','time','date'].forEach(k => { const e = T.makeNumCtx(k); out[k].push(e.s.zh);
            if(e.opts.length !== 4 || e.opts.filter(o => o.ok).length !== 1 || new Set(e.opts.map(o => o.label)).size !== 4) bad.push(k + ':' + e.s.zh + ':' + e.opts.map(o => o.label).join('/'));
            if(k !== 'date' && e.opts.some(o => /^2 /.test(o.label))) bad.push('zwei:' + e.s.zh); }); }
          return {bad, two:out.time.filter(z => z === '现在二点。').length + out.price.filter(z => z === '这个二块。').length, ex:[out.price[0], out.time[0], out.date[0]]}; }""")
        ok(not cx["bad"] and cx["two"] == 0, f"{view}: Preis, Uhrzeit, Datum: 4 verschiedene Antworten, nie »2 Uhr« oder »2 Kuai« {cx['bad'][:3]} {cx['ex']}")
        # --- ganze Runde ---
        pg.evaluate("() => { window.__t.state().num = {}; window.__t.startNumbers(); }"); pg.wait_for_timeout(100)
        ok("Zahlen-Training" in pg.inner_text("#session .s-ctx"), f"{view}: Kopfzeile »Zahlen-Training«")
        types = play(pg)
        fin = pg.evaluate("() => { const S = window.__t.getS(); return S && S.finished; }")
        ok(fin and fin["pct"] == 100 and fin["xp"] == 10 and len(types) == 10, f"{view}: Runde ohne Fehler {fin} {types}")
        ok("Zahlen-Training geschafft" in pg.inner_text("#session"), f"{view}: Abschluss-Text")
        pg.click('#session [data-act="exit"]'); pg.wait_for_timeout(150)
        pg.evaluate("() => window.__t.startNumbers()"); pg.wait_for_timeout(100)
        types = play(pg, wrong_every=2)
        miss = pg.evaluate("() => window.__t.state().num")
        ok(len(types) > 10 and len(miss) >= 1, f"{view}: Fehler kommen nochmal und werden gemerkt ({len(types)} Aufgaben, {miss})")
        pg.click('#session [data-act="exit"]'); pg.wait_for_timeout(150)
        pk = pg.evaluate("() => { const T = window.__t, m = T.state().num, k = Object.keys(m).map(Number); let hit = 0; for(let r=0;r<20;r++){ T.startNumbers(); const ns = T.getS().queue.map(e => e.n); if(k.some(x => ns.includes(x))) hit++; } return hit; }")
        ok(pk == 20, f"{view}: gemerkte Zahlen kommen in der nächsten Runde wieder ({pk}/20)")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        # --- Anzeige: Lesen und Bauen ---
        pg.evaluate("() => { const T = window.__t; T.startNumbers(); const S = T.getS(); S.queue = [T.makeNum('nread', 18), T.makeNum('nbuild', 47), T.makeNum('nhear', 80)]; T.renderSession(); }"); pg.wait_for_timeout(100)
        ok(pg.inner_text("#session .sent").replace("\n", "").startswith("十") and pg.locator("#session .nopt").count() == 4, f"{view}: 十八 lesen, vier Zahlen zur Auswahl")
        c = pg.evaluate(CUR); pg.click(f'#session [data-opt="{c["right"]}"]'); pg.wait_for_timeout(80)
        how = pg.inner_text("#session .numhow") if pg.locator("#session .numhow").count() else ""
        ok("10 + 8" in how, f"{view}: Erklärung nach der Antwort ({how!r})")
        ov = pg.evaluate("() => { const s = document.getElementById('s-main'); return [document.scrollingElement.scrollWidth - innerWidth, s ? s.scrollWidth - s.clientWidth : 0]; }")
        ok(ov[0] <= 1 and ov[1] <= 1, f"{view}: kein seitlicher Überlauf {ov}")
        pg.click("#s-next"); pg.wait_for_timeout(80)
        ok(pg.inner_text("#session .bignum") == "47" and "Schreib die Zahl" in pg.inner_text("#session .kicker"), f"{view}: 47 auf Chinesisch bauen")
        st = pg.evaluate(STEP)
        for i in st["order"]: pg.click(f'#session [data-bank="{i}"]')
        pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }"); pg.wait_for_timeout(80)
        ok(pg.locator("#session .s-foot.ok").count() == 1, f"{view}: 四十七 richtig gebaut")
        pg.click("#s-next"); pg.wait_for_timeout(80)
        # --- Ohne Ton: Hören wird Lesen ---
        pg.evaluate("() => window.__t.setQuiet(30)"); pg.wait_for_timeout(50)
        pg.evaluate("() => window.__t.renderSession()")
        ok(pg.evaluate("() => window.__t.getS().queue.every(e => e.type !== 'nhear')") or pg.locator("#session .bigplay").count() == 0, f"{view}: Ohne Ton keine Höraufgabe mehr")
        nq = pg.evaluate("() => { const T = window.__t; let n = 0; for(let r=0;r<20;r++){ T.startNumbers(); n += T.getS().queue.filter(e => e.type === 'nhear').length; } return n; }")
        ok(nq == 0, f"{view}: Ohne Ton: neue Runden ohne Hören ({nq})")
        pg.evaluate("() => window.__t.setQuiet(null)")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        # --- Handzeichen auf der Wortkarte und in der Anleitung ---
        pg.evaluate("() => { const T = window.__t, s = T.state(); s.learn.done = {}; s.words = {}; T.LESSONS.slice(0, 4).forEach(l => { s.learn.done[l.id] = {at:T.today(), best:90}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.today()}); }); T.startLesson('l6'); const S = T.getS(); S.queue.unshift({id:9999, type:'intro', w:T.WORD['六']}); T.renderSession(); }"); pg.wait_for_timeout(150)
        hand = pg.inner_text("#session .wordcard .hand") if pg.locator("#session .wordcard .hand").count() else ""
        ok("Daumen und kleiner Finger" in hand, f"{view}: 六 zeigt das Handzeichen ({hand[:40]!r})")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]')
        pg.evaluate(MARK, 6); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(100); pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(250)
        pg.click("#view-wiederholen .numguide summary"); pg.wait_for_timeout(100)
        g = pg.inner_text("#view-wiederholen .numguide")
        ok("十八" in g and "两" in g and "yāo" in g and g.count("\n") > 10, f"{view}: Anleitung mit 18/80, 两, yāo und Handzeichen")
        ok(not errs, f"{view}: keine JS-Fehler {errs[:3]}")
        ctx.close()
    b.close()
print("\n".join(res)); print(sum(1 for r in res if r.startswith("OK")), "/", len(res))
