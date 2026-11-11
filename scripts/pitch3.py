# Strengere, aber realistischere Regeln (Anlaut-Anstieg bei Ton 4 und späten Anstieg bei Ton 2 erlaubt).
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import os, glob, json, subprocess, tempfile, sys
import numpy as np, parselmouth
AUDIO = ROOT + "/dl/audio-cmn"
def contour(path):
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        subprocess.run(["ffmpeg","-v","quiet","-y","-i",path,"-ac","1","-ar","22050",t.name], check=True)
        snd = parselmouth.Sound(t.name)
    f0 = snd.to_pitch_ac(time_step=0.01, pitch_floor=75, pitch_ceiling=500).selected_array["frequency"]
    st = np.where(f0 > 0, 12*np.log2(np.where(f0 > 0, f0, 1)), np.nan)
    med = np.nanmedian(st); st[np.abs(st-med) > 9] = np.nan
    v = st[~np.isnan(st)]
    if len(v) < 5: return None
    return np.array([np.median(v[max(0,i-2):i+3]) for i in range(len(v))])
data = {os.path.basename(f)[:-4]: contour(f) for f in sorted(glob.glob(AUDIO+"/syl/*.mp3"))}
ref = np.median([np.mean(c) for c in data.values() if c is not None])
def ok(c, t):
    c = c - ref; n = len(c); a, b = int(n*0.2), max(int(n*0.8), int(n*0.2)+1)
    if t == 1: return (np.ptp(c[a:b]) < 3.5) and c.mean() > -1.5
    if t == 2: return c[int(n*0.7):].mean() - c[:max(1,int(n*0.7))].min() > 2.0
    if t == 3: return c.min() < -4 or c.mean() < -2.5
    if t == 4: return c[:max(1,int(n*0.6))].max() - c[-max(1,n//6):].mean() > 3.0
flag = [k for k, c in data.items() if c is None or not ok(c, int(k[-1]))]
print("geprüft", len(data), "auffällig:", flag)
json.dump(flag, open(ROOT + "/audit/syl_flag.json","w"))
