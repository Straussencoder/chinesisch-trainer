// Prüft die Gespräche: nur bis zur Etappe gelernte Wörter, Silbenzahl passt, Pinyin passt zum Wörterbuch der App.
const fs = require("fs"), dir = process.argv[2];
const window = {};
eval(fs.readFileSync(dir + "/lessons.data.js", "utf8"));
eval(fs.readFileSync(dir + "/dialogs.data.js", "utf8"));
const L = window.ZH_LESSONS, DL = window.ZH_DIALOGS;
const MARK = {}; [["āēīōūǖĀĒĪŌŪǕ",1],["áéíóúǘÁÉÍÓÚǗ",2],["ǎěǐǒǔǚǍĚǏǑǓǙ",3],["àèìòùǜÀÈÌÒÙǛ",4]].forEach(p => Array.from(p[0]).forEach(c => MARK[c]=p[1]));
const BASE = {"ā":"a","á":"a","ǎ":"a","à":"a","ē":"e","é":"e","ě":"e","è":"e","ī":"i","í":"i","ǐ":"i","ì":"i","ō":"o","ó":"o","ǒ":"o","ò":"o","ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v"};
const toneOf = s => { for (const c of Array.from(s)) if (MARK[c]) return MARK[c]; return 0; };
const plain = s => Array.from(s.toLowerCase()).map(c => BASE[c]||c).join("").replace(/[^a-z]/g,"");
const isHan = c => /\p{Script=Han}/u.test(c), isSyl = s => /[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/.test(s);
const NAMES = {"弗洛里安":"Fú_luò_lǐ_'ān", "小明":"Xiǎo_Míng", "安娜":"Ān_nà"};
let err = 0, nLines = 0; const E = (...a) => { err++; console.log("FEHLER:", ...a); };
const known = new Map();
L.forEach(u => {
  u.lessons.forEach(l => l.words.forEach(w => known.set(w[0], w[1].split("_"))));
  const d = DL[u.id];
  if (!d) { E("kein Gespräch für", u.id); return; }
  const check = (zh, py, where) => {
    nLines++;
    const chars = Array.from(zh).filter(isHan), chunks = py.split(" ").map(w => w.split("_").filter(isSyl)).filter(x => x.length);
    const syls = chunks.flat();
    if (syls.length !== chars.length) { E(where, "Silbenzahl", zh, py); return; }
    let i = 0;
    chunks.forEach(ch => {
      const czh = chars.slice(i, i + ch.length).join(""), cs = ch.map(s => s.replace(/[^\p{L}']/gu, ""));
      i += ch.length;
      if (NAMES[czh]) return;
      // in bekannte Wörter zerlegen (längster Treffer zuerst)
      let k = 0;
      while (k < czh.length) {
        let hit = 0;
        for (let n = Math.min(4, czh.length - k); n > 0; n--) if (known.has(czh.slice(k, k + n))) { hit = n; break; }
        if (!hit) { E(where, "Wort noch nicht gelernt:", czh.slice(k), "in", zh); return; }
        const w = czh.slice(k, k + hit), ref = known.get(w), mine = cs.slice(k, k + hit);
        mine.forEach((m, j) => {
          const r = ref[j]; if (m.toLowerCase() === r.toLowerCase()) return;
          if (plain(m) !== plain(r)) { E(where, "andere Silbe", w, m, "vs", r); return; }
          const ok = ["不","一"].includes(w) || (["个","上","里"].includes(w) && !toneOf(m)) || (w === "不客气" && j === 0);
          if (!ok) E(where, "anderer Ton", w, m, "vs", r, "in", zh);
        });
        k += hit;
      }
    });
  };
  d.lines.forEach((ln, li) => { check(ln.zh, ln.py, u.id + ":" + li); (ln.alt || []).forEach((a, ai) => { check(a.zh, a.py, u.id + ":" + li + " alt" + ai); if (!a.why) E(u.id, "Begründung fehlt", a.zh); }); });
  if (!d.lines.some(l => l.alt)) E(u.id, "keine Auswahl im Gespräch");
});
console.log("Gespräche:", Object.keys(DL).length, "Zeilen inkl. Auswahl:", nLines);
console.log(err ? err + " Fehler" : "Keine Fehler");
