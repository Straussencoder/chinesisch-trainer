import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys
from playwright.sync_api import sync_playwright
path = sys.argv[1]
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto("file://" + path + "#toene")
    pg.click('.tbtn[data-tone="2"]')
    pg.evaluate("location.hash='saetze'")
    pg.click("#c-reveal")
    pg.click('[data-act="good"]')
    pg.click("#c-reveal")
    pg.evaluate("location.hash='heute'")
    pg.wait_for_timeout(300)
    pg.evaluate("document.querySelectorAll('.view').forEach(v=>v.classList.add('on'))")
    pg.screenshot(path=ROOT + "/shots/all.png", full_page=True)
    b.close()
print("errors:", [e for e in errs if "fonts.g" not in e and "net::" not in e])
