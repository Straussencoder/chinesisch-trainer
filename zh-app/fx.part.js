/* ================= Effekte und Klänge ================= */
function reducedMotion(){ return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches); }
function fxLayer(){
  var c = document.createElement("canvas"); c.className = "fxlayer"; document.body.appendChild(c);
  var dpr = Math.min(2, window.devicePixelRatio || 1), W = window.innerWidth, H = window.innerHeight;
  c.width = W*dpr; c.height = H*dpr; var x = c.getContext("2d");
  if(!x){ c.remove(); return null; }
  x.scale(dpr, dpr);
  return {c:c, x:x, W:W, H:H};
}
/* Tuschespritzer: wenige kleine Tropfen in Siegelrot und Gold fliegen kurz vom Punkt weg */
function inkBurst(px, py, colors, n){
  if(reducedMotion()) return;
  var f = fxLayer(); if(!f) return;
  colors = colors || [cssVar("--seal") || "#b23c2c", cssVar("--gold") || "#98702a"];
  var P = [];
  for(var i=0;i<Math.min(n||12, 14);i++){ var a = Math.random()*6.283, v = 1.4 + Math.random()*2.8; P.push({x:px, y:py, vx:Math.cos(a)*v, vy:Math.sin(a)*v - 1, r:1 + Math.random()*1.8, c:colors[i%colors.length]}); }
  var t0 = performance.now(), dur = 0.5;
  (function fr(t){
    var el = (t - t0)/1000, life = Math.max(0, 1 - el/dur);
    f.x.clearRect(0, 0, f.W, f.H);
    P.forEach(function(p){ p.x += p.vx; p.y += p.vy; p.vy += 0.2; p.vx *= 0.9; p.vy *= 0.94; var sp = Math.min(2.2, Math.hypot(p.vx, p.vy)/2.5); f.x.globalAlpha = life*0.7; f.x.fillStyle = p.c; f.x.beginPath(); f.x.ellipse(p.x, p.y, p.r*(1 + sp*0.4), p.r*(1 - sp*0.15), Math.atan2(p.vy, p.vx), 0, 6.283); f.x.fill(); });
    if(el < dur) requestAnimationFrame(fr); else f.c.remove();
  })(t0);
}
function burstOn(el, colors, n){ if(!el) return; var b = el.getBoundingClientRect(); if(b.width) inkBurst(b.left + b.width/2, b.top + b.height/2, colors || null, n); }
/* Fallende Pflaumenblüten */
function petals(n, gold){
  if(reducedMotion()) return;
  var f = fxLayer(); if(!f) return;
  var cols = gold ? ["#e8c766", "#f4dc8e", "#c4952e", "#fbefc4", "#d4a63a"] : ["#e8a0a8", "#f2c4c9", "#c23a2c", "#f7dfe2", "#d9787f"], P = [];
  /* nur an den Rändern, damit die Mitte mit Text und Knöpfen frei bleibt */
  var edge = Math.min(140, f.W*0.2);
  for(var i=0;i<n;i++) P.push({x:i%2 ? Math.random()*edge : f.W - Math.random()*edge, y:-20-Math.random()*f.H*0.6, s:4+Math.random()*5, vy:1.2+Math.random()*2, vx:-0.5+Math.random()*1, r:Math.random()*6.28, vr:-0.06+Math.random()*0.12, c:cols[i%cols.length], ph:Math.random()*6.28});
  var t0 = performance.now(), x = f.x, fade = 1;
  function petal(p){ x.save(); x.translate(p.x, p.y); x.rotate(p.r); x.fillStyle = p.c; x.globalAlpha = .8*fade;
    for(var k=0;k<5;k++){ x.rotate(1.2566); x.beginPath(); x.ellipse(0, -p.s*0.55, p.s*0.38, p.s*0.6, 0, 0, 6.283); x.fill(); }
    x.fillStyle = "#c49a3e"; x.beginPath(); x.arc(0, 0, p.s*0.18, 0, 6.283); x.fill(); x.restore(); }
  (function frame(t){
    var el = t - t0; x.clearRect(0, 0, f.W, f.H); fade = Math.max(0, Math.min(1, (3400 - el)/1000));
    P.forEach(function(p){ p.y += p.vy; p.x += p.vx + Math.sin(p.ph + el/500)*0.6; p.r += p.vr; petal(p); });
    if(el < 3800) requestAnimationFrame(frame); else f.c.remove();
  })(t0);
}
/* Feuerwerk in Rot, Gold und Jade */
function fireworksOn(ctx, list, W, H, t){
  /* list: Partikel und Raketen, wird pro Bild weitergerechnet */
  for(var i=list.length-1;i>=0;i--){
    var p = list[i];
    if(p.rocket){
      p.y += p.vy; p.vy += 0.12; ctx.globalAlpha = 1; ctx.fillStyle = "#f6e3b0"; ctx.beginPath(); ctx.arc(p.x, p.y, 2, 0, 6.283); ctx.fill();
      if(p.vy >= -0.6){
        list.splice(i, 1);
        var cols = [["#c23a2c","#f0a35e"],["#c49a3e","#fff1c4"],["#2f8a6a","#bfe8d3"],["#d9545f","#ffd1d6"]][Math.floor(Math.random()*4)];
        for(var k=0;k<46;k++){ var a = k/46*6.283, v = 1.2 + Math.random()*2.6; list.push({x:p.x, y:p.y, vx:Math.cos(a)*v, vy:Math.sin(a)*v, life:1, c:cols[k%2]}); }
      }
      continue;
    }
    p.x += p.vx; p.y += p.vy; p.vy += 0.035; p.vx *= 0.985; p.vy *= 0.985; p.life -= 0.013;
    if(p.life <= 0){ list.splice(i, 1); continue; }
    ctx.globalAlpha = Math.max(0, p.life); ctx.fillStyle = p.c; ctx.beginPath(); ctx.arc(p.x, p.y, 1.9, 0, 6.283); ctx.fill();
  }
  ctx.globalAlpha = 1;
}
function launchRocket(list, W, H){ list.push({rocket:true, x:W*(0.15 + Math.random()*0.7), y:H, vy:-(H/48 + Math.random()*H/90)}); }

/* Klänge (nur mit eingeschalteten Signaltönen) */
function audioCtx(){
  if(!state.prefs.fx || quiet()) return null;
  try{
    if(!actx){ var AC = window.AudioContext || window.webkitAudioContext; if(!AC) return null; actx = new AC(); }
    if(actx.state==="suspended") actx.resume();
    return actx;
  }catch(e){ return null; }
}
function noiseBuf(a, dur){
  var b = a.createBuffer(1, Math.floor(a.sampleRate*dur), a.sampleRate), d = b.getChannelData(0);
  for(var i=0;i<d.length;i++) d[i] = (Math.random()*2-1) * (1 - i/d.length);
  return b;
}
/* Trommelschlag: tiefer Ton mit fallender Tonhöhe plus kurzer Anschlag */
function drum(strong){
  var a = audioCtx(); if(!a) return;
  var t = a.currentTime, o = a.createOscillator(), g = a.createGain();
  o.type = "sine"; o.frequency.setValueAtTime(strong ? 120 : 96, t); o.frequency.exponentialRampToValueAtTime(42, t+0.22);
  g.gain.setValueAtTime(strong ? 0.55 : 0.4, t); g.gain.exponentialRampToValueAtTime(0.001, t+0.34);
  o.connect(g); g.connect(a.destination); o.start(t); o.stop(t+0.36);
  var n = a.createBufferSource(), ng = a.createGain(), bp = a.createBiquadFilter();
  n.buffer = noiseBuf(a, 0.05); bp.type = "bandpass"; bp.frequency.value = 1800; ng.gain.value = 0.18;
  n.connect(bp); bp.connect(ng); ng.connect(a.destination); n.start(t);
}
/* Gong: mehrere unharmonische Teiltöne mit langem Ausklang */
function gong(){
  var a = audioCtx(); if(!a) return;
  var t = a.currentTime, base = 196;
  [[1, .32], [1.47, .16], [2.09, .12], [2.76, .08], [3.43, .05]].forEach(function(p){
    var o = a.createOscillator(), g = a.createGain();
    o.type = "sine"; o.frequency.setValueAtTime(base*p[0]*1.02, t); o.frequency.exponentialRampToValueAtTime(base*p[0], t+0.6);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(p[1], t+0.02); g.gain.exponentialRampToValueAtTime(0.0001, t+2.6);
    o.connect(g); g.connect(a.destination); o.start(t); o.stop(t+2.7);
  });
}
/* Wasserplatscher */
function splashSound(){
  var a = audioCtx(); if(!a) return;
  var t = a.currentTime, n = a.createBufferSource(), f = a.createBiquadFilter(), g = a.createGain();
  n.buffer = noiseBuf(a, 0.45); f.type = "lowpass"; f.frequency.setValueAtTime(2600, t); f.frequency.exponentialRampToValueAtTime(400, t+0.4);
  g.gain.value = 0.35; n.connect(f); f.connect(g); g.connect(a.destination); n.start(t);
}
/* Kurze Melodie in der chinesischen Fünftonleiter */
function melody(up){
  var a = audioCtx(); if(!a) return;
  var notes = up ? [392, 440, 523, 587, 659, 784] : [523, 440, 392, 330], t = a.currentTime;
  notes.forEach(function(f, i){
    var o = a.createOscillator(), g = a.createGain(), s = t + i*0.13;
    o.type = "triangle"; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, s); g.gain.exponentialRampToValueAtTime(0.16, s+0.02); g.gain.exponentialRampToValueAtTime(0.0001, s+0.32);
    o.connect(g); g.connect(a.destination); o.start(s); o.stop(s+0.34);
  });
}
