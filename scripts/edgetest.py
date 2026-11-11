# Randfälle: leerer Zustand, alter Speicherstand, alles geschafft, Tastatur bei offenen Fenstern, Spiel-Fragen
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import json
res = []
def ok(c, msg): res.append(("OK  " if c else "FEHLER ") + msg)
URL = "file://" + ROOT + "/test/index.html"
def fresh(b, w=390, h=844, state=None, hash=""):
    ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    if state is not None:
        pg.add_init_script("localStorage.setItem('zh-trainer-v1', " + json.dumps(json.dumps(state)) + ");")
    pg.goto(URL + hash); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
    return ctx, pg, errs
with sync_playwright() as p:
    b = p.chromium.launch()
    # a) leerer Zustand, alle Ansichten
    ctx, pg, errs = fresh(b)
    for v in ["lernen", "wiederholen", "spiel", "toene", "saetze", "einstellungen", "lernen"]:
        pg.evaluate(f"() => {{ location.hash = '{v}'; }}"); pg.wait_for_timeout(250)
        ok(pg.is_visible(f"#view-{v}"), f"leer: Ansicht {v} sichtbar")
    ok(pg.inner_text(".tile-rev b") == "Noch nichts zu wiederholen", "leer: Kachel Wiederholen")
    ok(not errs, f"leer: keine JS-Fehler {errs}")
    ctx.close()
    # b) alter Speicherstand ohne Spiel-Felder
    old = {"v": 3, "updatedAt": 1790000000000, "cards": {}, "tones": {"1": {"n": 3, "ok": 2}, "2": {"n": 0, "ok": 0}, "3": {"n": 0, "ok": 0}, "4": {"n": 0, "ok": 0}}, "conf": {},
           "days": {"2026-10-31": {"tones": 3, "toneOk": 2, "cards": 0, "neu": 0, "xp": 20, "lessons": 2, "reviews": 0}},
           "learn": {"done": {"l1": {"at": "2026-10-31", "best": 100}, "l2": {"at": "2026-10-31", "best": 90}}},
           "words": {"你": {"b": 1, "d": "2026-11-01"}, "好": {"b": 1, "d": "2026-11-01"}, "你好": {"b": 1, "d": "2026-11-01"}, "我": {"b": 1, "d": "2026-11-01"}, "是": {"b": 1, "d": "2026-11-01"},
                     "谢谢": {"b": 1, "d": "2026-11-01"}, "不": {"b": 1, "d": "2026-11-01"}, "再见": {"b": 1, "d": "2026-11-01"}, "吗": {"b": 1, "d": "2026-11-01"}, "很": {"b": 1, "d": "2026-11-01"}},
           "prefs": {"tmode": "syl", "dir": "say", "cat": "alle", "slow": False, "voice": "", "autoplay": "words", "pinyin": True, "toneColors": True, "fx": True, "theme": "auto", "hz": "normal", "goal": 20}}
    ctx, pg, errs = fresh(b, state=old, hash="#spiel")
    g = pg.evaluate("() => window.__t.state().game")
    ok(g == {"played": 0, "wins": {}, "best": {}}, f"alter Stand: Spielfeld ergänzt {g}")
    ok(not pg.is_disabled('[data-race="wang"]'), "alter Stand: Rennen startbar")
    pg.click('[data-race="wang"]'); pg.wait_for_timeout(3300)
    a = pg.evaluate("() => { const G = window.__t.getG(); const q = G.q; return q.type==='tone' ? window.__t.toneOf(q.w.py) : q.opts.indexOf(q.w); }")
    pg.click(f'[data-gopt="{a}"]'); pg.wait_for_timeout(300)
    pg.evaluate("() => { const G = window.__t.getG(); G.me = 100; G.crossed = true; G.crossT = 30; }"); pg.wait_for_timeout(1800)
    d = pg.evaluate("() => { const T = window.__t; return T.state().days[T.today()]; }")
    ok(d and d.get("games") == 1, f"alter Stand: Tag bekommt games {d}")
    streak = pg.evaluate("() => document.querySelector('#top-chips .stat-chip').textContent")
    ok(not errs, f"alter Stand: keine JS-Fehler {errs}")
    ctx.close()
    # c) alles geschafft
    ctx, pg, errs = fresh(b)
    pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today();
      T.LESSONS.forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:2, d:T.addDays(t, 3)}); }); location.hash = 'spiel'; }""")
    pg.wait_for_timeout(200); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(400)
    txt = pg.inner_text(".hero-ribbon")
    ok("HSK 1 komplett" in txt and "Zum Rennen" in txt, f"alles geschafft: Titel und Knopf ({txt[:60]!r})")
    ok(pg.evaluate("() => document.querySelectorAll('.mini-route i.on').length") == 9, "alles geschafft: Mini-Route von Teil 2 voll")
    ok(pg.evaluate("() => document.querySelectorAll('.stamp.got').length") == 9, "alles geschafft: 9 Stempel auf Seite 2")
    pg.click('[data-bkpart="1"]'); pg.wait_for_timeout(200)
    ok(pg.evaluate("() => document.querySelectorAll('.stamp.got').length") == 8, "alles geschafft: 8 Stempel auf Seite 1")
    ok(pg.locator(".dl-banner:not(.day-banner)").count() == 1, "alles geschafft: offenes Gespräch wird angeboten")
    ok(not errs, f"alles geschafft: keine JS-Fehler {errs}")
    # d) Tastatur: Wiederholen über Kachel starten, dann Leertaste
    pg.evaluate("() => { const T = window.__t, s = T.state(), t = T.today(); Object.keys(s.words).slice(0, 5).forEach(k => s.words[k].d = t); location.hash = 'wiederholen'; }")
    pg.wait_for_timeout(200); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(300)
    pg.click(".tile-rev"); pg.wait_for_timeout(300)
    pg.evaluate("() => { window.__S1 = window.__t.getS(); }")
    pg.keyboard.press(" "); pg.wait_for_timeout(200); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    same = pg.evaluate("() => window.__S1 === window.__t.getS()")
    ok(same, "Tastatur: Leertaste/Enter starten die Wiederholung nicht neu")
    foc = pg.evaluate("() => { const a = document.activeElement; return a ? (a.closest('#session') ? 'session' : a.tagName + '.' + a.className) : 'none'; }")
    ok(foc == "session" or foc.startswith("BODY"), f"Tastatur: Fokus nicht im Hintergrund ({foc})")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    # e) Spiel: Antreten, dann Leertaste im Countdown
    pg.evaluate("() => { location.hash = 'spiel'; }"); pg.wait_for_timeout(400)
    pg.click('[data-race="li"]'); pg.wait_for_timeout(500)
    pg.evaluate("() => { window.__G1 = window.__t.getG(); }")
    pg.keyboard.press(" "); pg.wait_for_timeout(150); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    ok(pg.evaluate("() => window.__G1 === window.__t.getG()"), "Tastatur: Leertaste/Enter starten das Rennen nicht neu")
    # f) Tonfarben aus gilt auch im Rennen
    pg.evaluate("() => { window.__t.getG(); }")
    ok(pg.evaluate("() => document.getElementById('game').classList.contains('tc')"), "Tonfarben an: Rennen hat Tonfarben")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.evaluate("() => { location.hash = 'einstellungen'; }"); pg.wait_for_timeout(300)
    pg.click('[data-switch="toneColors"]'); pg.wait_for_timeout(100)
    ok(not pg.evaluate("() => document.getElementById('game').classList.contains('tc')"), "Tonfarben aus: auch im Rennen aus")
    pg.click('[data-switch="toneColors"]')
    # g) Zurück-Taste im Rennen
    pg.evaluate("() => { location.hash = 'spiel'; }"); pg.wait_for_timeout(300)
    pg.click('[data-race="wang"]'); pg.wait_for_timeout(300)
    pg.evaluate("() => { location.hash = 'toene'; }"); pg.wait_for_timeout(200)
    ok(pg.evaluate("() => !!window.__t.getG()"), "Zurück/Hash-Wechsel im Rennen: Rennen bleibt offen")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    ok(pg.is_visible("#view-toene"), "nach dem Schließen passt die Ansicht zur Adresse")
    # h) Doppelklick auf eine Antwort zählt nur einmal
    pg.evaluate("() => { location.hash = 'spiel'; }"); pg.wait_for_timeout(300)
    pg.click('[data-race="wang"]'); pg.wait_for_timeout(3300)
    a = pg.evaluate("() => { const G = window.__t.getG(); const q = G.q; return q.type==='tone' ? window.__t.toneOf(q.w.py) : q.opts.indexOf(q.w); }")
    pg.dblclick(f'[data-gopt="{a}"]'); pg.wait_for_timeout(100)
    n = pg.evaluate("() => window.__t.getG().n")
    ok(n == 1, f"Doppelklick zählt einmal (n={n})")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    ok(not errs, f"Tastatur/Spiel: keine JS-Fehler {errs}")
    ctx.close()
    # i) Fragen im Spiel: viele Runden simulieren und jede Frage prüfen
    ctx, pg, errs = fresh(b)
    rep = pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(), out = {n:0, bad:[]};
      for(const upto of [2, 4, 8, 16, 24, 33]){
        s.words = {}; T.LESSONS.slice(0, upto).forEach(l => l.W.forEach(w => s.words[w.zh] = {b:1, d:t}));
        for(let r = 0; r < 60; r++){
          T.startGame('wang'); const G = T.getG(); G.phase = 'race';
          for(let k = 0; k < 25; k++){
            G.answered = false; G.q = null; G.order = G.order || [];
            // nächste Frage erzeugen wie im Spiel
            G.phase = 'race'; window.__t_next && window.__t_next();
            const q = G.q; if(!q) { out.bad.push('keine Frage'); break; }
            out.n++;
            if(q.type !== 'tone'){
              if(q.opts.length < 2) out.bad.push('zu wenig Optionen ' + q.w.zh);
              if(q.opts.indexOf(q.w) < 0) out.bad.push('richtige fehlt ' + q.w.zh);
              const des = q.opts.map(o => o.de), zhs = q.opts.map(o => o.zh);
              if(new Set(des).size !== des.length) out.bad.push('gleiche Bedeutung ' + des.join('/'));
              if(new Set(zhs).size !== zhs.length) out.bad.push('gleiches Zeichen ' + zhs.join('/'));
              if(q.type === 'hear'){ const keys = q.opts.map(o => o.py.normalize('NFD').replace(/[\\u0300-\\u036f_]/g, '') + T.toneOf(o.py)); if(keys.filter(k2 => k2 === keys[q.opts.indexOf(q.w)]).length > 1) out.bad.push('gleicher Klang ' + zhs.join('/')); }
            } else if(!(q.w.syls.length === 1 && T.toneOf(q.w.py) > 0)) out.bad.push('Tonfrage falsch ' + q.w.zh);
            if(q.type === 'hear' && !T.clipsFor(q.w)) out.bad.push('Hörfrage ohne eigene Aufnahme ' + q.w.zh);
          }
          T.closeGame();
        }
      }
      return out; }""")
    ok(rep["n"] > 0 and not rep["bad"], f"Spielfragen geprüft: {rep['n']} Fragen, Probleme: {sorted(set(rep['bad']))[:8]}")
    noaudio = pg.evaluate("() => window.__t.WORDS.filter(w => !window.__t.clipsFor(w)).map(w => w.zh + (w.ex ? '+Satz' : ''))")
    ok(noaudio == ['了+Satz', '哪儿'], f"nur 了 (mit Beispielsatz) und 哪儿 (Gerätestimme, keine Er-Aufnahme) ohne eigene Aufnahme {noaudio}")
    ok(not errs, f"Spielfragen: keine JS-Fehler {errs[:3]}")
    ctx.close()
    b.close()
print("\n".join(res))
