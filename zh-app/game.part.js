/* ================= Drachenboot-Rennen 龙舟赛 ================= */
var RIVALS = [
  {id:"wang", zh:"王爷爷", py:"Wáng yé_ye", de:"Opa Wang", tag:"gemütlich", stars:1, time:72, hull:"#2f6b58", accent:"#d6ad4e", bonus:3,
   intro:"Paddelt mit einer Hand. In der anderen hält er seinen Tee.",
   behind:["Opa Wang schlürft Tee und liegt trotzdem vorne.", "Opa Wang winkt dir freundlich zu. Von vorne."],
   ahead:["Opa Wang verschluckt sich vor Schreck an seinem Tee.", "Opa Wang murmelt: 年轻人！ (niánqīngrén, junge Leute!)"],
   win:"Opa Wang verbeugt sich und schenkt dir eine Tasse Jasmintee.",
   lose:"Opa Wang gewinnt und lädt dich trotzdem auf Tee ein."},
  {id:"li", zh:"李阿姨", py:"Lǐ ā_yí", de:"Tante Li", tag:"flott", stars:2, time:50, hull:"#2c4f8a", accent:"#e0b04a", bonus:6,
   intro:"Verkauft morgens Baozi und paddelt nachmittags um Medaillen.",
   behind:["Tante Li ruft: 快点！ (kuài diǎn, schneller!)", "Tante Li feilscht schon um den Siegerpokal."],
   ahead:["Tante Li schimpft wie ein Rohrspatz.", "Tante Li droht, dir keine Baozi mehr zu verkaufen."],
   win:"Tante Li gibt zu: 你很厉害！ (nǐ hěn lìhai, du bist echt gut!)",
   lose:"Tante Li gewinnt und schenkt dir zum Trost einen Pfirsich."},
  {id:"long", zh:"龙师傅", py:"Lóng shī_fu", de:"Meister Long", tag:"Profi", stars:3, time:37, hull:"#26231e", accent:"#c23a2c", bonus:10,
   intro:"Hat noch nie verloren. Sagt er jedenfalls.",
   behind:["Meister Long gähnt. Zeig ihm, was du kannst!", "Meister Long paddelt, als wäre es Meditation."],
   ahead:["Meister Long zieht eine Augenbraue hoch.", "Meister Long schaut zum ersten Mal nervös nach hinten."],
   win:"Meister Long verbeugt sich tief. Ein neuer Meister ist da!",
   lose:"Meister Long nickt: Nächstes Mal vielleicht."}
];
var SAY = {
  start:["Die Trommeln donnern. Los geht's!", "Und ab ins Wasser!"],
  ok:["Sauberer Schlag!", "Dein Drache nickt zufrieden.", "Das Publikum ruft: 好！ (hǎo, gut!)", "Paddel im Takt, Wort im Kopf.", "Wie geschmiert. Mit Sesamöl."],
  fast:["Blitzschnell! Extra-Schwung fürs Boot.", "So schnell, das Wasser hat dich kaum bemerkt."],
  c3:["Drei in Folge! Der Trommler kommt ins Schwitzen.", "连击 ×3! (liánjī, Serie) Dein Drache faucht vor Freude."],
  c5:["Fünf in Folge! Jemand wirft vor Begeisterung Baozi.", "Unaufhaltsam! Sogar die Enten machen Platz."],
  c8:["Acht in Folge! Am Ufer wird schon Feuerwerk gezündet.", "Legendär! Dein Drache will gar nicht mehr aufhören."],
  bad:["Platsch! Das Paddel hat nur Luft erwischt.", "Uiii. Kurz die Richtung vergessen.", "Eine Ente schaut dich vorwurfsvoll an.", "Der Trommler hat sich verzählt. Weiter!"],
  close:["Kopf an Drachenkopf!", "Ganz knapp! Jetzt bloß keinen Fehler."],
  final:["Das Ziel ist in Sicht!", "Noch ein paar Schläge!"]
};
function pickOne(a){ return a[Math.floor(Math.random()*a.length)]; }
var RACE_M = 500, WORLD = 1500;
var G = null, gameRaf = 0, lobbyRaf = 0, gameTimers = [];
function gameReady(){ return learnedWords().length >= 4; }
function rivalById(id){ return RIVALS.find(function(r){ return r.id===id; }) || RIVALS[0]; }

/* ---------- Kulisse (vorberechnet) ---------- */
function ridgeVals(seed, n){ var r = rng(seed), a = []; for(var i=0;i<n;i++) a.push(0.25 + 0.75*r()); return a; }
var FAR = ridgeVals(91, 90), MID = ridgeVals(37, 90), CROWD = ridgeVals(5, 400);
function gRidge(c, W, base, off, vals, amp, fill){
  var step = 90, start = Math.floor(off/step), x0 = -(off % step) - step;
  c.fillStyle = fill; c.beginPath(); c.moveTo(x0, base + 40);
  for(var i=0;i<=Math.ceil(W/step)+3;i++){
    var v = vals[(start + i + vals.length*10) % vals.length], x = x0 + i*step, y = base - amp*v;
    if(i===0) c.lineTo(x, y); else { var pv = vals[(start + i - 1 + vals.length*10) % vals.length], px = x - step, py = base - amp*pv; c.quadraticCurveTo(px + step*0.5, Math.min(py, y) - amp*0.25*v, x, y); }
  }
  c.lineTo(x0 + (Math.ceil(W/step)+3)*step, base + 40); c.closePath(); c.fill();
}
function gPagoda(c, x, base, s){
  c.fillStyle = "rgba(70,74,70,.55)";
  for(var i=0;i<5;i++){ var w = (26 - i*4)*s, y = base - i*11*s; c.fillRect(x - w*0.35, y - 9*s, w*0.7, 9*s); c.beginPath(); c.moveTo(x - w*0.7, y - 8*s); c.quadraticCurveTo(x, y - 14*s, x + w*0.7, y - 8*s); c.lineTo(x + w*0.5, y - 11*s); c.lineTo(x - w*0.5, y - 11*s); c.closePath(); c.fill(); }
  c.fillRect(x - 0.8*s, base - 64*s, 1.6*s, 12*s);
}
function gShore(c, W, H, off, t, cheer){
  var y0 = H*0.468, y1 = H*0.53;
  c.fillStyle = "#4a443b"; c.fillRect(0, y0 + (y1-y0)*0.45, W, (y1-y0)*0.6);
  var sp = 8, start = Math.floor(off/sp), x0 = -(off % sp);
  var cols = ["#c23a2c", "#2c4f8a", "#d6ad4e", "#2f6b58", "#e8dcc4", "#8a3b6a"];
  for(var i=0;i<W/sp+2;i++){
    var k = (start + i + 4000) % CROWD.length, v = CROWD[k], x = x0 + i*sp, bob = cheer ? Math.abs(Math.sin(t*0.012 + k))*3 : Math.sin(t*0.003 + k)*0.6;
    var hy = y0 + (y1-y0)*0.42 - v*4 - bob;
    c.fillStyle = cols[k % cols.length]; c.fillRect(x - 2.6, hy + 2, 5.2, 7);
    c.fillStyle = "#e7c9a3"; c.beginPath(); c.arc(x, hy, 2.4, 0, 6.283); c.fill();
    c.fillStyle = "#2a2520"; c.fillRect(x - 2.4, hy - 2.6, 4.8, 1.6);
  }
  /* Fahnen */
  var fs = 170, fstart = Math.floor(off/fs), fx0 = -(off % fs);
  for(var j=0;j<W/fs+2;j++){
    var fx = fx0 + j*fs + 40, wave = Math.sin(t*0.006 + j)*3;
    c.strokeStyle = "#2a2520"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(fx, y0 + 6); c.lineTo(fx, y0 - 22); c.stroke();
    c.fillStyle = (fstart + j) % 2 ? "#c23a2c" : "#d6ad4e"; c.beginPath(); c.moveTo(fx, y0 - 22); c.quadraticCurveTo(fx + 9, y0 - 22 + wave*0.5, fx + 18, y0 - 18 + wave); c.lineTo(fx, y0 - 13); c.closePath(); c.fill();
  }
}
function gGate(c, x, H, label, big){
  var top = big ? H*0.16 : H*0.3, bot = H*0.97, w = big ? 26 : 16;
  c.fillStyle = "#a33b2b"; c.fillRect(x - w*1.6, top + 10, 4, bot - top - 10); c.fillRect(x + w*1.6 - 4, top + 10, 4, bot - top - 10);
  c.fillStyle = "#26231e"; c.beginPath(); c.moveTo(x - w*2.2, top + 12); c.quadraticCurveTo(x - w*1.6, top + 8, x - w*1.4, top); c.lineTo(x + w*1.4, top); c.quadraticCurveTo(x + w*1.6, top + 8, x + w*2.2, top + 12); c.closePath(); c.fill();
  c.fillStyle = "#c23a2c"; c.fillRect(x - w*1.1, top + 13, w*2.2, big ? 22 : 15);
  c.fillStyle = "#f3e2b6"; c.font = (big ? 17 : 12) + "px 'Ma Shan Zheng', KaiTi, serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(label, x, top + 13 + (big ? 11 : 7.5));
  c.strokeStyle = "rgba(194,58,44,.6)"; c.setLineDash([5, 6]); c.lineWidth = 2; c.beginPath(); c.moveTo(x, H*0.55); c.lineTo(x, bot); c.stroke(); c.setLineDash([]);
}
/* Drachenboot, Bug nach rechts */
function gBoat(c, x, y, s, hull, accent, t, phase, stroke, glow, wob, label){
  c.save(); c.translate(x, y); c.rotate(wob ? Math.sin(t*0.03)*0.06*wob : 0); c.scale(s, s);
  if(glow){ c.shadowColor = "rgba(214,173,78,.9)"; c.shadowBlur = 18; }
  /* Rumpf */
  c.fillStyle = hull; c.beginPath(); c.moveTo(-112, -6); c.lineTo(96, -6); c.quadraticCurveTo(108, -6, 110, -1); c.lineTo(100, 9); c.lineTo(-100, 9); c.quadraticCurveTo(-114, 9, -118, 0); c.closePath(); c.fill();
  c.shadowBlur = 0;
  c.strokeStyle = accent; c.lineWidth = 1.4; for(var i=-100;i<94;i+=9){ c.beginPath(); c.arc(i, 1, 4, Math.PI*0.1, Math.PI*0.9); c.stroke(); }
  c.fillStyle = accent; c.fillRect(-108, -7.5, 204, 2.4);
  /* Schwanz */
  c.fillStyle = hull; c.beginPath(); c.moveTo(-110, -5); c.bezierCurveTo(-122, -14, -128, -28, -118, -38); c.bezierCurveTo(-116, -30, -110, -22, -100, -8); c.closePath(); c.fill();
  c.strokeStyle = accent; c.lineWidth = 1.6; c.beginPath(); c.moveTo(-118, -38); c.quadraticCurveTo(-112, -42, -108, -36); c.stroke();
  /* Hals und Kopf */
  c.fillStyle = hull; c.beginPath(); c.moveTo(92, -6); c.bezierCurveTo(106, -10, 110, -24, 114, -34); c.lineTo(122, -32); c.bezierCurveTo(118, -22, 112, -10, 104, -4); c.closePath(); c.fill();
  c.beginPath(); c.moveTo(110, -38); c.quadraticCurveTo(118, -46, 128, -40); c.lineTo(140, -37); c.lineTo(132, -33); c.lineTo(138, -29); c.lineTo(126, -29); c.quadraticCurveTo(116, -26, 110, -30); c.closePath(); c.fill();
  c.fillStyle = "#fff8e8"; c.beginPath(); c.arc(121, -38, 2.6, 0, 6.283); c.fill(); c.fillStyle = "#111"; c.beginPath(); c.arc(121.6, -38, 1.3, 0, 6.283); c.fill();
  c.strokeStyle = accent; c.lineWidth = 1.6; c.beginPath(); c.moveTo(114, -42); c.lineTo(108, -52); c.moveTo(118, -43); c.lineTo(116, -54); c.moveTo(138, -33); c.quadraticCurveTo(146, -30, 144, -22); c.stroke();
  c.fillStyle = accent; for(var m=0;m<4;m++){ c.beginPath(); c.moveTo(100 + m*3.2, -10 - m*6); c.lineTo(96 + m*3.2, -14 - m*6); c.lineTo(103 + m*3.2, -15 - m*6); c.fill(); }
  /* Paddler */
  var hit = stroke ? Math.max(0, 1 - (t - stroke)/420) : 0;
  for(var p=0;p<7;p++){
    var px = -82 + p*24, a = 1.75 + Math.sin(phase + p*0.4)*(0.45 + hit*0.35);
    c.strokeStyle = "#5b4630"; c.lineWidth = 2.2; c.beginPath(); c.moveTo(px + 2, -16); c.lineTo(px + 2 + Math.cos(a)*25, -16 + Math.sin(a)*25); c.stroke();
    c.fillStyle = "#5b4630"; c.beginPath(); c.ellipse(px + 2 + Math.cos(a)*25, -16 + Math.sin(a)*25, 2.2, 4.5, a, 0, 6.283); c.fill();
    c.fillStyle = hull==="#26231e" ? "#5a5047" : hull; c.beginPath(); c.ellipse(px, -13, 5, 7, 0, 0, 6.283); c.fill();
    c.fillStyle = "#e7c9a3"; c.beginPath(); c.arc(px + 1, -23.5, 4.5, 0, 6.283); c.fill();
    c.fillStyle = accent; c.fillRect(px - 3.6, -27, 9.2, 2);
  }
  /* Trommler */
  var dh = Math.abs(Math.sin(t*0.02 + (hit ? 3 : 0)))*(hit ? 6 : 2.5);
  c.fillStyle = "#c23a2c"; c.beginPath(); c.ellipse(86, -15, 7, 8, 0, 0, 6.283); c.fill(); c.strokeStyle = "#d6ad4e"; c.lineWidth = 1.4; c.stroke();
  c.fillStyle = "#e7c9a3"; c.beginPath(); c.arc(76, -27, 4.5, 0, 6.283); c.fill(); c.fillStyle = "#2a2520"; c.fillRect(71.5, -31, 9, 2.2);
  c.strokeStyle = "#2a2520"; c.lineWidth = 1.6; c.beginPath(); c.moveTo(78, -20); c.lineTo(86, -24 + dh); c.stroke();
  /* Steuermann */
  c.fillStyle = "#e7c9a3"; c.beginPath(); c.arc(-102, -30, 4.5, 0, 6.283); c.fill(); c.fillStyle = "#3a332c"; c.fillRect(-106, -26, 8, 16);
  c.strokeStyle = "#5b4630"; c.lineWidth = 2; c.beginPath(); c.moveTo(-100, -22); c.lineTo(-130, 10); c.stroke();
  c.restore();
  if(label){
    c.save(); c.font = "600 " + Math.round(11.5*Math.max(0.9, s*1.7)) + "px 'Noto Sans', sans-serif"; c.textAlign = "center"; c.textBaseline = "middle";
    var tw = c.measureText(label).width + 14, ly = y - 66*s;
    c.fillStyle = "rgba(251,246,234,.92)"; c.beginPath(); c.roundRect ? c.roundRect(x - tw/2, ly - 10, tw, 20, 9) : c.rect(x - tw/2, ly - 10, tw, 20); c.fill();
    c.fillStyle = "#1d1a16"; c.fillText(label, x, ly + 0.5); c.restore();
  }
}
/* Ein Bild des Rennens. R: Zustand mit me, opp, cam, parts usw. */
function drawRace(c, W, H, R, t){
  var cam = R.cam || 0, k = H/240;
  var hz = H*0.47;
  var g = c.createLinearGradient(0, 0, 0, hz); g.addColorStop(0, "#f0dfc1"); g.addColorStop(1, "#f6e9d4"); c.fillStyle = g; c.fillRect(0, 0, W, hz + 4);
  var sg = c.createRadialGradient(W*0.82 - cam*0.02, H*0.17, 0, W*0.82 - cam*0.02, H*0.17, H*0.12); sg.addColorStop(0, "rgba(214,120,72,.5)"); sg.addColorStop(.55, "rgba(214,120,72,.28)"); sg.addColorStop(1, "rgba(214,120,72,0)"); c.fillStyle = sg; c.beginPath(); c.arc(W*0.82 - cam*0.02, H*0.17, H*0.12, 0, 6.283); c.fill();
  gRidge(c, W, hz + 2, cam*0.1, FAR, H*0.24, "rgba(150,146,128,.42)");
  var po = cam*0.22; for(var pi=0;pi<6;pi++){ var px = 260 + pi*620 - po; if(px > -60 && px < W + 60) gPagoda(c, px, hz - 4, k*0.9); }
  gRidge(c, W, hz + 6, cam*0.22, MID, H*0.13, "rgba(98,96,82,.5)");
  gShore(c, W, H, cam*0.75, t, R.cheer);
  var rg = c.createLinearGradient(0, H*0.53, 0, H); rg.addColorStop(0, "#bcc8b8"); rg.addColorStop(1, "#ece4d0"); c.fillStyle = rg; c.fillRect(0, H*0.53, W, H*0.47);
  c.strokeStyle = "rgba(80,104,98,.32)"; c.lineWidth = 1.2;
  for(var row=0; row<8; row++){
    var y = H*0.57 + row*H*0.058, sp = 64 - row*3, off = (cam*(0.92 + row*0.012) + t*0.015*(row%2 ? 1 : -1)) % sp;
    for(var x = -sp - off; x < W + sp; x += sp){ c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + sp*0.25, y - 2.5, x + sp*0.5, y); c.stroke(); }
  }
  /* Start, Meter, Ziel */
  var toS = function(wx){ return wx - cam; };
  gGate(c, toS(0), H, "起点", false);
  for(var m=100; m<RACE_M; m+=100){ var mx = toS(m/RACE_M*WORLD); if(mx > -30 && mx < W + 30){ c.fillStyle = "rgba(251,246,234,.85)"; c.fillRect(mx - 15, H*0.535, 30, 12); c.fillStyle = "#3b352d"; c.font = "600 9px 'Noto Sans', sans-serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(m + " m", mx, H*0.535 + 6.5); } }
  for(var b=80; b<WORLD; b+=160){ var bx = toS(b); if(bx > -10 && bx < W + 10){ c.fillStyle = (b/160|0) % 2 ? "#c23a2c" : "#f6efe0"; c.beginPath(); c.arc(bx, H*0.775 + Math.sin(t*0.004 + b)*1.2, 3.2*k, 0, 6.283); c.fill(); } }
  gGate(c, toS(WORLD), H, "终点", true);
  /* Wellen hinter den Booten */
  var oppX = R.opp/100*WORLD, meX = R.me/100*WORLD, oy = H*0.69, my = H*0.885, os = 0.42*k, ms = 0.5*k;
  [[oppX, oy, os], [meX, my, ms]].forEach(function(bt){
    var sx = toS(bt[0]);
    c.strokeStyle = "rgba(246,239,224,.75)"; c.lineWidth = 2; c.beginPath(); c.moveTo(sx - 120*bt[2], bt[1] + 9*bt[2]); c.quadraticCurveTo(sx - 170*bt[2], bt[1] + 6*bt[2], sx - 230*bt[2], bt[1] + 12*bt[2]); c.stroke();
  });
  /* Tempo-Linien bei Serie */
  if(R.glow){ c.strokeStyle = "rgba(214,173,78,.55)"; c.lineWidth = 2; for(var sl=0; sl<5; sl++){ var ly = my - 30*ms + sl*9*ms, lx = toS(meX) - 140*ms - ((t*0.4 + sl*37) % 90); c.beginPath(); c.moveTo(lx, ly); c.lineTo(lx - 40, ly); c.stroke(); } }
  gBoat(c, toS(oppX), oy, os, R.rival.hull, R.rival.accent, t, t*0.009*(R.oppPaddle||1), 0, false, 0, R.nolabel ? "" : R.rival.zh);
  gBoat(c, toS(meX), my, ms, "#a8342a", "#d6ad4e", t, R.phase || t*0.004, R.stroke, R.glow, R.wob, R.nolabel ? "" : "Du");
  /* Spritzer */
  if(R.parts){
    for(var i=R.parts.length-1;i>=0;i--){ var p = R.parts[i]; p.x += p.vx; p.y += p.vy; p.vy += 0.22; p.life -= 0.025;
      if(p.life <= 0 || p.y > H){ R.parts.splice(i, 1); continue; }
      c.globalAlpha = Math.max(0, p.life); c.fillStyle = p.c; c.beginPath(); c.arc(p.x - cam, p.y, p.r, 0, 6.283); c.fill(); }
    c.globalAlpha = 1;
  }
  if(R.pop && t - R.pop.t < 1100){ var pa = 1 - (t - R.pop.t)/1100; c.globalAlpha = pa; c.font = "700 " + Math.round(20*k) + "px 'Noto Sans', sans-serif"; c.textAlign = "center"; c.fillStyle = "#2c4f8a"; c.fillText(R.pop.text, toS(meX) + 10, my - 70*ms - (1 - pa)*24); c.globalAlpha = 1; }
  /* Gegner außerhalb des Bildes */
  var osx = toS(oppX);
  if(!R.nolabel && (osx > W + 30 || osx < -30)){
    var right = osx > W, ax = right ? W - 8 : 8, dist = Math.round(Math.abs(R.opp - R.me)/100*RACE_M);
    c.font = "700 " + Math.round(11.5*Math.max(1, k*0.9)) + "px 'Noto Sans', sans-serif"; c.textBaseline = "middle";
    var txt = (right ? "" : "◀ ") + R.rival.zh + " " + (right ? "+" : "−") + dist + " m" + (right ? " ▶" : "");
    var tw = c.measureText(txt).width + 14; c.fillStyle = "rgba(29,26,22,.82)";
    var bx2 = right ? ax - tw : ax; c.beginPath(); c.roundRect ? c.roundRect(bx2, oy - 40*os - 11, tw, 22, 11) : c.rect(bx2, oy - 40*os - 11, tw, 22); c.fill();
    c.fillStyle = "#fbf6ea"; c.textAlign = "left"; c.fillText(txt, bx2 + 7, oy - 40*os);
  }
  if(R.fw) fireworksOn(c, R.fw, W, H, t);
}
function splashAt(R, wx, wy, n, strong){
  for(var i=0;i<n;i++){ var a = -Math.PI*(0.15 + Math.random()*0.7); var v = (strong ? 3 : 1.6) + Math.random()*(strong ? 4 : 2.4);
    R.parts.push({x:wx + (Math.random()-0.5)*(strong ? 60 : 14), y:wy, vx:Math.cos(a)*v*(Math.random()<.5 ? -1 : 1), vy:Math.sin(a)*v, r:1.2 + Math.random()*(strong ? 2.8 : 1.8), life:1, c:Math.random()<.6 ? "#f6efe0" : "#9fbab1"}); }
}

/* ---------- Leinwand ---------- */
function sizeCanvas(cv){
  var dpr = Math.min(2, window.devicePixelRatio || 1), W = cv.clientWidth, H = cv.clientHeight;
  if(cv.width !== Math.round(W*dpr) || cv.height !== Math.round(H*dpr)){ cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr); }
  var c = cv.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0);
  return {c:c, W:W, H:H};
}
/* Vorschau in der Spielhalle: Boote treiben ruhig dahin */
function lobbyLoop(){
  cancelAnimationFrame(lobbyRaf);
  var cv = $("#lobby-canvas"); if(!cv) return;
  var R = {me:40, opp:42, cam:0, rival:RIVALS[(Math.floor(Date.now()/9000)) % 3], parts:[], phase:0};
  var t0 = performance.now();
  (function fr(t){
    var cv2 = $("#lobby-canvas"); if(!cv2 || G || currentView!=="spiel"){ return; }
    var s = sizeCanvas(cv2), el = (t - t0)/1000;
    R.me = 40 + Math.sin(el*0.4)*1.2; R.opp = 42 + Math.sin(el*0.33 + 1)*1.4; R.cam = R.me/100*WORLD - s.W*0.4; R.phase = t*0.004;
    drawRace(s.c, s.W, s.H, R, t);
    lobbyRaf = requestAnimationFrame(fr);
  })(t0);
}

/* ---------- Ablauf ---------- */
function gameSay(text){ if(!G) return; G.say = text; var el = $("#race-say"); if(el){ el.textContent = text; el.classList.remove("pop"); void el.offsetWidth; el.classList.add("pop"); } }
function clearGameTimers(){ gameTimers.forEach(clearTimeout); gameTimers = []; }
function later(fn, ms){ gameTimers.push(setTimeout(fn, ms)); }
function startGame(rid){
  if(!gameReady()) return;
  stopAll(); clearGameTimers(); cancelAnimationFrame(gameRaf); cancelAnimationFrame(lobbyRaf);
  var rv = rivalById(rid);
  G = {phase:"count", rival:rv, me:0, meShown:0, opp:0, cam:-60, raceT:0, last:0, q:null, answered:false, combo:0, maxCombo:0, ok:0, n:0,
       results:{}, order:[], parts:[], fw:[], wob:0, stroke:0, phase0:0, paddle:0, lastSay:0, pop:null, say:pickOne(SAY.start), confirm:false};
  state.prefs.lastRival = rv.id;
  var ov = $("#game"); ov.hidden = false; document.body.style.overflow = "hidden"; $("#app").inert = true;
  renderRace();
  ov.focus({preventScroll:true});
  /* Countdown auf Chinesisch: 三 二 一 开始 */
  var steps = [["三", "sān", "san1"], ["二", "èr", "er4"], ["一", "yī", "yi1"]];
  steps.forEach(function(st, i){ later(function(){ showCount(st[0], st[1]); var cl = clip("s", st[2]); if(cl) playClips([cl]); else drum(false); }, i*900); });
  later(function(){ showCount("开始", "kāishǐ · los!"); gong(); G.phase = "race"; G.raceT = 0; gameSay(G.say); gameNextQ(); }, 2700);
  later(function(){ showCount("", ""); }, 3500);
  G.last = 0; gameRaf = requestAnimationFrame(gameFrame);
}
function showCount(zh, py){ var el = $("#race-count"); if(!el) return; el.innerHTML = zh ? '<b class="brush">'+esc(zh)+'</b><small>'+esc(py)+'</small>' : ""; el.classList.remove("cgo"); void el.offsetWidth; if(zh) el.classList.add("cgo"); }
function gameOrder(){
  var pool = learnedWords(), t = today();
  var due = shuffle(pool.filter(function(w){ return state.words[w.zh].d <= t; }));
  var rest = shuffle(pool.filter(function(w){ return state.words[w.zh].d > t; })).sort(function(a, b){ return state.words[a.zh].b - state.words[b.zh].b; });
  return due.concat(rest);
}
function gameNextQ(){
  if(!G || G.phase!=="race") return;
  var pool = learnedWords();
  if(!G.order.length) G.order = gameOrder();
  var w = G.order.shift();
  if(G.q && w===G.q.w && G.order.length){ G.order.push(w); w = G.order.shift(); }
  var types = canHear(w) && !quiet() ? ["hear", "mean", "char"] : ["mean", "char"]; if(canTone(w)) types.push("tone");
  var type = types[Math.floor(Math.random()*types.length)];
  var q = {w:w, type:type};
  if(type!=="tone") q.opts = shuffle([w].concat(distractors(w, pool, 3, type==="char")));
  G.q = q; G.answered = false; G.pick = null; G.qStart = performance.now();
  renderRaceQ();
  if(type!=="char") playWord(w);
}
function gameAnswer(i, el){
  if(!G || G.phase!=="race" || G.answered || !G.q) return;
  var q = G.q, ok = q.type==="tone" ? i===toneOf(q.w.py) : q.opts[i]===q.w, dt = (performance.now() - G.qStart)/1000;
  G.answered = true; G.pick = i; G.n++;
  var r = G.results[q.w.zh] || (G.results[q.w.zh] = {ok:0, bad:0});
  noteResult(q.w.zh, ok);
  if(q.type==="tone"){ var tn = toneOf(q.w.py), rec = dayRec(); state.tones[tn].n++; rec.tones++; if(ok){ state.tones[tn].ok++; rec.toneOk++; } else { var ck = tn+">"+i; state.conf[ck] = (state.conf[ck]||0)+1; } }
  if(ok){
    r.ok++; G.ok++; G.combo++; G.maxCombo = Math.max(G.maxCombo, G.combo);
    var fast = Math.max(0, Math.min(4, (3.2 - dt)*1.5)), gain = 8.5 + fast + Math.min(3, Math.floor(G.combo/2));
    G.me = Math.min(100, G.me + gain); G.stroke = performance.now(); drum(G.combo >= 3);
    if(G.me >= 100 && !G.crossed){ G.crossed = true; G.crossT = G.raceT; }
    var H = ($("#race-canvas")||{}).clientHeight || 240;
    splashAt(G, G.meShown/100*WORLD + 20, H*0.885 + 6, 16, false);
    if(el){ var bb = el.getBoundingClientRect(); inkBurst(bb.left + bb.width/2, bb.top + bb.height/2, ["#c23a2c", "#d6ad4e", "#1d1a16"]); }
    if(G.combo===3) gameSay(SAY.c3[Math.floor(Math.random()*2)]);
    else if(G.combo===5) gameSay(pickOne(SAY.c5));
    else if(G.combo===8) gameSay(pickOne(SAY.c8));
    else if(fast > 2.8 && Math.random() < 0.5) gameSay(pickOne(SAY.fast));
    else if(Math.random() < 0.45) gameSay(pickOne(SAY.ok));
    renderRaceQ();
    if(G.crossed) gameSay("Ziel! Dein Drache schießt über die Linie!"); else later(gameNextQ, 450);
  } else {
    r.bad++; G.combo = 0; G.wob = 1; splashSound();
    var H2 = ($("#race-canvas")||{}).clientHeight || 240;
    splashAt(G, G.meShown/100*WORLD, H2*0.885, 34, true); G.pop = {text:"Platsch!", t:performance.now()};
    gameSay(pickOne(SAY.bad));
    renderRaceQ();
    playWord(q.w, 300);
    later(gameNextQ, 1500);
  }
  renderRaceHud();
}
function gameFrame(t){
  if(!G) return;
  var dt = G.last ? Math.min(0.05, (t - G.last)/1000) : 0; G.last = t;
  if(G.phase==="race"){
    var gap = G.opp - G.me, rub = gap > 18 ? 0.82 : (gap < -18 ? 1.12 : 1);
    G.opp = Math.min(100, G.opp + dt*(100/G.rival.time)*rub);
    G.raceT += dt;
    if(G.raceT - G.lastSay > 5.5){
      G.lastSay = G.raceT;
      var d2 = G.opp - G.meShown;
      if(Math.max(G.opp, G.meShown) > 82) gameSay(pickOne(SAY.final));
      else if(d2 > 12) gameSay(pickOne(G.rival.behind));
      else if(d2 < -12) gameSay(pickOne(G.rival.ahead));
      else if(Math.abs(d2) < 5 && G.raceT > 4) gameSay(pickOne(SAY.close));
    }
    if(G.crossed){ G.opp = Math.min(G.opp, 99); if(G.meShown >= 99.4) gameFinish(true); }
    else if(G.opp >= 100) gameFinish(false);
  }
  G.meShown += (G.me - G.meShown)*Math.min(1, dt*3.4);
  G.wob = Math.max(0, G.wob - dt*1.3);
  G.paddle += dt*(G.phase==="race" ? 5.5 + (G.combo >= 3 ? 3 : 0) : 1.5);
  var cv = $("#race-canvas");
  if(cv){
    var s = sizeCanvas(cv), target = Math.max(-60, Math.min(G.meShown/100*WORLD - s.W*0.34, WORLD + 200 - s.W*0.85));
    G.cam += (target - G.cam)*Math.min(1, dt*3);
    if(G.phase==="done" && G.won && Math.random() < 0.06 && t - G.doneT < 5200) launchRocket(G.fw, s.W, s.H);
    drawRace(s.c, s.W, s.H, {me:G.meShown, opp:G.opp, cam:G.cam, rival:G.rival, parts:G.parts, fw:G.fw, phase:G.paddle, stroke:G.stroke, glow:G.combo >= 3 && G.phase==="race", wob:G.wob, pop:G.pop, cheer:G.combo >= 3 || G.phase==="done", oppPaddle:G.phase==="race" ? 1 : 0.4}, t);
    if(Math.floor(t/120) !== G.hudTick){ G.hudTick = Math.floor(t/120); renderRaceHud(); }
  }
  if(G.phase==="done" && t - G.doneT > 9000) return;
  gameRaf = requestAnimationFrame(gameFrame);
}
function gameFinish(won){
  if(!G || G.phase==="done") return;
  clearGameTimers();
  G.phase = "done"; G.won = won; G.doneT = performance.now(); G.time = won && G.crossT ? G.crossT : G.raceT;
  if(won) G.me = G.meShown = 100;
  /* Ergebnisse mit Wiederholung und Punkten abgleichen */
  var d = dayRec(), xp = G.ok + (won ? G.rival.bonus : 0);
  applyResults(G.results);
  d.xp += xp; d.games = (d.games||0) + 1;
  var gs = state.game || (state.game = {played:0, wins:{}, best:{}});
  gs.played++;
  if(won){ gs.wins[G.rival.id] = (gs.wins[G.rival.id]||0) + 1; var tm = Math.round(G.time*10)/10; if(!gs.best[G.rival.id] || tm < gs.best[G.rival.id]) { gs.best[G.rival.id] = tm; G.record = true; } }
  G.xp = xp;
  touch();
  if(won){ gong(); later(function(){ melody(true); }, 350); gameSay(G.rival.win); }
  else { melody(false); gameSay(G.rival.lose); }
  renderRaceQ();
}
function closeGame(){
  clearGameTimers(); cancelAnimationFrame(gameRaf); stopAll();
  var answered = G && G.n > 0 && G.phase!=="done";
  G = null; var ov = $("#game"); ov.hidden = true; ov.innerHTML = ""; document.body.style.overflow = ""; $("#app").inert = false;
  if(answered) touch();
  route();
}

/* ---------- Oberfläche ---------- */
function panda(){
  return '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="11" cy="12" r="7" fill="#1d1a16"/><circle cx="37" cy="12" r="7" fill="#1d1a16"/><circle cx="24" cy="25" r="17" fill="#fbf6ea" stroke="#1d1a16" stroke-width="1.5"/>'+
    '<ellipse cx="17" cy="24" rx="5" ry="6.5" fill="#1d1a16" transform="rotate(-20 17 24)"/><ellipse cx="31" cy="24" rx="5" ry="6.5" fill="#1d1a16" transform="rotate(20 31 24)"/>'+
    '<circle cx="17.6" cy="23.4" r="1.8" fill="#fff"/><circle cx="30.4" cy="23.4" r="1.8" fill="#fff"/><ellipse cx="24" cy="30" rx="3" ry="2" fill="#1d1a16"/>'+
    '<path d="M20 33.5 q4 3.5 8 0" fill="none" stroke="#1d1a16" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="31" r="2.6" fill="#e8a0a8" opacity=".7"/><circle cx="36" cy="31" r="2.6" fill="#e8a0a8" opacity=".7"/>'+
    '<path d="M18 43 l6 -3 l6 3 l-6 3 z" fill="#c23a2c"/></svg>';
}
function portrait(id){
  var skin = "#ecc9a0", ink = "#1d1a16", h = '<svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="38" fill="'+({wang:"#dfe8df", li:"#e3e8f3", long:"#f2dfd9"})[id]+'"/>';
  if(id==="wang"){
    h += '<path d="M18 40 q-2 -8 4 -12 M62 40 q2 -8 -4 -12" stroke="#d9d4ca" stroke-width="6" stroke-linecap="round" fill="none"/>'+
      '<ellipse cx="40" cy="40" rx="20" ry="22" fill="'+skin+'"/><path d="M24 30 q16 -14 32 0" fill="#f4efe6" opacity=".9"/>'+
      '<circle cx="32" cy="40" r="5" fill="none" stroke="'+ink+'" stroke-width="1.6"/><circle cx="48" cy="40" r="5" fill="none" stroke="'+ink+'" stroke-width="1.6"/><path d="M37 40 h6" stroke="'+ink+'" stroke-width="1.4"/>'+
      '<path d="M30 40 q2 -2 4 0 M46 40 q2 -2 4 0" stroke="'+ink+'" stroke-width="1.4" fill="none"/>'+
      '<path d="M30 50 q10 22 20 0 q-10 6 -20 0 z" fill="#f4efe6" stroke="#d9d4ca"/><path d="M35 50 q5 3 10 0" stroke="'+ink+'" stroke-width="1.4" fill="none"/>'+
      '<g transform="translate(58 58)"><path d="M-7 -5 h14 l-2 10 h-10 z" fill="#fbf6ea" stroke="'+ink+'" stroke-width="1.2"/><path d="M7 -2 q4 0 3 4 q-1 2 -4 1" fill="none" stroke="'+ink+'" stroke-width="1.2"/><path d="M-2 -9 q-2 -3 0 -6 M2 -9 q-2 -3 0 -6" stroke="#9aa09a" stroke-width="1" fill="none"/></g>';
  } else if(id==="li"){
    h += '<circle cx="40" cy="18" r="9" fill="'+ink+'"/><rect x="45" y="12" width="9" height="3" rx="1.5" fill="#c23a2c" transform="rotate(-25 45 12)"/>'+
      '<ellipse cx="40" cy="42" rx="19" ry="21" fill="'+skin+'"/><path d="M21 38 q4 -18 19 -18 q15 0 19 18 q-6 -10 -19 -11 q-13 1 -19 11 z" fill="'+ink+'"/>'+
      '<path d="M31 42 q3 -3 6 0 M43 42 q3 -3 6 0" stroke="'+ink+'" stroke-width="1.8" fill="none" stroke-linecap="round"/>'+
      '<path d="M32 51 q8 9 16 0 z" fill="#8a2a22"/><path d="M34 52 q6 2 12 0" stroke="#fff" stroke-width="1.6" fill="none"/>'+
      '<circle cx="27" cy="49" r="3.2" fill="#e8a0a8" opacity=".75"/><circle cx="53" cy="49" r="3.2" fill="#e8a0a8" opacity=".75"/><circle cx="21" cy="50" r="2" fill="#d6ad4e"/><circle cx="59" cy="50" r="2" fill="#d6ad4e"/>';
  } else {
    h += '<circle cx="40" cy="16" r="6" fill="'+ink+'"/><ellipse cx="40" cy="42" rx="19" ry="22" fill="'+skin+'"/><path d="M21 36 q4 -16 19 -16 q15 0 19 16 q-8 -6 -19 -6 q-11 0 -19 6 z" fill="'+ink+'"/>'+
      '<rect x="21" y="29" width="38" height="6" fill="#c23a2c"/><path d="M59 31 l9 -3 l-3 7 z" fill="#c23a2c"/>'+
      '<path d="M29 40 l8 2 M51 40 l-8 2" stroke="'+ink+'" stroke-width="2.4" stroke-linecap="round"/><circle cx="34" cy="45" r="1.8" fill="'+ink+'"/><circle cx="46" cy="45" r="1.8" fill="'+ink+'"/>'+
      '<path d="M32 53 q8 -4 16 0" stroke="'+ink+'" stroke-width="2" fill="none" stroke-linecap="round"/><path d="M33 56 q7 3 14 0" stroke="'+ink+'" stroke-width="1.2" fill="none"/>';
  }
  return h + '</svg>';
}
function stars(n){ var h = ""; for(var i=1;i<=3;i++) h += '<i class="'+(i<=n ? "on" : "")+'"></i>'; return '<span class="stars" aria-label="Stufe '+n+' von 3">'+h+'</span>'; }
function renderLobby(){
  var v = $("#view-spiel"); if(!v) return;
  var ready = gameReady(), gs = state.game || {played:0, wins:{}, best:{}}, due = dueWords().length, n = learnedWords().length;
  var h = '<div class="lobby-hero"><canvas id="lobby-canvas" aria-label="Zwei Drachenboote auf dem Fluss"></canvas>'+
    '<div class="lobby-title"><span class="brush" lang="zh" aria-hidden="true">龙舟赛</span><h1 class="lt-de" id="h-spiel">Drachenboot-Rennen</h1></div></div>';
  h += '<p class="subtitle" style="max-width:62ch">Jede richtige Antwort zu deinen gelernten Wörtern ist ein Paddelschlag. Antworte schnell für mehr Schwung, schaff mehrere in Folge für eine Serie. Falsche Antworten kosten Zeit und landen wieder beim Wiederholen.</p>';
  h += '<div class="statline"><span><span class="sl"><span class="seal" style="background:var(--ink);color:var(--paper)" aria-hidden="true">词</span><b>'+n+'</b></span>Wörter im Rennen</span>'+
    '<span><span class="sl"><span class="seal" aria-hidden="true">复</span><b>'+due+'</b></span>fällig, kommen zuerst</span>'+
    '<span><span class="sl"><span class="seal" style="background:var(--gold)" aria-hidden="true">赛</span><b>'+(gs.played||0)+'</b></span>Rennen gefahren</span></div>';
  if(!ready) h += '<div class="card" style="padding:16px 18px; margin-top:14px"><b>Noch zu wenig Wörter.</b> Fürs Rennen brauchst du mindestens 4 gelernte Wörter. Mach zuerst Lektion 1.<div style="margin-top:12px"><a class="btn red" href="#lernen">Zum Lernpfad</a></div></div>';
  h += '<h2 class="sec">Wähl deinen Gegner</h2><div class="rivals">'+RIVALS.map(function(r){
    var wins = gs.wins[r.id]||0, best = gs.best[r.id];
    return '<div class="rival"><div class="rv-face">'+portrait(r.id)+'</div><div class="rv-body"><div class="rv-name"><span class="hz" lang="zh">'+esc(r.zh)+'</span> <span class="rvl-py">'+pyHTML(r.py)+'</span></div>'+
      '<div class="rv-de">'+esc(r.de)+' · '+esc(r.tag)+' '+stars(r.stars)+'</div><p class="rv-intro">'+esc(r.intro)+'</p>'+
      '<div class="rv-rec">'+(wins ? plural(wins, "Sieg", "Siege")+(best ? ", Bestzeit "+String(best).replace(".", ",")+" s" : "") : "Noch nicht besiegt")+'</div>'+
      '<button type="button" class="btn red" data-race="'+r.id+'"'+(ready ? "" : " disabled")+'>Antreten</button></div></div>';
  }).join("")+'</div>';
  h += '<p class="muted" style="font-size:13.5px; margin-top:18px">Tipp: 爷爷 yéye heißt Opa, 阿姨 āyí Tante und 师傅 shīfu Meister. So lernst du nebenbei, wie man Leute anspricht.</p>';
  v.innerHTML = h;
  lobbyLoop();
}
function renderRace(){
  var ov = $("#game");
  ov.innerHTML = '<div class="race-top"><button type="button" class="s-close" data-gact="close" aria-label="Rennen beenden">✕</button><div class="race-hud" id="race-hud"></div><span class="combo" id="race-combo"></span></div>'+
    '<div class="race-stage"><canvas id="race-canvas" aria-label="Rennen auf dem Fluss"></canvas><div class="race-count" id="race-count" aria-live="assertive"></div></div>'+
    '<div class="race-say"><span class="panda">'+panda()+'</span><p id="race-say" aria-live="polite">'+esc(G.say)+'</p></div>'+
    '<div class="race-q" id="race-q"></div>';
  renderRaceHud(); renderRaceQ();
}
function renderRaceHud(){
  var el = $("#race-hud"); if(!el || !G) return;
  var me = Math.round(G.meShown/100*RACE_M), op = Math.round(G.opp/100*RACE_M);
  el.innerHTML = '<div class="hud-track"><i class="hud-me" style="left:'+(G.meShown).toFixed(1)+'%"></i><i class="hud-op" style="left:'+(G.opp).toFixed(1)+'%; background:'+G.rival.hull+'"></i></div>'+
    '<div class="hud-num"><span><b>Du</b> '+me+' m</span><span>'+esc(G.rival.zh)+' '+op+' m</span><span class="muted">Ziel '+RACE_M+' m</span></div>';
  var cb = $("#race-combo"); if(cb){ cb.innerHTML = G.combo >= 2 ? '<span lang="zh">连击</span> ×'+G.combo : ""; cb.classList.toggle("hot", G.combo >= 3); }
  if(G.confirm){ var cl = $('[data-gact="close"]'); if(cl){ cl.classList.add("confirm"); cl.textContent = "Wirklich beenden?"; } }
}
function renderRaceQ(){
  var box = $("#race-q"); if(!box || !G) return;
  if(G.phase==="count"){ box.innerHTML = '<div class="rq-wait">Mach dich bereit …</div>'; return; }
  if(G.phase==="done"){ box.innerHTML = renderRaceResult(); var b = $("#race-again"); if(b) b.focus({preventScroll:true}); return; }
  var q = G.q; if(!q) return;
  var w = q.w, ans = G.answered, h = '<div class="rq-head">';
  var cls = function(i, right){ return !ans ? "" : right ? " right" : (G.pick===i ? " wrong" : " dim"); };
  if(q.type==="hear") h += '<button type="button" class="rq-play" data-gact="play" aria-label="Nochmal anhören">'+ICON_SPK_BIG+'</button><div><span class="rq-k">Was hörst du?</span>'+(ans ? '<b class="hz" lang="zh">'+esc(w.zh)+'</b> '+pyHTML(w.py) : '')+'</div>';
  else if(q.type==="mean") h += '<button type="button" class="rq-zi hz" data-gact="play" lang="zh">'+esc(w.zh)+'</button><div><span class="rq-k">Was bedeutet das?</span>'+(state.prefs.pinyin || ans ? '<span class="rq-py">'+pyHTML(w.py)+'</span>' : '')+'</div>';
  else if(q.type==="char") h += '<div><span class="rq-k">Welches Zeichen heißt</span><b class="rq-de">„'+esc(w.de)+'“</b></div>';
  else h += '<button type="button" class="rq-zi hz" data-gact="play" lang="zh">'+esc(w.zh)+'</button><div><span class="rq-k">Welcher Ton?</span><span class="rq-py">'+(ans ? pyHTML(w.py) : esc(toneless(w.py)))+'</span></div>';
  h += '</div>'+(ans ? '' : '<div class="rq-timer"><i></i></div>');
  if(q.type==="tone"){
    var tn = toneOf(w.py);
    h += '<div class="rq-opts">'+[1,2,3,4].map(function(k){ return '<button type="button" class="rq-opt tone'+cls(k, k===tn)+'" data-gopt="'+k+'" style="--tc:var(--t'+k+')"'+(ans ? " disabled" : "")+'><span class="mk">'+TONE_MARK[k]+'</span>'+toneCurve(k)+'<small>'+k+'. Ton</small></button>'; }).join("")+'</div>';
  } else {
    h += '<div class="rq-opts">'+q.opts.map(function(o, i){
      var inner = q.type==="char" ? '<span class="hz" lang="zh">'+esc(o.zh)+'</span>'+(state.prefs.pinyin ? '<small>'+pyHTML(o.py)+'</small>' : '') : esc(o.de);
      return '<button type="button" class="rq-opt'+(q.type==="char" ? " zh" : "")+cls(i, o===w)+'" data-gopt="'+i+'"'+(ans ? " disabled" : "")+'><span class="k">'+(i+1)+'</span>'+inner+'</button>'; }).join("")+'</div>';
  }
  if(ans && G.pick!==null && !(q.type==="tone" ? G.pick===toneOf(w.py) : q.opts[G.pick]===w)) h += '<p class="rq-fix">Richtig: <span class="hz" lang="zh">'+esc(w.zh)+'</span> '+pyHTML(w.py)+' · '+esc(w.de)+'</p>';
  box.innerHTML = h;
}
function renderRaceResult(){
  var won = G.won, r = G.rival, words = Object.keys(G.results);
  var h = '<div class="rr"><div class="rr-head"><span class="rr-seal'+(won ? "" : " lost")+'" aria-hidden="true">'+(won ? "胜" : "输")+'</span><div><b class="rr-title">'+(won ? "Gewonnen!" : "Knapp verloren")+'</b>'+
    '<span class="rr-sub"><span class="hz" lang="zh">'+(won ? "胜" : "输")+'</span> '+(won ? '<span class="py t4">shèng</span> heißt Sieg' : '<span class="py t1">shū</span> heißt verlieren')+(G.record ? " · Neue Bestzeit!" : "")+'</span></div></div>'+
    '<div class="rr-stats"><span><b>'+(Math.round(G.time*10)/10).toString().replace(".", ",")+' s</b>Zeit</span><span><b>'+G.ok+'/'+G.n+'</b>richtig</span><span><b>'+G.maxCombo+'</b>beste Serie</span><span><b>+'+G.xp+'</b>Punkte</span></div>';
  h += '<div class="rr-words">'+words.map(function(zh){ var w = WORD[zh], res = G.results[zh], ok = res.bad===0;
    return '<button type="button" class="rr-w'+(ok ? "" : " bad")+'" data-word="'+esc(zh)+'"><span class="m">'+(ok ? "✓" : "✗")+'</span><span class="hz" lang="zh">'+esc(zh)+'</span><span>'+pyHTML(w.py)+' · '+esc(w.de)+'</span></button>'; }).join("")+'</div>';
  if(words.some(function(zh){ return G.results[zh].bad; })) h += '<p class="muted" style="font-size:13.5px; margin:6px 0 0">Die Wörter mit ✗ kommen heute beim Wiederholen nochmal dran.</p>';
  h += '<div class="rr-actions"><button type="button" class="btn red" id="race-again" data-race="'+r.id+'">Revanche</button><button type="button" class="btn light" data-gact="lobby">Anderer Gegner</button><button type="button" class="btn light" data-gact="close">Fertig</button></div></div>';
  return h;
}
function gameClick(el){
  var ds = el.dataset;
  if(ds.race){ startGame(ds.race); return true; }
  if(ds.gopt!==undefined){ gameAnswer(+ds.gopt, el); return true; }
  if(ds.gact==="play"){ if(G && G.q) playWord(G.q.w); return true; }
  if(ds.gact==="lobby"){ closeGame(); location.hash = "spiel"; return true; }
  if(ds.gact==="close"){
    if(!G || G.phase==="done" || G.confirm){ closeGame(); return true; }
    G.confirm = true; renderRaceHud();
    later(function(){ if(G && G.confirm){ G.confirm = false; var cl = $('[data-gact="close"]'); if(cl){ cl.classList.remove("confirm"); cl.textContent = "✕"; } } }, 3500);
    return true;
  }
  return false;
}
function gameKey(e){
  if(!G) return false;
  var tag = e.target.tagName, onCtl = (tag==="BUTTON" || tag==="INPUT" || tag==="SELECT" || tag==="A") && !!(e.target.closest && e.target.closest("#game"));
  if(!onCtl && e.key==="Enter"){ e.preventDefault(); return true; }
  if(e.key==="Escape"){ e.preventDefault(); var cl = $('[data-gact="close"]'); if(cl) gameClick(cl); return true; }
  if(G.phase==="race" && !G.answered && G.q && /^[1-4]$/.test(e.key)){
    var k = +e.key; e.preventDefault();
    var btn = $('[data-gopt="'+(G.q.type==="tone" ? k : k-1)+'"]');
    if(btn) gameAnswer(G.q.type==="tone" ? k : k-1, btn);
    return true;
  }
  if(e.key===" " && !onCtl && G.q){ e.preventDefault(); playWord(G.q.w); return true; }
  return true;
}
