import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
FAKE = """
window.__fakeSay = "";
window.SpeechRecognition = window.webkitSpeechRecognition = function(){ var self=this; this.start=function(){ setTimeout(function(){ var t=window.__fakeSay; if(t){ var res=[[{transcript:t}, {transcript:t+"呢"}]]; res[0].isFinal=true; res.length=1; self.onresult && self.onresult({results:res}); } else { self.onerror && self.onerror({error:"no-speech"}); } self.onend && self.onend(); }, 150); }; this.stop=function(){}; this.abort=function(){}; };
"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":390,"height":844}); fontroute.setup(pg)
    pg.add_init_script(FAKE)
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    T = pg.evaluate("""() => { const T=window.__t;
      const a=T.sayScore(["我是德国人"], ["我是德国人"]), b=T.sayScore(["我是德国"], ["我是德国人"]), c=T.sayScore(["你好"], ["我是德国人"]), d=T.sayScore(["她叫李娜。"], ["他叫李娜"]), e=T.sayScore(["今天我去"], ["我今天去","今天我去"]);
      return {a:[a.ok,a.sim], b:[b.ok,+b.sim.toFixed(2)], c:[c.ok,+c.sim.toFixed(2)], d:[d.ok], e:[e.ok], m:T.sayMatch("我德国人","我是德国人")}; }""")
    print(T)
    assert T["a"][0] and not T["b"][0] and T["b"][1]>=0.75 and T["c"][1]<0.5 and T["d"][0] and T["e"][0] and T["m"]==[True,False,True,True,True]
    pg.evaluate("() => { const T=window.__t, s=T.state(); s.prefs.fx=false; T.LESSONS.slice(0,8).forEach(l => { s.learn.done[l.id]={at:T.today(), best:90}; l.W.forEach(w => s.words[w.zh]={b:1, d:T.today()}); }); location.hash='wiederholen'; }"); pg.wait_for_timeout(500)
    assert pg.query_selector(".saycard [data-act='sayprac']:not([disabled])"), "Karte/Knopf fehlt"
    pg.click(".saycard [data-act='sayprac']"); pg.wait_for_timeout(400)
    st = pg.evaluate("() => { const S=window.__t.getS(); return {kind:S.kind, n:S.queue.length, types:[...new Set(S.queue.map(e=>e.type))], first:S.queue[0].s.key}; }")
    print(st); assert st["kind"]=="say" and st["n"]==8 and st["types"]==["say"]
    pg.screenshot(path="/tmp/say1.png")
    # 1: richtig
    pg.evaluate("() => { window.__fakeSay = window.__t.getS().queue[0].s.key; }")
    pg.click("[data-act='say']"); pg.wait_for_timeout(500)
    r = pg.evaluate("() => { const S=window.__t.getS(); return {ans:S.answered, ok:S.correct, half:S.half}; }"); print(r); assert r["ans"] and r["ok"] and not r["half"]
    pg.screenshot(path="/tmp/say2.png"); pg.click("#s-next"); pg.wait_for_timeout(300)
    # 2: nichts gehört -> Fehlermeldung, kein Urteil
    pg.evaluate("() => { window.__fakeSay = ''; }")
    pg.click("[data-act='say']"); pg.wait_for_timeout(500)
    r = pg.evaluate("() => { const S=window.__t.getS(); return {ans:S.answered, err:S.queue[0].err, txt:document.querySelector('.w-note') && document.querySelector('.w-note').textContent}; }"); print(r); assert not r["ans"] and r["err"]=="no-speech"
    # 3: fast richtig (ein Zeichen fehlt)
    pg.evaluate("() => { const k=window.__t.getS().queue[0].s.key; window.__fakeSay = Array.from(k).slice(0,-1).join(''); }")
    pg.click("[data-act='say']"); pg.wait_for_timeout(500)
    r = pg.evaluate("() => { const S=window.__t.getS(); return {ans:S.answered, ok:S.correct, half:S.half, key:S.queue[0].s.key}; }"); print(r); assert r["ans"] and (r["half"] or not r["ok"])
    pg.screenshot(path="/tmp/say3.png"); pg.click("#s-next"); pg.wait_for_timeout(300)
    # 4: falsch
    pg.evaluate("() => { window.__fakeSay = '再见'; }")
    pg.click("[data-act='say']"); pg.wait_for_timeout(500)
    r = pg.evaluate("() => { const S=window.__t.getS(); return {ans:S.answered, ok:S.correct}; }"); print(r); assert r["ans"] and not r["ok"]
    pg.screenshot(path="/tmp/say4.png"); pg.click("#s-next"); pg.wait_for_timeout(300)
    # 5: Weiß ich nicht
    pg.click("[data-act='sayskip']"); pg.wait_for_timeout(300)
    r = pg.evaluate("() => { const S=window.__t.getS(); return {ans:S.answered, ok:S.correct}; }"); print(r); assert r["ans"] and not r["ok"]
    print("errs", errs)
    b.close()
