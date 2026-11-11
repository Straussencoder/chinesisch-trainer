cd "$(dirname "$0")/.."
python3 scripts/build_page.py zh-app >/dev/null; python3 scripts/build_page.py zh-app test test/index.html >/dev/null; cp zh-app/audio-?.js zh-app/pinyin.js zh-app/schreiben.js test/ 2>/dev/null; cp -r zh-app/img test/
rm -f test/suite_done
for n in check_lessons check_grammar check_dialogs check_data; do echo "=== $n"; case $n in check_lessons) node scripts/$n.js zh-app/lessons.data.js dl/audio-cmn;; check_data) node scripts/$n.js zh-app/index.html;; *) node scripts/$n.js zh-app;; esac 2>&1 | tail -3; done; node scripts/check_drill.js | tail -2; echo "=== build_texts"; node scripts/build_texts.js | cut -c1-80
for t in "fulltest.py mobile" "fulltest.py desktop" settingstest.py gametest.py edgetest.py lessontest.py owntest.py typetest.py dialogtest.py drawtest.py wtest.py chattest.py quiettest.py seentest.py srstest.py senttest.py numtest.py extratest.py r5test.py r6test.py sweep.py; do
  echo "=== $t"; timeout 1500 python3 scripts/$t 2>&1 | grep -E "FEHLER|Fehler|Error|error| / |^ok|Probleme|issues" | tail -15
done
touch test/suite_done
