import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, time; sys.path.insert(0, ROOT + "/scripts"); import fontroute
# Prüft den echten Bau (Teil 1 sofort, Rest nach Bedarf). Der Haken fehlt dort, also über das DOM und window.
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":390,"height":844}); fontroute.setup(pg)
    reqs=[]; pg.on("request", lambda r: reqs.append(r.url.split("/")[-1]) if "audio-" in r.url else None)
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/zh-app/index.html"); pg.wait_for_function("!!window.ZH_AUDIO_PARTS[1]"); pg.wait_for_timeout(800)
    print("frisch, lernen:", sorted(set(reqs)), pg.evaluate("() => Object.keys(window.ZH_AUDIO_PARTS)"))
    assert sorted(set(reqs))==["audio-1.js"], reqs
    pg.evaluate("() => { location.hash='toene'; }"); pg.wait_for_timeout(1500)
    print("toene:", sorted(set(reqs)), pg.evaluate("() => Object.keys(window.ZH_AUDIO_PARTS)"))
    assert pg.evaluate("() => [1,2,3,4].every(n => window.ZH_AUDIO_PARTS[n])")
    # Zweiter Lauf: 10 Lektionen fertig -> Teile 1 und 2 beim Start, Lektion 25 wartet auf Teil 3
    pg2 = b.new_page(viewport={"width":390,"height":844}); fontroute.setup(pg2)
    reqs2=[]; pg2.on("request", lambda r: reqs2.append(r.url.split("/")[-1]) if "audio-" in r.url else None)
    pg2.goto("file://" + ROOT + "/zh-app/index.html"); pg2.wait_for_function("!!window.ZH_AUDIO_PARTS[1]")
    pg2.evaluate("""() => { var d = new Date().toISOString().slice(0,10), done = {}; for(var i=1;i<=10;i++) done['l'+i] = {at:d, best:90}; localStorage.setItem('zh-trainer-v1', JSON.stringify({v:3, updatedAt:Date.now(), learn:{done:done, dlg:{}}, words:{}, prefs:{fx:false}})); }""")
    reqs2.clear(); pg2.reload(); pg2.wait_for_function("!!window.ZH_AUDIO_PARTS[1]"); pg2.wait_for_timeout(1200)
    print("10 fertig, lernen:", sorted(set(reqs2)), pg2.evaluate("() => ({parts:Object.keys(window.ZH_AUDIO_PARTS), txt: document.querySelector('.hr-go') && document.querySelector('.hr-go').textContent, ls:(localStorage.getItem('zh-trainer-v1')||'').slice(0,60)})"))
    assert "audio-2.js" in reqs2 and "audio-3.js" not in reqs2 and "audio-4.js" not in reqs2
    # Lektion 25 starten (Teil 3): Hinweis, dann Start. Der Knopf ist gesperrt, also über den Klick-Handler mit einem künstlichen Knopf
    started = pg2.evaluate("""() => new Promise(ok => { var t0 = Date.now(); var btn = document.createElement('button'); btn.setAttribute('data-lesson', 'l25'); document.querySelector('#app').appendChild(btn); btn.click(); var iv = setInterval(function(){ var s = document.querySelector('#session'); if(s && !s.hidden && s.innerHTML){ clearInterval(iv); ok({ms:Date.now()-t0, toast:(document.querySelector('#toast')||{}).textContent, parts:Object.keys(window.ZH_AUDIO_PARTS)}); } if(Date.now()-t0 > 5000){ clearInterval(iv); ok('timeout'); } }, 50); })""")
    print("Lektion 25:", started)
    assert isinstance(started, dict) and "3" in started["parts"] and "geladen" in (started["toast"] or "")
    print("errs", errs)
    b.close()
