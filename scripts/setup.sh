#!/usr/bin/env bash
# Einmalige Einrichtung nach dem Klonen: Schriften, Hanzi-Writer, Playwright, Ordner.
set -e
cd "$(dirname "$0")/.."
mkdir -p test test2 shots/r1 shots/r2 shots/v5 shots/v6 audit
# Schriften fuer die Tests (Google Fonts werden im Test lokal umgeleitet)
(cd dl/fonts/npm && npm ci --silent)
# Hanzi-Writer (Quelle fuer schreiben.js)
for t in dl/hw/*.tgz; do d="${t%.tgz}"; [ -d "$d" ] || { mkdir -p "$d" && tar -xzf "$t" -C "$d"; }; done
# eslint
npm install --silent
# Playwright fuer die Browser-Tests
python3 -c "import playwright" 2>/dev/null || pip install playwright --break-system-packages
python3 -m playwright install chromium
echo "Einrichtung fertig."
