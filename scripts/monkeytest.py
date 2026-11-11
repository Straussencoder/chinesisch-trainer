# Zufallstest: klickt sich quer durch die App und sammelt JS-Fehler, Sackgassen und Überlauf.
# Aufruf: python3 scripts/monkeytest.py <szenario> <schritte> <seed>   Szenarien: frisch, mitte, alles, still, dunkel, mac
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, random, json, time
sys.path.insert(0, ROOT + "/scripts"); import fontroute
scen = sys.argv[1] if len(sys.argv) > 1 else "mitte"
steps = int(sys.argv[2]) if len(sys.argv) > 2 else 300
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rnd = random.Random(seed)
FAKES = """

window.__mkRoot = function(){ return ['game','session','app'].map(id => document.getElementById(id)).find(e => e && !e.hidden && e.getBoundingClientRect().height > 0 && !e.inert); };
window.__mkEls = function(root){ return [...root.querySelectorAll('button, a[href^="#"], select, input:not([type=file]), textarea, summary, [tabindex="0"]')].filter(e => { if(e.disabled || e.getAttribute('aria-disabled')==='true') return false; if(e.closest('[inert]')) return false; const b=e.getBoundingClientRect(); if(!b.width||!b.height) return false; const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.pointerEvents==='none') return false; return true; }); };
Object.defineProperty(window, 'speechSynthesis', {value: {speak:function(u){ setTimeout(function(){ if(u.onend) u.onend({}); }, 60); }, cancel:function(){}, getVoices:function(){ return []; }, speaking:false, pending:false, paused:false, resume:function(){}, addEventListener:function(){}, onvoiceschanged:null}});
window.SpeechRecognition = window.webkitSpeechRecognition = function(){ var self=this; this.start=function(){ setTimeout(function(){ var r=Math.random(); if(r<0.3){ self.onerror && self.onerror({error:"no-speech"}); } else { var t = r<0.6 ? "我是德国人" : "你好吗"; var res=[[{transcript:t}]]; res[0].isFinal=true; self.onresult && self.onresult({results:res}); } self.onend && self.onend(); }, 80); }; this.stop=function(){}; this.abort=function(){}; };
"""
SETUP = {
 "frisch": "() => {}",
 "mitte": "() => { const T=window.__t, s=T.state(), t=T.today(); T.LESSONS.slice(0,12).forEach((l,i) => { s.learn.done[l.id]={at:t, best:90, gold:(i%3?undefined:t)}; l.W.forEach(w => s.words[w.zh]={b:1+(i%4), d:T.addDays(t, i%3-1), iv:[1,3,8,20][i%4], e:2.5}); }); s.learn.dlg={u1:{at:t,best:100},u2:{at:t,best:80},u3:{at:t,best:100}}; }",
 "alles": "() => { const T=window.__t, s=T.state(), t=T.today(); T.LESSONS.forEach((l,i) => { s.learn.done[l.id]={at:t, best:100, gold:t}; l.W.forEach(w => s.words[w.zh]={b:3, d:T.addDays(t, (i%5)-1), iv:8, e:2.6}); }); for(let u=1;u<=17;u++) s.learn.dlg['u'+u]={at:t,best:100}; }",
 "still": "() => { const T=window.__t, s=T.state(), t=T.today(); T.LESSONS.slice(0,9).forEach(l => { s.learn.done[l.id]={at:t, best:90}; l.W.forEach(w => s.words[w.zh]={b:1, d:t}); }); T.setQuiet(60); }",
 "dunkel": "() => { const T=window.__t, s=T.state(), t=T.today(); s.prefs.theme='dark'; s.prefs.hz='gross'; T.LESSONS.slice(0,6).forEach(l => { s.learn.done[l.id]={at:t, best:70}; l.W.forEach(w => s.words[w.zh]={b:0, d:t}); }); }",
 "mac": "() => { const T=window.__t, s=T.state(), t=T.today(); T.LESSONS.slice(0,20).forEach(l => { s.learn.done[l.id]={at:t, best:90}; l.W.forEach(w => s.words[w.zh]={b:2, d:t}); }); s.learn.dlg={u1:{at:t,best:100},u2:{at:t,best:100},u5:{at:t,best:100}}; }",
}
vw = (1366, 900) if scen == "mac" else (390, 844)
PICK = """() => {
  const root = window.__mkRoot(); if(!root) return {els:[], stuck:'kein Wurzelknoten', over:0};
  const els = window.__mkEls(root);
  return {els: els.map((e, i) => ({i, tag:e.tagName, act:e.dataset.act||e.dataset.opt||e.dataset.lesson||e.dataset.node||e.dataset.dlg||e.getAttribute('href')||e.id||'', type:e.type||''})), root:root.id,
    over: document.scrollingElement.scrollWidth - innerWidth};
}"""
CLICK = """(i) => { const root = window.__mkRoot(); const e = window.__mkEls(root)[i]; if(!e) return null; e.scrollIntoView({block:'center'}); return {x:0}; }"""
issues, log = [], []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream", "--autoplay-policy=no-user-gesture-required"])
    ctx = b.new_context(viewport={"width": vw[0], "height": vw[1]}, permissions=["microphone"])
    pg = ctx.new_page(); fontroute.setup(pg)
    pg.add_init_script(FAKES)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
    pg.on("console", lambda m: errs.append("console: " + m.text[:200]) if m.type == "error" and "favicon" not in m.text and "net::" not in m.text else None)
    pg.on("dialog", lambda d: d.dismiss())
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    pg.evaluate("() => { window.__t.state().prefs.fx = false; }")
    pg.evaluate(SETUP[scen]); pg.evaluate("() => { location.hash = 'lernen'; }"); pg.wait_for_timeout(300)
    stuck_n = 0; last_sig = None; same = 0
    for k in range(steps):
        try:
            info = pg.evaluate(PICK)
        except Exception as e:
            issues.append(f"Schritt {k}: Seite kaputt: {e}"); break
        if info.get("over", 0) > 2: issues.append(f"Schritt {k}: waagerechter Überlauf {info['over']}px in {info.get('root')} nach {log[-3:]}")
        els = info["els"]
        if not els:
            stuck_n += 1
            issues.append(f"Schritt {k}: Sackgasse, nichts klickbar in {info.get('root')} nach {log[-4:]}")
            pg.keyboard.press("Escape"); pg.evaluate("() => { const T=window.__t; if(T.getS()) T.exitSession(); location.hash='lernen'; }"); pg.wait_for_timeout(200); continue
        r = rnd.random()
        if r < 0.06:
            key = rnd.choice(["Enter", "Escape", "1", "2", "3", "4", " ", "Backspace", "Tab"]); pg.keyboard.press(key); log.append("key " + key)
        elif r < 0.10:
            v = rnd.choice(["lernen", "wiederholen", "spiel", "toene", "saetze", "einstellungen", "heute", "quatsch"]); pg.evaluate(f"() => {{ location.hash = '{v}'; }}"); log.append("hash " + v)
        else:
            # Antwortknöpfe und Weiter bevorzugen, damit Übungen auch vorankommen
            pref = [e for e in els if str(e["act"]) in ("next", "check", "good", "again") or e["tag"] == "BUTTON" and str(e["act"]).isdigit()]
            e = rnd.choice(pref) if pref and rnd.random() < 0.55 else rnd.choice(els)
            log.append(f'{e["tag"]}:{e["act"]}')
            try:
                pg.evaluate(CLICK, e["i"])
                if e["tag"] == "SELECT":
                    opts = pg.evaluate("(i) => { const s=[...document.querySelectorAll('select')][i]; return s ? [...s.options].map(o=>o.value) : []; }", 0)
                    if opts: pg.select_option("select", rnd.choice(opts))
                elif e["tag"] in ("INPUT", "TEXTAREA"):
                    pg.evaluate("(i) => { const el = window.__mkEls(window.__mkRoot())[i]; if(el) el.focus(); }", e["i"])
                    pg.keyboard.type(rnd.choice(["ni3hao3", "wo3", "你好", "abc", "xie4xie", "5", "", "ta1 shi4"]))
                    if rnd.random() < 0.6: pg.keyboard.press("Enter")
                else:
                    pg.evaluate("(i) => { const el = window.__mkEls(window.__mkRoot())[i]; if(el) el.click(); }", e["i"])
            except Exception as ex:
                issues.append(f"Schritt {k}: Klick fehlgeschlagen {e}: {str(ex)[:120]}")
        pg.wait_for_timeout(rnd.choice([40, 80, 150, 400]))
        if errs:
            issues.append(f"Schritt {k}: JS {errs[:3]} nach {log[-5:]}"); errs.clear()
        # steckt die Ansicht fest? (gleiche Signatur über 40 Schritte)
        sig = pg.evaluate("() => { const S=window.__t.getS(); const r=document.querySelector('#session'); return (S ? S.kind+':'+(S.queue[0]&&S.queue[0].type)+':'+S.queue.length+':'+S.answered : 'app:'+location.hash) + ':' + (r && !r.hidden ? r.innerText.length : 0); }")
        same = same + 1 if sig == last_sig else 0; last_sig = sig
        if same >= 60: issues.append(f"Schritt {k}: hängt seit 60 Schritten bei {sig} nach {log[-6:]}"); same = 0; pg.evaluate("() => { const T=window.__t; if(T.getS()) T.exitSession(); }")
    b.close()
print(json.dumps({"szenario": scen, "schritte": steps, "seed": seed, "probleme": len(issues)}, ensure_ascii=False))
for i in issues[:40]: print(" -", i)
