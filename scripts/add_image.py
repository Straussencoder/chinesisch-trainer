#!/usr/bin/env python3
"""Neues Etappen-Bild einbauen.

Aufruf:  python3 scripts/add_image.py 06 pfad/zum/bild.png
- legt das Original als dl/scenes/06.png ab,
- schreibt zh-app/img/06.webp (1280 px breit) und zh-app/img/06-640.webp,
- trägt die Etappe in SCENE_IMG in zh-app/scenes.part.js ein.
Danach: Build, Tests, veröffentlichen (siehe CLAUDE.md).
"""
import os, re, shutil, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIND = {"01": "gate", "02": "hutong", "03": "wall", "04": "tea", "05": "market",
        "06": "train", "07": "bund", "08": "water", "09": "lane", "10": "school",
        "11": "street", "12": "garden", "13": "lake", "14": "restaurant",
        "15": "tower", "16": "park", "17": "airport"}

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in KIND:
        sys.exit("Aufruf: add_image.py <01..17> <bild>")
    n, src = sys.argv[1], sys.argv[2]
    im = Image.open(src).convert("RGB")
    if abs(im.width / im.height - 1.5) > 0.05:
        print(f"Hinweis: Seitenverhältnis {im.width}x{im.height} ist nicht 3:2, das Bild wird beschnitten angezeigt.")
    os.makedirs(os.path.join(ROOT, "dl/scenes"), exist_ok=True)
    if os.path.abspath(src) != os.path.join(ROOT, f"dl/scenes/{n}.png"):
        im.save(os.path.join(ROOT, f"dl/scenes/{n}.png"))
    for w, name in ((1280, f"{n}.webp"), (640, f"{n}-640.webp")):
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(os.path.join(ROOT, "zh-app/img", name), quality=75, method=6)
    p = os.path.join(ROOT, "zh-app/scenes.part.js")
    s = open(p, encoding="utf-8").read()
    m = re.search(r"var SCENE_IMG = \{([^}]*)\};", s)
    items = dict(re.findall(r'(\w+):"(\d+)"', m.group(1)))
    items[KIND[n]] = n
    order = sorted(items.items(), key=lambda kv: kv[1])
    new = "var SCENE_IMG = {" + ", ".join(f'{k}:"{v}"' for k, v in order) + "};"
    s = s[:m.start()] + new + s[m.end():]
    open(p, "w", encoding="utf-8").write(s)
    print("eingebaut:", n, KIND[n])
    print(new)

if __name__ == "__main__":
    main()
