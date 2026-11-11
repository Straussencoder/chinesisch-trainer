// Prüft die Übungssätze: nur gelernte Wörter, Pinyin passt, Zerlegung vollständig, Lücke und falscher Satz sinnvoll.
const fs = require("fs");
const window = {};
eval(fs.readFileSync(require("path").resolve(__dirname, "..") + "/zh-app/lessons.data.js", "utf8"));
eval(fs.readFileSync(require("path").resolve(__dirname, "..") + "/zh-app/grammar.data.js", "utf8"));
eval(fs.readFileSync(require("path").resolve(__dirname, "..") + "/zh-app/drill.data.js", "utf8"));
const BASE = {"ā":"a","á":"a","ǎ":"a","à":"a","ē":"e","é":"e","ě":"e","è":"e","ī":"i","í":"i","ǐ":"i","ì":"i","ō":"o","ó":"o","ǒ":"o","ò":"o","ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v"};
const plain = s => Array.from(s.toLowerCase()).map(c => BASE[c]||c).join("").replace(/[^a-z]/g,"");
const hasTone = s => /[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]/.test(s);
const W = new Map(); let n = 0; const keys = new Set();
window.ZH_LESSONS.forEach(u => u.lessons.forEach(l => { n++; l.words.forEach(w => W.set(w[0], {py:w[1], n})); l.sents.forEach(s => keys.add(s.t.split(" ").map(t => t.split("|")[0]).join(""))); }));
const GP = {}; window.ZH_GRAMMAR.points.forEach(p => GP[p.id] = +p.l.slice(1));
const SLOTS = "SVOADTLZQPX";
let err = 0; const E = (...a) => { err++; console.log("FEHLER:", ...a); };
const tok = (t, de, what) => t.split(" ").map(x => { const [zh, py] = x.split("|"); const w = W.get(zh);
  if (!w) { E(what, "Wort nicht gelernt", zh, de); return {zh, n:99}; }
  if (w.py !== py) { const ok = plain(w.py) === plain(py) && (["不","一"].includes(zh) || (["个","上","里"].includes(zh) && !hasTone(py))); if (!ok) E(what, "Pinyin", zh, w.py, "vs", py, de); }
  if (py.split("_").length !== Array.from(zh).length) E(what, "Silbenzahl", zh, py, de);
  return {zh, n:w.n}; });
const per = {}; const seen = new Set(); let nGap = 0, nBad = 0;
window.ZH_DRILL.forEach(s => {
  const T = tok(s.t, s.de, "Satz"), key = T.map(t => t.zh).join("");
  if (seen.has(key)) E("doppelt", key); seen.add(key);
  if (keys.has(key)) E("gibt es schon in den Lektionen", key);
  let ln = Math.max(...T.map(t => t.n));
  if (s.gp) { if (!GP[s.gp]) E("Bauplan fehlt", s.gp, s.de); else ln = Math.max(ln, GP[s.gp]); }
  const g = (s.g||"").split("|");
  if (g.length !== T.length) E("Zerlegung passt nicht", g.length, "vs", T.length, s.de);
  g.forEach(x => { const m = x.match(/^(\S) (\S+) (.+)$/); if (!m || SLOTS.indexOf(m[1]) < 0) E("Zerlegung kaputt", x, s.de); });
  if (!s.de || !/[.?!)]$/.test(s.de)) E("Deutsch fehlt/Satzzeichen", s.de);
  if (!s.p) E("Satzzeichen fehlt", s.de);
  if (s.x) { nGap++;
    const [i, rest] = s.x.split(":"), k = +i, d = rest.split(",");
    if (!(k >= 0 && k < T.length)) E("Lücke außerhalb", s.x, s.de);
    if (d.length !== 2) E("Lücke braucht 2 falsche", s.x, s.de);
    d.forEach(z => { const w = W.get(z); if (!w) E("Lücke: Wort nicht gelernt", z, s.de); else if (w.n > ln) E("Lücke: Wort kommt erst später", z, "L"+w.n, ">", "L"+ln, s.de);
      if (T[k] && z === T[k].zh) E("Lücke: falsches = richtiges", z, s.de);
      const alt = T.map((t, j) => j === k ? z : t.zh).join(""); if (keys.has(alt) || seen.has(alt) || window.ZH_DRILL.some(o => o.t.split(" ").map(x => x.split("|")[0]).join("") === alt)) E("Lücke ergibt einen richtigen Satz", alt); });
  } else E("keine Lücke", s.de);
  if (s.bad) { nBad++;
    const B = tok(s.bad, s.de, "Falsch"); B.forEach(b => { if (b.n > ln) E("Falsch-Satz nutzt späteres Wort", b.zh, s.de); });
    if (B.map(b => b.zh).join("") === key) E("Falsch-Satz = richtig", s.de);
    if (!s.why) E("Begründung fehlt", s.de);
  }
  per[ln] = (per[ln]||0) + 1;
});
console.log("Sätze:", window.ZH_DRILL.length, "mit Lücke:", nGap, "mit Falsch-Satz:", nBad);
console.log("ab Lektion:", Object.keys(per).sort((a,b)=>a-b).map(k => "L"+k+":"+per[k]).join(" "));
console.log(err ? err + " Fehler" : "Keine Fehler");
