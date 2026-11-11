# Leitet Google-Fonts-Anfragen in Playwright auf lokale @fontsource-Dateien um.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import os, re
BASE = ROOT + "/dl/fonts/npm/node_modules/@fontsource/"
SETS = [("noto-sans", ["400", "500", "600", "700", "800"]), ("bodoni-moda", ["500", "600", "700"]),
        ("ma-shan-zheng", ["400"]), ("noto-serif-sc", ["400", "500", "600", "700"])]
def build_css():
    out = []
    for fam, ws in SETS:
        for w in ws:
            f = BASE + fam + "/" + w + ".css"
            if not os.path.exists(f): continue
            css = open(f).read()
            css = re.sub(r"url\(\./files/([^)]+)\)", lambda m: "url(https://fonts.gstatic.com/local/" + fam + "/files/" + m.group(1) + ")", css)
            out.append(css)
    return "\n".join(out)
CSS = None
def setup(page):
    global CSS
    if CSS is None: CSS = build_css()
    page.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=CSS))
    def font(r):
        path = BASE + r.request.url.split("/local/")[1]
        if os.path.exists(path): r.fulfill(status=200, content_type="font/woff2" if path.endswith("woff2") else "font/woff", body=open(path, "rb").read(), headers={"Access-Control-Allow-Origin": "*"})
        else: r.fulfill(status=404, body="")
    page.route("https://fonts.gstatic.com/**", font)
