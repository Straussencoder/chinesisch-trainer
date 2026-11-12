// Baut audio.js: nur die Aufnahmen, die die App wirklich braucht, als Base64.
const fs = require("fs"), path = require("path");
const [htmlPath, audioDir, outPath] = process.argv.slice(2);
const html = fs.readFileSync(htmlPath, "utf8");
const window = {}; eval(html.match(/<script id="zh-data">([\s\S]*?)<\/script>/)[1]); const D = window.ZH_DATA;
const MARK = {};
[["āēīōūǖĀĒĪŌŪǕ",1],["áéíóúǘÁÉÍÓÚǗ",2],["ǎěǐǒǔǚǍĚǏǑǓǙ",3],["àèìòùǜÀÈÌÒÙǛ",4]].forEach(p => Array.from(p[0]).forEach(c => MARK[c]=p[1]));
const BASE = {"ā":"a","á":"a","ǎ":"a","à":"a","ē":"e","é":"e","ě":"e","è":"e","ī":"i","í":"i","ǐ":"i","ì":"i","ō":"o","ó":"o","ǒ":"o","ò":"o","ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v"};
const toneOf = s => { for (const c of Array.from(s)) if (MARK[c]) return MARK[c]; return 0; };
const numeric = s => { const t = toneOf(s); return t ? Array.from(s.toLowerCase()).map(c => BASE[c]||c).join("").replace(/[^a-z]/g,"") + t : null; };
const isHan = c => /\p{Script=Han}/u.test(c);
const isSyl = s => /[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/.test(s);
// Geprüft und aussortiert: ren4 steigt statt zu fallen, guo4 fällt kaum, 了 ist als "liǎo" gelesen
const BLOCK = new Set(["s:ren4", "s:guo4", "w:了"]);
const sylFile0 = n => path.join(audioDir, "syl", n + ".mp3");
const wFile0 = w => path.join(audioDir, "hsk", encodeURIComponent(w) + ".mp3");
const sylFile = n => BLOCK.has("s:" + n) ? "/nonexistent" : sylFile0(n);
const wFile = w => BLOCK.has("w:" + w) ? "/nonexistent" : wFile0(w);
const S = new Set(), W = new Set(), missing = [];
D.syl.flat().forEach(([zh, py]) => { const n = numeric(py); fs.existsSync(sylFile(n)) ? S.add(n) : missing.push("Silbe " + zh + " " + n); });
D.words.forEach(([zh]) => { fs.existsSync(wFile(zh)) ? W.add(zh) : missing.push("Wort " + zh); });
(D.duel || []).forEach(([s0]) => [s0 + "2", s0 + "3"].forEach(n => { fs.existsSync(sylFile(n)) ? S.add(n) : missing.push("Silbe " + n); }));
D.cards.forEach(c => {
  const chars = Array.from(c.zh).filter(isHan); let i = 0;
  c.py.split(" ").forEach(w => {
    const ss = w.split("_").filter(isSyl); if (!ss.length) return;
    const zh = chars.slice(i, i + ss.length).join(""); i += ss.length;
    if (zh.length === 1) {
      const n = numeric(ss[0]);
      if (n && fs.existsSync(sylFile(n))) S.add(n);
      else if (!n && !/^r\W*$/i.test(ss[0]) && fs.existsSync(wFile(zh))) W.add(zh);
      return;
    }
    for (let a = 0; a < zh.length; a++) for (let b = a + 2; b <= zh.length; b++) { const sub = zh.slice(a, b); if (fs.existsSync(wFile(sub))) W.add(sub); }
    ss.forEach(s => { const n = numeric(s); if (n && fs.existsSync(sylFile(n))) S.add(n); });
  });
});
// Lernpfad: Wörter und Satz-Wörter
const lw = {}; eval(fs.readFileSync(path.join(path.dirname(htmlPath), "lessons.data.js"), "utf8").replace("window.", "lw."));
const addWord = (zh, py) => {
  const ss = py.split("_"), chars = Array.from(zh), tones = ss.map(toneOf);
  if (chars.length === 1) {
    const n = numeric(ss[0]);
    if (n) { fs.existsSync(sylFile(n)) ? S.add(n) : missing.push("Silbe " + n); }
    else if (fs.existsSync(wFile(zh))) W.add(zh); else missing.push("Partikel " + zh);
    return;
  }
  if (fs.existsSync(wFile(zh))) { W.add(zh); return; }
  for (let a = 0; a < chars.length; a++) for (let b = a + 2; b <= chars.length; b++) { const sub = chars.slice(a, b).join(""); if (fs.existsSync(wFile(sub))) W.add(sub); }
  ss.forEach((x, i) => { let t = tones[i]; if (!t) return; if (t === 3 && tones[i+1] === 3) t = 2; const k = numeric(x).slice(0, -1) + t; fs.existsSync(sylFile(k)) ? S.add(k) : missing.push("Silbe " + k); });
};
lw.ZH_LESSONS.forEach(u => u.lessons.forEach(l => {
  l.words.forEach(([zh, py]) => addWord(zh, py));
  l.sents.forEach(s => s.t.split(" ").forEach(t => { const [zh, py] = t.split("|"); addWord(zh, py); }));
  l.words.forEach(w => { if (w[3] && w[3].ex) { const [zh, py] = w[3].ex.split("|"); const chars = Array.from(zh).filter(isHan); let i = 0;
    py.split(" ").forEach(x => { const n = x.split("_").length; addWord(chars.slice(i, i + n).join(""), x); i += n; }); } });
}));
// Reisesätze: Tonwechsel-Silben ergänzen
D.cards.forEach(c => c.py.split(" ").forEach(w => { const ss = w.split("_").filter(isSyl); const t = ss.map(toneOf); ss.forEach((x, i) => { if (t[i] === 3 && t[i+1] === 3) { const k = numeric(x).slice(0, -1) + "2"; if (fs.existsSync(sylFile(k))) S.add(k); } }); }));
// crossToken: Tonwechsel 3+3 über Wortgrenzen (einsilbiges Wort vor einem 3. Ton)
const crossToken = (toks) => toks.forEach((t, i) => {
  const ss = t.py.split("_"); if (ss.length !== 1 || !toks[i+1]) return;
  if (toneOf(ss[0]) === 3 && toneOf(toks[i+1].py.split("_")[0]) === 3) { const k = numeric(ss[0]).slice(0, -1) + "2"; fs.existsSync(sylFile(k)) ? S.add(k) : missing.push("Silbe " + k); }
});
lw.ZH_LESSONS.forEach(u => u.lessons.forEach(l => {
  l.sents.forEach(s => crossToken(s.t.split(" ").map(t => ({py: t.split("|")[1]}))));
  l.words.forEach(w => { if (w[3] && w[3].ex) crossToken(w[3].ex.split("|")[1].split(" ").map(x => ({py: x}))); });
}));
D.cards.forEach(c => crossToken(c.py.split(" ").map(w => ({py: w.split("_").filter(isSyl).map(x => x.replace(/[^\p{L}']/gu, "")).join("_")})).filter(t => t.py)));
const enc = f => fs.readFileSync(f).toString("base64");
const obj = {s:{}, w:{}};
[...S].sort().forEach(n => obj.s[n] = enc(sylFile(n)));
[...W].sort().forEach(w => obj.w[w] = enc(wFile(w)));
const js = "/* Aufnahmen aus audio-cmn (https://github.com/hugolpz/audio-cmn), CC BY-SA. Silben: Chen Wang. Wörter: Yue Tan. */\n" +
  "window.ZH_AUDIO=" + JSON.stringify(obj) + ";\nwindow.dispatchEvent(new Event(\"zh-audio-ready\"));\n";
fs.writeFileSync(outPath, js);
console.log("Silben:", S.size, "Wörter:", W.size, "Größe:", (js.length/1024/1024).toFixed(2), "MB");
console.log("Fehlend:", missing.join(", ") || "nichts");
