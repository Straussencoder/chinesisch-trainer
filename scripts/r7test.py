# Prüft Runde 7 (12.11.2026): Ton-Duell 2 gegen 3, hartnäckige Wörter neu erklären, Tagesrunde zuerst nach einer Pause,
# Hinweise in der Heute-Karte (schwache Lektion, neu freie Übung), Pluszeichen beim Satzbauen, neues Feld tips im Lernstand
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
from playwright.sync_api import sync_playwright
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
URL = "file://" + ROOT + "/test/index.html"
# Lernstand ähnlich wie nach sechs Lektionen; best = Ergebnis auf Anhieb je Lektion, due = Wörter heute fällig
SETUP = """([best, due]) => { const T = window.__t, s = T.state(), t = T.today();
  T.LESSONS.slice(0, 6).forEach((l, i) => { s.learn.done[l.id] = {at:T.addDays(t, -5), best:best[i]}; l.W.forEach(w => s.words[w.zh] = {b:1, d:due ? T.addDays(t, -2) : T.addDays(t, 2), iv:1, e:2.5}); });
  location.hash = 'wiederholen'; }"""
def fresh(b, view):
    ctx = b.new_context(viewport={"width": 390, "height": 844} if view == "mobile" else {"width": 1280, "height": 860})
    pg = ctx.new_page(); fontroute.setup(pg)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    return ctx, pg, errs
def home(pg):
    pg.evaluate("() => { location.hash = 'spiel'; }"); pg.wait_for_timeout(80); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(300)
with sync_playwright() as p:
    b = p.chromium.launch()
    for view in ["mobile", "desktop"]:
        # --- Ton-Duell ---
        ctx, pg, errs = fresh(b, view)
        n = pg.evaluate("() => window.ZH_DATA.duel.length")
        miss = pg.evaluate("() => window.ZH_DATA.duel.flatMap(d => [d[0] + '2', d[0] + '3']).filter(k => !window.__t.clip('s', k))")
        ok(n == 17 and not miss, f"{view}: 17 Silbenpaare, zu jedem Ton eine Aufnahme ({miss})")
        bad = pg.evaluate("() => window.ZH_DATA.duel.filter(d => window.__t.toneOf(d[2]) !== 2 || window.__t.toneOf(d[5]) !== 3 || d[2].normalize('NFD').replace(/[\\u0300-\\u036f]/g, '') !== d[0] || d[5].normalize('NFD').replace(/[\\u0300-\\u036f]/g, '') !== d[0]).map(d => d[0])")
        ok(not bad, f"{view}: Pinyin im Duell passt zu Silbe und Ton ({bad})")
        pg.evaluate("() => { const s = window.__t.state(); s.conf = {'2>3':5, '3>2':1, '1>4':2}; s.prefs.tmode = 'syl'; location.hash = 'toene'; }"); pg.wait_for_timeout(300)
        ok(pg.is_visible("#t-hint") and "2. und den 3. Ton (6-mal)" in pg.inner_text("#t-hint"), f"{view}: Hinweis auf die Verwechslung 2/3 mit Zahl")
        pg.click('#t-hint [data-tmode="duel"]'); pg.wait_for_timeout(200)
        ok(pg.evaluate("() => window.__t.state().prefs.tmode") == "duel" and pg.locator("#t-btns .tbtn").count() == 2 and not pg.is_visible("#t-hint"), f"{view}: Duell mit zwei Tonknöpfen, Hinweis weg")
        seen = set(); tones = set(); okc = 0
        for k in range(24):
            it = pg.evaluate("() => { const q = window.__t.getTq(); return {base:q.item.duel.base, t:q.item.tones[0], py:q.item.py, zh:q.item.zh}; }")
            seen.add(it["base"]); tones.add(it["t"])
            if k == 0: ok(it["py"] not in pg.inner_text("#t-reveal") and it["base"] in pg.inner_text("#t-reveal"), f"{view}: vor der Antwort nur die Silbe ohne Ton ({it['base']})")
            pg.keyboard.press("1"); pg.wait_for_timeout(30)
            if k == 0: ok(not pg.evaluate("() => window.__t.getTq().done"), f"{view}: Taste 1 zählt im Duell nicht")
            pg.click(f'[data-tone="{it["t"] if k % 3 else (5 - it["t"])}"]'); pg.wait_for_timeout(60)
            if k == 0:
                rows = pg.locator(".duel-row").count()
                ok(rows == 2 and pg.locator(".duel-row.on").count() == 1 and pg.is_visible('[data-act="duelboth"]'), f"{view}: danach beide Töne zum Anhören, der gespielte markiert")
            if k % 3: okc += 1
            pg.click("#t-next"); pg.wait_for_timeout(40)
        st = pg.evaluate("() => window.__t.state().tones")
        ok(len(seen) >= 8 and tones == {2, 3}, f"{view}: Duell wechselt Silben und Töne ({len(seen)} Silben, Töne {sorted(tones)})")
        ok(st["2"]["n"] + st["3"]["n"] == 24 and st["2"]["ok"] + st["3"]["ok"] == okc and st["1"]["n"] == 0 and st["4"]["n"] == 0, f"{view}: Duell zählt in der Trefferquote nur Ton 2 und 3 ({st})")
        # ohne Ton: Duell nimmt keine Antwort an, Zeichen bleibt verdeckt
        pg.evaluate("() => { window.__t.setQuiet(30); location.hash = 'lernen'; }"); pg.wait_for_timeout(60); pg.evaluate("() => { location.hash = 'toene'; }"); pg.wait_for_timeout(200)
        before_n = pg.evaluate("() => window.__t.state().tones['2'].n + window.__t.state().tones['3'].n")
        pg.evaluate("() => window.__t.pickTone(2)"); pg.keyboard.press("3"); pg.wait_for_timeout(60)
        ok(pg.evaluate("() => window.__t.state().tones['2'].n + window.__t.state().tones['3'].n") == before_n and pg.locator("#t-zis .q").count() == 1 and pg.locator("#t-btns .tbtn[disabled]").count() == 2 and pg.locator('#t-reveal [data-act="quietoff"]').count() == 1, f"{view}: ohne Ton ist das Duell gesperrt und verrät nichts")
        pg.evaluate("() => window.__t.setQuiet(null)")
        # Wörter-Modus: ohne geübte Tonpaare kommt der schwächste Einzelton öfter
        pg.evaluate("() => { const s = window.__t.state(); s.tpair = {}; s.tones = {'1':{n:10,ok:9}, '2':{n:10,ok:2}, '3':{n:10,ok:9}, '4':{n:10,ok:9}}; s.prefs.tmode = 'word'; }")
        share = pg.evaluate("() => { const T = window.__t; let c = 0; for(let i=0;i<400;i++){ T.newToneQ(); if(T.getTq().item.tones.indexOf(2)>=0) c++; } return c; }")
        base = pg.evaluate("() => window.__t.TONE_WORDS.filter(w => w.tones.indexOf(2)>=0).length / window.__t.TONE_WORDS.length * 400")
        ok(share > base + 40, f"{view}: Wörter mit dem schwachen 2. Ton kommen öfter ({share} von 400, ohne Gewichtung etwa {round(base)})")
        ok(not errs, f"{view}: keine JS-Fehler (Duell) {errs[:3]}")
        ctx.close()
        # --- hartnäckige Wörter ---
        ctx, pg, errs = fresh(b, view)
        pg.evaluate(SETUP, [[100, 83, 61, 70, 90, 76], True])
        pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today();
          s.err['国'] = {n:9, ok:0, last:T.addDays(t, -3)}; s.err['九'] = {n:5, ok:1, last:T.addDays(t, -3)}; s.err['我'] = {n:6, ok:4, last:t}; s.err['你'] = {n:3, ok:0, last:t}; }""")
        order = pg.evaluate("() => window.__t.dueSorted(window.__t.dueWords()).slice(0, 2).map(w => w.zh).sort().join('')")
        ok(order == "九国", f"{view}: hartnäckige Wörter stehen in der Wiederholung vorne ({order})")
        q = pg.evaluate("() => { window.__t.startReview(); return window.__t.getS().queue.map(e => ({t:e.type, re:!!e.re, zh:e.w ? e.w.zh : ''})); }")
        def before(zh):
            i = next((k for k, e in enumerate(q) if e["re"] and e["zh"] == zh), -1); j = next((k for k, e in enumerate(q) if not e["re"] and e["zh"] == zh and e["t"] != "pairs"), 99)
            return 0 <= i < j
        ok(before("国") and before("九"), f"{view}: Wortkarte vor der ersten Frage zu 国 und 九")
        gap = min((next(k for k, e in enumerate(q) if not e["re"] and e["zh"] == zh and e["t"] != "pairs") - next(k for k, e in enumerate(q) if e["re"] and e["zh"] == zh)) for zh in ("国", "九"))
        ok(gap >= 3, f"{view}: zwischen Karte und Frage liegen mindestens zwei andere Aufgaben (Abstand {gap})")
        pw = pg.evaluate("() => { const S = window.__t.getS(); const p = S.queue.find(e => e.type === 'pairs'); return p ? p.ws.map(w => w.zh) : []; }")
        ok("国" not in pw and "九" not in pw, f"{view}: hartnäckige Wörter nicht schon im Paare-Finden vor ihrer Karte ({pw})")
        ok(not any(e["re"] and e["zh"] in ("我", "你") for e in q), f"{view}: keine Karte für 我 (danach oft richtig) und 你 (erst 3 Fehler)")
        pg.evaluate("() => { const S = window.__t.getS(); const i = S.queue.findIndex(e => e.re); S.queue.unshift(S.queue.splice(i, 1)[0]); window.__t.renderSession(); }"); pg.wait_for_timeout(150)
        txt = pg.inner_text("#session .s-main")
        ok("Nochmal erklärt" in txt and "-mal falsch" in txt and pg.locator("#session .wordcard .mnemo").count() >= 1, f"{view}: Karte »Nochmal erklärt« mit Merkhilfe")
        zh0 = pg.evaluate("() => window.__t.getS().queue[0].w.zh")
        ok(pg.evaluate(f"() => window.__t.state().err['{zh0}'].re") == pg.evaluate("() => window.__t.today()"), f"{view}: angezeigt wird vermerkt ({zh0})")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
        pg.evaluate("() => { window.__t.exitSession(); }"); pg.wait_for_timeout(100)
        q2 = pg.evaluate("() => { window.__t.startReview(); return window.__t.getS().queue.filter(e => e.re).map(e => e.w.zh); }")
        ok(zh0 not in q2, f"{view}: ohne neuen Fehler kommt die Karte nicht gleich wieder ({q2})")
        pg.evaluate("() => { window.__t.exitSession(); }")
        ok(not errs, f"{view}: keine JS-Fehler (Wortkarte) {errs[:3]}")
        ctx.close()
        # --- nach einer Pause: Tagesrunde zuerst ---
        ctx, pg, errs = fresh(b, view)
        pg.evaluate(SETUP, [[100, 83, 61, 70, 90, 76], True]); home(pg)
        due = pg.evaluate("() => window.__t.dueWords().length")
        ok(due > 15 and pg.locator('#view-lernen .hr-btn[data-act="dayround"]').count() == 1 and "Erst wiederholen" in pg.inner_text(".hero-ribbon"), f"{view}: {due} fällig: oben zuerst die Tagesrunde")
        ok(pg.locator('#view-lernen .hr-go[data-lesson="l7"]').count() == 1, f"{view}: die nächste Lektion bleibt als zweiter Knopf")
        ok(f"{due} Wörter warten" in pg.inner_text(".day-banner") and "12 fällige Wörter" in pg.inner_text(".day-banner"), f"{view}: Heute-Karte sagt, wie viele warten")
        ok(pg.locator(".daycard .tip-row").count() == 0, f"{view}: bei vielen fälligen Wörtern keine weiteren Hinweise")
        pg.evaluate("() => { window.__t.state().days[window.__t.today()] = Object.assign(window.__t.state().days[window.__t.today()] || {}, {round:1}); }"); home(pg)
        ok(pg.locator("#view-lernen .hr-btn").count() == 0 and "Weiter mit Lektion 7" in pg.inner_text(".hero-ribbon"), f"{view}: nach der Tagesrunde wieder die Lektion als Hauptknopf")
        pg.evaluate(SETUP, [[100, 83, 61, 70, 90, 76], False]); home(pg)
        ok(pg.locator("#view-lernen .hr-btn").count() == 0, f"{view}: ohne Rückstand der gewohnte Knopf")
        pg.click("#view-lernen .hr-go"); pg.wait_for_timeout(250)
        ok(pg.evaluate("() => { const S = window.__t.getS(); return S && S.kind === 'lesson' && S.lesson.id; }") == "l7", f"{view}: Knopf startet Lektion 7")
        pg.evaluate("() => window.__t.exitSession()"); pg.wait_for_timeout(100)
        ok(not errs, f"{view}: keine JS-Fehler (Pause) {errs[:3]}")
        ctx.close()
        # --- Hinweise in der Heute-Karte ---
        ctx, pg, errs = fresh(b, view)
        pg.evaluate(SETUP, [[100, 83, 61, 48, 90, 76], False]); home(pg)
        tip = pg.inner_text(".daycard .tip-row") if pg.locator(".daycard .tip-row").count() else ""
        ok("Lektion 4 nochmal" in tip and "48 %" in tip, f"{view}: schwache Lektion wird vorgeschlagen ({tip[:40]!r})")
        ok(pg.locator(".tip-row.dl-banner").count() == 0 and pg.locator(".dl-banner:not(.day-banner)").count() == pg.locator(".dl-banner[data-dlg], .dl-banner[data-act=test]").count(), f"{view}: Hinweis zählt nicht als Gesprächs-/Test-Zeile")
        pg.click(".daycard .tip-row"); pg.wait_for_timeout(250)
        ok(pg.evaluate("() => window.__t.getS() && window.__t.getS().lesson.id") == "l4", f"{view}: Tippen startet Lektion 4")
        pg.evaluate("() => { window.__t.exitSession(); const s = window.__t.state(); s.learn.done.l4.best = 80; }"); home(pg)
        tip = pg.inner_text(".daycard .tip-row") if pg.locator(".daycard .tip-row").count() else ""
        ok("Noch nicht ausprobiert: Zahlen-Training" in tip, f"{view}: danach die neu freie Übung ({tip[:40]!r})")
        pg.click(".daycard .tip-row"); pg.wait_for_timeout(250)
        ok(pg.evaluate("() => window.__t.getS() && window.__t.getS().kind") == "num" and pg.evaluate("() => window.__t.state().tips.num") == "x", f"{view}: Zahlen-Training startet und ist vermerkt")
        pg.evaluate("() => window.__t.exitSession()"); home(pg)
        tip = pg.inner_text(".daycard .tip-row") if pg.locator(".daycard .tip-row").count() else ""
        ok("Zahlen" not in tip, f"{view}: Zahlen-Hinweis verschwindet nach dem ersten Mal ({tip[:40]!r})")
        old = pg.evaluate("() => { const T = window.__t, s = T.state(); Object.keys(s.tips).forEach(k => { if(s.tips[k] !== 'x') s.tips[k] = T.addDays(T.today(), -8); }); return Object.keys(s.tips); }"); home(pg)
        ok(pg.locator(".daycard .tip-row").count() == 0 or pg.evaluate("() => Object.keys(window.__t.state().tips).length") > len(old), f"{view}: Hinweise verschwinden nach einer Woche ({old})")
        ok(not errs, f"{view}: keine JS-Fehler (Hinweise) {errs[:3]}")
        ctx.close()
    # --- Speichern: tips bleibt erhalten, Unsinn wird bereinigt ---
    ctx = b.new_context(); pg = ctx.new_page()
    pg.add_init_script("if(!sessionStorage.getItem('x')){ sessionStorage.setItem('x', 1); localStorage.setItem('zh-trainer-v1', JSON.stringify({v:3, tips:{num:'x', l4:'2026-11-01'}, words:{}, prefs:{tmode:'duel'}})); }")
    pg.goto(URL); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(200)
    t1 = pg.evaluate("() => window.__t.state().tips"); m1 = pg.evaluate("() => window.__t.state().prefs.tmode")
    ok(t1.get("num") == "x" and m1 == "duel", f"Lernstand: tips und Duell-Modus bleiben nach dem Laden ({t1}, {m1})")
    for bad in ["[1,2]", "'x'", "null", "{num:5, txt:true, l4:'gestern'}"]:
        pg.evaluate(f"() => {{ localStorage.setItem('zh-trainer-v1', JSON.stringify({{v:3, tips:{bad}}})); }}"); pg.reload(); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(150)
        ok(pg.evaluate("() => { const t = window.__t.state().tips; return !!t && typeof t === 'object' && !Array.isArray(t); }"), f"Lernstand: kaputtes tips ({bad}) wird zu leerem Objekt")
    pg.evaluate("() => { localStorage.setItem('zh-trainer-v1', JSON.stringify({v:3, num:{'47':{n:2, bad:0}}, learn:{done:{}, dlg:{}, lsn:{}, txt:{t01:{at:'2026-11-01', best:100, n:1}}}, words:{}})); }"); pg.reload(); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(150)
    t2 = pg.evaluate("() => window.__t.state().tips")
    ok(t2.get("num") == "x" and t2.get("txt") == "x" and "sent" not in t2, f"Lernstand ohne tips: schon genutzte Übungen gelten als ausprobiert ({t2})")
    ctx.close()
    # --- Pluszeichen beim Satzbauen ---
    ctx, pg, errs = fresh(b, "mobile")
    pg.set_viewport_size({"width": 320, "height": 640})
    pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(); T.LESSONS.slice(0, 24).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t, 1)}); }); }""")
    bad = 0; seen = 0
    for k in range(12):
        pg.evaluate("() => { window.__t.startSentences(); }"); pg.wait_for_timeout(120)
        for j in range(10):
            st = pg.evaluate("() => { const S = window.__t.getS(); return S && S.queue[0] && S.queue[0].type; }")
            if st == "build" and pg.locator("#session .ansslots").count():
                seen += 1
                bad += pg.evaluate("""() => { const sl = document.querySelector('#session .ansslots'); if(!sl) return 0; const kids = [...sl.children]; let b = 0;
                  kids.forEach((el, i) => { if(i === 0) return; const prev = kids[i-1].getBoundingClientRect(), r = el.getBoundingClientRect();
                    const plus = el.querySelector(':scope > .as-plus, :scope.as-plus'); if(r.top > prev.top + 4 && el.firstElementChild && el.firstElementChild.classList.contains('as-plus')) b++; });
                  return b + (kids.length && kids[kids.length-1].querySelector('.as-plus') ? 1 : 0); }""")
                break
            pg.evaluate("() => { const S = window.__t.getS(); if(S && S.queue.length > 1) S.queue.push(S.queue.shift()); window.__t.renderSession(); }")
        pg.evaluate("() => window.__t.exitSession()")
    ok(seen > 0 and bad == 0, f"320 px: keine Zeile beginnt mit »+«, kein »+« am Ende ({seen} Sätze geprüft, {bad} Fehler)")
    ok(not errs, f"keine JS-Fehler (Satzbauen) {errs[:3]}")
    ctx.close()
    b.close()
print("\n".join(res)); print(f"{sum(1 for r in res if r.startswith('OK'))} / {len(res)}")
