import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
p = ROOT + "/zh-app/index.src.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:100])
    s = s.replace(a, b)

# ---------- renderLearn neu ----------
a = s.index("function renderLearn(){"); b = s.index("/* Route zwischen den Lektions-Punkten zeichnen */")
learn = r'''var BIRDS_SVG = '<svg class="birds" viewBox="0 0 70 30" aria-hidden="true"><path d="M2 14 q5 -6 10 0 q5 -6 10 0" fill="none" stroke="#2a2520" stroke-width="1.6" stroke-linecap="round"/><path d="M26 6 q4 -5 8 0 q4 -5 8 0" fill="none" stroke="#2a2520" stroke-width="1.4" stroke-linecap="round"/><path d="M46 20 q3.5 -4 7 0 q3.5 -4 7 0" fill="none" stroke="#2a2520" stroke-width="1.3" stroke-linecap="round"/></svg>';
function heroCloud(style){ return '<svg class="cl" style="'+style+'" viewBox="0 0 64 28" aria-hidden="true"><path d="M6 22 C0 22 0 13 7 13 C7 5 18 3 21 10 C24 2 38 2 39 11 C44 6 54 8 52 16 C60 16 62 24 54 24 Z" fill="currentColor" stroke="#b9a582" stroke-width="1.3" stroke-linejoin="round"/><path d="M21 10 C24 13 22 18 18 17 M39 11 C40 15 37 18 34 17" fill="none" stroke="#b9a582" stroke-width="1.2" stroke-linecap="round"/></svg>'; }
function viewBanner(scene, zh, de, id){
  return '<header class="vbanner"><div class="vb-art">'+sceneSVG(scene)+'</div><div class="vb-text"><span class="brush" aria-hidden="true">'+zh+'</span><h1 id="'+id+'">'+esc(de)+'</h1></div></header>';
}
function renderLearn(){
  var d = dayGet(), goal = state.prefs.goal, nx = nextLesson(), due = dueWords().length, learned = learnedWords().length;
  var doneL = LESSONS.filter(isDone).length, curU = UNITS.findIndex(function(u){ return !unitDone(u); });
  if(openAuto) openLesson = nx ? nx.id : "";
  /* Titelbild: die nächste Etappe als Tuschebild */
  var pl = nx ? nx.unit.place : UNITS[UNITS.length-1].place, scene = nx ? pl.scene : "water";
  var h = '<header class="hero" id="hero"><div class="hero-art" id="hero-art">'+sceneSVG(scene)+'</div>'+
    heroCloud("top:16%; animation-duration:46s; animation-delay:-12s")+heroCloud("top:31%; width:92px; animation-duration:64s; animation-delay:-40s; opacity:.8")+BIRDS_SVG+
    '<div class="hero-ink"><h1 class="hero-hello" id="h-lernen"><span lang="zh">你好</span><span class="sr">, Florian</span></h1><span class="name-seal" lang="zh" title="Florian auf Chinesisch: Fúluòlǐ’ān" aria-hidden="true">弗洛里安</span></div>'+
    '<span class="hero-date">'+esc(new Date().toLocaleDateString("de-DE", {weekday:"long", day:"numeric", month:"long"}))+'</span>';
  var mini = '<div class="mini-route" aria-hidden="true">'+UNITS.map(function(u, i){
    var dn = u.lessons.filter(isDone).length;
    return unitDone(u) ? '<i class="on"></i>' : i===curU ? '<i class="cur" style="--p:'+Math.round(100*dn/u.lessons.length)+'%"></i>' : '<i></i>';
  }).join("")+'</div>';
  if(nx){
    h += '<div class="hero-ribbon"><div><span class="hr-step">Etappe '+(curU+1)+' von '+UNITS.length+' · Lektion '+nx.n+' von '+LESSONS.length+'</span>'+
      '<b class="hr-name"><span class="brush" lang="zh">'+esc(pl.zh)+'</span> '+esc(pl.de)+'</b>'+mini+'</div>'+
      '<button type="button" class="btn red hr-go" data-lesson="'+nx.id+'">'+(doneL ? "Weiter mit Lektion "+nx.n : "Erste Lektion starten")+'<small>'+esc(nx.title)+'</small></button></div>';
  } else {
    h += '<div class="hero-ribbon"><div><span class="hr-step">Alle '+UNITS.length+' Etappen geschafft</span><b class="hr-name"><span class="brush" lang="zh">到了</span> Angekommen in Shanghai</b>'+mini+'</div>'+
      (due ? '<button type="button" class="btn red hr-go" data-act="review">Wiederholen<small>'+plural(due, "Wort", "Wörter")+' fällig</small></button>' : '<a class="btn red hr-go" href="#spiel">Zum Rennen<small>Wörter im Drachenboot üben</small></a>')+'</div>';
  }
  h += '</header>';
  /* Tageswerte in einer Zeile */
  h += '<div class="statline"><span><span class="seal" aria-hidden="true">火</span><b>'+plural(streakInfo().count, "Tag", "Tage")+'</b> in Folge</span>'+
    '<span><span class="seal" style="background:var(--gold)" aria-hidden="true">今</span><b>'+Math.min(d.xp, goal)+' / '+goal+'</b> Punkte heute</span>'+
    '<span><span class="seal" style="background:var(--ink);color:var(--paper)" aria-hidden="true">词</span><b>'+learned+' / '+WORDS.length+'</b> Wörter</span></div>';
  /* Kacheln: Wiederholen und Spiel */
  var ready = gameReady();
  h += '<div class="tiles2">'+
    (due ? '<button type="button" class="tile tile-rev" data-act="review">' : '<a class="tile tile-rev" href="#wiederholen">')+
      '<span class="big" aria-hidden="true">复</span><span class="count">'+due+'<em>'+(due===1 ? "Wort" : "Wörter")+'</em></span>'+
      '<b>'+(due ? "Jetzt wiederholen" : learned ? "Alles wiederholt" : "Noch nichts zu wiederholen")+'</b><small>'+(due ? "Dauert ein paar Minuten" : learned ? "Neue Wörter kommen in den nächsten Tagen" : "Nach der ersten Lektion geht's los")+'</small>'+
    (due ? '</button>' : '</a>')+
    '<a class="tile tile-game" href="#spiel" id="tile-game"><canvas id="tile-canvas" aria-hidden="true"></canvas><span class="tz" lang="zh" aria-hidden="true">龙舟赛</span><b>Drachenboot-Rennen</b><small>'+(ready ? "Deine Wörter gegen die Uhr" : "Ab 4 gelernten Wörtern")+'</small></a></div>';
  /* Reisepass als aufgeschlagenes Heft */
  var got = UNITS.filter(unitDone).length;
  var stamp = function(u, i){
    var ok = unitDone(u), r = (rng(i*31+7)()*16-8).toFixed(1);
    return '<div class="stamp '+(ok ? "got" : "open")+(i%2 ? " sq" : "")+'" style="--r:'+r+'deg" title="'+esc(u.place.de)+'"><span class="sz" lang="zh">'+esc(u.place.zh)+'</span><small>'+(ok ? shortDate(unitDate(u)) : esc(u.place.de.replace(/^(Ankunft in|In den|An der|Im|Auf dem|Mit dem|Am)\s+/, "")))+'</small></div>';
  };
  h += '<section class="booklet" aria-label="Reisepass"><div class="bk-head"><b><span class="brush" lang="zh">护照</span>Reisepass</b><span class="muted" style="font-size:13.5px">'+got+' von '+UNITS.length+' Stempeln</span></div>'+
    '<div class="bk"><div class="bk-page" data-wm="护">'+UNITS.slice(0, 4).map(stamp).join("")+'</div><div class="bk-page" data-wm="照">'+UNITS.slice(4).map(function(u, i){ return stamp(u, i+4); }).join("")+'</div></div></section>';
  /* Lernpfad */
  h += '<div class="journey-head"><span class="brush" lang="zh" aria-hidden="true">旅程</span><div><h2>Deine Reise: Peking → Shanghai</h2><p>'+doneL+' von '+LESSONS.length+' Lektionen'+(curU<0 ? ' · alle Etappen geschafft' : ' · Etappe '+(curU+1)+' von '+UNITS.length)+'</p></div></div>';
  var cur = nx ? nx.n : LESSONS.length + 1, gi = 0;
  h += '<div class="trail" id="trail"><svg class="route" id="route" aria-hidden="true"></svg>';
  UNITS.forEach(function(u, ui){
    var dn = u.lessons.filter(isDone).length, up = u.place;
    h += '<section class="stage2" aria-label="Etappe '+(ui+1)+': '+esc(up.de)+'"><div class="st-art">'+sceneSVG(up.scene)+'</div><span class="st-vname" lang="zh" aria-hidden="true">'+esc(up.zh)+'</span>'+(unitDone(u) ? '<span class="st-done" title="Etappe geschafft">到</span>' : '')+
      '<div class="st-info"><span class="st-num">Etappe '+(ui+1)+' · '+esc(u.title)+'</span><h3>'+esc(up.de)+' <span class="hz" lang="zh" style="font-size:.8em; color:var(--muted)">'+esc(up.zh)+'</span></h3><p>'+esc(up.text)+'</p><span class="st-prog">'+dn+' / '+u.lessons.length+' Lektionen</span></div></section>';
    u.lessons.forEach(function(l){
      var x = ROW_X[gi % ROW_X.length], side = x.charAt(0)==="-" || x==="0%" ? "r" : "l"; gi++;
      var done = isDone(l), isCur = l.n===cur, locked = l.n>cur, open = openLesson===l.id && !locked;
      var cls = done ? "done" : isCur ? "current" : "locked";
      h += '<div class="nrow" style="--x:'+x+'">'+(x==="0%" ? cloud("cloud") .replace('class="cloud"', 'class="cloud" style="left:6%"') : '')+
        '<button type="button" class="node '+cls+(open ? " open" : "")+'" data-node="'+l.id+'" style="--d:'+(gi*0.04).toFixed(2)+'s"'+(locked ? ' disabled aria-disabled="true"' : '')+' aria-label="Lektion '+l.n+': '+esc(l.title)+(done ? ", geschafft" : locked ? ", gesperrt" : "")+'" aria-expanded="'+open+'">'+
        (isCur && !open ? '<span class="go">Start</span>' : '')+'<span class="cn">'+cnNum(l.n)+'</span><small class="an">'+l.n+'</small></button>'+
        '<span class="nlabel '+side+'"><small>Lektion '+l.n+(done ? " · geschafft" : locked ? " · gesperrt" : "")+'</small><b>'+esc(l.title)+'</b><span class="hz" lang="zh">'+l.W.map(function(w){ return esc(w.zh); }).join(" · ")+'</span></span></div>';
      if(open){
        var best = (state.learn.done[l.id]||{}).best;
        h += '<div class="card lpop" style="--x:'+x+'"><h4>Lektion '+l.n+': '+esc(l.title)+'</h4><div class="wl">'+
          l.W.map(function(w){ return '<button type="button" data-word="'+esc(w.zh)+'"><span class="hz" lang="zh">'+esc(w.zh)+'</span><span><span style="font-size:13px; font-weight:600">'+pyHTML(w.py)+'</span> <span class="de">'+esc(w.de.split(/[,(]/)[0].trim())+'</span></span></button>'; }).join("")+'</div>'+
          '<div class="pop-actions">'+(done ? '<button type="button" class="btn light" data-lesson="'+l.id+'">Nochmal üben</button><span class="muted" style="font-size:13.5px">Bestes Ergebnis: '+best+' % auf Anhieb</span>' : '<button type="button" class="btn red" data-lesson="'+l.id+'">Lektion starten</button><span class="muted" style="font-size:13.5px">'+l.W.length+' neue Wörter'+(l.S.length ? ", "+plural(l.S.length, "Satz", "Sätze") : "")+'</span>')+'</div></div>';
      }
    });
  });
  h += '</div>';
  h += '<footer class="credits">Aufnahmen von Muttersprachlerinnen: Silben gesprochen von Chen Wang, Wörter von Yue Tan, aus dem Projekt <a href="https://github.com/hugolpz/audio-cmn">audio-cmn</a> (Lizenz CC BY-SA).</footer>';
  $("#view-lernen").innerHTML = h;
  drawRoute();
  drawTile(1000);
  heroParallax();
}
/* Kachel mit einem Standbild des Rennens; bei Mausberührung fahren die Boote los */
var tileRaf = 0;
function drawTile(t){
  var cv = $("#tile-canvas"); if(!cv || !cv.clientWidth) return;
  var s = sizeCanvas(cv), me = 9 + Math.sin(t/1400)*1.5;
  drawRace(s.c, s.W, s.H, {me:me, opp:10.5 + Math.sin(t/1700 + 1)*1.5, cam:me/100*WORLD - s.W*0.42, rival:RIVALS[1], parts:[], phase:t*0.004}, t);
}
document.addEventListener("mouseover", function(e){
  var tile = e.target.closest && e.target.closest("#tile-game"); if(!tile || tileRaf || reducedMotion()) return;
  (function fr(t){ if(!$("#tile-game") || !$("#tile-game").matches(":hover")){ tileRaf = 0; return; } drawTile(t); tileRaf = requestAnimationFrame(fr); })(performance.now());
});
/* Titelbild bewegt sich beim Scrollen langsamer als die Seite */
var heroTick = false;
function heroParallax(){
  var art = $("#hero-art"); if(!art) return;
  var y = window.scrollY || 0;
  art.style.transform = y < 700 && !reducedMotion() ? "translateY("+(y*0.32).toFixed(1)+"px)" : "";
}
window.addEventListener("scroll", function(){
  if(heroTick || currentView!=="lernen" || S || G) return;
  heroTick = true; requestAnimationFrame(function(){ heroTick = false; heroParallax(); });
}, {passive:true});
'''
s = s[:a] + learn + s[b:]

# Route: Text der Etappen bekommt einen Papierhof
rep(".st-info{text-align:center; margin-top:-4px; padding:0 8px}",
    ".st-info{position:relative; width:fit-content; max-width:100%; margin:-4px auto 0; text-align:center; padding:4px 14px 6px; border-radius:16px; background:var(--paper); box-shadow:0 0 18px 14px var(--paper)}")
rep(".tile-game::after{content:\"\"; position:absolute; inset:45% 0 0 0; background:linear-gradient(to bottom, rgba(233,220,192,0), rgba(246,239,224,.96) 62%)}",
    ".tile-game{justify-content:flex-start}\n.tile-game::after{content:\"\"; position:absolute; inset:0 0 42% 0; background:linear-gradient(to bottom, rgba(246,239,224,.94) 30%, rgba(246,239,224,0))}")
# Hilfsklasse für Screenreader
if ".sr{" not in s:
    rep("[hidden]{display:none !important}", "[hidden]{display:none !important}\n.sr{position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap}")

# ---------- Wiederholen und Einstellungen mit Bannerbild ----------
rep('''  var h = '<h1 class="title" id="h-wdh"><span class="brush">复习</span> Wiederholen</h1>'+''',
    '''  var h = viewBanner("tea", "复习", "Wiederholen", "h-wdh")+''')
rep('''  var h = '<h1 class="title" id="h-set"><span class="brush">设置</span> Einstellungen</h1><p class="subtitle">''',
    '''  var h = viewBanner("water", "设置", "Einstellungen", "h-set")+'<p class="subtitle">''')

# ---------- Fortschritt als Pinselstrich ----------
rep('''    '<div class="pbar" role="progressbar" aria-label="Fortschritt" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+pct+'"><i style="width:'+pct+'%"></i></div>'+''',
    '''    brushBar(S.lastPct==null ? pct : S.lastPct, pct)+''')
rep('''  var f = $("#s-next") || $("#s-check");
  if(f && (S.answered || ex.type==="intro")) f.focus({preventScroll:true});
}''', '''  var f = $("#s-next") || $("#s-check");
  if(f && (S.answered || ex.type==="intro")) f.focus({preventScroll:true});
  var pf = $("#pb-fill");
  if(pf && S.lastPct!==pct){ pf.getBoundingClientRect(); requestAnimationFrame(function(){ pf.style.transform = "scaleX("+(pct/100)+")"; }); }
  S.lastPct = pct;
}
var BRUSH_D = "M4 9.5 C30 4 90 3.5 150 4.6 C210 5.6 262 3 292 5.4 C298.5 6.4 299.5 12 295 14 C270 17.6 200 15.6 150 16 C95 16.4 40 17.6 10 15.6 C3 15 1 12 4 9.5 Z";
function brushBar(from, pct){
  return '<svg class="pbrush" viewBox="0 0 300 20" preserveAspectRatio="none" role="progressbar" aria-label="Fortschritt" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+pct+'">'+
    '<defs><clipPath id="pb-clip"><path d="'+BRUSH_D+'"/></clipPath></defs><g clip-path="url(#pb-clip)"><rect width="300" height="20" fill="var(--paper-2)"/>'+
    '<rect class="fillrect" id="pb-fill" width="300" height="20" fill="var(--seal)" style="transform:scaleX('+(from/100)+')"/>'+
    '<path d="M0 8.2 H300 M0 12.6 H300" stroke="var(--paper)" stroke-width=".7" opacity=".35" stroke-dasharray="40 9 70 6 25 12"/></g></svg>';
}''')

# ---------- Tuschespritzer bei richtigen Antworten ----------
rep('''  chime(ok);
  renderSession();
  if(ex.type==="char") playWord(ex.w, 380);''', '''  chime(ok);
  renderSession();
  if(ok) burstOn($(".opt.right") || $(".tbtn.right") || $(".s-foot .seal"));
  if(ex.type==="char") playWord(ex.w, 380);''')
rep('''      chime(true);
    }
    renderSession();
  } else {''', '''      chime(true);
    }
    renderSession();
    burstOn(S.answered ? $(".s-foot .seal") : $('[data-p'+side+'="'+i+'"]'), S.answered ? null : ["#2f8a6a", "#c49a3e", "#1d1a16"], S.answered ? 30 : 14);
  } else {''')
rep('''    chime(allOk); touch(); renderToneStats(); renderNav();
  }
  renderTone();''', '''    chime(allOk); touch(); renderToneStats(); renderNav();
  }
  renderTone();
  if(tq.done && tq.picks.every(function(p, i){ return p===tq.item.tones[i]; })) burstOn($("#view-toene .zi"));''')
# alte Blütenfunktion entfernen (neue steckt in fx.part.js)
a = s.index("/* Fallende Pflaumenblüten zur Belohnung */"); b = s.index("function renderFinish(){")
s = s[:a] + s[b:]
rep(".petals{position:fixed; inset:0; pointer-events:none; z-index:60}\n", "")

# ---------- Tage: Rennen zählt als Üben ----------
rep("function active(ds){ var r = state.days[ds]; return !!(r && (r.tones>0 || r.cards>0 || r.xp>0)); }",
    "function active(ds){ var r = state.days[ds]; return !!(r && (r.tones>0 || r.cards>0 || r.xp>0 || r.games>0)); }")

# ---------- Bedienung: Spiel ----------
rep('''document.addEventListener("click", function(e){
  var el = e.target.closest(''', '''document.addEventListener("click", function(e){
  var gel = e.target.closest("[data-race],[data-gopt],[data-gact]");
  if(gel){ if(!gel.disabled) gameClick(gel); return; }
  var el = e.target.closest(''')
rep('''document.addEventListener("keydown", function(e){
  if(e.metaKey || e.ctrlKey || e.altKey) return;''', '''document.addEventListener("keydown", function(e){
  if(e.metaKey || e.ctrlKey || e.altKey) return;
  if(G){ gameKey(e); return; }''')

# ---------- Start: Bannerbilder und Seitenleisten-Bild ----------
rep('''document.body.insertAdjacentHTML("afterbegin", SVG_DEFS);''', '''document.body.insertAdjacentHTML("afterbegin", SVG_DEFS);
$$("[data-scene]").forEach(function(el){ el.innerHTML = sceneSVG(el.getAttribute("data-scene")); });
$("#side-art").innerHTML = '<svg viewBox="0 0 360 300" preserveAspectRatio="xMidYMax slice"><circle cx="262" cy="96" r="30" fill="#c23a2c" opacity=".9"/><circle cx="262" cy="96" r="44" fill="#c23a2c" opacity=".08"/>'+
  '<path d="'+ridge(17, 200, 70, 5, 0, 360).replace(/ 180/g, " 300")+'" fill="#3a342c" opacity=".55"/><path d="'+ridge(29, 236, 54, 6, 0, 360).replace(/ 180/g, " 300")+'" fill="#2a2520" opacity=".85"/>'+
  '<path d="'+ridge(43, 276, 38, 7, 0, 360).replace(/ 180/g, " 300")+'" fill="#0f0d0a"/>'+
  '<g fill="none" stroke="#a99f8c" stroke-width="1.3" stroke-linecap="round" opacity=".7"><path d="M70 70 q4 -4 8 0 q4 -4 8 0"/><path d="M94 58 q3 -3 6 0 q3 -3 6 0"/><path d="M84 84 q3 -3 6 0 q3 -3 6 0"/></g></svg>';''')
open(p, "w", encoding="utf-8").write(s)
print("Teil 2 ok")
