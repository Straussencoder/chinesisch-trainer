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
      '<rect x="150" y="80" width="26" height="16" fill="#3e4f45"/><path d="M154 85 h8 M154 90 h14 M166 85 l4 4" stroke="#e9e2d3" stroke-width="1" stroke-linecap="round"/>'+
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
      roof(262, 334, 92, 9) + '<path d="M270 92 v40 M326 92 v40" stroke="#a8342a" stroke-width="4"/><rect x="266" y="96" width="64" height="4" fill="#a8342a"/>' +
      tree(40, 92, 1.1) + tree(228, 100, 0.9) +
      '<ellipse cx="300" cy="150" rx="60" ry="8" fill="url(#water)"/>'+
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
      '<g transform="translate(90 150)"><path d="M-22 0 h44 v-6 h-44 Z" fill="'+INK+'" opacity=".7"/></g>' + birds(140, 30, 3);
  },
