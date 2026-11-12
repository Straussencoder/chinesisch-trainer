# Prüft "Ohne Ton" (keine Höraufgaben, nichts spielt ab, Umschalten mitten in der Übung, Ablauf, Spiel, Töne)
# und goldene Lektionen (nur fehlerfreie Wiederholung, Etappe und Stempel gold, Speichern).
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
src = open(ROOT + "/scripts/fulltest.py").read()
STEP = src[src.index('STEP = """')+10:src.index('"""', src.index('STEP = """')+10)]
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
COUNT = """
window.__snd = {play:0, tts:0};
const op = HTMLMediaElement.prototype.play; HTMLMediaElement.prototype.play = function(){ window.__snd.play++; return op.call(this).catch(()=>{}); };
if(window.speechSynthesis){ const sp = window.speechSynthesis.speak.bind(window.speechSynthesis); window.speechSynthesis.speak = function(u){ window.__snd.tts++; try{ sp(u); }catch(e){} }; }
"""
def play_lesson(pg, wrong_at=None):
    n = 0; types = []
    for _ in range(120):
        st = pg.evaluate(STEP)
        if st.get("finished") or st.get("none"): break
        t = st["type"]; types.append(t)
        if t in ("intro", "rule"): pg.click("#s-next"); continue
        if t == "draw": pg.click('[data-act="drawskip"]'); pg.wait_for_timeout(40); continue
        n += 1; wrong = (wrong_at == n)
        if t in ("mean","hear","char","sentmean","gap","judge"): pg.click(f'[data-opt="{(st["right"]+1)%st.get("nopt",3) if wrong else st["right"]}"]')
        elif t == "write": pg.fill("#w-in", "xx" if wrong else st["typed"]); pg.keyboard.press("Enter")
        elif t == "tone": pg.click(f'[data-stone="{(st["tone"]%4)+1 if wrong else st["tone"]}"]')
        elif t == "pairs":
            st = pg.evaluate(STEP)
            for li, ri in enumerate(st["pairs"]): pg.click(f'[data-pl="{li}"]'); pg.click(f'[data-pr="{ri}"]')
        elif t == "build":
            for i in (list(reversed(st["order"])) if wrong else st["order"]): pg.click(f'[data-bank="{i}"]')
            pg.click("#s-check"); pg.evaluate("() => { const S = window.__t.getS(); if(S && !S.answered && S.queue[0] && S.queue[0].tried) document.querySelector('#s-check').click(); }")
        pg.wait_for_timeout(30); pg.click("#s-next"); pg.wait_for_timeout(30)
    return types
MARK = """(n) => { const T = window.__t, s = T.state(), t = T.today(); T.LESSONS.slice(0, n).forEach(l => { s.learn.done[l.id] = {at:t, best:90}; l.W.forEach(w => s.words[w.zh] = {b:1, d:t}); }); location.hash='saetze'; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for view, (w, h) in (("mobile", (390, 844)), ("desktop", (1366, 900))):
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); fontroute.setup(pg); pg.add_init_script(COUNT)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(500)
        pg.evaluate(MARK, 10); pg.wait_for_timeout(150); pg.evaluate("() => { location.hash='lernen'; }"); pg.wait_for_timeout(300)
        # --- Ohne Ton von Anfang an ---
        pg.evaluate("() => window.__t.setQuiet(60)")
        nh = pg.evaluate("() => window.__t.LESSONS.reduce((a, l) => a + window.__t.buildLesson(l).filter(e => e.type==='hear').length, 0)")
        ok(nh == 0, f"{view}: ohne Ton keine Höraufgabe in allen 33 Lektionen ({nh})")
        ok(pg.locator("#top-chips .quiet-chip").count() == 1 or pg.locator(".side-quiet").count() == 1, f"{view}: Anzeige »Ohne Ton« sichtbar")
        pg.evaluate("() => { window.__snd.play = 0; window.__snd.tts = 0; window.__t.startLesson('l11'); }"); pg.wait_for_timeout(200)
        ok(pg.locator(".s-snd.off").count() == 1, f"{view}: Lautsprecher in der Übung zeigt »aus«")
        types = play_lesson(pg)
        snd = pg.evaluate("() => window.__snd")
        ok("hear" not in types and snd["play"] == 0 and snd["tts"] == 0, f"{view}: ganze Lektion ohne Ton: keine Höraufgabe, nichts abgespielt {snd}")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(200)
        # Wiederholen, Wochen-Test, Spiel
        pg.evaluate("() => { window.__t.startReview(true); }"); pg.wait_for_timeout(150)
        ok(pg.evaluate("() => window.__t.getS().queue.every(e => e.type !== 'hear')"), f"{view}: Freies Üben ohne Höraufgabe")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
        pg.evaluate("() => window.__t.startTest()"); pg.wait_for_timeout(150)
        ok(pg.evaluate("() => window.__t.getS().queue.length === 15 && window.__t.getS().queue.every(e => e.type !== 'hear')"), f"{view}: Wochen-Test ohne Höraufgabe, weiter 15 Fragen")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
        gq = pg.evaluate("""() => { const T = window.__t, out = []; T.startGame('wang'); const G = T.getG(); G.phase = 'race';
          for(let k = 0; k < 200; k++){ G.answered = false; G.phase = 'race'; window.__t_next(); out.push(G.q.type); } T.closeGame(); return out; }""")
        ok("hear" not in gq and "tone" in gq, f"{view}: Rennen ohne Hörfragen (200 Fragen), Tonfragen als Lesefrage bleiben")
        pg.evaluate("() => { location.hash='toene'; }"); pg.wait_for_timeout(300)
        ok(pg.locator("#t-zis .q").count() == 0 and pg.is_visible(".t-quiet"), f"{view}: Töne-Trainer zeigt ohne Ton Zeichen und Hinweis")
        pg.evaluate("() => { location.hash='einstellungen'; }"); pg.wait_for_timeout(300)
        ok(pg.locator('[data-quiet="off"]').count() == 1, f"{view}: Schalter in den Einstellungen")
        pg.click('[data-quiet="off"]'); pg.wait_for_timeout(200)
        ok(pg.evaluate("() => !window.__t.quiet()") and pg.locator(".quiet-chip, .side-quiet").count() == 0, f"{view}: »Aus« schaltet den Ton wieder ein, Anzeige weg")
        # --- mitten in der Lektion: »Kann gerade nicht hören« ---
        pg.evaluate("""() => { const T = window.__t; T.startLesson('l12'); const S = T.getS(); const i = S.queue.findIndex(e => e.type==='hear');
          if(i > 0){ const e = S.queue.splice(i, 1)[0]; S.queue.unshift(e); } T.renderSession(); }"""); pg.wait_for_timeout(200)
        ok(pg.evaluate("() => window.__t.getS().queue[0].type") == "hear", f"{view}: Höraufgabe steht vorne")
        pg.click('#session .nohear'); pg.wait_for_timeout(150)
        ok(pg.is_visible(".quiet-ask"), f"{view}: »Kann gerade nicht hören« fragt nach der Dauer")
        if view == "mobile": pg.screenshot(path=ROOT + "/shots/r2/quiet_ask.png")
        pg.click('#session [data-quiet="15"]'); pg.wait_for_timeout(200)
        qs = pg.evaluate("() => { const S = window.__t.getS(); return {t:S.queue[0].type, sub:!!S.queue[0].quietSub, hear:S.queue.filter(e => e.type==='hear').length}; }")
        ok(qs["t"] == "char" and qs["sub"] and qs["hear"] == 0, f"{view}: Aufgabe sofort ersetzt, keine Höraufgabe mehr in der Lektion {qs}")
        if view == "mobile": pg.screenshot(path=ROOT + "/shots/r2/quiet_sub.png")
        left = pg.evaluate("() => window.__t.quiet()")
        pg.click('#session .s-snd'); pg.wait_for_timeout(150)
        ok(left and pg.evaluate("() => !window.__t.quiet()"), f"{view}: Lautsprecher oben schaltet den Ton wieder ein")
        pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
        ok(not errs, f"{view}: keine JS-Fehler (Ohne Ton) {errs[:3]}")
        # --- Gold ---
        pg.evaluate("() => window.__t.startLesson('l1')"); pg.wait_for_timeout(150); play_lesson(pg)
        g1 = pg.evaluate("() => { const S = window.__t.getS(); return {gn:S.goldNew, gold:window.__t.state().learn.done.l1.gold}; }")
        ok(g1["gn"] and g1["gold"] and "gemeistert" in pg.inner_text(".finish"), f"{view}: fehlerfreie Wiederholung macht Lektion 1 gold {g1}")
        if view == "mobile": pg.screenshot(path=ROOT + "/shots/r2/gold_fin.png")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(200)
        pg.evaluate("() => window.__t.startLesson('l2')"); pg.wait_for_timeout(150); play_lesson(pg, wrong_at=3)
        g2 = pg.evaluate("() => { const S = window.__t.getS(); return {gn:S.goldNew, gt:S.goldTry, m:S.mistakes, gold:!!window.__t.state().learn.done.l2.gold}; }")
        ok(not g2["gn"] and g2["gt"] and not g2["gold"] and "Für Gold" in pg.inner_text(".finish"), f"{view}: mit einem Fehler kein Gold, Hinweis da {g2}")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(150)
        pg.evaluate("() => window.__t.setQuiet(60)")
        pg.evaluate("() => window.__t.startLesson('l2')"); pg.wait_for_timeout(150); play_lesson(pg)
        g3 = pg.evaluate("() => { const S = window.__t.getS(); return {gn:S.goldNew, ug:S.unitGoldNew}; }")
        ok(g3["gn"] and g3["ug"] and "Stempel" in pg.inner_text(".finish"), f"{view}: Gold auch ohne Ton möglich, Etappe 1 komplett gold {g3}")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(250)
        pg.evaluate("() => window.__t.setQuiet(null)"); pg.wait_for_timeout(200)
        pg.evaluate("() => { location.hash='saetze'; }"); pg.wait_for_timeout(150); pg.evaluate("() => { location.hash='lernen'; }"); pg.wait_for_timeout(400)
        ok(pg.locator('.node.gold[data-node="l1"]').count() == 1 and pg.locator('.node.gold[data-node="l2"]').count() == 1, f"{view}: Kreise im Lernpfad gold")
        ok(pg.locator(".st-done.gold").count() == 1 and pg.locator(".stamp.got.gold").count() == 1, f"{view}: Etappen-Siegel und Stempel gold")
        ok("2 gold" in pg.inner_text(".journey-head"), f"{view}: Zähler »2 gold« im Lernpfad")
        if view == "mobile":
            pg.evaluate("() => document.querySelector('[data-node=\"l2\"]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300); pg.screenshot(path=ROOT + "/shots/r2/gold_trail.png")
        # erste Runde fehlerfrei: noch kein Gold
        pg.evaluate("() => window.__t.startLesson('l11')"); pg.wait_for_timeout(100)
        pg.evaluate("() => { const s = window.__t.state(); delete s.learn.done.l11; }")
        play_lesson(pg)
        g4 = pg.evaluate("() => ({gn:window.__t.getS().goldNew, gold:!!window.__t.state().learn.done.l11.gold})")
        ok(not g4["gn"] and not g4["gold"] and "später nochmal" in pg.inner_text(".finish"), f"{view}: beim ersten Mal fehlerfrei noch kein Gold, aber Hinweis {g4}")
        pg.click('[data-act="exit"]'); pg.wait_for_timeout(200)
        # Speichern: neu laden
        pg.reload(); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(400)
        ok(pg.evaluate("() => window.__t.isGold(window.__t.LESSONS[0]) && window.__t.isGold(window.__t.LESSONS[1])"), f"{view}: Gold bleibt nach Neuladen")
        ok(not errs, f"{view}: keine JS-Fehler (Gold) {errs[:3]}")
        ctx.close()
    # Ablauf der Zeit und Speicherort
    ctx = b.new_context(); pg = ctx.new_page()
    pg.add_init_script("if(!sessionStorage.getItem('x')){ sessionStorage.setItem('x', 1); localStorage.setItem('zh-trainer-quiet', String(Date.now() + 6000)); }")
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(200)
    a = pg.evaluate("() => window.__t.quiet()"); pg.wait_for_function("() => !window.__t.quiet()", timeout=15000)
    ok(a and pg.evaluate("() => !window.__t.quiet()"), "Ohne Ton endet von selbst nach Ablauf der Zeit")
    pg.evaluate("() => window.__t.setQuiet(0)")
    ok(pg.evaluate("() => localStorage.getItem('zh-trainer-quiet') === '-1' && !('quiet' in window.__t.state().prefs)"), "»Dauerhaft« gilt nur auf diesem Gerät, nicht im geteilten Speicherstand")
    ctx.close(); b.close()
print("\n".join(res))
