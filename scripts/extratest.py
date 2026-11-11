# Prüft Tagesrunde, Tonpaare, Pinyin-Tabelle und HSK-1-Probetest.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import os, sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
URL = os.environ.get("ZH_URL", "file://" + ROOT + "/test/index.html")
src = open(ROOT + "/scripts/fulltest.py").read()
STEP = src[src.index('STEP = """')+10:src.index('"""', src.index('STEP = """')+10)]
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
MARK = """(n) => { const T = window.__t, s = T.state(), t = T.today(); s.learn.done = {}; s.words = {}; T.LESSONS.slice(0, n).forEach(l => { s.learn.done[l.id] = {at:t, best:90}; l.W.forEach(w => s.words[w.zh] = {b:1, d:t, iv:1, e:2.5}); }); }"""
RIGHT = """() => { const S = window.__t.getS(); if(!S || S.finished) return null; const e = S.queue[0];
  if(!e.opts) return {type:e.type, right:-1, n:0};
  let r; if(e.type==='sentmean' || e.type==='shear') r = e.opts.indexOf(e.s); else if(e.type==='gap') r = e.opts.indexOf(e.gw); else if('ok' in e.opts[0]) r = e.opts.findIndex(o => o.ok); else r = e.opts.indexOf(e.w);
  return {type:e.type, right:r, n:e.opts.length, part:e.part}; }"""
def play(pg, wrong_every=0, limit=200):
    n = 0; types = []
    for _ in range(limit):
        st = pg.evaluate(STEP)
        if st.get("finished") or st.get("none"): break
        c = pg.evaluate(RIGHT); t = st["type"]; types.append(t); n += 1
        wrong = wrong_every and n % wrong_every == 0 and not st.get("retry")
        if t in ("intro", "rule"): pg.click("#s-next"); continue
        if c["n"]: pg.click(f'#session [data-opt="{(c["right"]+1) % c["n"] if wrong else c["right"]}"]')
        elif t == "write": pg.fill("#w-in", "xx" if wrong else st["typed"]); pg.keyboard.press("Enter")
        elif t == "tone": pg.click(f'#session [data-stone="{(st["tone"]%4)+1 if wrong else st["tone"]}"]')
        elif t == "pairs":
            for li, ri in enumerate(st["pairs"]): pg.click(f'#session [data-pl="{li}"]'); pg.click(f'#session [data-pr="{ri}"]')
        elif t == "build":
            for i in (list(reversed(st["order"])) if wrong else st["order"]): pg.click(f'#session [data-bank="{i}"]')
            pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }")
        pg.wait_for_timeout(25); pg.click("#s-next"); pg.wait_for_timeout(25)
    return types
def leave(pg):
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    if pg.locator('#session [data-act="exit"]').count(): pg.click('#session [data-act="exit"]'); pg.wait_for_timeout(100)
with sync_playwright() as p:
    b = p.chromium.launch()
    for view, (w, h) in (("mobile", (390, 844)), ("desktop", (1366, 900))):
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); fontroute.setup(pg)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.add_init_script("window.__plays=0; const op = HTMLMediaElement.prototype.play; HTMLMediaElement.prototype.play = function(){ window.__plays++; return op.call(this).catch(()=>{}); };")
        pg.goto(URL); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
        # --- Tagesrunde ---
        ok(pg.locator(".day-banner").count() == 0, f"{view}: ohne gelernte Wörter keine Tagesrunde")
        pg.evaluate(MARK, 14); pg.evaluate("() => { location.hash = 'saetze'; }"); pg.wait_for_timeout(80); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(250)
        txt = pg.inner_text(".day-banner")
        ok("12 fällige Wörter" in txt and "Sätze" in txt and "Zahlen" in txt, f"{view}: Banner nennt Wörter, Sätze, Zahlen ({txt.splitlines()[-2] if len(txt.splitlines())>1 else txt!r})")
        pg.click(".day-banner"); pg.wait_for_timeout(150)
        q = pg.evaluate("() => { const S = window.__t.getS(); return {kind:S.kind, sub:S.sub, types:S.queue.map(e => e.type)}; }")
        ok(q["kind"] == "day" and q["sub"] == "review" and any(t in ("nread", "build") for t in q["types"]) and "gap" in q["types"], f"{view}: Tagesrunde mit Wörtern, Sätzen, Zahlen {q['types']}")
        play(pg)
        fin = pg.inner_text("#session")
        ok("Tagesrunde geschafft" in fin and pg.locator('#session #fin-go[data-lesson="l15"]').count() == 1, f"{view}: Abschluss bietet Lektion 15 an")
        due = pg.evaluate("() => window.__t.dueWords().length")
        ok(due == 0 or due < 72, f"{view}: fällige Wörter abgearbeitet (noch {due})")
        pg.click('#session [data-act="exit"]'); pg.wait_for_timeout(200)
        ok("Tagesrunde geschafft" in pg.inner_text(".day-banner"), f"{view}: Banner zeigt »geschafft«")
        # --- Tonpaare ---
        pg.evaluate("() => { const s = window.__t.state(); s.tpair = {}; s.prefs.tmode = 'word'; location.hash = 'toene'; }"); pg.wait_for_timeout(300)
        for _ in range(3):
            pg.evaluate("() => { const T = window.__t; T.newToneQ(); }")
            tones = pg.evaluate("() => window.__t.getTq().item.tones")
            for k in tones: pg.evaluate(f"() => window.__t.pickTone({k})")
        tp = pg.evaluate("() => window.__t.state().tpair")
        ok(sum(v["n"] for v in tp.values()) == 3 and all(v["ok"] == v["n"] for v in tp.values()), f"{view}: Tonpaare werden gezählt {tp}")
        pg.evaluate("() => { window.__t.state().tpair = {'4-3':{n:6, ok:1}, '1-1':{n:6, ok:6}}; }")
        wp = pg.evaluate("() => { const T = window.__t; let c = 0; for(let i=0;i<300;i++){ T.newToneQ(); if(T.getTq().item.tones.join('-')==='4-3') c++; } return c; }")
        ok(wp > 300*0.3, f"{view}: schwaches Tonpaar 4-3 kommt öfter ({wp} von 300, ohne Gewichtung etwa 34)")
        pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(80); pg.evaluate("() => { location.hash = 'toene'; }"); pg.wait_for_timeout(300)
        cells = pg.locator("#t-stats .tpgrid .tpc").count()
        ok(cells == 25 and pg.locator("#t-stats .tpc.low").count() == 1 and pg.locator("#t-stats .tpc.good").count() >= 1, f"{view}: 4×4-Raster mit Farben ({cells} Felder)")
        # --- Pinyin-Tabelle ---
        n = pg.locator("#py-tab .py-chip").count()
        ok(n == 405, f"{view}: Pinyin-Tabelle mit 405 Silben ({n})")
        lv = pg.locator('#py-tab .py-chip[data-py="lv"]').text_content()
        ok(lv == "lü", f"{view}: lv wird als lü angezeigt ({lv})")
        pg.locator("#py-tab").scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
        pg.evaluate("() => { window.__plays = 0; }")
        pg.evaluate("() => document.querySelectorAll('#py-tab .py-row')[15].open = true"); pg.wait_for_timeout(50)
        pg.click('#py-tab .py-chip[data-py="zhi"]'); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => !!window.ZH_PY_AUDIO && window.__plays >= 1"), f"{view}: Silbe antippen spielt die Aufnahme")
        miss = pg.evaluate("() => [...document.querySelectorAll('#py-tab .py-chip')].map(b => b.dataset.py).filter(s => !window.ZH_PY_AUDIO[s + '1'])")
        ok(not miss, f"{view}: zu jeder Silbe gibt es eine Aufnahme {miss[:5]}")
        ov = pg.evaluate("() => document.scrollingElement.scrollWidth - innerWidth")
        ok(ov <= 1, f"{view}: kein seitlicher Überlauf ({ov})")
        pg.evaluate("() => window.__t.setQuiet(30)"); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(80); pg.evaluate("() => { location.hash = 'toene'; }"); pg.wait_for_timeout(250)
        ok(pg.locator('#py-tab .py-chip[disabled]').count() == 405, f"{view}: Ohne Ton sind die Silben stumm geschaltet")
        pg.evaluate("() => window.__t.setQuiet(null)")
        # --- HSK-Probetest ---
        pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(250)
        ok(pg.locator('#view-wiederholen [data-act="hsk"]').is_disabled(), f"{view}: Probetest vor Lektion 33 gesperrt")
        pg.evaluate(MARK, 33); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(80); pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(250)
        pg.click('#view-wiederholen [data-act="hsk"]'); pg.wait_for_timeout(150)
        hq = pg.evaluate("() => { const S = window.__t.getS(); return {kind:S.kind, n:S.queue.length, h:S.queue.filter(e => e.part==='h').length, l:S.queue.filter(e => e.part==='l').length, types:[...new Set(S.queue.map(e => e.type))], first:S.queue.findIndex(e => e.part==='l'), lastH:S.queue.map(e => e.part).lastIndexOf('h')}; }")
        ok(hq["kind"] == "hsk" and hq["n"] == 40 and hq["h"] == 20 and hq["l"] == 20, f"{view}: 40 Fragen, 20 Hören, 20 Lesen {hq}")
        ok(hq["lastH"] < hq["first"], f"{view}: erst Hören, dann Lesen")
        ok("Hören" in pg.inner_text("#session .s-ctx"), f"{view}: Kopfzeile zeigt den Teil")
        mute = pg.evaluate("() => window.__t.getS().queue.filter(e => e.part==='l' && (e.type==='mean' || e.type==='sentmean')).every(e => e.mute)")
        ok(mute, f"{view}: im Leseteil spielt nichts von selbst")
        types = play(pg, wrong_every=8)
        fin = pg.evaluate("() => { const S = window.__t.getS(); return S && S.finished && S.hskRes; }")
        ok(fin and len(types) == 40 and fin["h"] < 100 and fin["l"] < 100, f"{view}: keine zweite Chance, Punkte pro Teil {fin} ({len(types)} Aufgaben)")
        txt = pg.inner_text("#session .finish")
        ok("von 200" in txt and "bestanden" in txt and "keine offizielle" in txt, f"{view}: Ergebnis mit 200 Punkten und Hinweis")
        ok(len(pg.evaluate("() => window.__t.state().hsk")) == 1, f"{view}: Ergebnis gespeichert")
        pg.click('#session [data-act="exit"]'); pg.wait_for_timeout(150)
        pg.evaluate("() => window.__t.setQuiet(30)"); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(80); pg.evaluate("() => { location.hash = 'wiederholen'; }"); pg.wait_for_timeout(250)
        ok(pg.locator('#view-wiederholen [data-act="hsk"]').is_disabled(), f"{view}: Ohne Ton kein Probetest (Hörteil)")
        pg.evaluate("() => window.__t.setQuiet(null)")
        ok(not errs, f"{view}: keine JS-Fehler {errs[:3]}")
        ctx.close()
    b.close()
print("\n".join(res)); print(sum(1 for r in res if r.startswith("OK")), "/", len(res))
