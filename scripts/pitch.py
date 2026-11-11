# Misst den Tonhöhenverlauf aller verwendeten Silben-Aufnahmen und prüft, ob er zum Ton passt.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import os, sys, json, glob, subprocess, tempfile
import numpy as np
import parselmouth

AUDIO = ROOT + "/dl/audio-cmn"

def load(path):
    # mp3 -> wav über ffmpeg, dann Praat-Pitch
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-i", path, "-ac", "1", "-ar", "22050", t.name], check=True)
        snd = parselmouth.Sound(t.name)
    pitch = snd.to_pitch_ac(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
    f0 = pitch.selected_array["frequency"]
    times = pitch.xs()
    inten = snd.to_intensity(time_step=0.01)
    return snd, f0, times, inten

def contour(f0):
    v = f0[f0 > 0]
    if len(v) < 6:
        return None
    # längsten zusammenhängenden stimmhaften Abschnitt nehmen
    voiced = f0 > 0
    best, cur, start, bs = 0, 0, 0, 0
    for i, x in enumerate(voiced):
        if x:
            if cur == 0: start = i
            cur += 1
            if cur > best: best, bs = cur, start
        else:
            cur = 0
    seg = f0[bs:bs+best]
    # Ränder abschneiden (Ein- und Ausschwingen)
    k = max(1, len(seg)//10)
    seg = seg[k:len(seg)-k] if len(seg) > 8 else seg
    st = 12*np.log2(seg)
    # Median-Glättung
    sm = np.array([np.median(st[max(0,i-2):i+3]) for i in range(len(st))])
    idx = np.linspace(0, len(sm)-1, 10)
    return np.interp(idx, np.arange(len(sm)), sm), len(seg)

def tone_of(key):
    return int(key[-1])

files = sorted(glob.glob(AUDIO + "/syl/*.mp3"))
data = {}
for f in files:
    key = os.path.basename(f)[:-4]
    try:
        snd, f0, t, inten = load(f)
        c = contour(f0)
        if c is None:
            data[key] = None; continue
        data[key] = {"c": c[0].tolist(), "n": c[1], "dur": snd.duration,
                     "hz": float(np.median(f0[f0 > 0]))}
    except Exception as e:
        data[key] = None
        print("Fehler", key, e)

ok = {k: v for k, v in data.items() if v}
ref = np.median([np.mean(v["c"]) for v in ok.values()])
print("Sprecherin Silben: Median", round(np.median([v["hz"] for v in ok.values()])), "Hz")

def feats(c):
    c = np.array(c) - ref
    return np.array([c[0], c[3], c[5], c[7], c[9], c.min(), np.argmin(c)/9, c[9]-c[0], c.max()-c.min()])

X = {k: feats(v["c"]) for k, v in ok.items()}
labels = {k: tone_of(k) for k in ok}
# Klassen-Mittelwerte (leave-one-out)
def predict(k):
    best, bd, dists = None, 1e9, {}
    for t in (1, 2, 3, 4):
        others = [X[j] for j in X if labels[j] == t and j != k]
        if not others: continue
        mu = np.mean(others, axis=0); sd = np.std(others, axis=0) + 0.8
        d = float(np.sqrt(np.sum(((X[k]-mu)/sd)**2)))
        dists[t] = d
        if d < bd: best, bd = t, d
    return best, dists

bad = []
for k in sorted(ok):
    p, d = predict(k)
    if p != labels[k]:
        margin = d[labels[k]] - d[p]
        bad.append((k, p, round(margin, 2), [round(x, 1) for x in (np.array(ok[k]["c"]) - ref)]))
print("Silben geprüft:", len(ok), "ohne Messung:", [k for k, v in data.items() if not v])
print("Auffällig (Messung passt eher zu anderem Ton):", len(bad))
for b in bad:
    print("  ", b[0], "-> klingt eher nach Ton", b[1], "Abstand", b[2], "Verlauf (Halbtöne):", b[3])
# Mittlere Verläufe zur Kontrolle
for t in (1, 2, 3, 4):
    cs = np.array([np.array(v["c"]) - ref for k, v in ok.items() if labels[k] == t])
    print("Ton", t, "mittlerer Verlauf:", [round(x, 1) for x in cs.mean(axis=0)], "n=", len(cs))
json.dump({"ref": ref, "data": data, "bad": [b[0] for b in bad]}, open(ROOT + "/audit/pitch_syl.json", "w"))
