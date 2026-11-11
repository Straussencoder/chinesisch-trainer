// Prüft den Lernpfad: Satz-Wörter schon gelernt, Pinyin passt, Silbenzahl passt. Schreibt Download-Liste.
const fs = require("fs");
const window = {}; eval(fs.readFileSync(process.argv[2], "utf8"));
const audioDir = process.argv[3];
const MARK = {};
[["āēīōūǖĀĒĪŌŪǕ",1],["áéíóúǘÁÉÍÓÚǗ",2],["ǎěǐǒǔǚǍĚǏǑǓǙ",3],["àèìòùǜÀÈÌÒÙǛ",4]].forEach(p => Array.from(p[0]).forEach(c => MARK[c]=p[1]));
const BASE = {"ā":"a","á":"a","ǎ":"a","à":"a","ē":"e","é":"e","ě":"e","è":"e","ī":"i","í":"i","ǐ":"i","ì":"i","ō":"o","ó":"o","ǒ":"o","ò":"o","ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v"};
const toneOf = s => { for (const c of Array.from(s)) if (MARK[c]) return MARK[c]; return 0; };
const plain = s => Array.from(s.toLowerCase()).map(c => BASE[c]||c).join("").replace(/[^a-z]/g,"");
const numeric = s => { const t = toneOf(s); return t ? plain(s) + t : null; };
let err = 0; const E = (...a) => { err++; console.log("FEHLER:", ...a); };
const known = new Map(); const need = new Set(); const sylNeed = new Set();
let nWords = 0, nSents = 0;
window.ZH_LESSONS.forEach(u => u.lessons.forEach(l => {
  l.words.forEach(([zh, py, de]) => {
    nWords++;
    if (known.has(zh)) E("doppelt", zh, l.id);
    const ss = py.split("_");
    if (ss.length !== Array.from(zh).length) E("Silbenzahl", zh, py);
    known.set(zh, py); need.add(zh); Array.from(zh).forEach(c => need.add(c));
    ss.forEach(s => { const n = numeric(s); if (n) sylNeed.add(n); });
  });
  l.sents.forEach(s => {
    nSents++;
    s.t.split(" ").forEach(tok => {
      const [zh, py] = tok.split("|");
      if (!known.has(zh)) E("Satz-Wort noch nicht gelernt", l.id, zh, s.de);
      else {
        const wp = known.get(zh);
        if (wp !== py) {
          /* 不 und 一 wechseln den Ton; 个, 上, 里 sind hinter Zahl oder Nomen unbetont */
          const same = plain(wp) === plain(py) && (["不","一"].includes(zh) || (["个","上","里"].includes(zh) && !toneOf(py)));
          if (!same) E("Pinyin weicht ab", l.id, zh, wp, "vs", py);
        }
      }
      if (py.split("_").length !== Array.from(zh).length) E("Satz Silbenzahl", zh, py);
      py.split("_").forEach(x => { const n = numeric(x); if (n) sylNeed.add(n); });
    });
    (s.alt||[]).forEach(a => {
      const toks = s.t.split(" ").map(t => t.split("|")[0]);
      if ([...a].sort().join("") !== toks.join("").split("").sort().join("")) E("Alternative passt nicht", a);
    });
  });
  if (l.words.length < 4) E("zu wenige Wörter", l.id);
}));
console.log("Wörter:", nWords, "Sätze:", nSents);
const urls = [];
need.forEach(h => { const f = audioDir + "/hsk/" + encodeURIComponent(h) + ".mp3"; if (!fs.existsSync(f)) urls.push(f + " https://raw.githubusercontent.com/hugolpz/audio-cmn/master/64k/hsk/cmn-" + encodeURIComponent(h) + ".mp3"); });
sylNeed.forEach(n => { const f = audioDir + "/syl/" + n + ".mp3"; if (!fs.existsSync(f)) urls.push(f + " https://raw.githubusercontent.com/hugolpz/audio-cmn/master/64k/syllabs/cmn-" + n + ".mp3"); });
fs.writeFileSync(require("path").resolve(__dirname, "..") + "/dl/urls2.txt", urls.join("\n") + (urls.length ? "\n" : ""));
console.log("Neu zu laden:", urls.length);
console.log(err ? err + " Fehler" : "Keine Fehler");
