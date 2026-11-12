#!/usr/bin/env bash
# Einmalige Einrichtung nach dem Klonen: Schriften, Hanzi-Writer, Playwright, Ordner.
set -e
cd "$(dirname "$0")/.."
mkdir -p test test2 shots/r2 shots/v5 audit
# Schriften fuer die Tests (Google Fonts werden im Test lokal umgeleitet)
(cd dl/fonts/npm && npm ci --silent)
# Hanzi-Writer (Quelle fuer schreiben.js)
for t in dl/hw/*.tgz; do d="${t%.tgz}"; [ -d "$d" ] || { mkdir -p "$d" && tar -xzf "$t" -C "$d"; }; done
# eslint
npm install --silent
# Playwright fuer die Browser-Tests. Ein schon vorhandenes Chromium wird benutzt, nicht neu geladen.
# Ist schon ein Playwright fuer Node da (z. B. in Claude Code im Browser), dieselbe Version nehmen, sonst passt der Browser nicht.
v=$(node -e "console.log(require('playwright/package.json').version)" 2>/dev/null || true)
python3 -c "import playwright" 2>/dev/null || pip install "playwright${v:+==$v}" --break-system-packages
if python3 - <<'EOF' 2>/dev/null
from playwright.sync_api import sync_playwright
with sync_playwright() as p: p.chromium.launch().close()
EOF
then echo "Chromium ist schon da."
else python3 -m playwright install chromium
fi
echo "Einrichtung fertig."
