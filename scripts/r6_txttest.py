import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":390,"height":844}); fontroute.setup(pg)
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    pg.evaluate("() => { const T=window.__t, s=T.state(); s.prefs.fx=false; T.LESSONS.slice(0,10).forEach(l => { s.learn.done[l.id]={at:T.today(), best:90}; l.W.forEach(w => s.words[w.zh]={b:1, d:T.today()}); }); location.hash='wiederholen'; }"); pg.wait_for_timeout(500)
    print("texts:", pg.evaluate("() => window.__t.textUnits().map(t=>t.id)"), "pick:", pg.evaluate("() => window.__t.textPick().id"))
    assert pg.query_selector(".txtcard"), "Karte fehlt"
    pg.select_option("#txt-sel", "t03")
    pg.click(".txtcard [data-act='readtext']"); pg.wait_for_timeout(400)
    st = pg.evaluate("() => { const S=window.__t.getS(); return {kind:S.kind, id:S.t.id, q:S.queue.map(e=>e.type)}; }")
    print(st); assert st["kind"]=="text" and st["id"]=="t03" and st["q"]==["tq","tq","tq","ttext"]
    pg.screenshot(path="/tmp/txt1.png")
    for k in range(3):
        ex = pg.evaluate("() => { const S=window.__t.getS(); const e=S.queue[0]; return {q:e.q, a:e.a, opts:e.opts, l:e.l}; }")
        print(ex)
        pg.click('[data-opt="%d"]' % (ex["a"] if k!=1 else (ex["a"]+1)%3)); pg.wait_for_timeout(300)
        hit = pg.evaluate("() => { const h=document.querySelector('.rt-line.hit'); return h && h.innerText.replace(/\\n/g,' | '); }")
        print("  hit:", hit); assert hit
        if k==1: pg.screenshot(path="/tmp/txt2.png")
        pg.click("#s-next"); pg.wait_for_timeout(300)
    # Wiederholung der falschen Frage
    t = pg.evaluate("() => window.__t.getS().queue.map(e=>e.type)"); print(t)
    if t[0]=="tq":
        a = pg.evaluate("() => window.__t.getS().queue[0].a"); pg.click('[data-opt="%d"]' % a); pg.wait_for_timeout(200); pg.click("#s-next"); pg.wait_for_timeout(300)
    assert pg.evaluate("() => window.__t.getS().queue[0].type")=="ttext"
    pg.screenshot(path="/tmp/txt3.png")
    pg.click("#s-next"); pg.wait_for_timeout(400)
    fin = pg.evaluate("() => { const S=window.__t.getS(); const st=window.__t.state(); return {fin:S.finished, txt:st.learn.txt}; }")
    print(fin); assert fin["fin"]["xp"]==4 and fin["txt"]["t03"]["n"]==1
    # Chat-Text
    pg.evaluate("() => window.__t.exitSession()"); pg.wait_for_timeout(200)
    pg.evaluate("() => window.__t.startText('t02')"); pg.wait_for_timeout(300)
    pg.screenshot(path="/tmp/txt4.png")
    # Daten: jede Frage hat genau eine richtige Antwort, Zeilenindex gültig
    bad = pg.evaluate("() => window.__t.TEXTS.filter(t => t.qs.some(q => q.opts.length!==3 || q.a<0 || q.a>2 || q.l>=t.lines.length)).map(t=>t.id)")
    assert not bad, bad
    print("errs", errs)
    b.close()
