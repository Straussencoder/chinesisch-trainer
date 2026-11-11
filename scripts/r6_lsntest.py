import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":390,"height":844}); fontroute.setup(pg)
    pg.add_init_script("Object.defineProperty(window, 'speechSynthesis', {value: {speak:function(u){ setTimeout(function(){ if(u.onend) u.onend({}); }, 120); }, cancel:function(){}, getVoices:function(){ return []; }, speaking:false, pending:false, paused:false, resume:function(){}, addEventListener:function(){}, onvoiceschanged:null}});")
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    pg.evaluate("() => { const T=window.__t, s=T.state(); s.prefs.fx=false; T.LESSONS.slice(0,6).forEach(l => { s.learn.done[l.id]={at:T.today(), best:90}; l.W.forEach(w => s.words[w.zh]={b:1, d:T.today()}); }); s.learn.dlg={u1:{at:T.today(),best:100}, u2:{at:T.today(),best:80}}; location.hash='wiederholen'; }"); pg.wait_for_timeout(500)
    print("units:", pg.evaluate("() => window.__t.lsnUnits().map(u=>u.id)"), "pick:", pg.evaluate("() => window.__t.lsnPick().id"))
    assert pg.query_selector(".lsncard"), "Karte fehlt"
    pg.select_option("#lsn-sel", "u2")
    pg.click(".lsncard [data-act='listen']"); pg.wait_for_timeout(400)
    st = pg.evaluate("() => { const S=window.__t.getS(); return {kind:S.kind, unit:S.unit.id, q:S.queue.map(e=>e.type), playing:S.lsnPlaying, cur:S.lsnCur}; }")
    print(st); assert st["kind"]=="listen" and st["unit"]=="u2" and st["q"][0]=="listen" and st["q"][-1]=="ltext" and len(st["q"])==5
    assert pg.is_disabled("#s-next"), "Weiter sollte gesperrt sein"
    pg.screenshot(path="/tmp/lsn1.png")
    pg.wait_for_function("() => window.__t.getS().lsnDone", timeout=30000)
    print("done; next enabled:", not pg.is_disabled("#s-next"))
    pg.screenshot(path="/tmp/lsn2.png")
    pg.click("#s-next"); pg.wait_for_timeout(300)
    for k in range(3):
        ex = pg.evaluate("() => { const S=window.__t.getS(); const e=S.queue[0]; return {type:e.type, n:e.opts.length, right:e.opts.indexOf(e.ln), de:e.opts.map(o=>o.de)}; }")
        print(ex); assert ex["type"]=="lhear" and ex["n"]==3 and len(set(ex["de"]))==3
        if k==0: pg.screenshot(path="/tmp/lsn3.png")
        pg.click('[data-opt="%d"]' % (ex["right"] if k<2 else (ex["right"]+1)%3)); pg.wait_for_timeout(300)
        if k==2: pg.screenshot(path="/tmp/lsn4.png")
        pg.click("#s-next"); pg.wait_for_timeout(300)
        if k==2:
            # falsche Antwort kommt nochmal
            ex2 = pg.evaluate("() => { const S=window.__t.getS(); const e=S.queue[0]; return e.type; }")
            if ex2=="lhear":
                r = pg.evaluate("() => { const S=window.__t.getS(); const e=S.queue[0]; return e.opts.indexOf(e.ln); }")
                pg.click('[data-opt="%d"]' % r); pg.wait_for_timeout(300); pg.click("#s-next"); pg.wait_for_timeout(300)
    ex = pg.evaluate("() => { const S=window.__t.getS(); return S.queue[0] && S.queue[0].type; }")
    print("now:", ex); assert ex=="ltext"
    pg.screenshot(path="/tmp/lsn5.png")
    print(pg.evaluate("() => { const S=window.__t.getS(); return {q:S.queue.map(e=>e.type), ans:S.answered, btn: !!document.querySelector('#s-next'), dis: document.querySelector('#s-next') && document.querySelector('#s-next').disabled}; }"))
    pg.click("#s-next"); pg.wait_for_timeout(400)
    print(pg.evaluate("() => { const S=window.__t.getS(); return {q:S.queue.map(e=>e.type), fin:S.finished}; }"))
    fin = pg.evaluate("() => { const S=window.__t.getS(); const st=window.__t.state(); return {fin:S.finished, lsn:st.learn.lsn}; }")
    print(fin); assert fin["fin"]["xp"]>=3 and fin["lsn"]["u2"]["n"]==1 and fin["lsn"]["u2"]["best"]==67
    pg.screenshot(path="/tmp/lsn6.png")
    print("errs", errs)
    b.close()
