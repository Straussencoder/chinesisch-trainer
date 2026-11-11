# Prüft: In Lektionen taucht kein Wort auf, das zu diesem Zeitpunkt noch nicht eingeführt war
# (Aufgabe, Antwortmöglichkeiten, Paare, Satzbausteine, Beispiele, Baupläne). 40 Zufallsdurchläufe pro Lektion.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import json
AUDIT = """(runs) => { const T = window.__t, bad = {};
  const toks = ph => (ph && ph.toks ? ph.toks.map(t => t.zh) : []);
  T.LESSONS.forEach((l, li) => {
    for(let r = 0; r < runs; r++){
      const q = T.buildLesson(l), seen = new Set();
      T.LESSONS.slice(0, li).forEach(x => x.W.forEach(w => seen.add(w.zh)));
      const miss = (zh, where) => { if(!seen.has(zh) && !(zh.length > 1 && !T.WORD[zh] && Array.from(zh).every(c => seen.has(c)))){ const k = l.id + ': ' + zh + ' (' + where + ')'; bad[k] = (bad[k]||0) + 1; } };
      q.forEach(ex => {
        if(ex.type === 'intro'){ seen.add(ex.w.zh); toks(ex.w.ex).forEach(z => { if(!/儿$/.test(z)) miss(z, 'Beispiel bei ' + ex.w.zh); });  /* 这儿/那儿/一点儿: nördliche Form desselben Worts */ return; }
        if(ex.type === 'rule'){ ex.p.ex.forEach(e => (e.toks ? e.toks.map(t => t.zh) : e.t.split(' ').map(t => t.split('|')[0])).forEach(z => miss(z, 'Bauplan ' + ex.p.id))); return; }
        if(ex.w) miss(ex.w.zh, ex.type);
        if(ex.type === 'judge'){ toks(ex.s.bad).forEach(z => miss(z, 'falscher Satz')); }
        if(ex.gw) miss(ex.gw.zh, 'Lücke');
        if(ex.type !== 'judge') (ex.opts || []).forEach(o => { if(o.toks) toks(o).forEach(z => miss(z, 'Satz-Auswahl')); else miss(o.zh, ex.type + '-Auswahl'); });
        (ex.ws || []).forEach(w => miss(w.zh, 'Paare'));
        if(ex.s) toks(ex.s).forEach(z => miss(z, 'Satz'));
        (ex.bank || []).forEach(b => miss(b.zh, 'Satzbaustein'));
      });
    }
  });
  return bad; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.__t")
    bad = pg.evaluate(AUDIT, 40)
    print(len(bad), "Probleme")
    for k, v in sorted(bad.items(), key=lambda x: (int(x[0].split(':')[0][1:]), x[0]))[:60]: print("  ", k, v)
    b.close()
