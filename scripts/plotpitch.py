# Zeichnet Tonhöhe (Halbtöne, normiert) und Lautstärke für ausgewählte Aufnahmen.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys, subprocess, tempfile, urllib.parse
import numpy as np, parselmouth
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
AUDIO = ROOT + "/dl/audio-cmn"
items = [x.split("=") for x in sys.argv[2:]]   # key=label, key is syl:ma1 or w:你好
out = sys.argv[1]
n = len(items); cols = 4; rows = (n + cols - 1)//cols
fig, axs = plt.subplots(rows, cols, figsize=(cols*3.6, rows*2.4), squeeze=False)
for ax, (key, label) in zip(axs.flat, items):
    kind, k = key.split(":", 1)
    path = f"{AUDIO}/syl/{k}.mp3" if kind == "syl" else f"{AUDIO}/hsk/{urllib.parse.quote(k)}.mp3"
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        subprocess.run(["ffmpeg","-v","quiet","-y","-i",path,"-ac","1","-ar","22050",t.name], check=True)
        snd = parselmouth.Sound(t.name)
    p = snd.to_pitch_ac(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
    f0 = p.selected_array["frequency"]; xs = p.xs()
    inten = snd.to_intensity(time_step=0.01)
    ax2 = ax.twinx()
    ax2.plot(inten.xs(), inten.values[0], color="#bbb", lw=1)
    ax2.set_yticks([])
    v = np.where(f0 > 0, f0, np.nan)
    ax.plot(xs, v, ".", ms=3, color="#c0392b")
    ax.set_ylim(120, 520); ax.set_yscale("log")
    ax.set_yticks([150, 200, 250, 300, 400]); ax.set_yticklabels(["150","200","250","300","400"], fontsize=7)
    ax.set_title(label, fontsize=9)
    ax.tick_params(axis="x", labelsize=7)
for ax in list(axs.flat)[n:]: ax.axis("off")
plt.tight_layout(); plt.savefig(out, dpi=80)
print("ok", out)
