// Baut zh-app/dialogs.data.js aus scripts/dialogs_src.js. Pinyin kommt aus dem Wörterbuch der App.
const fs = require("fs"), window = {};
eval(fs.readFileSync(require("path").resolve(__dirname, "..") + "/zh-app/lessons.data.js", "utf8"));
const SRC = require(require("path").resolve(__dirname, "..") + "/scripts/dialogs_src.js");
const W = new Map(); window.ZH_LESSONS.forEach(u => u.lessons.forEach(l => l.words.forEach(w => W.set(w[0], w[1]))));
const NAMES = {"弗洛里安":"Fú_luò_lǐ_'ān", "小明":"Xiǎo_Míng", "安娜":"Ān_nà"};
const MARK = {}; [["āēīōūǖ",1],["áéíóúǘ",2],["ǎěǐǒǔǚ",3],["àèìòùǜ",4]].forEach(p => Array.from(p[0]).forEach(c => MARK[c]=p[1]));
const toneOf = s => { for (const c of Array.from(s)) if (MARK[c]) return MARK[c]; return 0; };
const isHan = c => /\p{Script=Han}/u.test(c);
const NUM = "一二三四五六七八九十";
function segment(zh){
  const out = []; const ch = Array.from(zh); let i = 0;
  while(i < ch.length){
    const c = ch[i];
    if(!isHan(c)){ let j = i; while(j < ch.length && !isHan(ch[j])) j++; out.push({p:ch.slice(i, j).join("")}); i = j; continue; }
    let hit = null;
    for(const n of Object.keys(NAMES)) if(ch.slice(i, i+Array.from(n).length).join("") === n){ hit = {w:n, py:NAMES[n].split("_"), name:true}; break; }
    if(!hit) for(let n = Math.min(4, ch.length - i); n > 0; n--){ const w = ch.slice(i, i+n).join(""); if(W.has(w)){ hit = {w, py:W.get(w).split("_")}; break; } }
    if(!hit) throw new Error("Unbekanntes Wort in: " + zh + " bei " + ch.slice(i).join(""));
    out.push(hit); i += Array.from(hit.w).length;
  }
  // Tonwechsel
  out.forEach((t, k) => {
    if(!t.w) return;
    const next = out[k+1] && out[k+1].w ? out[k+1] : null, prev = out[k-1] && out[k-1].w ? out[k-1] : null;
    if(t.w === "不"){ t.py = [next && toneOf(next.py[0]) === 4 ? "bú" : "bù"]; }
    if(t.w === "一"){
      if(!next || (prev && prev.w === "十") || NUM.includes(next.w)) t.py = ["yī"];
      else t.py = [toneOf(next.py[0]) === 4 || next.w === "个" ? "yí" : "yì"];
    }
    if(t.w === "个") t.py = ["ge"];
    if(t.w === "上") t.py = ["shang"];
    if(t.w === "里") t.py = ["li"];
  });
  return out;
}
const PUNCT = {"，":", ", "。":". ", "！":"! ", "？":"? ", "、":", ", "……":" … ", "…":" … "};
function pinyin(zh){
  let s = "";
  segment(zh).forEach(t => {
    if(t.p !== undefined){ s = s.replace(/ $/, ""); s += t.p.split("").reduce((a, c) => a, "") ; s += (PUNCT[t.p] !== undefined ? PUNCT[t.p] : t.p); return; }
    s += t.py.join("_") + " ";
  });
  s = s.replace(/\s+/g, " ").trim().replace(/ …/g, " …");
  // Satzanfänge groß
  s = s.replace(/(^|[.!?] )([a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ])/g, (m, a, b) => a + b.toUpperCase());
  return s;
}
const esc = x => JSON.stringify(x);
let out = "/* Kleine Gespräche, eins pro Ort. Nur Wörter, die bis zum Ende der Etappe gelernt sind (plus Namen).\n   Erzeugt mit scripts/build_dialogs.js aus scripts/dialogs_src.js. s: \"a\" = Gesprächspartner, \"me\" = Florian.\n   Zeilen mit alt: Florian wählt seine Antwort, alt sind die falschen Möglichkeiten mit Begründung. */\nwindow.ZH_DIALOGS = {\n";
const ids = Object.keys(SRC);
ids.forEach((id, n) => {
  const d = SRC[id];
  out += `  ${id}: {title:${esc(d.title)}, who:{zh:${esc(d.who.zh)}, py:${esc(d.who.py)}, de:${esc(d.who.de)}}, lines:[\n`;
  out += d.lines.map(l => {
    let x = `    {s:${esc(l[0])}, zh:${esc(l[1])}, py:${esc(pinyin(l[1]))}, de:${esc(l[2])}`;
    if(l[4]) x += `, cue:${esc(l[4])}`;
    if(l[3]) x += ", alt:[\n" + l[3].map(a => `      {zh:${esc(a[0])}, py:${esc(pinyin(a[0]))}, de:${esc(a[1])}, why:${esc(a[2])}}`).join(",\n") + "]";
    return x + "}";
  }).join(",\n") + "\n  ]}" + (n < ids.length - 1 ? "," : "") + "\n";
});
out += "};\n";
fs.writeFileSync(require("path").resolve(__dirname, "..") + "/zh-app/dialogs.data.js", out);
console.log("geschrieben", ids.length, "Gespräche,", ids.map(i => SRC[i].lines.length).join("/"), "Zeilen,", ids.map(i => SRC[i].lines.filter(l => l[3]).length).join("/"), "Auswahlen");
