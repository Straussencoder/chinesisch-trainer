// Teilt zh-app/audio.js in Teile nach Etappen, damit die App beim Start nur lädt, was gerade gebraucht wird.
// Teil 1: Lektionen 1–8, Teil 2: 9–20, Teil 3: 21–33, Teil 4: alles Übrige (Tontraining, Reisesätze).
// Aufruf: node scripts/split_audio.js  → zh-app/audio-1.js … audio-4.js (audio.js bleibt als Ganzes für Prüfskripte erhalten)
const fs = require("fs"), path = require("path");
const dir = require("path").resolve(__dirname, "..") + "/zh-app";
const window = {dispatchEvent(){}}; function Event(){} eval(fs.readFileSync(path.join(dir, "audio.js"), "utf8"));
const A = window.ZH_AUDIO;
const lw = {}; eval(fs.readFileSync(path.join(dir, "lessons.data.js"), "utf8").replace("window.", "lw."));
const MARK = {}; [["āēīōūǖĀĒĪŌŪǕ",1],["áéíóúǘÁÉÍÓÚǗ",2],["ǎěǐǒǔǚǍĚǏǑǓǙ",3],["àèìòùǜÀÈÌÒÙǛ",4]].forEach(p => Array.from(p[0]).forEach(c => MARK[c]=p[1]));
const BASE = {"ā":"a","á":"a","ǎ":"a","à":"a","ē":"e","é":"e","ě":"e","è":"e","ī":"i","í":"i","ǐ":"i","ì":"i","ō":"o","ó":"o","ǒ":"o","ò":"o","ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v"};
const toneOf = s => { for (const c of Array.from(s)) if (MARK[c]) return MARK[c]; return 0; };
const plain = s => Array.from(s.toLowerCase()).map(c => BASE[c]||c).join("").replace(/[^a-z]/g, "");
const numeric = s => { const t = toneOf(s); return t ? plain(s) + t : null; };
const BOUND = [8, 20, 33];
const partOfLesson = n => n <= BOUND[0] ? 1 : n <= BOUND[1] ? 2 : 3;
const need = {s:{}, w:{}};
const take = (kind, key, part) => { if(!A[kind][key]) return false; need[kind][key] = Math.min(need[kind][key] || 9, part); return true; };
/* Wie clipsFor in der App: einzelnes Zeichen → Silbe (sonst Wort), mehrere Zeichen → Wortaufnahme, sonst Teilwörter und Silben mit Tonwechsel */
function addTok(zh, py, part, nextTone){
  const chars = Array.from(zh), syls = py.split("_"), tones = syls.map(toneOf);
  if(chars.length === 1){
    let n = numeric(syls[0]);
    if(n && tones[0] === 3){ take("s", plain(syls[0]) + "2", part); }
    if(n){ if(!take("s", n, part)) take("w", zh, part); return; }
    take("w", zh, part); return;
  }
  if(take("w", zh, part)) return;
  let i = 0;
  while(i < chars.length){
    let found = false;
    for(let j = chars.length; j > i+1; j--){ const sub = chars.slice(i, j).join(""); if(take("w", sub, part)){ i = j; found = true; break; } }
    if(found) continue;
    let t = tones[i]; if(!t){ i++; continue; }
    if(t === 3 && tones[i+1] === 3) t = 2;
    take("s", plain(syls[i]) + t, part); i++;
  }
}
let n = 0;
lw.ZH_LESSONS.forEach(u => u.lessons.forEach(l => {
  n++; const part = partOfLesson(n);
  l.words.forEach(w => addTok(w[0], w[1], part));
  l.sents.forEach(s => s.t.split(" ").forEach(t => { const [zh, py] = t.split("|"); addTok(zh, py, part); }));
  l.words.forEach(w => { if(w[3] && w[3].ex){ const [zh, py] = w[3].ex.split("|"); const chars = Array.from(zh).filter(c => /\p{Script=Han}/u.test(c)); let i = 0;
    py.split(" ").forEach(x => { const k = x.split("_").length; addTok(chars.slice(i, i + k).join(""), x, part); i += k; }); } });
}));
const parts = {1:{s:{}, w:{}}, 2:{s:{}, w:{}}, 3:{s:{}, w:{}}, 4:{s:{}, w:{}}};
["s", "w"].forEach(kind => Object.keys(A[kind]).sort().forEach(key => { const p = need[kind][key] || 4; parts[p][kind][key] = A[kind][key]; }));
const head = "/* Aufnahmen aus audio-cmn (https://github.com/hugolpz/audio-cmn), CC BY-SA. Silben: Chen Wang. Wörter: Yue Tan. Teil ";
Object.keys(parts).forEach(p => {
  const js = head + p + " von 4 (" + ({1:"Lektionen 1 bis 8", 2:"Lektionen 9 bis 20", 3:"Lektionen 21 bis 33", 4:"Tontraining und Reisesätze"})[p] + ") */\n" +
    "window.zhAudioPart(" + p + ", " + JSON.stringify(parts[p]) + ");\n";
  fs.writeFileSync(path.join(dir, "audio-" + p + ".js"), js);
  console.log("audio-" + p + ".js:", Object.keys(parts[p].s).length, "Silben,", Object.keys(parts[p].w).length, "Wörter,", (js.length/1024/1024).toFixed(2), "MB");
});
