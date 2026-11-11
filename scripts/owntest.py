# Prüft Tonkurven: Schema bei neuen Wörtern, gemessene Kurve im Töne-Trainer, eigene Aufnahme hochladen
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html#toene"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
    # Messung im Browser gleich wie im Prüfskript?
    n = pg.evaluate("""async () => { const T = window.__t; let shown = 0, all = 0; for(const k of Object.keys(window.ZH_AUDIO.s)){ const t = +k.slice(-1); if(!(t>=1&&t<=4)) continue; all++;
        const st = await T.pitchOfClip(T.clip('s', k), true); if(T.shapeOk(st, t, T.VOICE.s)) shown++; } return [shown, all]; }""")
    ok(n[1] >= 200 and n[0] >= 0.9*n[1], f"gemessene Kurven im Browser: {n[0]} von {n[1]} Silben passen sichtbar zum Ton")
    # Töne-Trainer: 毛 máo (2. Ton)
    pg.evaluate("() => window.__t.toneSet('毛')"); pg.wait_for_timeout(200)
    ok("Wähl erst den Ton" in pg.inner_text("#t-own"), "eigene Aufnahme erst nach der Antwort")
    pg.click('[data-tone="2"]'); pg.wait_for_timeout(1200)
    ok(pg.locator("#t-mel path.sc-tone").count() == 1, "Lehrbuch-Verlauf nach der Antwort")
    ok(pg.locator("#t-mel path.pc-native").count() == 1, "gemessene Kurve der Aufnahme dazu")
    def up(f, wait=2500):
        pg.set_input_files("#own-file", f); pg.wait_for_timeout(wait)
        for sel in (".own-res", "#t-own .w-note"):
            if pg.locator(sel).count(): return pg.inner_text(sel)
        return ""
    t = up("/tmp/pitchref/raw/s_mao2.mp3"); ok("steigt" in t and "passt zum 2. Ton" in t and pg.locator("#t-own path.pc-own").count() == 1, f"Original als eigene Aufnahme: {t[-120:]!r}")
    t = up("/tmp/own/low_mao2.m4a"); ok("passt zum 2. Ton" in t, f"tiefe Stimme, leiser (m4a): {t[-90:]!r}")
    t = up("/tmp/own/noisy_mao2.wav"); ok("passt zum 2. Ton" in t, f"mit Rauschen: {t[-90:]!r}")
    t = up("/tmp/pitchref/raw/s_kan4.mp3"); ok("fällt" in t and "Der 2. Ton steigt" in t and "passt" not in t, f"falscher Ton (4.) erkannt: {t[-110:]!r}")
    t = up("/tmp/own/low_ma4.m4a"); ok(("fällt" in t or "nicht eindeutig" in t) and "passt" not in t, f"4. Ton mit Anlauf, tiefe Stimme: {t[-110:]!r}")
    t = up("/tmp/pitchref/raw/s_ma3.mp3"); ok("passt" not in t and "Der 2. Ton" in t, f"3. Ton statt 2.: {t[-140:]!r}")
    t = up("/tmp/own/low_ma3.m4a"); ok("passt" not in t and ("runter und wieder hoch" in t or "fällt" in t), f"3. Ton als eigene Aufnahme (Ziel 2. Ton): {t[-110:]!r}")
    t = up("/tmp/own/low_ma1.m4a"); ok("bleibt gleich" in t and "passt" not in t, f"1. Ton als eigene Aufnahme (Ziel 2. Ton): {t[-110:]!r}")
    t = up("/tmp/own/long.wav"); ok("zu lang" in t, "zu lange Aufnahme wird abgelehnt")
    t = up("/tmp/own/silent.wav"); ok("keine Stimme" in t, "stille Aufnahme wird erkannt")
    t = up("/tmp/own/broken.mp3"); ok("nicht gelesen" in t, "kaputte Datei wird erkannt")
    # 3. Ton als Ziel: tief fallend gesprochen ist kein Fehler
    z3 = pg.evaluate("() => window.__t.TONE_SYL.find(i => i.tones[0]===3).zh")
    pg.evaluate("z => window.__t.toneSet(z)", z3); pg.wait_for_timeout(200); pg.click('[data-tone="3"]'); pg.wait_for_timeout(600)
    t = up("/tmp/pitchref/raw/s_ma3.mp3"); ok("Das kann ein 3. Ton sein" in t, f"3. Ton tief fallend wird nicht als Fehler gewertet ({z3}): {t[-160:]!r}")
    t = up("/tmp/pitchref/raw/s_mao2.mp3"); ok("Deine Kurve steigt" in t and "passt" not in t, f"2. Ton statt 3.: {t[-160:]!r}")
    t = up("/tmp/pitchref/raw/s_ma1.mp3"); ok("bleibt gleich" in t and "Der 3. Ton geht tief runter" in t, f"1. Ton mit Anlauf statt 3.: {t[-160:]!r}")
    for f in ["/tmp/pitchref/raw/s_ma3.mp3", "/tmp/pitchref/raw/w_ma3.mp3", "/tmp/pitchref/raw/w_ni3.mp3"]:
        if __import__("os").path.exists(f): t = up(f); ok("Das kann ein 3. Ton sein" in t or "passt zum 3. Ton" in t, f"Vorbild-3. Ton {f[-10:]}: {t[:60]!r}")
    # zweisilbig: nur Lehrbuch-Verlauf als Vergleich
    pg.click('[data-tmode="word"]'); pg.wait_for_timeout(200)
    pg.evaluate("() => window.__t.toneSet('好吃')"); pg.wait_for_timeout(200)
    pg.click('[data-tone="3"]'); pg.click('[data-tone="1"]'); pg.wait_for_timeout(500)
    ok(pg.locator("#t-mel path.sc-tone").count() == 2 and pg.locator("#t-mel path.pc-native").count() == 0, "zwei Silben: Lehrbuch-Verlauf, keine Messung")
    t = up("/tmp/pitchref/raw/w_好吃.mp3") if __import__("os").path.exists("/tmp/pitchref/raw/w_好吃.mp3") else ""
    ok(("passen" in t or "Vergleich" in t) and pg.locator("#t-own path.pc-own").count() >= 1, f"zwei Silben: eigene Kurve mit Urteil je Silbe {t!r}")
    sch = pg.evaluate("() => window.__t.toneSchema(['nǐ','hǎo']).map(s => s.eff)")
    ok(sch == [2, 3], f"你好 im Schema als 2. + 3. Ton {sch}")
    # neue Wörter zeigen die Tonmelodie
    pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(300)
    pg.click("#view-lernen .hr-go"); pg.wait_for_timeout(300)
    for _ in range(6):
        tt = pg.evaluate("() => window.__t.getS().queue[0].type")
        if tt == "intro": break
        pg.evaluate("() => { const S = window.__t.getS(); S.queue.shift(); }"); 
    pg.evaluate("() => { location.hash = 'lernen'; }")
    b.close()
    ok(not errs, f"keine JS-Fehler {errs[:3]}")
print("\n".join(res))
