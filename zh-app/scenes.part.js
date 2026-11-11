/* ================= Tusche-Szenen der Reise ================= */
var INK = "#26231e", INK2 = "#4a463e", RED = "#c23a2c", RED2 = "#9e3427", GOLD = "#c49a3e", PAPER = "#f3ead6", STONE = "#8e8a80";
function rng(seed){ var s = seed % 2147483647; if(s<=0) s += 2147483646; return function(){ s = s*16807 % 2147483647; return (s-1)/2147483646; }; }
function ridge(seed, base, amp, n, x0, x1){
  x0 = x0||0; x1 = x1||360;
  var r = rng(seed), step = (x1-x0)/n, prevY = base - amp*(0.3+0.5*r()), d = "M"+x0+" 180 L"+x0+" "+prevY.toFixed(1);
  for(var i=1;i<=n;i++){
    var x = x0 + i*step, y = base - amp*(0.25+0.5*r()), peak = Math.min(prevY, y) - amp*(0.25+0.45*r()), px = x - step*(0.35+0.3*r());
    d += " C"+(x-step+step*0.25).toFixed(1)+" "+prevY.toFixed(1)+" "+(px-step*0.18).toFixed(1)+" "+peak.toFixed(1)+" "+px.toFixed(1)+" "+peak.toFixed(1);
    d += " C"+(px+step*0.16).toFixed(1)+" "+peak.toFixed(1)+" "+(x-step*0.2).toFixed(1)+" "+y.toFixed(1)+" "+x.toFixed(1)+" "+y.toFixed(1);
    prevY = y;
  }
  return d + " L"+x1+" 180 Z";
}
function mtn(seed, base, amp, n, grad, extra){ return '<path d="'+ridge(seed, base, amp, n)+'" fill="url(#'+grad+')" filter="url(#rough)" '+(extra||"")+'/>'; }
function mist(y, h, op){ return '<ellipse cx="180" cy="'+y+'" rx="230" ry="'+h+'" fill="'+PAPER+'" opacity="'+(op||0.9)+'" filter="url(#blur6)"/>'; }
function sun(cx, cy, r){ return '<circle cx="'+cx+'" cy="'+cy+'" r="'+(r+8)+'" fill="'+RED+'" opacity=".12" filter="url(#blur6)"/><circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="'+RED+'" opacity=".92"/>'; }
function birds(x, y, n){ var h = ""; for(var i=0;i<n;i++){ var bx = x + i*13 + (i%2)*4, by = y + (i%3)*5; h += '<path d="M'+bx+' '+by+' q3 -3 6 0 q3 -3 6 0" fill="none" stroke="'+INK+'" stroke-width="1.2" stroke-linecap="round"/>'; } return h; }
/* Chinesisches Dach mit hochgezogenen Ecken: x1..x2 Breite, y Traufe, h Höhe */
function roof(x1, x2, y, h, fill){
  var w = x2 - x1, c = Math.min(14, w*0.12);
  return '<path d="M'+(x1-c)+' '+(y+1)+' Q'+(x1+c*0.6)+' '+(y-1)+' '+(x1+c*1.2)+' '+(y-h)+' L'+(x2-c*1.2)+' '+(y-h)+' Q'+(x2-c*0.6)+' '+(y-1)+' '+(x2+c)+' '+(y+1)+' Q'+(x2-c*0.2)+' '+(y+4)+' '+(x2-c*0.8)+' '+(y+3)+' L'+(x1+c*0.8)+' '+(y+3)+' Q'+(x1+c*0.2)+' '+(y+4)+' '+(x1-c)+' '+(y+1)+' Z" fill="'+(fill||INK)+'"/>'+
    '<path d="M'+(x1+c*1.1)+' '+(y-h)+' L'+(x2-c*1.1)+' '+(y-h)+'" stroke="'+(fill||INK)+'" stroke-width="2.4" stroke-linecap="round"/>';
}
function lantern(x, y, s){
  s = s||1;
  return '<g transform="translate('+x+' '+y+') scale('+s+')"><line x1="0" y1="-12" x2="0" y2="-7" stroke="'+INK+'" stroke-width="1"/>'+
    '<rect x="-3.5" y="-8" width="7" height="2.2" rx="1" fill="'+GOLD+'"/><ellipse cx="0" cy="0" rx="7" ry="8" fill="'+RED+'"/>'+
    '<path d="M-3.5 -6.5 Q-5 0 -3.5 6.5 M0 -8 V8 M3.5 -6.5 Q5 0 3.5 6.5" stroke="'+RED2+'" stroke-width=".8" fill="none"/>'+
    '<rect x="-3.5" y="6" width="7" height="2.2" rx="1" fill="'+GOLD+'"/><line x1="0" y1="8" x2="0" y2="14" stroke="'+GOLD+'" stroke-width="1.2"/></g>';
}
function willow(x, n, len, seed){
  var r = rng(seed||5), h = '<g stroke="#5b6a58" fill="none" stroke-linecap="round" opacity=".85">';
  for(var i=0;i<n;i++){ var sx = x + i*7 + r()*5, l = len*(0.6+0.5*r()), bend = (r()-0.5)*14;
    h += '<path d="M'+sx.toFixed(1)+' -4 Q'+(sx+bend).toFixed(1)+' '+(l*0.5).toFixed(1)+' '+(sx+bend*0.6).toFixed(1)+' '+l.toFixed(1)+'" stroke-width="1.1"/>'+
         '<path d="M'+sx.toFixed(1)+' -4 Q'+(sx+bend).toFixed(1)+' '+(l*0.5).toFixed(1)+' '+(sx+bend*0.6).toFixed(1)+' '+l.toFixed(1)+'" stroke-width="3" stroke-dasharray="2 5" opacity=".7"/>'; }
  return h + '</g>';
}
function waterLines(y0, y1, seed, col){
  var r = rng(seed), h = "";
  for(var i=0;i<16;i++){ var x = r()*340, y = y0 + r()*(y1-y0), w = 10 + r()*34; h += '<path d="M'+x.toFixed(0)+' '+y.toFixed(0)+' h'+w.toFixed(0)+'" stroke="'+(col||"#7f8f8b")+'" stroke-width="1.1" stroke-linecap="round" opacity=".55"/>'; }
  return h;
}
function ground(y, col, op){ return '<path d="M0 '+y+' Q90 '+(y-6)+' 180 '+(y-2)+' T360 '+(y-4)+' L360 180 L0 180 Z" fill="'+(col||"#d6cab0")+'" opacity="'+(op||0.7)+'"/>'; }

var SCENES = {
  gate: function(){
    var cols = ""; for(var x=130;x<=230;x+=12.5) cols += '<rect x="'+x+'" y="90" width="3" height="20" fill="'+RED2+'"/>';
    var cols2 = ""; for(var x2=146;x2<=214;x2+=11.3) cols2 += '<rect x="'+x2+'" y="64" width="2.6" height="16" fill="'+RED2+'"/>';
    return sun(270, 52, 24) + mtn(11, 112, 46, 5, "mFar") + mist(122, 14) +
      '<g transform="translate(26 40) rotate(-14)"><path d="M0 0 L22 -2 L28 -1 L22 2 Z M9 -1 L4 -9 L8 -9 L14 -1 Z M9 1 L4 8 L8 8 L14 1 Z M1 0 L-3 -4 L-1 -4 L3 0 Z" fill="'+INK+'"/></g>'+
      '<path d="M-10 66 Q8 58 24 46" stroke="'+INK+'" stroke-width="1" stroke-dasharray="3 4" fill="none" opacity=".5"/>' +
      ground(156) +
      '<path d="M94 156 L102 114 L258 114 L266 156 Z" fill="#a33b2b" filter="url(#rough)"/>'+
      '<rect x="98" y="110" width="164" height="5" fill="'+INK+'"/>'+
      '<path d="M169 156 V138 a11 11 0 0 1 22 0 V156 Z M130 156 V146 a7 7 0 0 1 14 0 V156 Z M216 156 V146 a7 7 0 0 1 14 0 V156 Z" fill="#2a1d18"/>'+
      '<rect x="122" y="88" width="116" height="22" fill="#b5462f"/>' + cols +
      '<rect x="120" y="108" width="120" height="3" fill="'+INK+'"/>'+
      roof(120, 240, 90, 11) +
      '<rect x="140" y="62" width="80" height="18" fill="#b5462f"/>' + cols2 +
      roof(134, 226, 64, 13) +
      '<circle cx="150" cy="50" r="2" fill="'+GOLD+'"/><circle cx="210" cy="50" r="2" fill="'+GOLD+'"/>'+
      '<rect x="172" y="68" width="16" height="8" fill="'+GOLD+'" opacity=".9"/>'+
      '<g fill="#566552" opacity=".85" filter="url(#rough)"><ellipse cx="40" cy="146" rx="22" ry="12"/><ellipse cx="62" cy="150" rx="16" ry="9"/><ellipse cx="318" cy="147" rx="24" ry="12"/></g>';
  },
  hutong: function(){
    var tiles = ""; for(var x=-4;x<=364;x+=7) tiles += '<circle cx="'+x+'" cy="99" r="3.4" fill="#3b3833"/>';
    var bricks = ""; for(var y=108;y<=156;y+=7) bricks += '<path d="M0 '+y+' H360" stroke="#77736b" stroke-width=".6" opacity=".5"/>';
    return mtn(4, 84, 30, 4, "mFar", 'opacity=".55"') + birds(250, 30, 4) +
      '<rect x="0" y="98" width="360" height="62" fill="#9b968c"/>' + bricks +
      '<rect x="-4" y="90" width="368" height="9" fill="#3b3833"/>' + tiles +
      '<rect x="146" y="80" width="88" height="20" fill="#9b968c"/>'+
      roof(146, 234, 82, 12) +
      '<rect x="160" y="96" width="60" height="60" fill="#2a1d18"/>'+
      '<rect x="164" y="100" width="25" height="56" fill="#a8342a"/><rect x="191" y="100" width="25" height="56" fill="#a8342a"/>'+
      '<circle cx="185" cy="128" r="2.6" fill="'+GOLD+'"/><circle cx="195" cy="128" r="2.6" fill="'+GOLD+'"/>'+
      '<rect x="151" y="100" width="6" height="48" fill="'+RED+'"/><rect x="223" y="100" width="6" height="48" fill="'+RED+'"/>'+
      '<path d="M154 106 v34 M226 106 v34" stroke="'+GOLD+'" stroke-width="1.2" stroke-dasharray="3 3"/>'+
      lantern(150, 104, 1) + lantern(230, 104, 1) +
      '<rect x="156" y="156" width="68" height="4" fill="#6f6b63"/>' +
      '<g filter="url(#rough)"><path d="M58 160 C56 130 62 110 52 86 M56 120 C70 108 84 104 92 92 M54 104 C42 96 34 90 30 78" stroke="'+INK+'" stroke-width="4" fill="none" stroke-linecap="round"/>'+
      '<g fill="#56654f" opacity=".82"><ellipse cx="50" cy="76" rx="30" ry="16"/><ellipse cx="86" cy="86" rx="22" ry="12"/><ellipse cx="28" cy="92" rx="18" ry="10"/><ellipse cx="70" cy="66" rx="20" ry="10"/></g></g>'+
      '<g stroke="'+INK+'" stroke-width="2" fill="none" stroke-linecap="round"><circle cx="268" cy="148" r="10"/><circle cx="300" cy="148" r="10"/>'+
      '<path d="M268 148 L280 132 L296 132 L300 148 M280 132 L286 148 L296 132 M276 128 h8 M296 132 l-2 -6 h6"/></g>' + ground(160, "#cfc3a8", 0.9);
  },
  wall: function(){
    var towers = [[96,128],[206,110],[318,94]].map(function(t){
      return '<g transform="translate('+t[0]+' '+t[1]+')"><rect x="-8" y="-20" width="16" height="20" fill="#7d6a52" stroke="'+INK+'" stroke-width="1"/>'+
        '<path d="M-9 -20 v-4 h4 v4 h3 v-4 h4 v4 h3 v-4 h4 v4" fill="#7d6a52" stroke="'+INK+'" stroke-width="1"/><rect x="-2.5" y="-14" width="5" height="7" fill="'+INK+'"/></g>';
    }).join("");
    var top = "M-10 140 Q50 118 96 128 Q150 140 206 110 Q262 82 370 98";
    return sun(86, 48, 22) + mtn(21, 92, 42, 5, "mFar") + mist(104, 12) + mtn(7, 126, 40, 4, "mMid") + mist(136, 10, 0.7) +
      '<path d="'+top+' L370 180 L-10 180 Z" fill="url(#mNear)" filter="url(#rough)"/>'+
      '<path d="'+top+'" fill="none" stroke="#7d6a52" stroke-width="8" stroke-linecap="round"/>'+
      '<path d="'+top+'" fill="none" stroke="'+INK+'" stroke-width="3" stroke-dasharray="3 3" transform="translate(0 -5)"/>'+
      towers + birds(150, 36, 5) + mist(170, 14, 0.8);
  },
  tea: function(){
    var cols = [76, 104, 156, 184].map(function(x){ return '<rect x="'+x+'" y="80" width="4.5" height="32" fill="#a8342a"/>'; }).join("");
    return mtn(31, 96, 34, 4, "mFar", 'opacity=".8"') + mist(108, 12) +
      '<rect x="0" y="116" width="360" height="64" fill="url(#water)"/>' + waterLines(124, 176, 9) +
      '<g opacity=".18" transform="translate(0 232) scale(1 -1)">'+roof(54, 206, 116, 26)+cols+'</g>'+
      '<rect x="54" y="110" width="152" height="6" fill="'+INK+'"/><path d="M62 116 v8 M100 116 v8 M160 116 v8 M198 116 v8" stroke="'+INK+'" stroke-width="2"/>'+
      cols + '<path d="M70 102 H190" stroke="'+INK+'" stroke-width="1.4"/><path d="M70 98 H190" stroke="'+INK+'" stroke-width="1" stroke-dasharray="2 4"/>'+
      roof(54, 206, 82, 30) + '<circle cx="130" cy="48" r="3" fill="'+GOLD+'"/>' + lantern(130, 96, 0.8) +
      willow(268, 12, 82, 3) +
      '<g transform="translate(286 148)"><ellipse cx="0" cy="0" rx="30" ry="20" fill="#3a332c"/><ellipse cx="0" cy="-19" rx="13" ry="4" fill="#2a2520"/><circle cx="0" cy="-25" r="3.5" fill="#2a2520"/>'+
      '<path d="M-28 -6 Q-44 -10 -50 -24 L-46 -25 Q-40 -14 -27 -12 Z" fill="#3a332c"/><path d="M27 -10 Q44 -8 40 8 Q38 14 28 10" fill="none" stroke="#3a332c" stroke-width="5"/>'+
      '<path d="M-20 -4 Q0 4 20 -4" stroke="'+GOLD+'" stroke-width="1.2" fill="none"/></g>'+
      '<g transform="translate(236 162)"><path d="M-10 -10 h20 l-3 12 h-14 Z" fill="#3a332c"/></g>'+
      '<g fill="none" stroke="#8e968f" stroke-width="1.3" stroke-linecap="round" opacity=".7"><path d="M-50 -30 q-4 -8 2 -14 q6 -6 0 -14" transform="translate(286 148)"/><path d="M-44 -34 q-4 -8 2 -14 q6 -6 0 -12" transform="translate(286 148)"/><path d="M236 146 q-3 -6 1 -11 q4 -5 0 -10"/></g>';
  },
  market: function(){
    function lanterns(x0, y0, x1, y1, sag, n){
      var h = '<path d="M'+x0+' '+y0+' Q'+((x0+x1)/2)+' '+(Math.max(y0,y1)+sag)+' '+x1+' '+y1+'" stroke="'+INK+'" stroke-width="1" fill="none"/>';
      for(var i=1;i<n;i++){ var t = i/n, mx = (x0+x1)/2, my = Math.max(y0,y1)+sag;
        var x = (1-t)*(1-t)*x0 + 2*(1-t)*t*mx + t*t*x1, y = (1-t)*(1-t)*y0 + 2*(1-t)*t*my + t*t*y1;
        h += lantern(x.toFixed(1), (y+12).toFixed(1), 0.85); }
      return h;
    }
    function stall(x, w, col){
      var sc = ""; for(var i=0;i<w;i+=10) sc += '<path d="M'+(x+i)+' 112 q5 7 10 0" fill="'+col+'"/>';
      var fruit = ""; var r = rng(x+3); for(var j=0;j<9;j++) fruit += '<circle cx="'+(x+10+r()*(w-20)).toFixed(1)+'" cy="'+(130+r()*5).toFixed(1)+'" r="3.4" fill="'+["#d4622a","#c23a2c","#e0a43a","#6c8a4a"][j%4]+'"/>';
      return '<rect x="'+(x+3)+'" y="104" width="3" height="52" fill="'+INK2+'"/><rect x="'+(x+w-6)+'" y="104" width="3" height="52" fill="'+INK2+'"/>'+
        '<path d="M'+(x-4)+' 112 L'+(x+6)+' 96 L'+(x+w-6)+' 96 L'+(x+w+4)+' 112 Z" fill="'+col+'"/>' + sc +
        '<path d="M'+(x+8)+' 140 q'+((w-16)/2)+' 10 '+(w-16)+' 0 Z" fill="#8a6a4a"/>' + fruit +
        '<rect x="'+(x+4)+'" y="140" width="'+(w-8)+'" height="18" fill="#6b5442"/>';
    }
    return mtn(41, 70, 20, 3, "mFar", 'opacity=".4"') +
      '<g fill="#b9b2a2" opacity=".7"><rect x="10" y="64" width="70" height="50"/><rect x="290" y="58" width="64" height="56"/></g>'+
      roof(10, 80, 66, 10, "#7e786d") + roof(290, 354, 60, 10, "#7e786d") +
      lanterns(-6, 24, 366, 30, 34, 9) + lanterns(-6, 58, 366, 50, 22, 7) +
      stall(22, 120, RED) + stall(214, 122, "#2f5a54") +
      '<rect x="170" y="70" width="22" height="58" rx="2" fill="'+RED+'" stroke="'+GOLD+'" stroke-width="1.5"/>'+
      '<text x="181" y="108" text-anchor="middle" font-family="Ma Shan Zheng, KaiTi, serif" font-size="22" fill="'+GOLD+'">市</text>'+
      '<rect x="179" y="128" width="4" height="30" fill="'+INK2+'"/>' + ground(158, "#cfc3a8", 0.95);
  },
  train: function(){
    var piers = ""; for(var x=8;x<360;x+=44) piers += '<path d="M'+x+' 124 v38 h7 v-38" fill="#6f6b63"/><path d="M'+(x+7)+' 132 Q'+(x+29)+' 120 '+(x+44)+' 132" fill="none" stroke="#6f6b63" stroke-width="3"/>';
    return sun(300, 46, 20) + mtn(51, 90, 40, 5, "mFar") + mist(102, 10) + mtn(13, 118, 30, 4, "mMid", 'opacity=".8"') + mist(130, 10, 0.7) +
      '<rect x="0" y="140" width="360" height="40" fill="#bfc6a8" opacity=".6"/>' + waterLines(146, 176, 4, "#8f9a74") +
      piers + '<rect x="0" y="118" width="360" height="7" fill="#4a463e"/>'+
      '<path d="M54 116 L236 116 Q288 116 312 104 Q292 92 236 92 L54 92 Z" fill="#f7f4ec" stroke="'+INK+'" stroke-width="1.4"/>'+
      '<path d="M54 109 L240 109 Q280 109 300 102" stroke="'+RED+'" stroke-width="3" fill="none"/>'+
      '<path d="M66 99 H232" stroke="#3a3832" stroke-width="5" stroke-dasharray="11 5"/><path d="M262 96 Q286 97 298 103 L270 103 Z" fill="#3a3832"/>'+
      '<path d="M118 93 v22 M182 93 v22" stroke="'+INK+'" stroke-width="1" opacity=".5"/>'+
      '<g stroke="'+INK+'" stroke-width="1.6" stroke-linecap="round" opacity=".55"><path d="M8 98 H44 M18 106 H48 M4 112 H40"/></g>' + birds(60, 40, 3);
  },
  bund: function(){
    var bund = "", r = rng(77);
    for(var x=118;x<206;x+=22){ var h = 30 + r()*16; bund += '<rect x="'+x+'" y="'+(128-h)+'" width="21" height="'+h+'" fill="#4d4840"/><path d="M'+(x+4)+' '+(132-h)+' v'+(h-6)+' M'+(x+10)+' '+(132-h)+' v'+(h-6)+' M'+(x+16)+' '+(132-h)+' v'+(h-6)+'" stroke="#2c2924" stroke-width="1.2" opacity=".6"/>'; }
    return '<rect x="0" y="0" width="360" height="180" fill="#f1dfc8" opacity=".55"/>' + sun(318, 70, 20) +
      '<g fill="#9aa09a">'+
        '<rect x="258" y="70" width="3" height="58"/><circle cx="259.5" cy="98" r="9"/><circle cx="259.5" cy="76" r="6"/><circle cx="259.5" cy="58" r="3"/><rect x="258.6" y="38" width="1.8" height="20"/>'+
        '<path d="M252 128 L258 104 M267 128 L261 104" stroke="#9aa09a" stroke-width="2.4"/>'+
        '<rect x="226" y="96" width="14" height="32"/><rect x="242" y="108" width="10" height="20"/><rect x="276" y="90" width="14" height="38"/>'+
        '<path d="M294 128 L297 70 L309 64 L312 128 Z"/><path d="M330 128 L334 44 Q338 38 342 44 L346 128 Z"/><rect x="348" y="84" width="14" height="44"/></g>'+
      '<rect x="0" y="126" width="360" height="54" fill="url(#water)"/>' + waterLines(132, 176, 21) +
      '<path d="M306 136 h24 M312 142 h14 M316 148 h8" stroke="'+RED+'" stroke-width="2" opacity=".45" stroke-linecap="round"/>'+
      '<g filter="url(#rough)">'+ bund +
      '<rect x="0" y="80" width="118" height="48" fill="#4d4840"/><path d="M8 84 v40 M20 84 v40 M32 84 v40 M44 84 v40 M100 84 v40" stroke="#2c2924" stroke-width="1.4" opacity=".6"/>'+
      '<rect x="56" y="40" width="34" height="88" fill="#3d3832"/><path d="M52 40 L73 18 L94 40 Z" fill="'+INK+'"/><rect x="72" y="6" width="2" height="14" fill="'+INK+'"/></g>'+
      '<path d="M74 7 h9 v5 h-9" fill="'+RED+'"/>'+
      '<circle cx="73" cy="62" r="10" fill="#f6efe0" stroke="'+GOLD+'" stroke-width="2"/><path d="M73 62 V55 M73 62 H79" stroke="'+INK+'" stroke-width="1.8" stroke-linecap="round"/>'+
      '<g transform="translate(176 150)"><path d="M-26 0 H26 L20 8 H-20 Z" fill="'+INK+'"/><rect x="-14" y="-8" width="24" height="8" fill="#e8e2d2" stroke="'+INK+'"/><rect x="2" y="-14" width="4" height="6" fill="'+RED+'"/></g>';
  },
  water: function(){
    function house(x, y, w, h, flip){
      var step = w/4, top = y - h;
      var gable = flip
        ? 'M'+x+' '+top+' h'+step+' v-8 h'+step+' v-8 h'+step+' v8 h'+step+' v8'
        : 'M'+x+' '+top+' h'+step+' v-8 h'+step+' v-8 h'+step+' v8 h'+step+' v8';
      return '<rect x="'+x+'" y="'+top+'" width="'+w+'" height="'+h+'" fill="#f6f2e8" stroke="#a49e92" stroke-width="1"/>'+
        '<path d="'+gable+'" fill="none" stroke="'+INK+'" stroke-width="4" stroke-linejoin="miter"/>'+
        '<rect x="'+(x+w*0.2)+'" y="'+(top+h*0.35)+'" width="'+(w*0.18)+'" height="'+(h*0.22)+'" fill="'+INK2+'"/><rect x="'+(x+w*0.6)+'" y="'+(top+h*0.35)+'" width="'+(w*0.18)+'" height="'+(h*0.22)+'" fill="'+INK2+'"/>';
    }
    return mtn(61, 70, 26, 4, "mFar", 'opacity=".6"') + willow(-6, 9, 70, 8) +
      house(10, 120, 70, 44) + house(70, 118, 50, 36) + house(258, 118, 56, 40) + house(306, 120, 60, 46) +
      lantern(84, 96, 0.8) + lantern(262, 92, 0.8) +
      '<rect x="0" y="118" width="360" height="62" fill="url(#water)"/>' + waterLines(126, 176, 33) +
      '<path d="M108 120 Q180 50 252 120 L238 120 Q180 66 122 120 Z" fill="#8e8a80" filter="url(#rough)"/>'+
      '<path d="M108 120 Q180 50 252 120" fill="none" stroke="'+INK+'" stroke-width="1.6"/>'+
      '<path d="M100 118 h20 M240 118 h20" stroke="#8e8a80" stroke-width="5"/>'+
      '<g opacity=".3"><path d="M122 120 Q180 174 238 120" fill="none" stroke="#5e5a52" stroke-width="10"/></g>'+
      '<g transform="translate(70 152)"><path d="M-34 -2 Q0 10 34 -4 L30 4 Q0 14 -30 6 Z" fill="'+INK+'"/><path d="M-14 -4 Q-2 -18 12 -4 Z" fill="#3a3530"/>'+
      '<circle cx="24" cy="-14" r="3.4" fill="'+INK+'"/><path d="M18 -16 L24 -22 L30 -16 Z" fill="#8a6a3e"/><path d="M24 -11 L22 -2 M23 -8 L34 4" stroke="'+INK+'" stroke-width="1.8"/><path d="M34 4 L44 14" stroke="'+INK+'" stroke-width="1.2"/></g>' + birds(200, 26, 3);
  },
  /* ---------- Teil 2: Shanghai und Hangzhou ---------- */
  lane: function(){
    /* Shikumen-Gasse: Steintor mit schwarzen Türen, Wäsche über der Gasse */
    var bricks = ""; for(var y=70;y<=150;y+=8) bricks += '<path d="M0 '+y+' H130 M230 '+y+' H360" stroke="#7d776d" stroke-width=".6" opacity=".45"/>';
    var wins = function(x, y){ return '<rect x="'+x+'" y="'+y+'" width="22" height="26" fill="#3b3833"/><path d="M'+(x+11)+' '+y+' v26 M'+x+' '+(y+13)+' h22" stroke="#8b867c" stroke-width="1.2"/>'; };
    var clothes = ["#c23a2c", "#e8e2d2", "#5b7085", "#c49a3e", "#e8e2d2", "#8a5a44", "#5b6a58"], cl = "";
    clothes.forEach(function(c, i){ var x = 52 + i*38 + (i%2)*6, y = 34 + Math.sin(i*1.3)*3 + (i>2 && i<5 ? 4 : 0); cl += i%3===1
      ? '<path d="M'+x+' '+y+' h16 l3 18 h-8 l-1 -9 l-1 9 h-8 Z" fill="'+c+'" stroke="'+INK+'" stroke-width=".6"/>'
      : '<path d="M'+x+' '+y+' l-5 5 l3 4 l2 -2 v13 h16 v-13 l2 2 l3 -4 l-5 -5 Z" fill="'+c+'" stroke="'+INK+'" stroke-width=".6"/>'; });
    return '<rect x="0" y="0" width="360" height="180" fill="#efe4cf" opacity=".5"/>' + birds(290, 14, 3) +
      '<rect x="0" y="54" width="130" height="106" fill="#a49d91"/><rect x="230" y="54" width="130" height="106" fill="#a49d91"/>' + bricks +
      roof(-10, 132, 56, 8, "#3b3833") + roof(228, 372, 56, 8, "#3b3833") +
      wins(20, 70) + wins(80, 70) + wins(258, 70) + wins(318, 70) +
      '<rect x="18" y="112" width="26" height="40" fill="#2a2622"/><rect x="314" y="112" width="26" height="40" fill="#2a2622"/>'+
      /* Steintor */
      '<g filter="url(#rough)"><rect x="142" y="66" width="76" height="94" fill="#cfc6b5"/><path d="M136 68 Q180 30 224 68 Z" fill="#b9b0a0"/>'+
      '<path d="M146 66 Q180 40 214 66" fill="none" stroke="#8e8576" stroke-width="2"/><rect x="164" y="54" width="32" height="10" fill="#e9e2d3" stroke="#8e8576"/></g>'+
      '<path d="M170 59 h20" stroke="'+RED+'" stroke-width="2.2" stroke-linecap="round" opacity=".8"/>'+
      '<rect x="154" y="80" width="52" height="80" fill="#2b2420"/><rect x="157" y="83" width="22" height="77" fill="#1d1916"/><rect x="181" y="83" width="22" height="77" fill="#1d1916"/>'+
      '<circle cx="175" cy="118" r="3" fill="none" stroke="'+GOLD+'" stroke-width="1.4"/><circle cx="185" cy="118" r="3" fill="none" stroke="'+GOLD+'" stroke-width="1.4"/>'+
      '<path d="M157 100 h46 M157 140 h46" stroke="#3a332d" stroke-width="1.2"/>'+
      /* Wäscheleine mit Bambusstange */
      '<path d="M30 30 Q180 46 330 30" fill="none" stroke="#6b5a3e" stroke-width="2.2"/>' + cl +
      lantern(136, 84, 0.8) + lantern(224, 84, 0.8) +
      /* Fahrrad und Topfpflanze */
      '<g stroke="'+INK+'" stroke-width="1.8" fill="none" stroke-linecap="round"><circle cx="262" cy="150" r="9"/><circle cx="290" cy="150" r="9"/><path d="M262 150 L272 136 L286 136 L290 150 M272 136 L277 150 L286 136 M269 132 h7 M286 136 l-1 -5 h5"/></g>'+
      '<path d="M98 160 l4 -14 h14 l4 14 Z" fill="#8a5a44"/><g fill="#56654f"><ellipse cx="103" cy="140" rx="7" ry="5"/><ellipse cx="114" cy="138" rx="8" ry="5"/><ellipse cx="108" cy="132" rx="6" ry="5"/></g>' +
      ground(160, "#cfc3a8", 0.9);
  },
  school: function(){
    /* Sprachschule: Backsteinhaus mit großen Fenstern, Tafel, Platanen */
    var win = function(x){ return '<rect x="'+x+'" y="74" width="34" height="34" fill="#e9e2d3" stroke="'+INK+'" stroke-width="1.6"/><path d="M'+(x+17)+' 74 v34 M'+x+' 91 h34" stroke="'+INK+'" stroke-width="1.2"/>'; };
    var tree = function(x, s){ return '<g transform="translate('+x+' 0)"><path d="M0 160 C-2 130 4 112 -2 92 M-1 120 C8 110 16 106 22 96 M-1 108 C-10 100 -16 94 -20 86" stroke="#6f6a5e" stroke-width="'+(3.4*s)+'" fill="none" stroke-linecap="round"/>'+
      '<g fill="#6d7d5e" opacity=".85" filter="url(#rough)"><ellipse cx="0" cy="80" rx="'+(30*s)+'" ry="'+(18*s)+'"/><ellipse cx="22" cy="92" rx="'+(18*s)+'" ry="'+(11*s)+'"/><ellipse cx="-20" cy="92" rx="'+(17*s)+'" ry="'+(10*s)+'"/></g>'+
      '<g fill="#a4ad8a" opacity=".6"><circle cx="-8" cy="76" r="4"/><circle cx="10" cy="72" r="3"/><circle cx="16" cy="88" r="3.5"/></g></g>'; };
    return mtn(14, 74, 24, 4, "mFar", 'opacity=".45"') + birds(60, 22, 3) +
      '<rect x="92" y="56" width="176" height="104" fill="#b4796a"/>'+
      '<path d="M92 66 H268 M92 76 H268 M92 116 H268 M92 126 H268 M92 136 H268 M92 146 H268" stroke="#94594c" stroke-width=".7" opacity=".55"/>'+
      roof(86, 274, 58, 12) + win(104) + win(146) + win(188) + win(230) +
      /* Tafel im Fenster */
      '<rect x="150" y="80" width="26" height="16" fill="#3e4f45"/><path d="M163 82 Q162.5 89 156 94 M163.2 86.5 Q166 91 171 94" stroke="#e9e2d3" stroke-width="1.3" fill="none" stroke-linecap="round"/>'+
      '<rect x="160" y="118" width="40" height="42" fill="#3b2a22"/><path d="M180 118 v42" stroke="#1e1612" stroke-width="1.5"/>'+
      '<rect x="166" y="44" width="28" height="12" fill="#f3ead6" stroke="'+GOLD+'" stroke-width="1.4"/><circle cx="180" cy="50" r="3" fill="'+RED+'"/>'+
      tree(46, 1) + tree(318, 0.95) +
      '<g stroke="'+INK+'" stroke-width="1.6" fill="none" stroke-linecap="round"><circle cx="232" cy="152" r="7"/><circle cx="254" cy="152" r="7"/><path d="M232 152 L240 141 L251 141 L254 152 M240 141 L244 152 L251 141"/>'+
      '<circle cx="106" cy="152" r="7"/><circle cx="128" cy="152" r="7"/><path d="M106 152 L114 141 L125 141 L128 152 M114 141 L118 152 L125 141"/></g>' +
      ground(160, "#cfc3a8", 0.9);
  },
  street: function(){
    /* Nanjing-Straße am Abend: Leuchtschilder, Häuser, Menschen */
    var r = rng(41), people = "";
    for(var i=0;i<14;i++){ var x = 14 + i*25 + r()*10, h = 16 + r()*6; people += '<g fill="'+INK+'" opacity="'+(0.55+r()*0.4).toFixed(2)+'"><circle cx="'+x.toFixed(0)+'" cy="'+(150-h).toFixed(0)+'" r="3.2"/><path d="M'+(x-4).toFixed(0)+' '+(152-h+3).toFixed(0)+' h8 l2 '+(h-3).toFixed(0)+' h-12 Z"/></g>'; }
    var sign = function(x, y, h, col){ return '<rect x="'+x+'" y="'+y+'" width="14" height="'+h+'" rx="2" fill="'+col+'" stroke="#2a2622" stroke-width="1"/><rect x="'+(x+3)+'" y="'+(y+4)+'" width="8" height="'+(h-8)+'" rx="1" fill="#fff" opacity=".18"/>'+
      '<g fill="#fff" opacity=".6">'+[0,1,2].map(function(k){ return '<rect x="'+(x+4)+'" y="'+(y+7+k*(h-12)/3)+'" width="6" height="'+((h-12)/3-4)+'"/>'; }).join("")+'</g>'+
      '<rect x="'+(x-3)+'" y="'+(y-3)+'" width="20" height="'+(h+6)+'" rx="4" fill="'+col+'" opacity=".18" filter="url(#blur6)"/>'; };
    return '<rect x="0" y="0" width="360" height="180" fill="#e3d6c2" opacity=".55"/><circle cx="300" cy="28" r="10" fill="#f6efe0" stroke="#d8cdb6"/>'+
      '<g fill="#6d665c"><rect x="0" y="40" width="70" height="120"/><rect x="74" y="22" width="60" height="138"/><rect x="138" y="50" width="54" height="110"/><rect x="196" y="30" width="64" height="130"/><rect x="264" y="46" width="96" height="114"/></g>'+
      '<path d="M74 22 l30 -12 l30 12 Z M196 30 h64 l-6 -8 h-52 Z" fill="#4e4840"/>'+
      '<g fill="#d8c79a" opacity=".55">'+[[8,52],[30,52],[8,76],[30,76],[84,36],[110,36],[84,62],[110,62],[146,64],[168,64],[206,44],[234,44],[206,70],[234,70],[276,60],[300,60],[324,60],[276,84],[324,84]].map(function(p){ return '<rect x="'+p[0]+'" y="'+p[1]+'" width="14" height="12"/>'; }).join("")+'</g>'+
      sign(54, 70, 56, RED) + sign(122, 52, 66, GOLD) + sign(182, 78, 50, "#3f7f7a") + sign(250, 60, 60, RED) + sign(346, 74, 50, "#b5577a") +
      '<rect x="0" y="118" width="360" height="6" fill="#3b3833" opacity=".6"/>'+
      lantern(96, 112, 0.7) + lantern(222, 112, 0.7) + people +
      '<path d="M40 160 V118 M40 118 q8 -4 14 0" stroke="'+INK+'" stroke-width="1.6" fill="none"/><circle cx="54" cy="119" r="2.4" fill="'+GOLD+'"/>'+
      '<path d="M310 160 V118 M310 118 q-8 -4 -14 0" stroke="'+INK+'" stroke-width="1.6" fill="none"/><circle cx="296" cy="119" r="2.4" fill="'+GOLD+'"/>' +
      ground(160, "#bfb39c", 0.95);
  },
  garden: function(){
    /* Yu-Garten: Pavillon im Teich, Zickzackbrücke, Felsen, Katze */
    var lotus = ""; [[40,150],[70,162],[290,156],[322,148],[258,168]].forEach(function(p){ lotus += '<ellipse cx="'+p[0]+'" cy="'+p[1]+'" rx="11" ry="4" fill="#6d7d5e" opacity=".8"/><path d="M'+p[0]+' '+p[1]+' l7 -2" stroke="#4c5a43" stroke-width=".8"/>'; });
    return mtn(23, 70, 22, 4, "mFar", 'opacity=".4"') +
      '<rect x="0" y="112" width="360" height="68" fill="url(#water)"/>' + waterLines(118, 176, 52) + lotus +
      /* Felsen */
      '<g filter="url(#rough)"><path d="M0 120 C6 84 18 70 28 80 C34 62 52 66 50 86 C62 80 70 98 64 120 Z" fill="#8e8a80"/><path d="M14 96 q6 -6 10 2 M36 84 q4 4 0 10 M48 104 q6 -2 6 6" stroke="#5e5a52" stroke-width="2" fill="none"/>'+
      '<path d="M304 120 C300 96 312 86 322 92 C330 78 352 82 350 100 C360 104 362 116 360 120 Z" fill="#8e8a80"/><circle cx="330" cy="100" r="4" fill="#5e5a52"/></g>'+
      /* Pavillon */
      '<rect x="146" y="88" width="68" height="28" fill="#a8342a"/><rect x="150" y="92" width="60" height="20" fill="#3b2a22"/>'+
      '<path d="M152 96 h56 M152 104 h56 M166 92 v20 M180 92 v20 M194 92 v20" stroke="'+GOLD+'" stroke-width=".8" opacity=".7"/>'+
      roof(140, 220, 88, 10) + '<rect x="152" y="66" width="56" height="12" fill="#a8342a"/>' + roof(144, 216, 68, 10) +
      '<path d="M180 46 v12" stroke="'+INK+'" stroke-width="2"/><circle cx="180" cy="45" r="2.4" fill="'+GOLD+'"/>'+
      /* Zickzackbrücke */
      '<g stroke="#8e8a80" stroke-width="5" stroke-linecap="square" fill="none"><path d="M60 140 L104 128 L128 140 L146 118"/><path d="M214 118 L238 134 L262 124 L300 138"/></g>'+
      '<g stroke="'+INK+'" stroke-width="1" fill="none"><path d="M60 136 L104 124 L128 136 L146 114 M214 114 L238 130 L262 120 L300 134"/></g>'+
      '<g opacity=".25"><rect x="146" y="118" width="68" height="20" fill="#a8342a"/></g>'+
      /* Katze auf dem Felsen */
      '<g transform="translate(332 82)" fill="'+INK+'"><ellipse cx="0" cy="0" rx="9" ry="6"/><circle cx="-8" cy="-6" r="4.4"/><path d="M-11 -9 l1 -5 l3 3 Z M-6 -9 l1 -5 l2 4 Z"/><path d="M8 -1 q8 -2 6 -10" stroke="'+INK+'" stroke-width="2" fill="none" stroke-linecap="round"/></g>'+
      willow(240, 6, 54, 12) + birds(70, 24, 3);
  },
  lake: function(){
    /* Westsee in Hangzhou: Leifeng-Pagode, Weiden, Boot, Nieselregen */
    var rain = "", r = rng(9); for(var i=0;i<40;i++){ var x = r()*360, y = r()*120; rain += '<path d="M'+x.toFixed(0)+' '+y.toFixed(0)+' l-2 7" stroke="#8b9794" stroke-width=".8" opacity=".45"/>'; }
    var pagoda = '<g transform="translate(250 0)">';
    for(var k=0;k<5;k++){ var w = 30 - k*4, y = 84 - k*11; pagoda += '<rect x="'+(-w/2+2)+'" y="'+(y-8)+'" width="'+(w-4)+'" height="9" fill="#a8342a"/>' + roof(-w/2, w/2, y-7, 4); }
    pagoda += '<path d="M0 26 v-10" stroke="'+INK+'" stroke-width="1.6"/></g>';
    return mtn(31, 78, 34, 4, "mFar", 'opacity=".75"') + mtn(32, 96, 22, 5, "mMid", 'opacity=".45"') + mist(92, 14, 0.8) +
      '<path d="M210 96 Q250 78 292 96 Z" fill="#58625d" opacity=".55"/>' + pagoda +
      '<rect x="0" y="104" width="360" height="76" fill="url(#water)"/>' + waterLines(110, 176, 63) +
      /* Bogenbrücke */
      '<path d="M40 106 Q78 82 116 106" fill="none" stroke="#8e8a80" stroke-width="5" filter="url(#rough)"/><path d="M48 106 Q78 128 108 106" fill="none" stroke="#8e8a80" stroke-width="1.5" opacity=".35"/>'+
      /* Boot mit Dach */
      '<g transform="translate(176 140)"><path d="M-38 0 Q0 12 38 -2 L32 6 Q0 16 -32 8 Z" fill="'+INK+'"/><path d="M-20 -1 Q0 -16 20 -1 Z" fill="#5b4a3a"/><path d="M-20 -1 v-4 M20 -1 v-4" stroke="'+INK+'"/>'+
      '<path d="M30 -4 L46 -16" stroke="'+INK+'" stroke-width="1.4"/><circle cx="29" cy="-9" r="2.8" fill="'+INK+'"/><path d="M24 -11 L29 -16 L34 -11 Z" fill="#8a6a3e"/></g>'+
      willow(0, 9, 86, 31) + willow(300, 6, 70, 32) +
      '<g transform="translate(110 152)" opacity=".7"><path d="M-14 0 Q0 6 14 -1 L11 4 Q0 8 -11 4 Z" fill="'+INK+'"/></g>' + rain;
  },
  restaurant: function(){
    /* Runder Tisch mit Drehteller, Dampfkörbe, Teekanne, Laternen, Gitterfenster */
    var lattice = '<g stroke="#8a5a44" stroke-width="2" fill="none">';
    for(var x=124;x<=236;x+=16) lattice += '<path d="M'+x+' 28 v64"/>';
    for(var y=28;y<=92;y+=16) lattice += '<path d="M124 '+y+' h112"/>';
    lattice += '</g>';
    var basket = function(x, y){ return '<g transform="translate('+x+' '+y+')"><ellipse cx="0" cy="4" rx="15" ry="5" fill="#a07c50"/><rect x="-15" y="-6" width="30" height="10" fill="#c8a46e"/><ellipse cx="0" cy="-6" rx="15" ry="5" fill="#d9bb86" stroke="#8a6a3e" stroke-width=".8"/>'+
      '<path d="M-15 -1 h30" stroke="#8a6a3e" stroke-width=".8"/><path d="M-4 -12 q2 -6 0 -10 M4 -13 q2 -5 -1 -9" stroke="#b7b0a2" stroke-width="1.2" fill="none" opacity=".7"/></g>'; };
    return '<rect x="0" y="0" width="360" height="180" fill="#e9dcc6" opacity=".6"/><rect x="0" y="0" width="360" height="104" fill="#c9b493" opacity=".35"/>'+
      '<rect x="116" y="20" width="128" height="80" rx="4" fill="#f3ead6" stroke="#6f4a38" stroke-width="5"/>' + lattice +
      '<circle cx="180" cy="60" r="20" fill="none" stroke="#8a5a44" stroke-width="3"/>'+
      lantern(70, 30, 1.3) + lantern(290, 30, 1.3) + '<path d="M70 0 v14 M290 0 v14" stroke="'+INK+'" stroke-width="1"/>'+
      /* Tisch */
      '<ellipse cx="180" cy="134" rx="150" ry="34" fill="#f6efe0" stroke="#8a5a44" stroke-width="2"/><path d="M30 134 v10 Q180 190 330 144 v-10" fill="#e3d6bd" stroke="#8a5a44" stroke-width="2"/>'+
      '<ellipse cx="180" cy="130" rx="64" ry="14" fill="#efe5d1" stroke="#b9a684" stroke-width="1.5"/>'+
      basket(150, 126) + basket(200, 124) +
      /* Teekanne und Tassen */
      '<g transform="translate(250 130)"><ellipse cx="0" cy="0" rx="12" ry="9" fill="#5b7085"/><path d="M11 -2 q8 -4 10 -10" stroke="#5b7085" stroke-width="3" fill="none"/><path d="M-11 -4 q-7 2 -6 8" stroke="#5b7085" stroke-width="2.4" fill="none"/><ellipse cx="0" cy="-8" rx="5" ry="2" fill="#3f5263"/></g>'+
      '<g fill="#f6f2e8" stroke="#5b7085" stroke-width="1.2"><path d="M88 138 h12 l-2 8 h-8 Z"/><path d="M270 150 h12 l-2 8 h-8 Z"/><path d="M110 156 h12 l-2 8 h-8 Z"/></g>'+
      '<path d="M226 152 l26 -10 M228 155 l26 -10" stroke="'+RED2+'" stroke-width="1.6" stroke-linecap="round"/>'+
      '<g fill="#c23a2c" opacity=".9"><circle cx="164" cy="146" r="4"/><circle cx="172" cy="148" r="4"/><circle cx="168" cy="142" r="4"/></g>';
  },
  tower: function(){
    /* Fernsehturm in Pudong bei Nacht, Skyline, Spiegelung im Fluss */
    var r = rng(5), lights = "";
    for(var i=0;i<30;i++){ var x = 10 + r()*340, y = 70 + r()*40; if(x>150 && x<210) continue; lights += '<rect x="'+x.toFixed(0)+'" y="'+y.toFixed(0)+'" width="2" height="2" fill="#e9c46a" opacity=".7"/>'; }
    var stars = ""; for(var j=0;j<12;j++) stars += '<circle cx="'+(r()*360).toFixed(0)+'" cy="'+(r()*50).toFixed(0)+'" r="'+(0.6+r()*0.8).toFixed(1)+'" fill="#f6efe0" opacity=".7"/>';
    return '<rect x="0" y="0" width="360" height="180" fill="#2f3a44" opacity=".88"/>' + stars + '<circle cx="64" cy="34" r="12" fill="#f3ead6"/><circle cx="68" cy="31" r="11" fill="#2f3a44" opacity=".55"/>'+
      '<g fill="#1f262c"><rect x="0" y="80" width="40" height="34"/><rect x="44" y="64" width="26" height="50"/><rect x="74" y="74" width="30" height="40"/><rect x="108" y="58" width="24" height="56"/>'+
      '<path d="M226 114 V56 l12 -24 l12 24 V114 Z"/><path d="M262 114 V44 h22 v70 Z"/><rect x="270" y="38" width="6" height="8"/><path d="M296 114 V30 Q306 16 316 30 V114 Z"/><rect x="322" y="70" width="38" height="44"/></g>'+
      '<path d="M266 52 h14" stroke="#2f3a44" stroke-width="5"/>' + lights +
      /* Fernsehturm */
      '<g><path d="M166 114 L174 70 M194 114 L186 70 M180 114 V70" stroke="#c9c2b4" stroke-width="3"/>'+
      '<circle cx="180" cy="78" r="14" fill="#c23a2c"/><circle cx="176" cy="74" r="4" fill="#f3ead6" opacity=".3"/>'+
      '<rect x="177" y="40" width="6" height="26" fill="#c9c2b4"/><circle cx="180" cy="40" r="8" fill="#c23a2c"/><rect x="178" y="14" width="4" height="20" fill="#c9c2b4"/><circle cx="180" cy="22" r="3.4" fill="#c23a2c"/><path d="M180 14 V2" stroke="#c9c2b4" stroke-width="1.4"/>'+
      '<circle cx="180" cy="78" r="22" fill="#c23a2c" opacity=".18" filter="url(#blur6)"/></g>'+
      '<rect x="0" y="114" width="360" height="66" fill="#3c4852"/>'+
      '<g opacity=".35"><path d="M174 118 v40 M186 118 v40" stroke="#c23a2c" stroke-width="6"/></g>' + waterLines(120, 176, 77, "#9fb0b6") +
      '<g transform="translate(90 150)"><path d="M-30 0 H30 L24 8 H-24 Z" fill="#1f262c"/><rect x="-16" y="-7" width="26" height="7" fill="#e9c46a" opacity=".8"/></g>';
  },
  park: function(){
    /* Volkspark: Tai-Chi, Bank mit Schirmen, Hund, Pavillon */
    var tree = function(x, y, s){ return '<g filter="url(#rough)"><path d="M'+x+' 160 C'+(x-2)+' 134 '+(x+3)+' 118 '+(x-1)+' '+y+'" stroke="#6f6a5e" stroke-width="'+(3*s)+'" fill="none"/><g fill="#5f7055" opacity=".85"><ellipse cx="'+x+'" cy="'+(y-8)+'" rx="'+(26*s)+'" ry="'+(16*s)+'"/><ellipse cx="'+(x+16*s)+'" cy="'+y+'" rx="'+(16*s)+'" ry="'+(10*s)+'"/><ellipse cx="'+(x-16*s)+'" cy="'+(y+2)+'" rx="'+(15*s)+'" ry="'+(9*s)+'"/></g></g>'; };
    var taichi = function(x, flip){ var f = flip ? -1 : 1; return '<g transform="translate('+x+' 138) scale('+f+' 1)" stroke="'+INK+'" stroke-width="2" fill="none" stroke-linecap="round"><circle cx="0" cy="-16" r="3.4" fill="'+INK+'"/>'+
      '<path d="M0 -12 V2 M0 -8 L10 -14 M0 -8 L-9 -4 M0 2 L7 12 M0 2 L-6 12"/><path d="M-2 -10 h4 v10 h-4 Z" fill="#e8e2d2" stroke="none"/></g>'; };
    var umbrella = function(x, col){ return '<path d="M'+(x-9)+' 128 Q'+x+' 116 '+(x+9)+' 128 Z" fill="'+col+'"/><path d="M'+x+' 128 v14" stroke="'+INK+'" stroke-width="1"/><rect x="'+(x-5)+'" y="131" width="10" height="7" fill="#f6f2e8" stroke="'+INK+'" stroke-width=".6"/>'; };
    return mtn(52, 76, 22, 4, "mFar", 'opacity=".45"') + birds(150, 20, 4) +
      /* Pavillon (亭) mit Doppeldach auf einer Steinplattform */
      '<rect x="282" y="132" width="74" height="8" fill="#b9b0a0" stroke="'+INK+'" stroke-width="1"/>'+
      '<path d="M292 132 V100 M346 132 V100 M310 132 V102 M328 132 V102" stroke="#a8342a" stroke-width="3.4"/>'+
      '<path d="M292 122 h54" stroke="#a8342a" stroke-width="2"/><path d="M296 122 v10 M304 122 v10 M334 122 v10 M342 122 v10" stroke="#a8342a" stroke-width="1.2"/>'+
      '<rect x="292" y="100" width="54" height="5" fill="#3b2a22"/>' + roof(286, 352, 100, 10) + roof(298, 340, 86, 8) +
      '<path d="M319 76 v-6" stroke="'+INK+'" stroke-width="1.6"/><circle cx="319" cy="69" r="2.2" fill="'+GOLD+'"/>' +
      tree(40, 92, 1.1) +
      '<ellipse cx="300" cy="156" rx="64" ry="7" fill="url(#water)"/>'+
      taichi(96, false) + taichi(126, true) + taichi(156, false) +
      /* Bank mit Schirmen (Partnermarkt) */
      '<path d="M182 140 h52 M186 140 v12 M230 140 v12 M182 134 h52" stroke="#6f4a38" stroke-width="3"/>' + umbrella(196, RED) + umbrella(220, "#5b7085") +
      /* Hund */
      '<g transform="translate(258 150)" fill="'+INK+'"><ellipse cx="0" cy="0" rx="9" ry="5"/><circle cx="9" cy="-5" r="4"/><path d="M11 -9 l3 -3 l0 5 Z M-8 -2 q-6 -6 -4 -10" stroke="'+INK+'" stroke-width="1.6"/><path d="M-6 3 v6 M-2 4 v5 M4 4 v5 M7 3 v6" stroke="'+INK+'" stroke-width="1.6"/></g>'+
      '<path d="M268 145 Q280 132 290 138" stroke="#8a5a44" stroke-width="1" fill="none"/><g transform="translate(296 140)" stroke="'+INK+'" stroke-width="2" fill="none" stroke-linecap="round"><circle cx="0" cy="-16" r="3.4" fill="'+INK+'"/><path d="M0 -12 V2 M0 -8 L-7 -2 M0 2 L5 12 M0 2 L-4 12"/></g>' +
      ground(160, "#c8c39f", 0.9);
  },
  airport: function(){
    /* Flughafen Pudong: geschwungenes Dach, Tower, startendes Flugzeug */
    return '<rect x="0" y="0" width="360" height="180" fill="#e7e4da" opacity=".6"/>' + sun(60, 40, 16) + mist(70, 10, 0.6) +
      /* Flugzeug */
      '<g transform="translate(250 46) rotate(-14)"><path d="M-40 0 Q-36 -5 -20 -5 H34 Q44 -5 46 0 Q44 5 34 5 H-20 Q-36 5 -40 0 Z" fill="#f6f2e8" stroke="'+INK+'" stroke-width="1.6"/>'+
      '<path d="M2 -4 L-14 -26 H-6 L18 -4 Z M2 4 L-10 22 H-3 L16 4 Z" fill="#d9d2c2" stroke="'+INK+'" stroke-width="1.4"/><path d="M-36 -4 L-44 -18 H-38 L-26 -4 Z" fill="'+RED+'"/>'+
      '<g fill="#5b7085">'+[0,1,2,3,4,5,6,7].map(function(k){ return '<circle cx="'+(-16+k*6)+'" cy="-1" r="1.2"/>'; }).join("")+'</g></g>'+
      '<path d="M140 92 Q190 76 220 64" stroke="#b7b0a2" stroke-width="2" fill="none" stroke-dasharray="4 6" opacity=".7"/>'+
      /* Terminal mit Wellendach */
      '<path d="M10 120 Q60 92 110 112 Q160 92 210 112 Q260 92 310 112 Q336 104 352 110 V140 H10 Z" fill="#c9c2b4" stroke="'+INK+'" stroke-width="1.6" filter="url(#rough)"/>'+
      '<rect x="20" y="114" width="326" height="26" fill="#9fb0b6" opacity=".55"/><path d="M20 120 H346 M20 128 H346" stroke="#f6f2e8" stroke-width=".8" opacity=".7"/>'+
      '<g stroke="#6f6a5e" stroke-width="1">'+[40,70,100,130,160,190,220,250,280,310,340].map(function(x){ return '<path d="M'+x+' 114 v26"/>'; }).join("")+'</g>'+
      /* Tower */
      '<rect x="316" y="56" width="10" height="58" fill="#b9b0a0" stroke="'+INK+'" stroke-width="1.2"/><path d="M306 56 h30 l-4 -12 h-22 Z" fill="#5b7085" stroke="'+INK+'" stroke-width="1.2"/><path d="M321 44 v-10" stroke="'+INK+'" stroke-width="1.4"/><circle cx="321" cy="33" r="2" fill="'+RED+'"/>'+
      '<rect x="0" y="140" width="360" height="40" fill="#8e8a80" opacity=".55"/><path d="M0 158 H360" stroke="#f6f2e8" stroke-width="2" stroke-dasharray="18 14" opacity=".8"/>'+
      birds(140, 30, 3);
  },
};
/* Gemalte Etappen-Bilder (aus dem Bildgenerator). Wo es noch keins gibt, bleibt die gezeichnete Szene. */
var SCENE_IMG = {gate:"01", hutong:"02", wall:"03", tea:"04", market:"05"};
function sceneSVG(kind, cls, eager){
  var n = SCENE_IMG[kind];
  if(n) return '<img class="scene-img" src="img/'+n+'.webp" srcset="img/'+n+'-640.webp 640w, img/'+n+'.webp 1280w" sizes="(max-width: 700px) 100vw, 1100px" alt="" aria-hidden="true" decoding="async"'+(eager ? '' : ' loading="lazy"')+' onerror="this.replaceWith(sceneFallback(\''+kind+'\'))">';
  return '<svg class="'+(cls||"scene-svg")+'" viewBox="0 0 360 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g filter="url(#wc)">'+(SCENES[kind] ? SCENES[kind]() : "")+'</g></svg>';
}
/* Falls ein Bild nicht lädt: die gezeichnete Szene einsetzen */
function sceneFallback(kind){
  var d = document.createElement("div"); d.innerHTML = '<svg class="scene-svg" viewBox="0 0 360 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g filter="url(#wc)">'+(SCENES[kind] ? SCENES[kind]() : "")+'</g></svg>';
  return d.firstChild;
}
var SVG_DEFS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'+
  '<linearGradient id="mFar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b9794" stop-opacity=".8"/><stop offset=".75" stop-color="#8b9794" stop-opacity=".12"/><stop offset="1" stop-color="#8b9794" stop-opacity="0"/></linearGradient>'+
  '<linearGradient id="mMid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#58625d" stop-opacity=".9"/><stop offset=".8" stop-color="#58625d" stop-opacity=".15"/><stop offset="1" stop-color="#58625d" stop-opacity="0"/></linearGradient>'+
  '<linearGradient id="mNear" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f2d28" stop-opacity=".95"/><stop offset="1" stop-color="#2f2d28" stop-opacity=".35"/></linearGradient>'+
  '<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c3cdc4"/><stop offset="1" stop-color="#e9e3d2"/></linearGradient>'+
  '<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="3.5"/></filter>'+
  '<filter id="wc" x="-2%" y="-2%" width="104%" height="104%" color-interpolation-filters="sRGB">'+
  '<feTurbulence type="fractalNoise" baseFrequency=".07" numOctaves="2" seed="11" result="n"/>'+
  '<feDisplacementMap in="SourceGraphic" in2="n" scale="1.8" xChannelSelector="R" yChannelSelector="G" result="d"/>'+
  '<feGaussianBlur in="d" stdDeviation=".3" result="b"/>'+
  '<feMorphology in="b" operator="erode" radius=".9" result="e"/>'+
  '<feComposite in="b" in2="e" operator="arithmetic" k2=".72" k3=".28" result="m"/>'+
  '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="5" result="g"/>'+
  '<feColorMatrix in="g" values="0 0 0 0 .42 0 0 0 0 .32 0 0 0 0 .2 0 0 0 .16 -.06" result="ga"/>'+
  '<feComposite in="ga" in2="m" operator="in" result="gi"/>'+
  '<feMerge><feMergeNode in="m"/><feMergeNode in="gi"/></feMerge></filter>'+
  '<filter id="blur6" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'+
  '</defs></svg>';
/* Wolken-Ornament (祥云) */
function cloud(cls){ return '<svg class="'+(cls||"cloud")+'" viewBox="0 0 64 28" aria-hidden="true"><path d="M6 22 C0 22 0 13 7 13 C7 5 18 3 21 10 C24 2 38 2 39 11 C44 6 54 8 52 16 C60 16 62 24 54 24 Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M21 10 C24 13 22 18 18 17 M39 11 C40 15 37 18 34 17" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'; }
