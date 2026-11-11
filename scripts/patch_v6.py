import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
p = ROOT + "/zh-app/index.src.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:110])
    s = s.replace(a, b)

# ================= HTML =================
rep('''<script id="zh-lessons">
<!--ZH_LESSONS-->
</script>''', '''<script id="zh-lessons">
<!--ZH_LESSONS-->
</script>
<script id="zh-grammar">
<!--ZH_GRAMMAR-->
</script>''')
rep('''      <p class="subtitle">Fertige Sätze für die Reise zum Auswendiglernen. Leichter wird es, wenn du vorher die Lektionen machst.</p>
      <div class="chips" id="cats" role="group" aria-label="Thema"></div>''', '''      <p class="subtitle">Fertige Sätze für die Reise und die Baupläne dahinter. So verstehst du, warum ein Satz so gebaut ist und nicht anders.</p>
      <div class="seg smode" role="group" aria-label="Ansicht" id="smode"></div>
      <div id="plans" hidden></div>
      <div id="cards-wrap">
      <div class="chips" id="cats" role="group" aria-label="Thema"></div>''')
rep('''      <details class="list" id="all">
        <summary>Alle Sätze ansehen</summary>
        <div id="all-list"></div>
      </details>
    </section>''', '''      <details class="list" id="all">
        <summary>Alle Sätze ansehen</summary>
        <div id="all-list"></div>
      </details>
      </div>
    </section>''')

# ================= JS: Satzbau-Grundlagen =================
rep('''/* ================= Datum ================= */''', r'''/* ================= Satzbau ================= */
var GR = window.ZH_GRAMMAR || {points:[], sents:{}, cards:{}, wc:{}};
var SLOT = {S:["Subjekt","wer? was?"], V:["Verb","tut was?"], O:["Objekt","wen? was?"], A:["Eigenschaft","wie?"], D:["Adverb","wie? nicht?"], T:["Zeit","wann?"],
  L:["Ort","wo? wohin?"], Z:["Menge","wie viel?"], Q:["Frage","ja oder nein?"], P:["Partikel","kleines Zusatzwort"], X:["Ausdruck","feste Wendung"]};
function parseG(g){ return (g||"").split("|").filter(Boolean).map(function(x){ var m = x.match(/^(\S) (\S+) (.+)$/) || [x, "X", "Ausdruck", ""]; return {slot:SLOT[m[1]] ? m[1] : "X", wc:m[2], gl:m[3]}; }); }
var POINTS = (GR.points||[]).map(function(p){
  return {id:p.id, title:p.title, text:p.text, lesson:LESSONS.find(function(l){ return l.id===p.l; }) || LESSONS[0],
    ex:p.ex.map(function(e){ var toks = parseToks(e.t); return {toks:toks, zh:toks.map(function(t){ return t.zh; }).join("")+(e.p||""), de:e.de, gs:parseG(e.g)}; })};
});
var POINT = {}; POINTS.forEach(function(p){ POINT[p.id] = p; });
SENTS.forEach(function(s){ var a = GR.sents && GR.sents[s.key]; if(a){ s.gs = parseG(a.g); s.why = a.n; s.gp = a.gp; } });
function slotGroups(gs){ var out = []; gs.forEach(function(g, i){ var last = out[out.length-1]; if(last && last.slot===g.slot) last.idx.push(i); else out.push({slot:g.slot, idx:[i]}); }); return out; }
/* Chinesische Zeichen im Fließtext in der Zeichenschrift setzen */
function hzText(t){ return esc(t).replace(/([㐀-鿿　-〿！-？]+)/g, '<span class="hz" lang="zh">$1</span>'); }
function patternHTML(gs){
  if(!gs || !gs.length) return "";
  return '<div class="bauplan">'+slotGroups(gs).map(function(gr, k){
    return (k ? '<span class="bp-plus" aria-hidden="true">+</span>' : '')+'<span class="bp s-'+gr.slot+'"><b>'+SLOT[gr.slot][0]+'</b><small>'+SLOT[gr.slot][1]+'</small></span>';
  }).join("")+'</div>';
}
/* Satz zerlegt: Satzteile als farbige Gruppen, darin jedes Wort mit Pinyin, wörtlicher Bedeutung und Wortart */
function breakdownHTML(toks, gs, why, attr){
  if(!gs || !toks || gs.length!==toks.length) return "";
  var h = '<div class="satz">'+slotGroups(gs).map(function(gr, k){
    return (k ? '<span class="sg-plus" aria-hidden="true">+</span>' : '')+'<div class="sg s-'+gr.slot+'"><span class="sg-l">'+SLOT[gr.slot][0]+'</span><div class="sg-w">'+gr.idx.map(function(i){
      var t = toks[i], g = gs[i];
      return '<button type="button" class="sw" '+(attr ? attr(i) : 'data-say="'+esc(t.zh)+'|'+esc(t.py)+'"')+' aria-label="'+esc(t.zh)+' anhören"><span class="sw-hz" lang="zh">'+esc(t.zh)+'</span><span class="sw-py">'+pyHTML(t.py)+'</span><span class="sw-gl">'+esc(g.gl)+'</span><span class="sw-wc">'+esc(g.wc)+'</span></button>';
    }).join("")+'</div></div>';
  }).join("")+'</div>';
  if(why) h += '<p class="why"><span class="seal" aria-hidden="true">理</span><span><b>Warum so?</b> '+hzText(why)+'</span></p>';
  return h;
}
/* Tonverlauf als kleine Kurve (Tonhöhe 1 tief bis 5 hoch) */
var TONE_PATH = {1:"M6 5 L38 5", 2:"M6 14 C18 13 29 10 38 4", 3:"M6 11 C11 19 16 22 21 22 C28 22 33 15 38 9", 4:"M6 4 C17 7 29 14 38 22"};
function toneCurve(k){ return '<svg class="tcurve" viewBox="0 0 44 26" aria-hidden="true"><path d="M3 4 H41 M3 22 H41" stroke="currentColor" stroke-width=".8" opacity=".2"/><path d="'+TONE_PATH[k]+'" fill="none" stroke="var(--tc)" stroke-width="3.2" stroke-linecap="round"/><circle cx="'+TONE_PATH[k].match(/(\d+) (\d+)$/)[1]+'" cy="'+TONE_PATH[k].match(/(\d+) (\d+)$/)[2]+'" r="2.6" fill="var(--tc)"/></svg>'; }

/* ================= Datum ================= */''')

# Standardwert für die Ansicht der Sätze
rep('autoplay:"words", pinyin:true, toneColors:true, fx:true, theme:"auto", hz:"normal", goal:20}; }',
    'autoplay:"words", pinyin:true, toneColors:true, fx:true, theme:"auto", hz:"normal", goal:20, smode:"cards"}; }')

# ================= Lektion aufbauen: Wiederholung + Baupläne =================
a = s.index("function buildLesson(l){"); b = s.index("function makeBuild(s, pool){")
s = s[:a] + r'''/* Wörter aus früheren Lektionen: schwächere und fällige zuerst */
function weakSort(list){
  var t = today();
  return list.map(function(w){ var r = state.words[w.zh]; return {w:w, s:(r ? (r.d<=t ? 0 : 2) + (r.b||0)*0.6 : 1.5) + Math.random()*0.5}; })
    .sort(function(a, b){ return a.s - b.s; }).map(function(x){ return x.w; });
}
function pickOld(l){
  var used = {}, older = WORDS.filter(function(w){ return w.lesson.n < l.n; });
  var from = function(n){ return n>=1 ? LESSONS[n-1].W : []; };
  var take = function(list, k){ var out = weakSort(list.filter(function(w){ return !used[w.zh]; })).slice(0, k); out.forEach(function(w){ used[w.zh] = 1; }); return out; };
  var p1 = from(l.n-1), p2 = from(l.n-2);
  var warm = take(p1, 2);
  var mid = take(p1, 1).concat(take(p2.length ? p2 : p1, 1));
  mid = mid.concat(take(older, 3 - mid.length));
  return {warm:warm, mid:mid};
}
var lastOldType = "";
function oldQuiz(w, pool){
  var ts = (canHear(w) ? ["hear","mean","char"] : ["mean","char"]).concat(canTone(w) ? ["tone"] : []);
  var pick = ts.filter(function(t){ return t!==lastOldType; });
  var q = makeQuiz(pickN(pick.length ? pick : ts, 1)[0], w, pool);
  lastOldType = q.type; q.old = true;
  return q;
}
function buildLesson(l){
  var W = l.W, pool = poolUpTo(l), ex = [], types = ["mean","hear","char"], old = pickOld(l), shown = {};
  old.warm.forEach(function(w){ ex.push(oldQuiz(w, pool)); });
  W.forEach(function(w, i){
    ex.push({id:++exSeq, type:"intro", w:w});
    ex.push(makeQuiz(types[i%3], w, pool));
    if(i>0) ex.push(makeQuiz(types[(i+1)%3], W[i-1], pool));
    if(i===1 && old.mid[0]) ex.push(oldQuiz(old.mid[0], pool));
    if(i===3 && old.mid[1]) ex.push(oldQuiz(old.mid[1], pool));
  });
  ex.push({id:++exSeq, type:"pairs", ws:pickN(W, Math.min(5, W.length))});
  if(old.mid[2]) ex.push(oldQuiz(old.mid[2], pool));
  ex.push(makeQuiz(types[W.length%3], W[W.length-1], pool));
  pickN(W.slice(0, -1), 2).forEach(function(w){ ex.push(makeQuiz(types[(W.indexOf(w)+1)%3], w, pool)); });
  var tw = W.filter(canTone);
  if(tw.length) ex.push(makeQuiz("tone", pickN(tw,1)[0], pool));
  /* Baupläne dieser Lektion, die zu keinem Satz gehören (z. B. Lektion 1 und 6) */
  var inSents = {}; l.S.forEach(function(s){ if(s.gp) inSents[s.gp] = 1; });
  POINTS.forEach(function(p){ if(p.lesson===l && !inSents[p.id]){ ex.push({id:++exSeq, type:"rule", p:p}); shown[p.id] = 1; } });
  l.S.forEach(function(s, i){
    var p = s.gp && POINT[s.gp];
    if(p && p.lesson===l && !shown[p.id]){ ex.push({id:++exSeq, type:"rule", p:p}); shown[p.id] = 1; }
    ex.push(makeBuild(s, pool));
    if(i===0){ var sm = makeSentMean(s); if(sm) ex.push(sm); }
  });
  return ex;
}
''' + s[b:]
# Hören nur mit eigener Aufnahme, auch in Lektionen
rep('''function makeQuiz(type, w, pool){
  var ex = {id:++exSeq, type:type, w:w};''', '''function makeQuiz(type, w, pool){
  if(type==="hear" && !canHear(w)) type = "mean";
  var ex = {id:++exSeq, type:type, w:w};''')

# ================= Ergebnisse mit dem Wiederholungsplan abgleichen (gemeinsam für Lektion und Rennen) =================
rep('''function nextLesson(){ for(var i=0;i<LESSONS.length;i++) if(!isDone(LESSONS[i])) return LESSONS[i]; return null; }
function learnedWords(){''', '''function nextLesson(){ for(var i=0;i<LESSONS.length;i++) if(!isDone(LESSONS[i])) return LESSONS[i]; return null; }
/* results: {Zeichen: {ok, bad}}. Fällig + ohne Fehler = nächste Stufe, fällig + Fehler = zurück auf 0 und heute nochmal,
   nicht fällig + Fehler = eine Stufe zurück und heute nochmal, nicht fällig + richtig = bleibt */
function applyResults(results){
  var t = today();
  Object.keys(results||{}).forEach(function(zh){
    var r = results[zh], rec = state.words[zh]; if(!rec) return;
    var ok = r.bad===0;
    if(rec.d <= t){ if(ok){ var b = Math.min(5, (rec.b||0) + 1); state.words[zh] = {b:b, d:addDays(t, INTERVALS[b])}; } else state.words[zh] = {b:0, d:t}; }
    else if(!ok) state.words[zh] = {b:Math.max(0, (rec.b||0) - 1), d:t};
  });
}
function learnedWords(){''')

# Antworten zu alten Wörtern merken
rep('''  if(!ex.retry){ S.firstN++; if(ok) S.firstOk++; }
  if(ex.w) recordWord(ex.w, ok);''', '''  if(!ex.retry){ S.firstN++; if(ok) S.firstOk++; }
  if(ex.w) recordWord(ex.w, ok);
  if(ex.old && ex.w && S.kind==="lesson"){ S.oldRes = S.oldRes || {}; var orr = S.oldRes[ex.w.zh] || (S.oldRes[ex.w.zh] = {ok:0, bad:0}); if(ok) orr.ok++; else orr.bad++; }''')
rep('''    if(first) S.lesson.W.forEach(function(w){ if(!state.words[w.zh]) state.words[w.zh] = {b:1, d:addDays(today(), 1)}; });''',
    '''    if(first) S.lesson.W.forEach(function(w){ if(!state.words[w.zh]) state.words[w.zh] = {b:1, d:addDays(today(), 1)}; });
    applyResults(S.oldRes);''')

# Bauplan-Karte: wie Wortvorstellung ohne Antwort
rep('''  if(ex.type!=="intro" && !S.answered) return;''', '''  if(ex.type!=="intro" && ex.type!=="rule" && !S.answered) return;''')
rep('''  if(ex.type!=="intro" && ex.type!=="pairs" && !S.correct && !ex.retry){''', '''  if(ex.type!=="intro" && ex.type!=="rule" && ex.type!=="pairs" && !S.correct && !ex.retry){''')
rep('''    if(e.key==="Enter" && !onCtl){ e.preventDefault(); if(S.answered || ex.type==="intro") nextEx(); else if(ex.type==="build") checkBuild(); }''',
    '''    if(e.key==="Enter" && !onCtl){ e.preventDefault(); if(S.answered || ex.type==="intro" || ex.type==="rule") nextEx(); else if(ex.type==="build") checkBuild(); }''')
rep('''  if(f && (S.answered || ex.type==="intro")) f.focus({preventScroll:true});''', '''  if(f && (S.answered || ex.type==="intro" || ex.type==="rule")) f.focus({preventScroll:true});''')

# ================= Sitzung: Kopf mit Ort und Lektion =================
rep('''    brushBar(S.lastPct==null ? pct : S.lastPct, pct)+
    '<span class="s-pct">'+pct+' %</span></div>'+''', '''    '<div class="s-mid">'+sessCtx()+brushBar(S.lastPct==null ? pct : S.lastPct, pct)+'</div>'+
    '<span class="s-pct">'+pct+' %</span></div>'+''')
rep('''function kicker(seal, text){ return '<p class="kicker"><span class="seal" aria-hidden="true">'+seal+'</span>'+text+'</p>'; }''',
    '''function kicker(seal, text){ return '<p class="kicker"><span class="seal" aria-hidden="true">'+seal+'</span>'+text+'</p>'; }
function sessCtx(){
  if(S.kind==="lesson") return '<span class="s-ctx"><span class="s-place" lang="zh">'+esc(S.lesson.unit.place.zh)+'</span>Lektion '+S.lesson.n+' · '+esc(S.lesson.title)+'</span>';
  return '<span class="s-ctx"><span class="s-place" lang="zh">复</span>'+(S.kind==="review" ? "Wiederholen" : "Freies Üben")+'</span>';
}
function oldTag(ex){ return ex.old ? '<p class="oldtag"><span class="seal" aria-hidden="true">复</span>Wiederholung aus Lektion '+ex.w.lesson.n+' · '+esc(ex.w.lesson.title)+'</p>' : ''; }''')

# ================= Übungen anzeigen =================
rep('''function renderEx(ex){
  var w = ex.w, h = "";
  switch(ex.type){''', '''function renderEx(ex){
  var w = ex.w, h = oldTag(ex);
  switch(ex.type){
    case "rule":
      var pt = ex.p;
      h += '<article class="scroll"><div class="sc-rod" aria-hidden="true"></div><div class="sc-paper orn"><p class="sc-kick"><span class="seal" aria-hidden="true">法</span>Neuer Bauplan</p>'+
        '<h2 class="sc-title">'+hzText(pt.title)+'</h2>'+patternHTML(pt.ex[0].gs)+'<p class="sc-text">'+hzText(pt.text)+'</p>'+
        pt.ex.map(function(e){ return '<div class="sc-ex"><p class="sc-de"><span class="hz" lang="zh">'+esc(e.zh)+'</span> '+esc(e.de)+'</p>'+breakdownHTML(e.toks, e.gs)+'</div>'; }).join("")+
        '</div><div class="sc-rod" aria-hidden="true"></div></article>';
      break;''')
rep('''      h += kicker("新", "Neues Wort")+'<div class="center">'+zis(w.zh)+
        '<div class="big-py" style="margin-top:6px">'+pyHTML(w.py)+'</div><div class="big-de">'+esc(w.de)+'</div>'+''',
    '''      h += kicker("新", "Neues Wort")+'<div class="wordcard orn"><div class="center">'+zis(w.zh)+
        '<div class="big-py" style="margin-top:6px">'+pyHTML(w.py)+'</div><div class="big-de">'+esc(w.de)+'</div>'+
        (GR.wc && GR.wc[w.zh] ? '<span class="wc-tag">'+esc(GR.wc[w.zh])+'</span>' : '')+''')
rep('''        '<button type="button" class="iconbtn" data-act="sword" style="margin-top:4px">'+ICON_SPK+' Nochmal hören</button></div>';
      break;''', '''        '<button type="button" class="iconbtn" data-act="sword" style="margin-top:4px">'+ICON_SPK+' Nochmal hören</button></div></div>';
      break;''')
rep('''          return '<button type="button" class="tbtn'+cls+'" data-stone="'+k+'" style="--tc:var(--t'+k+')"'+(S.answered?" disabled":"")+'><span class="mk">'+TONE_MARK[k]+'</span><b>'+k+'. Ton</b><small>'+TONE_DESC[k]+'</small></button>';''',
    '''          return '<button type="button" class="tbtn'+cls+'" data-stone="'+k+'" style="--tc:var(--t'+k+')"'+(S.answered?" disabled":"")+'><span class="mk">'+TONE_MARK[k]+'</span>'+toneCurve(k)+'<b>'+k+'. Ton</b><small>'+TONE_DESC[k]+'</small></button>';''')
rep('''    return '<button type="button" class="tbtn'+cls+'" data-tone="'+k+'" style="--tc:var(--t'+k+')"'+(done?" disabled":"")+'><span class="mk">'+TONE_MARK[k]+'</span><b>'+k+'. Ton</b><small>'+TONE_DESC[k]+'</small></button>';''',
    '''    return '<button type="button" class="tbtn'+cls+'" data-tone="'+k+'" style="--tc:var(--t'+k+')"'+(done?" disabled":"")+'><span class="mk">'+TONE_MARK[k]+'</span>'+toneCurve(k)+'<b>'+k+'. Ton</b><small>'+TONE_DESC[k]+'</small></button>';''')
rep('''      h += kicker("句", "Bau den Satz auf Chinesisch")+'<p class="prompt">„'+esc(ex.s.de)+'“</p>'+''',
    '''      h += kicker("句", "Bau den Satz auf Chinesisch")+'<p class="prompt">„'+esc(ex.s.de)+'“</p>'+
        (ex.s.gs ? '<div class="bp-hint"><span class="bp-cap">Bauplan</span>'+patternHTML(ex.s.gs)+'</div>' : '')+''')
rep('''        '<div class="bank">'+ex.bank.map(function(t, i){ var used = ex.built.indexOf(i)>=0;
          return '<button type="button" class="tok'+(used?" used":"")+'" data-bank="'+i+'"'+(used||S.answered?" disabled":"")+'><span class="thz" lang="zh">'+esc(t.zh)+'</span>'+pyBlock(t.py, "tpy")+'</button>'; }).join("")+'</div>';
      break;''', '''        '<div class="bank">'+ex.bank.map(function(t, i){ var used = ex.built.indexOf(i)>=0;
          return '<button type="button" class="tok'+(used?" used":"")+'" data-bank="'+i+'"'+(used||S.answered?" disabled":"")+'><span class="thz" lang="zh">'+esc(t.zh)+'</span>'+pyBlock(t.py, "tpy")+'</button>'; }).join("")+'</div>';
      if(S.answered && ex.s.gs) h += '<div class="satzbox"><p class="sb-cap">So ist der Satz gebaut</p>'+breakdownHTML(ex.s.toks, ex.s.gs, ex.s.why)+'</div>';
      break;''')
rep('''        '<div class="opts">'+ex.opts.map(function(o, i){ return '<button type="button" class="opt'+optCls(i, o===ex.s)+'" data-opt="'+i+'"'+(S.answered?" disabled":"")+'><span class="k">'+(i+1)+'</span>'+esc(o.de)+'</button>'; }).join("")+'</div>';
      break;''', '''        '<div class="opts">'+ex.opts.map(function(o, i){ return '<button type="button" class="opt'+optCls(i, o===ex.s)+'" data-opt="'+i+'"'+(S.answered?" disabled":"")+'><span class="k">'+(i+1)+'</span>'+esc(o.de)+'</button>'; }).join("")+'</div>';
      if(S.answered && ex.s.gs) h += '<div class="satzbox"><p class="sb-cap">So ist der Satz gebaut</p>'+breakdownHTML(ex.s.toks, ex.s.gs, ex.s.why)+'</div>';
      break;''')
rep('''  if(ex.type==="intro") return '<div class="s-foot"><div class="s-foot-in"><span class="s-hint">Hör gut zu und sprich das Wort laut nach.</span>'+btnNext+'</div></div>';''',
    '''  if(ex.type==="intro") return '<div class="s-foot"><div class="s-foot-in"><span class="s-hint">Hör gut zu und sprich das Wort laut nach.</span>'+btnNext+'</div></div>';
  if(ex.type==="rule") return '<div class="s-foot"><div class="s-foot-in"><span class="s-hint">Tipp auf ein Wort, um es zu hören. Alle Baupläne findest du später unter Sätze.</span>'+btnNext+'</div></div>';''')

# ================= Abschluss: welche alten Wörter wiederholt wurden =================
rep('''  } else if(S.kind==="lesson"){
    h += '<h1>Lektion '+S.lesson.n+' geschafft!</h1><p class="muted" style="margin:0">'+(S.first ? "Diese Wörter kommen ab morgen beim Wiederholen dran:" : "Deine Wörter aus dieser Lektion:")+'</p>';
    h += '<div class="learned">'+S.lesson.W.map(function(w){ return '<button type="button" class="tok" data-word="'+esc(w.zh)+'"><span class="thz" lang="zh">'+esc(w.zh)+'</span><span class="tpy">'+pyHTML(w.py)+'</span></button>'; }).join("")+'</div>';
  } else''', '''  } else if(S.kind==="lesson"){
    h += '<h1>Lektion '+S.lesson.n+' geschafft!</h1><p class="muted" style="margin:0">'+(S.first ? "Diese Wörter kommen in den nächsten Lektionen und ab morgen beim Wiederholen wieder:" : "Deine Wörter aus dieser Lektion:")+'</p>';
    h += '<div class="learned">'+S.lesson.W.map(function(w){ return '<button type="button" class="tok" data-word="'+esc(w.zh)+'"><span class="thz" lang="zh">'+esc(w.zh)+'</span><span class="tpy">'+pyHTML(w.py)+'</span></button>'; }).join("")+'</div>';
  } else''')
rep('''  h += '<div class="stats"><div class="card stat"><b>'+f.pct+' %</b><span>auf Anhieb richtig</span></div>''', '''  var oldK = S.kind==="lesson" ? Object.keys(S.oldRes||{}) : [];
  if(oldK.length){
    h += '<div class="oldsum"><p class="muted" style="margin:0 0 6px">Aus früheren Lektionen wiederholt:</p><div class="rr-words">'+oldK.map(function(zh){ var w = WORD[zh], ok = S.oldRes[zh].bad===0;
      return '<button type="button" class="rr-w'+(ok ? "" : " bad")+'" data-word="'+esc(zh)+'"><span class="m">'+(ok ? "✓" : "✗")+'</span><span class="hz" lang="zh">'+esc(zh)+'</span><span>'+pyHTML(w.py)+'</span></button>'; }).join("")+'</div>'+
      (oldK.some(function(zh){ return S.oldRes[zh].bad; }) ? '<p class="muted" style="font-size:13.5px; margin:6px 0 0">Die Wörter mit ✗ kommen heute beim Wiederholen nochmal dran.</p>' : '')+'</div>';
  }
  h += '<div class="stats"><div class="card stat"><b>'+f.pct+' %</b><span>auf Anhieb richtig</span></div>''')

# ================= Wiederholen: Karteikasten =================
rep('''    '<div class="tiles3"><div class="card stat"><b>'+due.length+'</b><span>heute fällig</span></div><div class="card stat"><b>'+learned.length+'</b><span>gelernt</span></div><div class="card stat"><b>'+sure+'</b><span>sitzen sicher</span></div></div>';''',
    '''    kastenHTML(learned)+
    '<p class="kasten-sum"><b>'+due.length+'</b> heute fällig · <b>'+learned.length+'</b> gelernt · <b>'+sure+'</b> sitzen sicher</p>';''')
rep('''    '<p class="subtitle">Gelernte Wörter kommen nach 1, 3, 7, 14 und 30 Tagen wieder dran. Was du nicht weißt, kommt am selben Tag nochmal.</p>'+''',
    '''    '<p class="subtitle">Jedes Wort liegt in einem Fach deines Karteikastens. Weißt du es, rückt es ein Fach weiter und kommt erst später wieder: nach 1, 3, 7, 14 und 30 Tagen. Weißt du es nicht, rutscht es zurück und kommt am selben Tag nochmal.</p>'+''')
rep('''/* ================= Wiederholen ================= */
var revFilter = "alle";''', '''/* ================= Wiederholen ================= */
var revFilter = "alle";
function kastenHTML(learned){
  var cnt = [0,0,0,0,0,0], lab = ["heute nochmal","nach 1 Tag","nach 3 Tagen","nach 7 Tagen","nach 14 Tagen","nach 30 Tagen"];
  learned.forEach(function(w){ var r = state.words[w.zh]; cnt[Math.max(0, Math.min(5, r.b||0))]++; });
  return '<div class="kasten" role="img" aria-label="Karteikasten: '+cnt.map(function(n, b){ return "Fach "+b+": "+n; }).join(", ")+'">'+cnt.map(function(n, b){
    var stack = ""; for(var i=0;i<Math.min(8, n);i++) stack += '<i style="--i:'+i+'"></i>';
    return '<div class="fach'+(n ? "" : " leer")+'"><div class="stack" aria-hidden="true">'+stack+'</div><b>'+n+'</b><span>Fach '+b+'</span><small>'+lab[b]+'</small></div>';
  }).join("")+'</div>';
}''')

# ================= Reisesätze: Zerlegung und Baupläne =================
rep('''      h += '<div class="words" role="group" aria-label="Einzelne Wörter anhören">'+chunksOf(c).map(function(ch, i){
        var ok = aok && !!clipsFor(ch);
        return '<button type="button" class="wchip" data-chunk="'+i+'"'+(ok ? '' : ' disabled title="Keine Aufnahme"')+'><span class="whz" lang="zh">'+esc(ch.zh)+'</span><span class="wpy">'+pyHTML(ch.py)+'</span></button>';
      }).join("")+'</div>';''', '''      var cg = GR.cards && GR.cards[c.id];
      if(cg) h += '<div class="satzbox in-card"><p class="sb-cap">So ist der Satz gebaut</p>'+breakdownHTML(chunksOf(c), parseG(cg.g), cg.n, function(i){ return 'data-chunk="'+i+'"'; })+'</div>';
      else h += '<div class="words" role="group" aria-label="Einzelne Wörter anhören">'+chunksOf(c).map(function(ch, i){
        var ok = aok && !!clipsFor(ch);
        return '<button type="button" class="wchip" data-chunk="'+i+'"'+(ok ? '' : ' disabled title="Keine Aufnahme"')+'><span class="whz" lang="zh">'+esc(ch.zh)+'</span><span class="wpy">'+pyHTML(ch.py)+'</span></button>';
      }).join("")+'</div>';''')
rep('''function renderCards(){
  var p = state.prefs;''', '''function renderCards(){
  var p = state.prefs, sm = p.smode==="plans" ? "plans" : "cards";
  $("#smode").innerHTML = [["cards","Reisesätze"],["plans","Baupläne"]].map(function(m){ return '<button type="button" data-smode="'+m[0]+'" aria-pressed="'+(sm===m[0])+'">'+m[1]+'</button>'; }).join("");
  $("#cards-wrap").hidden = sm!=="cards"; $("#plans").hidden = sm!=="plans";
  if(sm==="plans"){ renderPlans(); return; }''')
rep('''function renderList(){''', r'''/* Alle Baupläne: gelernte ausklappbar, kommende gesperrt */
function renderPlans(){
  var got = POINTS.filter(function(pt){ return isDone(pt.lesson); }), last = got[got.length-1];
  var h = '<div class="card legend-card"><p class="lg-cap">Die Farben zeigen die Satzteile</p><div class="legend">'+Object.keys(SLOT).map(function(k){ return '<span class="bp s-'+k+'"><b>'+SLOT[k][0]+'</b><small>'+SLOT[k][1]+'</small></span>'; }).join("")+'</div>'+
    '<p class="muted" style="margin:10px 0 0; font-size:14px">'+got.length+' von '+POINTS.length+' Bauplänen gelernt. Neue kommen mit den Lektionen dazu.</p></div>';
  h += POINTS.map(function(pt){
    if(!isDone(pt.lesson)) return '<div class="plan locked"><span class="pl-n">L'+pt.lesson.n+'</span><b>'+hzText(pt.title)+'</b><small>kommt in Lektion '+pt.lesson.n+'</small></div>';
    return '<details class="plan"'+(pt===last ? ' open' : '')+'><summary><span class="pl-n">L'+pt.lesson.n+'</span><b>'+hzText(pt.title)+'</b><span class="pl-chev" aria-hidden="true">›</span></summary><div class="pl-body">'+patternHTML(pt.ex[0].gs)+
      '<p>'+hzText(pt.text)+'</p>'+pt.ex.map(function(e){ return '<div class="sc-ex"><p class="sc-de"><span class="hz" lang="zh">'+esc(e.zh)+'</span> '+esc(e.de)+'</p>'+breakdownHTML(e.toks, e.gs)+'</div>'; }).join("")+'</div></details>';
  }).join("");
  $("#plans").innerHTML = h;
}
function renderList(){''')

# ================= Bedienung =================
rep('''  var el = e.target.closest("[data-node],[data-act],''', '''  var el = e.target.closest("[data-say],[data-smode],[data-node],[data-act],''')
rep('''  var ds = el.dataset;
  if(ds.node){''', '''  var ds = el.dataset;
  if(ds.say){ var sp = ds.say.split("|"); playWord({zh:sp[0], py:sp[1], syls:sp[1].split("_")}); return; }
  if(ds.smode){ if(state.prefs.smode!==ds.smode){ state.prefs.smode = ds.smode; touch(); renderCards(); } return; }
  if(ds.node){''')
rep('''  if(ds.chunk!==undefined){ if(current) playClips(clipsFor(chunksOf(current)[+ds.chunk])); return; }''',
    '''  if(ds.chunk!==undefined){ if(current){ var chk = chunksOf(current)[+ds.chunk], chc = clipsFor(chk); if(!chc || !playClips(chc)) speak(chk.zh); } return; }''')
rep('''  } else if(currentView==="saetze" && current){''', '''  } else if(currentView==="saetze" && current && state.prefs.smode!=="plans"){''')
open(p, "w", encoding="utf-8").write(s)

g = ROOT + "/zh-app/game.part.js"
t = open(g, encoding="utf-8").read()
a = '''  /* Ergebnisse mit Wiederholung und Punkten abgleichen */
  var t = today(), d = dayRec(), xp = G.ok + (won ? G.rival.bonus : 0);
  Object.keys(G.results).forEach(function(zh){
    var r = G.results[zh], rec = state.words[zh]; if(!rec) return;
    var ok = r.bad === 0;
    if(rec.d <= t){ if(ok){ var b = Math.min(5, (rec.b||0) + 1); state.words[zh] = {b:b, d:addDays(t, INTERVALS[b])}; } else state.words[zh] = {b:0, d:t}; }
    else if(!ok) state.words[zh] = {b:Math.max(0, (rec.b||0) - 1), d:t};
  });'''
assert t.count(a) == 1
t = t.replace(a, '''  /* Ergebnisse mit Wiederholung und Punkten abgleichen */
  var d = dayRec(), xp = G.ok + (won ? G.rival.bonus : 0);
  applyResults(G.results);''')
a = '''<span class="mk">'+TONE_MARK[k]+'</span><small>'+k+'. Ton</small></button>'; }).join("")+'</div>';'''
assert t.count(a) == 1
t = t.replace(a, '''<span class="mk">'+TONE_MARK[k]+'</span>'+toneCurve(k)+'<small>'+k+'. Ton</small></button>'; }).join("")+'</div>';''')
open(g, "w", encoding="utf-8").write(t)

b = ROOT + "/scripts/build_page.py"
x = open(b, encoding="utf-8").read()
x = x.replace('护照到了市北京上海龙舟赛胜输起点终开始旅程弗洛里安"', '护照到了市北京上海龙舟赛胜输起点终开始旅程弗洛里安法理"')
if "ZH_GRAMMAR" not in x:
    x = x.replace('''out = out.replace("<!--ZH_DATA-->", data.rstrip()).replace("<!--ZH_LESSONS-->", lessons.rstrip())''',
                  '''out = out.replace("<!--ZH_DATA-->", data.rstrip()).replace("<!--ZH_LESSONS-->", lessons.rstrip())
out = out.replace("<!--ZH_GRAMMAR-->", open(d+"/grammar.data.js", encoding="utf-8").read().rstrip())
assert "<!--ZH_GRAMMAR-->" not in out''')
x = x.replace('addDays:addDays};window.__t_next=gameNextQ;")', 'addDays:addDays,POINTS:POINTS,POINT:POINT,buildLesson:buildLesson,GR:GR};window.__t_next=gameNextQ;")')
open(b, "w", encoding="utf-8").write(x)
print("ok")
