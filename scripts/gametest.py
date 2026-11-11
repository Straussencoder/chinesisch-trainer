# Prüft die Spiellogik: Abgleich mit der Wiederholung, Punkte, Siege, Abbruch, Sperre unter 4 Wörtern.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import json
res = []
def ok(c, msg): res.append(("OK  " if c else "FEHLER ") + msg)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html#spiel"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
    # Sperre ohne Wörter
    dis = pg.evaluate("() => [...document.querySelectorAll('[data-race]')].map(b => b.disabled)")
    ok(dis == [True, True, True], f"ohne Wörter sind alle Gegner gesperrt {dis}")
    pg.evaluate("() => window.__t.startGame('wang')")
    ok(pg.evaluate("() => window.__t.getG()") is None, "Start ohne Wörter wird verhindert")
    # Wörter anlegen: A,B fällig, C,D nicht fällig
    setup = pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(), W = T.LESSONS[0].W.concat(T.LESSONS[1].W);
      W.forEach(w => s.words[w.zh] = {b:3, d:T.addDays(t, 5)});
      const A = W[0].zh, B = W[1].zh, C = W[2].zh, D = W[3].zh;
      s.words[A] = {b:2, d:t}; s.words[B] = {b:4, d:T.addDays(t, -2)};
      location.hash = 'lernen'; return {A, B, C, D, t, n: W.length}; }""")
    pg.wait_for_timeout(200); pg.evaluate("() => { location.hash = 'spiel'; }"); pg.wait_for_timeout(500)
    dis = pg.evaluate("() => [...document.querySelectorAll('[data-race]')].map(b => b.disabled)")
    ok(dis == [False, False, False], "mit Wörtern sind die Gegner frei")
    pg.click('[data-race="wang"]'); pg.wait_for_timeout(3300)
    g = pg.evaluate("() => { const G = window.__t.getG(); return {phase:G.phase, q:G.q && G.q.w.zh, type:G.q && G.q.type, nopts:G.q && G.q.opts ? G.q.opts.length : 4}; }")
    ok(g["phase"] == "race", f"Countdown vorbei, Rennen läuft ({g['phase']})")
    ok(g["q"] in (setup["A"], setup["B"]), f"fällige Wörter kommen zuerst ({g['q']})")
    # Ergebnisse gezielt setzen und Rennen beenden
    xp0 = pg.evaluate("() => { const T = window.__t; return (T.state().days[T.today()]||{}).xp || 0; }")
    out = pg.evaluate(f"""() => {{ const T = window.__t, G = T.getG(), s = T.state();
      G.results = {{}}; G.results['{setup["A"]}'] = {{ok:1, bad:0}}; G.results['{setup["B"]}'] = {{ok:1, bad:1}};
      G.results['{setup["C"]}'] = {{ok:2, bad:0}}; G.results['{setup["D"]}'] = {{ok:0, bad:1}};
      G.ok = 4; G.n = 6; G.raceT = 42.3; G.me = 100; G.meShown = 100; G.crossed = true; G.crossT = 41.7;
      T.gameFinish(true); const d = s.days[T.today()];
      return {{A:s.words['{setup["A"]}'], B:s.words['{setup["B"]}'], C:s.words['{setup["C"]}'], D:s.words['{setup["D"]}'], game:s.game, games:d.games, xp:d.xp, gxp:G.xp, time:G.time, phase:G.phase}}; }}""")
    t = setup["t"]
    ad = lambda n: pg.evaluate(f"() => window.__t.addDays('{t}', {n})")
    ok(out["A"] == {"b": 3, "d": ad(8), "iv": 8, "e": 2.5}, f"fällig + richtig: 3 Tage × 2,5 = 8 Tage {out['A']}")
    ok(out["B"] == {"b": 1, "d": ad(1), "iv": 1, "e": 2.3}, f"fällig + Fehler, danach richtig: morgen wieder, Faktor 2,3 {out['B']}")
    ok(out["C"]["d"] == ad(5) and out["C"]["b"] == 3, f"nicht fällig + richtig: unverändert {out['C']}")
    ok(out["D"] == {"b": 2, "d": t, "iv": 3, "e": 2.4}, f"nicht fällig + nur falsch: Abstand kleiner, heute fällig {out['D']}")
    ok(out["gxp"] == 4 + 3 and out["xp"] == xp0 + 7, f"Punkte: 4 richtig + 3 Siegbonus = {out['gxp']}, Tag {xp0} -> {out['xp']}")
    ok(out["games"] == 1 and out["game"]["played"] == 1 and out["game"]["wins"].get("wang") == 1, f"Rennen gezählt {out['game']}")
    ok(out["game"]["best"].get("wang") == 41.7 and out["time"] == 41.7, f"Bestzeit = Zeit beim Zieldurchlauf {out['game']['best']}")
    pg.wait_for_timeout(500)
    ok(pg.is_visible("#race-again") and "Gewonnen" in pg.inner_text("#race-q"), "Ergebnis-Seite mit Revanche")
    stored = pg.evaluate("() => JSON.parse(localStorage.getItem('zh-trainer-v1')).game")
    ok(stored["played"] == 1, f"Spielstand lokal gespeichert {stored}")
    # Fällig-Zahl im Menü passt
    pg.click('[data-gact="close"]'); pg.wait_for_timeout(300)
    badge = pg.evaluate("() => { const b = document.querySelector('#tab-nav .badge'); return b ? +b.textContent : 0; }")
    due = pg.evaluate("() => window.__t.dueWords().length")
    ok(badge == due and due >= 1, f"Abzeichen zeigt {badge} fällige Wörter ({due})")
    ok(pg.evaluate("() => document.getElementById('game').hidden && document.body.style.overflow===''"), "Spiel geschlossen, Seite scrollt wieder")
    # Abbruch mitten im Rennen: keine Änderung an Wiederholungen
    before = pg.evaluate("() => JSON.stringify(window.__t.state().words)")
    pg.click('[data-race="li"]'); pg.wait_for_timeout(3300)
    a = pg.evaluate("() => { const G = window.__t.getG(); const q = G.q; return q.type==='tone' ? window.__t.toneOf(q.w.py) : q.opts.indexOf(q.w); }")
    pg.click(f'[data-gopt="{a}"]'); pg.wait_for_timeout(600)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    ok(pg.evaluate("() => !!window.__t.getG()"), "Esc fragt erst nach")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    ok(pg.evaluate("() => !window.__t.getG()"), "zweites Esc beendet")
    after = pg.evaluate("() => JSON.stringify(window.__t.state().words)")
    ok(before == after, "Abbruch ändert keine Wiederholungstermine")
    # Echte Runde gegen Meister Long mit Tastatur, alle richtig
    pg.click('[data-race="long"]'); pg.wait_for_timeout(3300)
    n = 0
    for _ in range(80):
        st = pg.evaluate("() => { const G = window.__t.getG(); if(!G) return null; if(G.phase!=='race') return {done:G.phase}; if(G.answered || !G.q) return {wait:1}; const q = G.q; return {k: q.type==='tone' ? window.__t.toneOf(q.w.py) : q.opts.indexOf(q.w) + 1, nopts: q.opts ? q.opts.length : 4}; }")
        if st is None or "done" in st: break
        if "wait" in st: pg.wait_for_timeout(100); continue
        if st["nopts"] < 2: res.append("FEHLER zu wenige Antworten")
        pg.keyboard.press(str(st["k"])); n += 1; pg.wait_for_timeout(500)
    pg.wait_for_timeout(1500)
    fin = pg.evaluate("() => { const G = window.__t.getG(); return G && {phase:G.phase, won:G.won, ok:G.ok, n:G.n, time:G.time}; }")
    ok(fin and fin["phase"] == "done" and fin["won"] and fin["ok"] == fin["n"], f"Sieg gegen Meister Long mit {n} Antworten per Tastatur {fin}")
    b.close()
print("\n".join(res)); print("JS-Fehler:", errs or "keine")
