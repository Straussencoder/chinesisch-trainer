import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, json; sys.path.insert(0, ROOT + "/scripts"); import fontroute
STATES = {
 "leer": "{}",
 "kaputt": "nicht json",
 "alt_v1": json.dumps({"v":1, "cards":{"k1":{"b":2,"d":"2026-10-01"}}, "tones":{"1":{"n":3,"ok":1}}, "prefs":{"tmode":"syl"}}),
 "halb": json.dumps({"v":3, "learn":{"done":{"l1":{"at":"2026-11-01","best":50}, "l2":"kaputt"}}, "words":{"你":{"b":"x"}, "好":None, "我":{"b":1,"d":"2026-13-45"}}, "days":{"heute":5, "2026-11-01":{"xp":"3"}}, "pats":[], "err":{"你":{"n":"a"}}, "game":None, "tests":"nein", "prefs":{"theme":"lila","goal":"zwanzig","hz":3}}),
 "voll": json.dumps({"v":3, "learn":{"done":{("l%d"%i):{"at":"2026-11-01","best":100,"gold":"2026-11-01"} for i in range(1,34)}, "dlg":{("u%d"%i):{"at":"2026-11-01","best":100} for i in range(1,18)}}, "words":{}, "prefs":{}}),
}
with sync_playwright() as p:
    b = p.chromium.launch(args=["--deny-permission-prompts"])
    for name, raw in STATES.items():
        ctx = b.new_context(viewport={"width":390,"height":844}); pg = ctx.new_page(); fontroute.setup(pg)
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO")
        pg.evaluate("(raw) => localStorage.setItem('zh-trainer-v1', raw)", raw); pg.reload(); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(400)
        for v in ["lernen","wiederholen","spiel","toene","saetze","einstellungen"]:
            pg.evaluate(f"() => {{ location.hash='{v}'; }}"); pg.wait_for_timeout(250)
        # Übung starten, falls möglich
        pg.evaluate("() => { const T=window.__t; try{ T.startReview(true); }catch(e){ window.__err=String(e); } }"); pg.wait_for_timeout(300)
        pg.evaluate("() => { const T=window.__t; if(T.getS()) T.exitSession(); try{ T.startDayRound(); }catch(e){ window.__err2=String(e); } }"); pg.wait_for_timeout(300)
        pg.evaluate("() => { const T=window.__t; if(T.getS()) T.exitSession(); try{ T.startLesson(T.LESSONS[0].id); }catch(e){ window.__err3=String(e); } }"); pg.wait_for_timeout(300)
        x = pg.evaluate("() => [window.__err, window.__err2, window.__err3].filter(Boolean)")
        print(name, "JS:", errs[:3], "Ausnahmen:", x)
        ctx.close()
    # Mikrofon verweigert
    ctx = b.new_context(viewport={"width":390,"height":844}); pg = ctx.new_page(); fontroute.setup(pg)
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    pg.evaluate("() => { location.hash='toene'; }"); pg.wait_for_timeout(400)
    pg.click(".tbtn[data-tone='1']"); pg.wait_for_timeout(200); pg.click("#t-own [data-act='rec']"); pg.wait_for_timeout(1500)
    assert not errs
    print("errs", errs)
    print("Mikro verweigert:", pg.evaluate("() => { const o=window.__t.getOwn(); return o && (o.error || (o.rec ? 'nimmt auf' : 'ok')); }"), "JS:", errs)
    b.close()
