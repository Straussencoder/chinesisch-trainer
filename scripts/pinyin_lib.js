// Pinyin aus dem Wörterbuch der App, mit Tonwechseln (不, 一) und unbetonten Silben (个, 上, 里).
// Gleiche Regeln wie in build_dialogs.js. Wirft einen Fehler bei Wörtern, die nicht im Lernpfad sind.
const fs = require("fs"), window = {};
eval(fs.readFileSync(require("path").resolve(__dirname, "..") + "/zh-app/lessons.data.js", "utf8"));
const W = new Map(), LESSON_OF = new Map(); let ln = 0;
window.ZH_LESSONS.forEach(u => u.lessons.forEach(l => { ln++; l.words.forEach(w => { W.set(w[0], w[1]); LESSON_OF.set(w[0], ln); }); }));
const NAMES = {"弗洛里安":"Fú_luò_lǐ_'ān", "小明":"Xiǎo_Míng", "安娜":"Ān_nà", "李娜":"Lǐ_Nà"};
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
const PUNCT = {"，":", ", "。":". ", "！":"! ", "？":"? ", "、":", ", "：":": ", "……":" … ", "…":" … "};
function pinyin(zh){
  let s = "";
  segment(zh).forEach(t => {
    if(t.p !== undefined){ s = s.replace(/ $/, ""); s += (PUNCT[t.p] !== undefined ? PUNCT[t.p] : t.p); return; }
    s += t.py.join("_") + " ";
  });
  s = s.replace(/\s+/g, " ").trim().replace(/ …/g, " …");
  s = s.replace(/(^|[.!?] )([a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ])/g, (m, a, b) => a + b.toUpperCase());
  return s;
}
/* Ab welcher Lektion ein Text lesbar ist: die späteste Lektion seiner Wörter */
function lessonOf(zh){ let n = 0; segment(zh).forEach(t => { if(t.w && !t.name) n = Math.max(n, LESSON_OF.get(t.w)); }); return n; }
module.exports = {segment, pinyin, lessonOf, W, NAMES};
