// Prüft die Lerninhalte: Töne passen zur Gruppe, Silbenzahl passt zur Zeichenzahl.
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const m = html.match(/<script id="zh-data">([\s\S]*?)<\/script>/);
const window = {};
eval(m[1]);
const D = window.ZH_DATA;

const MARK = {};
[["āēīōūǖĀĒĪŌŪǕ",1],["áéíóúǘÁÉÍÓÚǗ",2],["ǎěǐǒǔǚǍĚǏǑǓǙ",3],["àèìòùǜÀÈÌÒÙǛ",4]].forEach(p => Array.from(p[0]).forEach(c => MARK[c]=p[1]));
const toneOf = s => { for (const c of Array.from(s)) if (MARK[c]) return MARK[c]; return 0; };
const han = s => Array.from(s).filter(c => /\p{Script=Han}/u.test(c)).length;
const syls = py => py.split(/[ _]/).filter(s => /[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/.test(s));

let errors = 0;
const err = (...a) => { errors++; console.log("FEHLER:", ...a); };

D.syl.forEach((g, gi) => g.forEach(([zh, py]) => {
  if (toneOf(py) !== gi + 1) err("Silbe", zh, py, "erwartet Ton", gi + 1, "gefunden", toneOf(py));
  if (han(zh) !== 1) err("Silbe nicht 1 Zeichen", zh);
}));
const allSyl = D.syl.flat().map(x => x[0]);
const dupes = allSyl.filter((c, i) => allSyl.indexOf(c) !== i);
if (dupes.length) err("doppelte Silben", dupes);

D.words.forEach(([zh, py]) => {
  const s = py.split("_"), t = s.map(toneOf);
  if (s.length !== han(zh)) err("Wort Silbenzahl", zh, py);
  if (t.includes(0)) err("Wort mit neutralem Ton", zh, py);
  for (let i = 1; i < t.length; i++) if (t[i] === 3 && t[i - 1] === 3) err("Wort 3+3", zh, py);
});

const neutral = [];
const ids = new Set();
D.cards.forEach(c => {
  if (ids.has(c.id)) err("doppelte id", c.id); ids.add(c.id);
  const s = syls(c.py);
  if (s.length !== han(c.zh)) err("Karte Silbenzahl", c.id, c.zh, han(c.zh), c.py, s.length);
  s.forEach(x => { if (toneOf(x) === 0) neutral.push(c.id + ":" + x); });
});

console.log("Silben:", D.syl.flat().length, "Wörter:", D.words.length, "Karten:", D.cards.length);
const perTone = [0,0,0,0,0]; D.words.forEach(([,py]) => py.split("_").forEach(s => perTone[toneOf(s)]++));
console.log("Wort-Silben pro Ton 1-4:", perTone.slice(1).join(" / "));
console.log("Neutrale Silben in Karten:", neutral.join(", "));
console.log(errors ? errors + " Fehler" : "Keine Fehler");
