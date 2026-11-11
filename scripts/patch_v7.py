import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
p = ROOT + "/zh-app/index.src.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, count=1):
    global s
    n = s.count(a); assert n == count, (n, a[:110]); s = s.replace(a, b)

# ---------- Bausteine ----------
rep("/*SCENES*/\n/*FX*/\n", "/*SCENES*/\n/*FX*/\n/*PITCH*/\n")
rep('''conf:{}, days:{}, learn:{done:{}}, words:{}, game:{played:0, wins:{}, best:{}}, prefs:defaults()};''',
    '''conf:{}, days:{}, learn:{done:{}}, words:{}, err:{}, game:{played:0, wins:{}, best:{}}, prefs:defaults()};''')
rep('''learn:{done:(s.learn && s.learn.done) || {}}, words:s.words||{}, game:''', '''learn:{done:(s.learn && s.learn.done) || {}}, words:s.words||{}, err:s.err||{}, game:''')

# ---------- Fehlerheft: Ergebnisse je Wort ----------
rep('''function learnedWords(){''', '''/* Fehlerheft: wie oft ein Wort falsch war und wie oft danach richtig */
function noteResult(zh, ok){
  if(!zh || !WORD[zh]) return;
  var e = state.err[zh];
  if(ok){ if(e) e.ok = (e.ok||0) + 1; return; }
  state.err[zh] = {n:(e ? e.n||0 : 0) + 1, ok:0, last:today()};
}
function stumbles(){
  return Object.keys(state.err).filter(function(zh){ var e = state.err[zh]; return WORD[zh] && state.words[zh] && e.n > 0 && (e.ok||0) < 3; })
    .sort(function(a, b){ var x = state.err[a], y = state.err[b]; return (y.n - (y.ok||0)*0.5) - (x.n - (x.ok||0)*0.5) || (y.last > x.last ? 1 : -1); })
    .map(function(zh){ return WORD[zh]; });
}
function learnedWords(){''')
rep('''  if(ex.w) recordWord(ex.w, ok);''', '''  if(ex.w) recordWord(ex.w, ok);
  if(ex.w) noteResult(ex.w.zh, ok);''')
rep('''    ex.miss++; ex.missed[item.zh] = 1; ex.missed[other.zh] = 1;''', '''    ex.miss++; ex.missed[item.zh] = 1; ex.missed[other.zh] = 1; noteResult(item.zh, false); noteResult(other.zh, false);''')

# ---------- Tippen: Prüfung ----------
rep('''/* „Was hörst du?“ nur, wenn es eine Aufnahme genau dieses Worts gibt''', r'''/* ================= Tippen ================= */
var SYN = {"想":["要"], "要":["想"]};
/* Pinyin-Eingabe mit dem erwarteten Wort vergleichen: Silben, dann Töne (Zahl hinter der Silbe oder Tonzeichen) */
function matchPinyin(w, input){
  var s = input.toLowerCase().replace(/u:/g, "v"), letters = "", ev = [], bad = false;
  Array.from(s).forEach(function(c){
    if(/[a-z]/.test(c)){ letters += c; return; }
    if(c==="ü"){ letters += "v"; return; }
    if(/[0-5]/.test(c)){ ev.push({b:letters.length, t:(+c)%5}); return; }
    if(MARK[c]){ letters += BASE[c]; ev.push({i:letters.length-1, t:MARK[c]}); return; }
    if(/[\s'’\-·.,!?。，！？]/.test(c)) return;
    bad = true;
  });
  var syls = w.syls.map(function(x){ return x.replace(/[^\p{L}]/gu, ""); }), exp = syls.map(plainKey), tones = syls.map(toneOf), chars = Array.from(w.zh);
  if(bad || letters!==exp.join("")) return {ok:false, kind:"letters", syls:syls, tones:tones};
  var ends = [], acc = 0; exp.forEach(function(e){ acc += e.length; ends.push(acc); });
  var user = syls.map(function(){ return null; }), wrongPlace = false;
  ev.forEach(function(e){
    var k;
    if(e.b!==undefined){ k = ends.indexOf(e.b); if(k<0){ wrongPlace = true; return; } }
    else { k = 0; while(e.i >= ends[k]) k++; }
    if(user[k]!==null) wrongPlace = true; user[k] = e.t;
  });
  if(!ev.length && tones.some(function(t){ return t>0; })) return {ok:false, kind:"notones", syls:syls, tones:tones, user:user};
  var notes = [];
  var per = syls.map(function(sy, k){
    var e = tones[k], u = user[k], next = tones[k+1];
    if(e===0){ if(u) notes.push("neutral"); return true; }
    if(u===e) return true;
    if(e===3 && next===3 && u===2){ notes.push("33"); return true; }
    if(chars[k]==="不" && next===4 && u===2) return true;
    if(chars[k]==="一" && next!==undefined && (u===1 || u===2 || u===4)) return true;
    return false;
  });
  var ok = !wrongPlace && per.every(Boolean);
  return {ok:ok, kind:ok ? "ok" : (wrongPlace ? "place" : "tones"), syls:syls, tones:tones, user:user, per:per, notes:notes};
}
function checkTyped(w, raw){
  var input = (raw||"").normalize("NFC").trim();
  if(!input) return {ok:false, kind:"empty"};
  if(Array.from(input).some(isHan)){
    var han = Array.from(input).filter(isHan).join("");
    if(han===w.zh) return {ok:true, kind:"hz"};
    if((SYN[w.zh]||[]).indexOf(han)>=0) return {ok:true, kind:"hz", syn:han};
    return {ok:false, kind:"hzwrong", han:han};
  }
  var r = matchPinyin(w, input);
  if(!r.ok && r.kind==="letters"){
    var hit = (SYN[w.zh]||[]).filter(function(z){ return WORD[z] && matchPinyin(WORD[z], input).ok; })[0];
    if(hit) return {ok:true, kind:"ok", syn:hit, syls:r.syls, tones:r.tones};
  }
  return r;
}
function typedFeedback(ex){
  var w = ex.w, r = ex.res || {}, h = '<div class="w-res">';
  h += '<p class="w-you">Deine Antwort: <b>'+(ex.typed ? esc(ex.typed) : "–")+'</b></p>';
  if(r.syn) h += '<p class="w-note">Passt auch: <span class="hz" lang="zh">'+esc(r.syn)+'</span> '+pyHTML(WORD[r.syn].py)+' („'+esc(WORD[r.syn].de)+'“). Gesucht war <span class="hz" lang="zh">'+esc(w.zh)+'</span>.</p>';
  if(r.kind==="tones" || r.kind==="place"){
    h += '<div class="w-syls">'+r.syls.map(function(sy, k){ var ok = r.per && r.per[k], u = r.user[k];
      return '<span class="w-syl'+(ok ? " ok" : " bad")+'"><span class="py t'+toneOf(w.syls[k])+'">'+esc(w.syls[k].replace(/[^\p{L}]/gu, ""))+'</span><small>'+(ok ? "✓" : (u===null ? "Ton fehlt" : (u===0 ? "du: unbetont" : "du: "+u+". Ton")))+'</small></span>'; }).join("")+'</div>';
    if(r.kind==="place") h += '<p class="w-note">Die Tonzahl gehört direkt hinter ihre Silbe, zum Beispiel ni3hao3.</p>';
  }
  if(r.kind==="notones") h += '<p class="w-note">Die Silben stimmen, es fehlen nur die Töne. Schreib die Tonzahl hinter jede Silbe, zum Beispiel '+esc(r.syls.map(function(sy, k){ return plainKey(sy)+(r.tones[k]||""); }).join(""))+'.</p>';
  if(r.kind==="letters") h += '<p class="w-note">Die Silben stimmen noch nicht. Schau dir die Schreibweise unten genau an.</p>';
  if(r.kind==="hzwrong") h += '<p class="w-note">'+(WORD[r.han] ? 'Du hast <span class="hz" lang="zh">'+esc(r.han)+'</span> geschrieben, das heißt „'+esc(WORD[r.han].de)+'“.' : 'Diese Zeichen sind es nicht.')+'</p>';
  if(r.notes && r.notes.indexOf("33")>=0) h += '<p class="w-note">Gesprochen klingt der erste 3. Ton wie ein 2. Ton. Geschrieben wird er aber als 3. Ton: '+pyHTML(w.py)+'.</p>';
  if(r.notes && r.notes.indexOf("neutral")>=0) h += '<p class="w-note">Unbetonte Silben haben keinen Ton. Eine Zahl dort ist nicht falsch, aber nicht nötig.</p>';
  return h + '</div>';
}

/* „Was hörst du?“ nur, wenn es eine Aufnahme genau dieses Worts gibt''')

# Übungstyp „write“ in Lektionen, Wiederholen und als Wiederholung alter Wörter
rep('''  var ts = (canHear(w) ? ["hear","mean","char"] : ["mean","char"]).concat(canTone(w) ? ["tone"] : []);
  var pick = ts.filter(function(t){ return t!==lastOldType; });''', '''  var ts = (canHear(w) ? ["hear","mean","char","write"] : ["mean","char","write"]).concat(canTone(w) ? ["tone"] : []);
  var pick = ts.filter(function(t){ return t!==lastOldType; });''')
rep('''  var tw = W.filter(canTone);
  if(tw.length) ex.push(makeQuiz("tone", pickN(tw,1)[0], pool));
  /* Baupläne dieser Lektion''', '''  var tw = W.filter(canTone);
  if(tw.length) ex.push(makeQuiz("tone", pickN(tw,1)[0], pool));
  /* Zum Schluss zwei Wörter selbst schreiben: erst das Hervorholen macht sie fest */
  pickN(W, 2).forEach(function(w){ ex.push({id:++exSeq, type:"write", w:w}); });
  /* Baupläne dieser Lektion''')
rep('''function makeQuiz(type, w, pool){
  if(type==="hear" && !canHear(w)) type = "mean";
  var ex = {id:++exSeq, type:type, w:w};
  if(type==="tone") return ex;''', '''function makeQuiz(type, w, pool){
  if(type==="hear" && !canHear(w)) type = "mean";
  var ex = {id:++exSeq, type:type, w:w};
  if(type==="tone" || type==="write") return ex;''')
rep('''  var ex = [], types = ["mean","hear","char"], list = words.slice(0, 15);''', '''  var ex = [], types = ["mean","hear","char","write"], list = words.slice(0, 15);''')

# Anzeige
rep('''    case "rule":
      var pt = ex.p;''', '''    case "write":
      h += kicker("写", "Schreib es auf Chinesisch")+'<p class="prompt">„'+esc(w.de)+'“</p>'+
        '<div class="write"><input id="w-in" class="w-in'+(S.answered ? (S.correct ? " ok" : " bad") : "")+'" type="text" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" enterkeyhint="done" placeholder="z. B. ni3hao3 oder 你好" value="'+esc(ex.typed||"")+'" aria-label="Antwort auf Chinesisch"'+(S.answered ? " disabled" : "")+'>'+
        (S.answered ? '' : '<div class="w-tools"><span class="w-help">Pinyin mit Tonzahl hinter jeder Silbe, mit Tonzeichen oder direkt in Zeichen.</span><button type="button" class="iconbtn" data-act="giveup">Weiß ich nicht</button></div>')+'</div>'+
        (S.answered ? typedFeedback(ex)+'<div class="center" style="margin-top:12px">'+zis(w.zh)+'<div class="big-py">'+pyHTML(w.py)+'</div></div>' : '');
      break;
    case "rule":
      var pt = ex.p;''')
rep('''      h += kicker("新", "Neues Wort")+'<div class="wordcard orn"><div class="center">'+zis(w.zh)+
        '<div class="big-py" style="margin-top:6px">'+pyHTML(w.py)+'</div><div class="big-de">'+esc(w.de)+'</div>'+''',
    '''      h += kicker("新", "Neues Wort")+'<div class="wordcard orn"><div class="center">'+zis(w.zh)+
        '<div class="big-py" style="margin-top:6px">'+pyHTML(w.py)+'</div><div class="big-de">'+esc(w.de)+'</div>'+
        '<div class="melody" title="So läuft der Ton: oben hoch, unten tief">'+schemaSVG(w.syls)+'</div>'+''')
rep('''    var right = ex.type==="build" ? '<button type="button" class="btn ink" id="s-check" data-act="check"'+(ex.built.length?"":" disabled")+'>Prüfen <kbd>Enter</kbd></button>' : '';''',
    '''    var right = ex.type==="build" ? '<button type="button" class="btn ink" id="s-check" data-act="check"'+(ex.built.length?"":" disabled")+'>Prüfen <kbd>Enter</kbd></button>' :
      ex.type==="write" ? '<button type="button" class="btn ink" id="s-check" data-act="check">Prüfen <kbd>Enter</kbd></button>' : '';''')
rep('''      ex.type==="tone" ? "Tasten 1 bis 4 wählen den Ton, Leertaste spielt es nochmal ab." :''', '''      ex.type==="tone" ? "Tasten 1 bis 4 wählen den Ton, Leertaste spielt es nochmal ab." :
      ex.type==="write" ? "Zum Beispiel xie4xie, xièxie oder 谢谢. Unbetonte Silben ohne Zahl." :''')
# Fokus ins Eingabefeld
rep('''  var f = $("#s-next") || $("#s-check");
  if(f && (S.answered || ex.type==="intro" || ex.type==="rule")) f.focus({preventScroll:true});''', '''  var f = $("#s-next") || $("#s-check");
  if(f && (S.answered || ex.type==="intro" || ex.type==="rule")) f.focus({preventScroll:true});
  var wi = !S.answered && $("#w-in");
  if(wi){ wi.focus({preventScroll:true}); try{ wi.setSelectionRange(wi.value.length, wi.value.length); }catch(e){} }''')
# Prüfen
rep('''function checkBuild(){
  var ex = cur();''', '''function checkWrite(giveUp){
  var ex = cur();
  if(!ex || ex.type!=="write" || S.answered) return;
  var inp = $("#w-in"); if(inp) ex.typed = inp.value.trim();
  if(!giveUp && !ex.typed){ if(inp) inp.focus(); return; }
  ex.res = giveUp ? {ok:false, kind:"empty"} : checkTyped(ex.w, ex.typed);
  answer(!!ex.res.ok);
}
function checkBuild(){
  var ex = cur();
  if(ex && ex.type==="write"){ checkWrite(); return; }''')
rep('''  if(ex.type==="char") playWord(ex.w, 380);''', '''  if(ex.type==="char" || ex.type==="write") playWord(ex.w, 380);''')
rep('''if(ok) burstOn($("#session .opt.right") || $("#session .tbtn.right") || $("#session .s-foot .seal"));''',
    '''if(ok) burstOn($("#session .opt.right") || $("#session .tbtn.right") || $("#session .w-in") || $("#session .s-foot .seal"));''')
# Tasten: Enter im Eingabefeld prüft, Ziffern im Feld zählen nicht als Antwort-Tasten
rep('''  if(S && !(e.target.closest && e.target.closest("#session"))) onCtl = false;
  if(S){
    if(S.finished) return;
    var ex = cur();''', '''  if(S && !(e.target.closest && e.target.closest("#session"))) onCtl = false;
  if(S){
    if(S.finished) return;
    var ex = cur();
    if(e.target && e.target.id==="w-in"){ if(e.key==="Enter"){ e.preventDefault(); checkWrite(); } else if(e.key==="Escape"){ e.preventDefault(); $('[data-act="close"]').click(); } return; }''')
rep('''    case "check": checkBuild(); break;''', '''    case "check": checkBuild(); break;
    case "giveup": checkWrite(true); break;
    case "stumble": startReview(true, stumbles().slice(0, 10)); break;
    case "ownplay": playToneItem(); break;''')
# Eingabe merken, falls die Seite neu gezeichnet wird
rep('''document.addEventListener("change", function(e){''', '''document.addEventListener("input", function(e){ if(e.target && e.target.id==="w-in"){ var ex = cur(); if(ex) ex.typed = e.target.value; } });
document.addEventListener("change", function(e){
  if(e.target && e.target.id==="own-file" && e.target.files && e.target.files[0]){ ownAnalyze(e.target.files[0]); e.target.value = ""; return; }''')

# ---------- Freies Üben mit gewählten Wörtern (Stolpersteine) ----------
rep('''function startReview(practice){
  var pool = learnedWords();
  if(!pool.length) return;
  var words = practice ? pickN(pool, 10) : dueWords()''', '''function startReview(practice, chosen){
  var pool = learnedWords();
  if(!pool.length) return;
  var words = chosen && chosen.length ? chosen.slice() : practice ? pickN(pool, 10) : dueWords()''')

# ---------- Fehlerheft in Wiederholen ----------
rep('''  var F = [["alle","Alle"],["faellig","Fällig"],["neu","Frisch gelernt"],["sicher","Sitzen sicher"]];''', '''  var st = stumbles();
  if(st.length){
    h += '<h2 class="sec">Deine Stolpersteine</h2><p class="muted" style="margin:-4px 0 10px; font-size:14.5px">Wörter, bei denen du zuletzt danebenlagst. Nach dreimal richtig verschwinden sie von hier.</p>'+
      '<div class="stumbles">'+st.slice(0, 10).map(function(w){ var e = state.err[w.zh];
        return '<button type="button" class="stum" data-word="'+esc(w.zh)+'"><span class="hz" lang="zh">'+esc(w.zh)+'</span><span class="stum-t"><span>'+pyHTML(w.py)+'</span><small>'+esc(w.de.split(/[,(]/)[0].trim())+'</small></span><span class="stum-n" title="so oft falsch">'+e.n+'×</span><span class="stum-ok" aria-label="'+(e.ok||0)+' von 3 richtig">'+[0,1,2].map(function(i){ return '<i class="'+(i<(e.ok||0) ? "on" : "")+'"></i>'; }).join("")+'</span></button>'; }).join("")+'</div>'+
      '<div style="margin-top:12px"><button type="button" class="btn light" data-act="stumble">Stolpersteine üben</button></div>';
  }
  var F = [["alle","Alle"],["faellig","Fällig"],["neu","Frisch gelernt"],["sicher","Sitzen sicher"]];''')

# ---------- Töne: Tonverlauf nach der Antwort und eigene Aufnahme ----------
rep('''  $("#t-reveal").innerHTML = done
    ? '<div class="rv-py">'+pyHTML(item.py)+'</div><div class="muted">'+esc(item.de)+'</div>'
    : ''', '''  $("#t-reveal").innerHTML = done
    ? '<div class="rv-py">'+pyHTML(item.py)+'</div><div class="muted">'+esc(item.de)+'</div><div class="melody" id="t-mel">'+schemaSVG(item.syls)+'</div><p class="mel-leg" id="t-mel-leg"><span class="lg-s">Lehrbuch-Verlauf</span></p>'
    : ''')
rep('''  var d = dayGet();
  $("#t-today").textContent = d.tones ?''', '''  if(done) toneMeasured(item);
  renderOwn();
  var d = dayGet();
  $("#t-today").textContent = d.tones ?''')
rep('''function renderToneStats(){''', r'''/* Gemessene Kurve der Aufnahme (nur einzelne Silben, nur wenn sie klar zum Ton passt) */
function itemClip(it){ return it.tones.length===1 ? clip("s", numeric(it.py)) : null; }
function toneMeasured(it){
  var url = itemClip(it); if(!url) return;
  pitchOfClip(url, true).then(function(st){
    if(!tq || tq.item!==it || !tq.done || !shapeOk(st, it.tones[0], VOICE.s)) return;
    var m = $("#t-mel"); if(m) m.innerHTML = schemaSVG(it.syls, overlayPath(st, VOICE.s, "pc-native"));
    var lg = $("#t-mel-leg"); if(lg) lg.innerHTML = '<span class="lg-s">Lehrbuch-Verlauf</span><span class="lg-n">Aufnahme gemessen</span>';
  });
}
/* Eigene Aufnahme hochladen und mit der Muttersprachlerin vergleichen */
var own = null;
function renderOwn(){
  var box = $("#t-own"); if(!box || !tq) return;
  var it = tq.item, h = '<h3><span class="seal" aria-hidden="true">说</span>Deine Aussprache vergleichen</h3>';
  if(!tq.done){ box.innerHTML = h + '<p class="muted" style="margin:0">Wähl erst den Ton. Danach kannst du dich selbst aufnehmen und deine Tonkurve neben die der Sprecherin legen.</p>'; return; }
  h += '<p class="own-how">Nimm <span class="hz" lang="zh">'+esc(it.zh)+'</span> '+pyHTML(it.py)+' mit der Sprachmemo-App deines Handys auf, ruhig und nah am Mikrofon. Lade die Datei hier hoch. Sie bleibt auf deinem Gerät.</p>'+
    '<div class="own-row"><button type="button" class="iconbtn" data-act="ownplay">'+ICON_SPK+' Vorbild anhören</button><label class="btn red own-up"><input type="file" id="own-file" accept="audio/*,.m4a,.mp3,.wav,.ogg,.webm,.aac" hidden>Sprachmemo hochladen</label></div>';
  if(own && own.item===it){
    if(own.busy) h += '<p class="muted">Wird ausgewertet …</p>';
    else if(own.error) h += '<p class="w-note">'+esc(own.error)+'</p>';
    else h += '<div class="melody big">'+own.svg+'</div><p class="mel-leg"><span class="lg-s">Lehrbuch-Verlauf</span>'+(own.native ? '<span class="lg-n">Sprecherin</span>' : '')+'<span class="lg-u">du</span></p>'+(own.text ? '<p class="own-res">'+own.text+'</p>' : '')+
      '<p class="muted" style="font-size:13.5px; margin:6px 0 0">Deine Stimme ist anders hoch als die der Sprecherin. Darum zählt nur der Verlauf: bleibt gleich, steigt, fällt oder geht runter und wieder hoch.</p>';
  }
  box.innerHTML = h;
}
function ownAnalyze(file){
  if(!tq || !tq.done) return;
  var it = tq.item; own = {item:it, busy:true}; renderOwn();
  var single = it.tones.length===1;
  Promise.all([audioBufferOf(file), single ? pitchOfClip(itemClip(it), true) : Promise.resolve(null)]).then(function(r){
    var ab = r[0], nat = r[1];
    if(ab.duration > 12) throw new Error("long");
    var st = semis(yinTrack(ab.getChannelData(0), ab.sampleRate), single);
    if(!st.filter(function(v){ return v!==null; }).length) throw new Error("silent");
    var R = ownRange(st), natOk = single && shapeOk(nat, it.tones[0], VOICE.s);
    var extra = function(pad, top, bot, w){ return (natOk ? overlayPath(nat, VOICE.s, "pc-native")(pad, top, bot, w) : "") + overlayPath(st, R, "pc-own")(pad, top, bot, w); };
    var text = "";
    if(single){
      var dsc = describeOwn(st), want = it.tones[0];
      if(dsc && dsc.k) text = 'Deine Kurve '+dsc.de+'. '+(dsc.k===want ? '<b class="ok-t">Das passt zum '+want+'. Ton.</b>' : 'Der '+want+'. Ton '+({1:"bleibt hoch und gleich", 2:"steigt", 3:"geht tief runter und am Ende wieder hoch", 4:"fällt von oben nach unten"})[want]+'. Hör dir das Vorbild nochmal an und versuch es noch einmal.');
      else if(dsc) text = 'Deine Kurve ist nicht eindeutig. Sprich die Silbe etwas länger und deutlicher.';
    }
    own = {item:it, svg:schemaSVG(it.syls, extra, 300, 100), native:natOk, text:text};
    renderOwn();
  }).catch(function(e){
    own = {item:it, error: e && e.message==="long" ? "Die Aufnahme ist zu lang. Nimm nur das eine Wort auf (höchstens ein paar Sekunden)." : e && e.message==="silent" ? "In der Aufnahme war keine Stimme zu erkennen. Sprich lauter oder näher am Mikrofon." : "Diese Datei konnte nicht gelesen werden. Versuch es mit m4a, mp3 oder wav."};
    renderOwn();
  });
}
function renderToneStats(){''')
rep('''      <p class="muted" id="t-today" style="margin-top:12px"></p>''', '''      <p class="muted" id="t-today" style="margin-top:12px"></p>
      <div class="card own" id="t-own"></div>''')

# ---------- CSS ----------
rep("/* ---------- Wiederholen ---------- */", r'''/* ---------- Tippen ---------- */
.write{margin-top:6px}
.w-in{width:100%; font:inherit; font-size:24px; font-weight:600; padding:14px 16px; border-radius:14px; border:2px solid var(--line); border-bottom-width:4px; background:var(--sheet); color:var(--ink); outline:none; transition:border-color .15s}
.w-in:focus{border-color:var(--ink-2)}
.w-in.ok{border-color:var(--ok); background:var(--ok-bg)}
.w-in.bad{border-color:var(--bad); background:var(--bad-bg)}
.w-in::placeholder{color:var(--muted); font-weight:500; font-size:18px}
.w-tools{display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:8px 12px; margin-top:10px}
.w-help{font-size:14px; color:var(--muted); flex:1 1 220px}
.w-res{margin-top:12px}
.w-you{margin:0 0 6px; font-size:15px}
.w-note{margin:6px 0 0; font-size:14.5px; line-height:1.5; padding:8px 12px; border-radius:10px; background:var(--paper-2)}
.w-syls{display:flex; flex-wrap:wrap; gap:8px; margin-top:6px}
.w-syl{display:inline-flex; flex-direction:column; align-items:center; padding:6px 12px; border-radius:10px; background:var(--sheet); box-shadow:0 0 0 1.5px var(--line); font-size:18px; font-weight:700; line-height:1.2}
.w-syl small{font-size:11.5px; font-weight:700}
.w-syl.ok{box-shadow:0 0 0 1.5px var(--ok)} .w-syl.ok small{color:var(--ok)}
.w-syl.bad{box-shadow:0 0 0 1.5px var(--bad); background:var(--bad-bg)} .w-syl.bad small{color:var(--bad)}
/* ---------- Tonmelodie ---------- */
.melody{width:100%; max-width:260px; margin:4px auto 0}
.melody.big{max-width:360px}
.pcurve{display:block; width:100%; height:auto}
.pc-grid{stroke:var(--line); stroke-width:.7}
.sc-tone{fill:none; stroke-width:5; stroke-linecap:round; opacity:.85}
.sc-lbl{font:600 11px var(--body); fill:var(--muted)}
.pc-native{fill:none; stroke:var(--ink); stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; opacity:.75}
.pc-own{fill:none; stroke:var(--seal); stroke-width:2.6; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:6 4}
.mel-leg{display:flex; flex-wrap:wrap; justify-content:center; gap:4px 14px; margin:4px 0 0; font-size:12.5px; color:var(--muted)}
.mel-leg span{display:inline-flex; align-items:center; gap:6px}
.mel-leg span::before{content:""; width:18px; height:0; border-top:4px solid var(--t2); border-radius:2px; opacity:.85}
.mel-leg .lg-n::before{border-top:2px solid var(--ink); opacity:.75}
.mel-leg .lg-u::before{border-top:2.5px dashed var(--seal)}
.own{margin-top:16px; padding:16px 18px}
.own h3{display:flex; align-items:center; gap:10px; margin:0 0 8px; font-family:var(--display); font-weight:600; font-size:19px}
.own h3 .seal{width:28px; height:28px; font-size:18px; border-radius:7px}
.own-how{margin:0 0 10px; font-size:15px; line-height:1.5}
.own-how .hz{font-size:20px}
.own-row{display:flex; flex-wrap:wrap; gap:10px; align-items:center}
.own-up{cursor:pointer}
.own-res{margin:10px 0 0; font-size:15px; line-height:1.5}
.ok-t{color:var(--ok)}
/* ---------- Stolpersteine ---------- */
.stumbles{display:grid; grid-template-columns:repeat(auto-fill, minmax(230px, 1fr)); gap:8px}
.stum{display:flex; align-items:center; gap:10px; padding:8px 12px; border-radius:12px; border:0; background:var(--sheet) var(--texture); box-shadow:0 0 0 1px var(--line); cursor:pointer; text-align:left; font:inherit; color:var(--ink)}
.stum .hz{font-size:calc(26px * var(--hz-scale)); flex:none}
.stum-t{flex:1; min-width:0; display:flex; flex-direction:column; line-height:1.25}
.stum-t span{font-size:14px; font-weight:600}
.stum-t small{font-size:12.5px; color:var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
.stum-n{flex:none; font-weight:800; color:var(--bad); font-size:14px; font-variant-numeric:tabular-nums}
.stum-ok{display:flex; gap:3px} .stum-ok i{width:7px; height:7px; border-radius:50%; background:var(--line)} .stum-ok i.on{background:var(--ok)}

/* ---------- Wiederholen ---------- */''')
open(p, "w", encoding="utf-8").write(s)

g = ROOT + "/zh-app/game.part.js"
t = open(g, encoding="utf-8").read()
a = '''  var r = G.results[q.w.zh] || (G.results[q.w.zh] = {ok:0, bad:0});'''
assert t.count(a) == 1
t = t.replace(a, a + '''\n  noteResult(q.w.zh, ok);''')
open(g, "w", encoding="utf-8").write(t)

b = ROOT + "/scripts/build_page.py"
x = open(b, encoding="utf-8").read()
if '"/*PITCH*/"' not in x:
    x = x.replace('out = out.replace("/*FX*/", open(d+"/fx.part.js", encoding="utf-8").read())',
                  'out = out.replace("/*FX*/", open(d+"/fx.part.js", encoding="utf-8").read())\nout = out.replace("/*PITCH*/", open(d+"/pitch.part.js", encoding="utf-8").read())')
x = x.replace('护照到了市北京上海龙舟赛胜输起点终开始旅程弗洛里安法理"', '护照到了市北京上海龙舟赛胜输起点终开始旅程弗洛里安法理写说"')
x = x.replace('POINTS:POINTS,POINT:POINT,buildLesson:buildLesson,GR:GR};', 'POINTS:POINTS,POINT:POINT,buildLesson:buildLesson,GR:GR,checkTyped:checkTyped,WORD:WORD,stumbles:stumbles,yinTrack:yinTrack,semis:semis,shapeOk:shapeOk,toneSchema:toneSchema,pitchOfClip:pitchOfClip,clip:clip,VOICE:VOICE,audioBufferOf:audioBufferOf};')
open(b, "w", encoding="utf-8").write(x)
print("ok")
