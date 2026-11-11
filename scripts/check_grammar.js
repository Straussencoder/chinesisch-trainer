// Prüft die Satzbau-Daten: jedes Wort hat Satzteil, Wortart und Übersetzung; Anzahl passt; Baupläne vorhanden.
const fs = require("fs"), dir = process.argv[2];
const window = {};
eval(fs.readFileSync(dir + "/lessons.data.js", "utf8"));
eval(fs.readFileSync(dir + "/data.js", "utf8"));
eval(fs.readFileSync(dir + "/grammar.data.js", "utf8"));
const G = window.ZH_GRAMMAR, L = window.ZH_LESSONS, D = window.ZH_DATA;
const SLOTS = "SVOADTLZQPX".split(""), WC = ["Pronomen","Nomen","Name","Verb","Hilfsverb","Adjektiv","Adverb","Fragewort","Zahl","Zählwort","Partikel","Präposition","Zeitangabe","Ortswort","Mengenwort","Ausdruck","Anrede","Konjunktion"];
let err = [], n = 0;
const isSyl = s => /[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/.test(s);
function parseG(g, where){
  return g.split("|").map(x => { const m = x.match(/^(\S) (\S+) (.+)$/); if(!m){ err.push(where + ": kaputt '" + x + "'"); return null; }
    if(!SLOTS.includes(m[1])) err.push(where + ": Satzteil " + m[1]); if(!WC.includes(m[2])) err.push(where + ": Wortart " + m[2]); return m; });
}
const lessonIds = {}, pointIds = {};
L.forEach(u => u.lessons.forEach(l => lessonIds[l.id] = l));
G.points.forEach(p => { pointIds[p.id] = p; if(!lessonIds[p.l]) err.push("Bauplan " + p.id + ": Lektion " + p.l);
  p.ex.forEach((e, i) => { const toks = e.t.split(" "); const g = parseG(e.g, "Bauplan " + p.id); if(g.length !== toks.length) err.push("Bauplan " + p.id + " Beispiel " + i + ": " + g.length + " vs " + toks.length); n++; }); });
const usedKeys = {};
L.forEach(u => u.lessons.forEach(l => {
  const words = {}; l.words.forEach(w => words[w[0]] = 1);
  l.words.forEach(w => { if(!G.wc[w[0]]) err.push("Wortart fehlt: " + w[0]); else G.wc[w[0]].split(", ").forEach(x => { if(!WC.includes(x)) err.push("Wortart " + w[0] + ": " + x); }); });
  const gps = {};
  l.sents.forEach(s => {
    const toks = s.t.split(" "), key = toks.map(t => t.split("|")[0]).join(""); usedKeys[key] = 1;
    const a = G.sents[key]; if(!a){ err.push("Satz ohne Zerlegung: " + key); return; }
    const g = parseG(a.g, key); if(g.length !== toks.length) err.push(key + ": " + g.length + " Teile, " + toks.length + " Wörter");
    if(!pointIds[a.gp]) err.push(key + ": Bauplan " + a.gp + " fehlt"); else gps[a.gp] = 1;
    if(!a.n) err.push(key + ": Erklärung fehlt"); n++;
  });
  G.points.filter(p => p.l === l.id).forEach(p => { if(l.sents.length && !gps[p.id] && p.id !== "base") err.push("Bauplan " + p.id + " in " + l.id + " ohne Satz"); });
}));
Object.keys(G.sents).forEach(k => { if(!usedKeys[k]) err.push("Zerlegung ohne Satz: " + k); });
D.cards.forEach(c => {
  const chunks = c.py.split(" ").filter(w => w.split("_").filter(isSyl).length);
  const a = G.cards[c.id]; if(!a){ err.push("Karte ohne Zerlegung: " + c.id); return; }
  const g = parseG(a.g, c.id); if(g.length !== chunks.length) err.push(c.id + ": " + g.length + " Teile, " + chunks.length + " Wörter (" + c.py + ")");
  if(!a.n) err.push(c.id + ": Erklärung fehlt"); n++;
});
Object.keys(G.cards).forEach(k => { if(!D.cards.find(c => c.id === k)) err.push("Zerlegung ohne Karte: " + k); });
console.log("Geprüft:", n, "Sätze und Beispiele,", G.points.length, "Baupläne,", Object.keys(G.wc).length, "Wortarten");
console.log(err.length ? err.join("\n") : "Keine Fehler");
