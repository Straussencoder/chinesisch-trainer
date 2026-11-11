// Baut zh-app/texts.data.js aus scripts/texts_src.js. Pinyin kommt aus dem Wörterbuch der App, die Lektion aus dem spätesten Wort.
const fs = require("fs");
const P = require(require("path").resolve(__dirname, "..") + "/scripts/pinyin_lib.js");
const SRC = require(require("path").resolve(__dirname, "..") + "/scripts/texts_src.js");
const esc = x => JSON.stringify(x);
const KINDS = ["Nachricht", "Chat", "Speisekarte", "Preisschild", "Schild", "Notiz", "Einkaufszettel"];
let out = "/* Kurze Texte zum Lesen mit Verständnisfragen. Nur Wörter aus dem Lernpfad (plus Namen).\n   Erzeugt mit scripts/build_texts.js aus scripts/texts_src.js. lesson: ab dieser Lektion lesbar. */\nwindow.ZH_TEXTS = [\n";
const ids = new Set(); let nq = 0;
const items = SRC.map(t => {
  if(ids.has(t.id)) throw new Error("Doppelte Kennung " + t.id); ids.add(t.id);
  if(!KINDS.includes(t.kind)) throw new Error(t.id + ": unbekannte Art " + t.kind);
  let lesson = 0;
  const lines = t.lines.map(l => { lesson = Math.max(lesson, P.lessonOf(l[0])); return {zh:l[0], py:P.pinyin(l[0]), de:l[1], s:l[2] || "a"}; });
  if(t.qs.length < 2 || t.qs.length > 3) throw new Error(t.id + ": 2 bis 3 Fragen nötig");
  const qs = t.qs.map(q => {
    if(q[1].length !== 3 || new Set(q[1]).size !== 3) throw new Error(t.id + ": jede Frage braucht 3 verschiedene Antworten: " + q[0]);
    if(q[2] < 0 || q[2] > 2) throw new Error(t.id + ": richtige Antwort fehlt: " + q[0]);
    if(q[3] < 0 || q[3] >= lines.length) throw new Error(t.id + ": Zeile fehlt: " + q[0]);
    nq++; return {q:q[0], opts:q[1], a:q[2], l:q[3]};
  });
  return {id:t.id, kind:t.kind, title:t.title, from:t.from, lesson, lines, qs};
});
items.sort((a, b) => a.lesson - b.lesson || a.id.localeCompare(b.id));
out += items.map(t => `  {id:${esc(t.id)}, kind:${esc(t.kind)}, title:${esc(t.title)}, lesson:${t.lesson}, from:{zh:${esc(t.from.zh)}, de:${esc(t.from.de)}}, lines:[\n` +
  t.lines.map(l => `    {zh:${esc(l.zh)}, py:${esc(l.py)}, de:${esc(l.de)}${l.s !== "a" ? ", s:" + esc(l.s) : ""}}`).join(",\n") + "],\n   qs:[\n" +
  t.qs.map(q => `    {q:${esc(q.q)}, opts:${esc(q.opts)}, a:${q.a}, l:${q.l}}`).join(",\n") + "]}").join(",\n") + "\n];\n";
fs.writeFileSync(require("path").resolve(__dirname, "..") + "/zh-app/texts.data.js", out);
console.log("geschrieben", items.length, "Texte,", items.reduce((a, t) => a + t.lines.length, 0), "Zeilen,", nq, "Fragen; ab Lektion:", items.map(t => t.id + ":" + t.lesson).join(" "));
