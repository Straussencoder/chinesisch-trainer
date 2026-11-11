// Ermittelt, welche Aufnahmen aus audio-cmn gebraucht werden, und schreibt eine Download-Liste.
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const out = process.argv[3];
const m = html.match(/<script id="zh-data">([\s\S]*?)<\/script>/);
const window = {}; eval(m[1]); const D = window.ZH_DATA;

const MARK = {};
[["āēīōūǖĀĒĪŌŪǕ",1],["áéíóúǘÁÉÍÓÚǗ",2],["ǎěǐǒǔǚǍĚǏǑǓǙ",3],["àèìòùǜÀÈÌÒÙǛ",4]].forEach(p => Array.from(p[0]).forEach(c => MARK[c]=p[1]));
const BASE = {"ā":"a","á":"a","ǎ":"a","à":"a","ē":"e","é":"e","ě":"e","è":"e","ī":"i","í":"i","ǐ":"i","ì":"i","ō":"o","ó":"o","ǒ":"o","ò":"o","ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v"};
const toneOf = s => { for (const c of Array.from(s)) if (MARK[c]) return MARK[c]; return 0; };
const numeric = s => { const t = toneOf(s); const b = Array.from(s.toLowerCase()).map(c => BASE[c] || c).join("").replace(/[^a-z]/g, ""); return t ? b + t : null; };
const isHan = c => /\p{Script=Han}/u.test(c);
const isSyl = s => /[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/.test(s);

const syl = new Set(), hsk = new Set();
// Töne-Trainer
D.syl.flat().forEach(([zh, py]) => { syl.add(numeric(py)); hsk.add(zh); });
D.words.forEach(([zh, py]) => { hsk.add(zh); py.split("_").forEach(s => syl.add(numeric(s))); Array.from(zh).forEach(c => hsk.add(c)); });
// Karten: Wörter (Chunks) und einzelne Zeichen als Ersatz
const chunks = {};
D.cards.forEach(c => {
  const chars = Array.from(c.zh).filter(isHan);
  let i = 0; const list = [];
  c.py.split(" ").forEach(w => {
    const ss = w.split("_").filter(isSyl);
    if (!ss.length) return;
    const zh = chars.slice(i, i + ss.length).join(""); i += ss.length;
    list.push({zh, syls: ss.map(s => s.replace(/[^\p{L}']/gu, ""))});
    hsk.add(zh);
    Array.from(zh).forEach(ch => hsk.add(ch));
    for (let a = 0; a < zh.length; a++) for (let b = a + 2; b <= zh.length; b++) hsk.add(zh.slice(a, b));
    ss.forEach(s => { const n = numeric(s); if (n) syl.add(n); });
  });
  chunks[c.id] = list;
});
syl.delete(null);
fs.writeFileSync(out, JSON.stringify({syl: [...syl].sort(), hsk: [...hsk].sort(), chunks}, null, 1));
console.log("Silben:", syl.size, "HSK-Kandidaten:", hsk.size);
