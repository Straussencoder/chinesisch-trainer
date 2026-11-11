/* ================= Tonhöhe messen (YIN) ================= */
/* x: Abtastwerte (mono), sr: Abtastrate. Ergebnis: Tonhöhe in Hz alle 10 ms, 0 = stimmlos */
function yinTrack(x, sr){
  var fac = Math.max(1, Math.floor(sr / 11000)), n = Math.floor(x.length / fac), y = new Float32Array(n), r = sr / fac, i, k;
  for(i=0;i<n;i++){ var s = 0; for(k=0;k<fac;k++) s += x[i*fac+k]; y[i] = s/fac; }
  var W = Math.round(0.03*r), hop = Math.round(0.01*r), tmin = Math.floor(r/500), tmax = Math.ceil(r/70);
  var fr = [], rmsMax = 0;
  for(var st=0; st + W + tmax + 1 < n; st += hop){
    var e = 0; for(i=0;i<W;i++) e += y[st+i]*y[st+i];
    var rms = Math.sqrt(e/W); if(rms > rmsMax) rmsMax = rms;
    var d = new Float32Array(tmax+2), cum = 0; d[0] = 1;
    for(var tau=1; tau<=tmax+1; tau++){
      var s2 = 0; for(i=0;i<W;i++){ var df = y[st+i] - y[st+i+tau]; s2 += df*df; }
      cum += s2; d[tau] = cum > 0 ? s2*tau/cum : 1;
    }
    fr.push({rms:rms, d:d});
  }
  /* Periode an einem Minimum genauer bestimmen */
  var refine = function(d, t){ var a = d[t-1], b = d[t], c = d[t+1], den = a + c - 2*b; return t + (den > 0 ? (a - c)/(2*den) : 0); };
  /* Kandidaten je Abschnitt: lokale Minima der YIN-Kurve; dazu »stimmlos« */
  var C = fr.map(function(o){
    var list = [], t1 = 0, minD = 1;
    if(o.rms >= rmsMax*0.03){
      for(var t=tmin; t<=tmax; t++){
        if(o.d[t] < 0.5 && o.d[t] <= o.d[t-1] && o.d[t] <= o.d[t+1]){
          if(!t1) t1 = t; if(o.d[t] < minD) minD = o.d[t];
          list.push({p:refine(o.d, t), c:o.d[t] + 0.12*Math.log2(t/t1)});
        }
      }
    }
    list.sort(function(a, b){ return a.c - b.c; }); list = list.slice(0, 5);
    var loud = o.rms >= rmsMax*0.06;
    list.push({p:0, c: !list.length ? 0 : (loud && minD < 0.25 ? 0.8 : (loud ? 0.45 : 0.3))});
    return list;
  });
  /* Bester Weg durch alle Abschnitte: wenig Sprünge, wenig Wechsel zwischen stimmhaft und stimmlos */
  var tr = function(a, b){ if(!a.p && !b.p) return 0; if(!a.p || !b.p) return 0.25; return 0.05*Math.abs(12*Math.log2(a.p/b.p)); };
  var cost = C.length ? C[0].map(function(c){ return c.c; }) : [], back = [];
  for(var j=1; j<C.length; j++){
    var nc = [], bk = [];
    C[j].forEach(function(cb){ var best = 1e9, bi = 0; C[j-1].forEach(function(ca, ia){ var v = cost[ia] + tr(ca, cb); if(v < best){ best = v; bi = ia; } }); nc.push(best + cb.c); bk.push(bi); });
    cost = nc; back.push(bk);
  }
  var per = new Array(C.length).fill(0);
  if(C.length){
    var bi = 0; cost.forEach(function(v, i){ if(v < cost[bi]) bi = i; });
    for(j=C.length-1; j>=0; j--){ per[j] = C[j][bi].p; if(j > 0) bi = back[j-1][bi]; }
  }
  var f0 = per.map(function(p){ return p ? r/p : 0; });
  /* Ausreißer (Oktavsprünge) gegen den Median der Nachbarn prüfen */
  var med = function(a){ var b = a.filter(function(v){ return v > 0; }).sort(function(p, q){ return p - q; }); return b.length ? b[Math.floor(b.length/2)] : 0; };
  var g = f0.map(function(v, j){ if(!v) return 0; var m = med(f0.slice(Math.max(0, j-3), j+4)); return m && Math.abs(12*Math.log2(v/m)) > 7 ? 0 : v; });
  /* Glätten (Median über 5) und kurze Stücke unter 40 ms entfernen */
  var h = g.map(function(v, j){ return v ? med(g.slice(Math.max(0, j-2), j+3)) : 0; });
  var j0 = 0;
  for(j=0; j<=h.length; j++){
    if(j===h.length || !h[j]){ if(j - j0 < 4) for(var q=j0; q<j; q++) h[q] = 0; j0 = j+1; }
  }
  return h;
}
/* Halbtöne über 100 Hz, nur der stimmhafte Teil (von der ersten bis zur letzten stimmhaften Stelle) */
function semis(track, single){
  var a = track.map(function(v){ return v > 0 ? 12*Math.log2(v/100) : null; });
  /* stimmhafte Stücke suchen; Ränder sind unsicher (je 2 Werte weg) */
  var runs = [];
  for(var i=0; i<a.length; ){
    if(a[i]===null){ i++; continue; }
    var j = i; while(j < a.length && a[j]!==null) j++;
    runs.push([i, j]); i = j;
  }
  /* eine Silbe: nur das längste Stück; mehrere Silben: alle Stücke ab 80 ms */
  var longest = runs.reduce(function(m, r){ return !m || r[1]-r[0] > m[1]-m[0] ? r : m; }, null);
  var keep = runs.filter(function(r){ return single ? r===longest : r[1]-r[0] >= 8; });
  var b = a.map(function(){ return null; });
  keep.forEach(function(r){ for(var q=r[0]+2; q<r[1]-2; q++) b[q] = a[q]; });
  var s = 0, e = b.length - 1; while(s < b.length && b[s]===null) s++; while(e >= 0 && b[e]===null) e--;
  return s > e ? [] : b.slice(s, e+1);
}
var pitchCache = {};
function audioBufferOf(blobUrlOrBlob){
  var get = typeof blobUrlOrBlob === "string" ? fetch(blobUrlOrBlob).then(function(r){ return r.arrayBuffer(); }) : blobUrlOrBlob.arrayBuffer();
  return get.then(function(buf){
    var C = window.OfflineAudioContext || window.webkitOfflineAudioContext;
    var ctx = new C(1, 44100, 44100);
    return new Promise(function(ok, bad){ var p = ctx.decodeAudioData(buf, ok, bad); if(p && p.then) p.then(ok, bad); });
  });
}
/* Tonkurve einer Aufnahme (Ergebnis wird gemerkt) */
function pitchOfClip(url, single){
  if(!url) return Promise.resolve(null);
  var key = url + (single ? "#1" : "#n");
  if(pitchCache[key]) return pitchCache[key];
  return (pitchCache[key] = audioBufferOf(url).then(function(ab){ return semis(yinTrack(ab.getChannelData(0), ab.sampleRate), single); }).catch(function(){ return null; }));
}
/* Kurve der Sprecherin für ein Ziel (Silbe oder Wort). Mehrere Aufnahmen werden mit einer kurzen Lücke aneinandergehängt */
function nativeCurve(target){
  var clips = target.clips; if(!clips || !clips.length) return Promise.resolve(null);
  var single = target.syls.length===1;
  if(clips.length===1) return pitchOfClip(clips[0], single);
  return Promise.all(clips.map(function(u){ return pitchOfClip(u, false); })).then(function(parts){
    if(parts.some(function(p){ return !p || p.length < 6; })) return null;
    var out = [];
    parts.forEach(function(p, i){ if(i) for(var g=0; g<6; g++) out.push(null); out = out.concat(p); });
    return out;
  });
}
/* Stimmhafte Stücke einer Kurve (für den Vergleich Silbe für Silbe) */
function voicedRuns(st){
  var runs = [];
  for(var i=0; i<(st||[]).length; ){
    if(st[i]===null){ i++; continue; }
    var j = i; while(j < st.length && st[j]!==null) j++;
    if(j - i >= 6) runs.push(st.slice(i, j)); i = j;
  }
  return runs;
}
/* Bereich der Sprecherinnen in Halbtönen über 100 Hz (gemessen über alle Aufnahmen) */
var VOICE = {s:{lo:6, hi:20.5}, w:{lo:8, hi:23.5}};
/* Kurve als SVG: list = [{st:[...], lo, hi, cls}], 5 Tonhöhen-Stufen als feine Linien */
function curveSVG(list, w, h){
  w = w || 220; h = h || 70;
  var pad = 6, out = '<svg class="pcurve" viewBox="0 0 '+w+' '+h+'" aria-hidden="true">';
  for(var l=1; l<=5; l++){ var yy = pad + (h - 2*pad)*(5-l)/4; out += '<line x1="0" x2="'+w+'" y1="'+yy.toFixed(1)+'" y2="'+yy.toFixed(1)+'" class="pc-grid"/>'; }
  list.forEach(function(c){
    if(!c || !c.st || c.st.length < 3) return;
    var n = c.st.length, seg = "", path = "";
    c.st.forEach(function(v, i){
      if(v===null){ if(seg) path += seg; seg = ""; return; }
      var lv = Math.max(0.6, Math.min(5.4, 1 + 4*(v - c.lo)/(c.hi - c.lo)));
      var x = pad + (w - 2*pad)*i/(n-1), yv = pad + (h - 2*pad)*(5-lv)/4;
      seg += (seg ? " L" : " M")+x.toFixed(1)+" "+yv.toFixed(1);
    });
    path += seg;
    out += '<path d="'+path+'" class="'+(c.cls||"pc-line")+'"/>';
  });
  return out + '</svg>';
}
/* Eigener Bereich für die Stimme des Nutzers: um den Median, mindestens 12 Halbtöne Spanne */
function ownRange(st){
  var v = st.filter(function(x){ return x!==null; }).sort(function(a, b){ return a - b; });
  if(!v.length) return {lo:0, hi:12};
  var lo = v[Math.floor(v.length*0.05)], hi = v[Math.floor(v.length*0.95)], mid = (lo + hi)/2, span = Math.max(12, hi - lo + 2);
  return {lo:mid - span/2, hi:mid + span/2};
}
/* Passt die gemessene Kurve einer Silbe sichtbar zu ihrem Ton? Sonst zeigt die App nur das Schema */
function shapeOk(st, t, R){
  var v = (st||[]).filter(function(a){ return a!==null; }); if(v.length < 10 || st.length - v.length > 3) return false;
  var lv = v.map(function(a){ return 1 + 4*(a - R.lo)/(R.hi - R.lo); }), n = lv.length, q = Math.max(2, Math.floor(n/4));
  var avg = function(a){ return a.reduce(function(x, y){ return x + y; }, 0)/a.length; };
  var start = avg(lv.slice(0, q)), end = avg(lv.slice(-q)), mean = avg(lv), mn = Math.min.apply(null, lv), mx = Math.max.apply(null, lv);
  if(t===1) return mean >= 3.3 && mx - mn < 1.3;
  if(t===2) return end - start >= 0.6 && end > mean;
  if(t===3) return mn <= 2.4 && mean < 3;
  if(t===4) return Math.max.apply(null, lv.slice(0, Math.ceil(n/2))) - end >= 0.6;
  return false;
}
/* Lehrbuch-Tonverlauf (Stufen 1 bis 5) für eine Silbenfolge, mit Tonwechseln im Wort */
function toneSchema(syls){
  var tones = syls.map(toneOf), out = [];
  tones.forEach(function(t, i){
    var next = tones[i+1], prev = i ? out[i-1] : null, pts;
    if(t===1) pts = [5, 5];
    else if(t===2) pts = [3, 5];
    else if(t===3) pts = next===3 ? [3, 5] : (next!==undefined ? [2, 1, 1] : [2, 1, 4]);
    else if(t===4) pts = [5, 1];
    else { var pt = prev ? ({1:2, 2:3, 3:4, 4:1})[prev.t] || 3 : 3; pts = [pt, pt - 0.3]; }
    out.push({t:t, eff: t===3 && next===3 ? 2 : t, pts:pts, short:!t});
  });
  return out;
}
/* Schema als SVG: je Silbe ein Abschnitt in Tonfarbe, Pinyin darunter */
function schemaSVG(syls, extra, w, h){
  w = w || 240; h = h || 84;
  var sch = toneSchema(syls), pad = 8, top = 6, bot = h - 22, n = sch.length, unit = (w - 2*pad)/n, out = '<svg class="pcurve schema" viewBox="0 0 '+w+' '+h+'" aria-hidden="true">';
  for(var l=1; l<=5; l++){ var yy = top + (bot - top)*(5-l)/4; out += '<line x1="0" x2="'+w+'" y1="'+yy.toFixed(1)+'" y2="'+yy.toFixed(1)+'" class="pc-grid"/>'; }
  if(extra) out += extra(pad, top, bot, w);
  sch.forEach(function(s, i){
    var x0 = pad + unit*i + unit*0.12, x1 = pad + unit*(i+1) - unit*0.12;
    if(s.short){ x0 = pad + unit*i + unit*0.32; x1 = pad + unit*(i+1) - unit*0.32; }
    var p = s.pts, d = "";
    for(var k=0; k<=16; k++){
      var u = k/16, seg = u*(p.length-1), a = Math.floor(seg), b = Math.min(p.length-1, a+1), f = seg - a, e = (1 - Math.cos(f*Math.PI))/2;
      var lv = p[a] + (p[b]-p[a])*e, x = x0 + (x1 - x0)*u, y = top + (bot - top)*(5-lv)/4;
      d += (k ? " L" : "M")+x.toFixed(1)+" "+y.toFixed(1);
    }
    out += '<path d="'+d+'" class="sc-tone" style="stroke:var(--t'+s.eff+')"/>';
    out += '<text x="'+((x0+x1)/2).toFixed(1)+'" y="'+(h-5)+'" text-anchor="middle" class="sc-lbl">'+esc(syls[i].replace(/[^\p{L}]/gu, ""))+'</text>';
  });
  return out + '</svg>';
}
/* Gemessene Kurve in den Rahmen eines Schemas legen (gleiche Höhenstufen) */
function overlayPath(st, R, cls){
  return function(pad, top, bot, w){
    if(!st || st.length < 3) return "";
    var n = st.length, seg = "", path = "";
    st.forEach(function(v, i){
      if(v===null){ path += seg; seg = ""; return; }
      var lv = Math.max(0.6, Math.min(5.4, 1 + 4*(v - R.lo)/(R.hi - R.lo))), x = pad + (w - 2*pad)*i/(n-1), y = top + (bot - top)*(5-lv)/4;
      seg += (seg ? " L" : " M")+x.toFixed(1)+" "+y.toFixed(1);
    });
    return '<path d="'+(path + seg)+'" class="'+cls+'"/>';
  };
}
/* Einfache Beschreibung einer eigenen Silbe: bleibt, steigt, fällt, Tal */
function describeOwn(st){
  var v = (st||[]).filter(function(a){ return a!==null; }); if(v.length < 6) return null;
  var n = v.length, q = Math.max(2, Math.floor(n/4)), e = Math.max(2, Math.floor(n/6)), avg = function(a){ return a.reduce(function(x, y){ return x + y; }, 0)/a.length; };
  var start = avg(v.slice(0, q)), end = avg(v.slice(-q)), tail = avg(v.slice(-e)), inner = v.slice(q, n-q).length ? v.slice(q, n-q) : v;
  var mn = Math.min.apply(null, inner), low = Math.min.apply(null, v), range = Math.max.apply(null, v) - low, lowI = v.lastIndexOf(low), peak = Math.max.apply(null, v.slice(0, Math.ceil(n*0.6)));
  var body = v.slice(Math.floor(n/4)), bRange = Math.max.apply(null, body) - Math.min.apply(null, body), drop = Math.max.apply(null, body) - avg(body.slice(-3));
  if(start - mn > 1.5 && end - mn > 1.5) return {k:3, de:"geht runter und wieder hoch"};
  /* 1. Ton mit kurzem Anlauf von unten (z. B. nach m): danach gerade und oben */
  if(n >= 10 && bRange < 2 && drop < 0.8 && start <= avg(body) + 0.5) return {k:1, de:"bleibt gleich"};
  if(end - start > 2) return {k:2, de:"steigt"};
  if(start - end > 2.5) return {k:4, de:"fällt"};
  /* 4. Ton mit kurzem Anlauf (z. B. nach m, l, r): erst etwas hoch, dann deutlich runter bis zum Schluss */
  if(peak - tail > 2.2 && lowI >= n*2/3) return {k:4, de:"fällt"};
  if(range < 2.5 && n >= 10) return {k:1, de:"bleibt gleich"};
  return {k:0, de:"ist nicht eindeutig"};
}
