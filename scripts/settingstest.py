import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
errs, res = [], []
def check(name, cond): res.append(("OK  " if cond else "FEHLER ") + name)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 390, "height": 844}); pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html#einstellungen"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(200)
    S = lambda: pg.evaluate("() => window.__t.state().prefs")
    # Schalter
    for pref in ["pinyin", "toneColors", "slow", "fx"]:
        before = S()[pref]; pg.click(f'[data-switch="{pref}"]'); after = S()[pref]
        aria = pg.get_attribute(f'[data-switch="{pref}"]', "aria-checked")
        check(f"Schalter {pref}: {before} -> {after}, Anzeige {aria}", after == (not before) and aria == str(after).lower())
    check("Tonfarben aus entfernt Klasse", not pg.evaluate("() => document.getElementById('app').classList.contains('tc')"))
    pg.click('[data-switch="toneColors"]'); check("Tonfarben wieder an", pg.evaluate("() => document.getElementById('app').classList.contains('tc')"))
    # Pinyin aus -> in Lektion kein Pinyin bei Antworten
    pg.evaluate("location.hash='lernen'"); pg.wait_for_timeout(100)
    pg.click('button.btn[data-lesson="l1"]')
    for _ in range(10):
        t = pg.evaluate("() => window.__t.getS().queue[0].type")
        if t == "char": break
        if t == "intro": pg.click("#s-next"); continue
        st = pg.evaluate("() => { const S = window.__t.getS(); const ex = S.queue[0]; return ex.opts ? ex.opts.indexOf(ex.w) : -1; }")
        pg.click(f'[data-opt="{st}"]'); pg.click("#s-next")
    check("Pinyin aus: keine Pinyin-Zeile in Zeichen-Übung", pg.locator("#session .opy").count() == 0)
    pg.click('[data-act="close"]'); pg.click('[data-act="close"]')
    check("Lektion beenden schließt Übung", pg.locator("#session").is_hidden())
    pg.evaluate("location.hash='einstellungen'"); pg.wait_for_timeout(100)
    pg.click('[data-switch="pinyin"]')
    # Segmente
    for pref, val, test in [("hz","gross","() => document.documentElement.getAttribute('data-hz')==='gross'"),
                            ("theme","dark","() => document.documentElement.getAttribute('data-app-theme')==='dark' && getComputedStyle(document.body).backgroundColor === 'rgb(33, 27, 21)'"),
                            ("theme","light","() => document.documentElement.getAttribute('data-app-theme')==='light'"),
                            ("theme","auto","() => !document.documentElement.hasAttribute('data-app-theme')"),
                            ("autoplay","sentence","() => window.__t.state().prefs.autoplay==='sentence'"),
                            ("autoplay","words","() => window.__t.state().prefs.autoplay==='words'"),
                            ("goal","30","() => window.__t.state().prefs.goal===30 && document.getElementById('top-chips').textContent.includes('/30')"),
                            ("hz","normal","() => !document.documentElement.hasAttribute('data-hz')")]:
        pg.click(f'[data-pref="{pref}"][data-val="{val}"]'); pg.wait_for_timeout(50)
        pressed = pg.get_attribute(f'[data-pref="{pref}"][data-val="{val}"]', "aria-pressed")
        check(f"Auswahl {pref}={val}", pg.evaluate(test) and pressed == "true")
    check("Stimmen-Auswahl vorhanden", pg.locator("#voice-select").count() == 1)
    # Bleibt nach Neuladen erhalten
    pg.reload(); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(200)
    pr = S(); check(f"Nach Neuladen gespeichert (Ziel {pr['goal']}, Pinyin {pr['pinyin']})", pr["goal"] == 30 and pr["pinyin"] is True)
    # Zurücksetzen in zwei Schritten
    lessons_before = pg.evaluate("() => Object.keys(window.__t.state().learn.done).length")
    pg.click('[data-act="reset"]'); check("Zurücksetzen fragt nach", "Wirklich" in pg.inner_text('[data-act="reset"]'))
    pg.click('[data-act="reset"]')
    st = pg.evaluate("() => window.__t.state()")
    check(f"Zurückgesetzt (vorher {lessons_before} Lektionen), Einstellungen behalten", len(st["learn"]["done"]) == 0 and st["prefs"]["goal"] == 30)
    pg.click('[data-pref="goal"][data-val="20"]')
    b.close()
print("\n".join(res)); print("JS-Fehler:", errs or "keine")
