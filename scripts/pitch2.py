# Genauere Prüfung: Oktavsprünge entfernen, Regeln pro Ton, auch Wort-Aufnahmen (2 Silben).
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import os, sys, json, glob, subprocess, tempfile, re
import numpy as np
import parselmouth

AUDIO = ROOT + "/dl/audio-cmn"
MARK = {}
for chars, t in (("āēīōūǖ",1),("áéíóúǘ",2),("ǎěǐǒǔǚ",3),("àèìòùǜ",4)):
    for c in chars: MARK[c] = t
def tone_of_py(s):
    for c in s.lower():
        if c in MARK: return MARK[c]
    return 0

def analyse(path):
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-i", path, "-ac", "1", "-ar", "22050", t.name], check=True)
        snd = parselmouth.Sound(t.name)
    p = snd.to_pitch_ac(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
    f0 = p.selected_array["frequency"].copy()
    inten = snd.to_intensity(time_step=0.01)
    it = np.array([inten.get_value(x) or 0 for x in p.xs()])
    return snd, f0, it

def clean_segments(f0):
    """Stimmhafte Abschnitte (Indexbereiche), Oktavsprünge entfernt, Halbtöne."""
    st = np.where(f0 > 0, 12*np.log2(np.where(f0 > 0, f0, 1)), np.nan)
    med = np.nanmedian(st)
    st[np.abs(st - med) > 9] = np.nan          # Oktavfehler raus
    segs, cur = [], []
    for i, x in enumerate(st):
        if not np.isnan(x): cur.append(i)
        elif cur: segs.append(cur); cur = []
    if cur: segs.append(cur)
    segs = [s for s in segs if len(s) >= 5]
    return st, segs

def shape(st, idx):
    v = st[idx]
    k = max(1, len(v)//8)
    v = v[k:len(v)-k] if len(v) > 10 else v
    sm = np.array([np.median(v[max(0,i-2):i+3]) for i in range(len(v))])
    return np.interp(np.linspace(0, len(sm)-1, 10), np.arange(len(sm)), sm)

def judge(c, ref, t):
    c = np.array(c) - ref
    start, end, mn, mx = c[:2].mean(), c[-2:].mean(), c.min(), c.max()
    amin = int(np.argmin(c))
    ok = {
        1: (mx - mn) < 3.5 and c.mean() > -1.5,
        2: (end - mn) > 2.5 and amin <= 6 and end > start,
        3: c.mean() < -2.5 or mn < -5,
        4: (start - end) > 2.5,
    }[t]
    return ok, [round(float(x), 1) for x in c]

# --- Silben ---
syl = {}
for f in sorted(glob.glob(AUDIO + "/syl/*.mp3")):
    k = os.path.basename(f)[:-4]
    snd, f0, it = analyse(f)
    st, segs = clean_segments(f0)
    if not segs: syl[k] = None; continue
    longest = max(segs, key=len)
    syl[k] = shape(st, longest)
ref_s = np.median([np.mean(v) for v in syl.values() if v is not None])
bad_syl = []
for k, c in syl.items():
    if c is None: bad_syl.append((k, "keine Tonhöhe messbar", [])); continue
    ok, cc = judge(c, ref_s, int(k[-1]))
    if not ok: bad_syl.append((k, "passt nicht zu Ton " + k[-1], cc))
print("SILBEN geprüft:", len(syl), "auffällig:", len(bad_syl))
for b in bad_syl: print("  ", b[0], b[1], b[2])

# --- Wörter (HSK, Sprecherin/Sprecher Yue Tan) ---
words = json.load(open(ROOT + "/audit/used_words.json"))   # {hanzi: pinyin}
res, hz = {}, []
for zh, py in words.items():
    f = AUDIO + "/hsk/" + __import__("urllib.parse").parse.quote(zh) + ".mp3"
    if not os.path.exists(f): continue
    snd, f0, it = analyse(f)
    hz += list(f0[f0 > 0])
    st, segs = clean_segments(f0)
    res[zh] = (py, st, segs, snd.duration)
ref_w = np.median([np.nanmedian(r[1]) for r in res.values()])
print("\nWORT-Aufnahmen:", len(res), "Median-Tonhöhe", round(float(np.median(hz))), "Hz")
bad_w = []
for zh, (py, st, segs, dur) in res.items():
    syls = py.split("_")
    tones = [tone_of_py(s) for s in syls]
    if not segs: bad_w.append((zh, py, "keine Tonhöhe messbar")); continue
    if len(syls) == 1:
        if tones[0] == 0: continue
        ok, cc = judge(shape(st, max(segs, key=len)), ref_w, tones[0])
        if not ok: bad_w.append((zh, py, "Ton passt nicht", cc))
        continue
    # 2 Silben: auf zwei Abschnitte aufteilen
    allidx = [i for s in segs for i in s]
    if len(segs) >= 2:
        segs2 = sorted(segs, key=len, reverse=True)[:2]; segs2.sort(key=lambda s: s[0])
        parts = segs2
    else:
        s = segs[0]; m = len(s)//2; parts = [s[:m], s[m:]]
    for i, (part, t) in enumerate(zip(parts, tones)):
        if t == 0 or len(part) < 5 or i >= 2: continue
        tt = t
        if t == 3 and i == 0 and len(tones) > 1 and tones[1] == 3: tt = 2
        if t == 3 and i == 0: continue  # halber 3. Ton vor anderem Ton: nur tief, schwer messbar
        ok, cc = judge(shape(st, part), ref_w, tt)
        if not ok: bad_w.append((zh, py, f"Silbe {i+1} passt nicht zu Ton {tt}", cc))
print("auffällig:", len(bad_w))
for b in bad_w: print("  ", *b)
json.dump({"bad_syl": [b[0] for b in bad_syl], "bad_words": [b[0] for b in bad_w]}, open(ROOT + "/audit/pitch_bad.json", "w"), ensure_ascii=False)
