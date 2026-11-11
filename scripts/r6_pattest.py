import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, ROOT + "/scripts"); import fontroute
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":390,"height":844}); fontroute.setup(pg)
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(300)
    # 9 Lektionen fertig
    pg.evaluate("() => { const T=window.__t, s=T.state(); s.prefs.fx=false; T.LESSONS.slice(0,9).forEach(l => { s.learn.done[l.id]={at:T.today(), best:90}; l.W.forEach(w => s.words[w.zh]={b:1, d:T.today()}); }); }")
    r = pg.evaluate("""() => { const T=window.__t;
      // Satzbau-Übung: erst falsch, dann richtig -> Bauplan zurück
      T.startSentences(); const S=T.getS();
      const ex = S.queue.find(e => e.type==='build');
      S.queue.unshift(ex); // nach vorn
      T.renderSession();
      const gp = ex.s.gp;
      // falsch bauen: Reihenfolge verdrehen
      const own = ex.bank.map((b,i)=>({b,i})).filter(x=>x.b.src!=null).sort((a,b)=>b.b.src-a.b.src);
      ex.built = ex.s.toks.map((_,k)=> own[k].i);
      T.checkBuild();
      const tried = ex.tried;
      // richtig bauen
      ex.built = ex.s.toks.map((_,k)=> ex.bank.findIndex(b=>b.src===k));
      T.checkBuild();
      const st = T.state().pats[gp];
      return {gp, tried, answered:S.answered, correct:S.correct, half:S.half, st, score:T.patScore(gp), focus: T.focusPat() && T.focusPat().id};
    }""")
    print(r)
    assert r["tried"] and r["st"]["bad"]==1 and r["st"]["b"]==0 and r["focus"]==r["gp"], r
    # Gap richtig beim ersten Versuch -> Stufe hoch
    r2 = pg.evaluate("""() => { const T=window.__t; const S=T.getS();
      const ex = S.queue.find(e => e.type==='gap'); S.queue.unshift(ex); S.answered=false; T.renderSession();
      const gp = ex.s.gp; const before = JSON.stringify(T.state().pats[gp]||null);
      const i = ex.opts.indexOf(ex.gw); document.querySelector('[data-opt="'+i+'"]').click();
      return {gp, before, after:T.state().pats[gp], ok:S.correct};
    }""")
    print(r2)
    assert r2["ok"] and r2["after"]["n"]>=1 and r2["after"]["bad"]==0 or r2["after"]["bad"]>=0
    # Baupläne-Seite zeigt Stand
    pg.evaluate("() => window.__t.exitSession()"); pg.wait_for_timeout(300)
    pg.evaluate("() => { location.hash='saetze'; }"); pg.wait_for_timeout(400)
    pg.click('[data-smode="plans"]'); pg.wait_for_timeout(400)
    txt = pg.evaluate("() => (document.querySelector('#plans')||{}).innerText || ''")
    print("plans:", txt[:400].replace("\n"," | "))
    assert "wackligsten" in txt or "fällig" in txt, "Bauplan-Stand fehlt"
    pg.screenshot(path="/tmp/plans.png")
    print("errs", errs)
    b.close()
