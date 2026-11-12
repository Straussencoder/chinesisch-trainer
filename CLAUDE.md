# Chinesisch-Trainer

Eigene Lern-App für Mandarin (HSK 1), gebaut für Florian. Eine einzelne HTML-Seite, veröffentlicht als Artifact auf claude.ai. Alles über Florian, seine Ziele und den Funktionsumfang der App steht in `docs/chinesisch-projekt.md`, die Prompts für die Etappen-Bilder in `docs/etappen-bilder-prompts.md`.

## Arbeitsregeln

- **Immer auf Deutsch antworten.** Schlichtes Deutsch, keine Werbe- oder KI-Sprache, keine Floskeln.
- **Bei Änderungswünschen erst einen Plan vorlegen** und erst nach Florians „go“ / „start“ loslegen. Ausnahme: Er sagt ausdrücklich, dass ich direkt anfangen soll.
- Sorgfältig arbeiten, keine Sprachfehler, weder im Deutschen noch im Chinesischen (Zeichen, Pinyin, Töne).
- Pinyin wie im Wörterbuch: unbetonte Silben ohne Tonzeichen, Tonwechsel bei 不/一 im Satz-Pinyin, 3.+3. Ton nicht umschreiben (siehe docs).
- In Lektionen, Sätzen, Gesprächen und Texten nur Wörter verwenden, die bis dahin gelernt sind. Die Prüfskripte achten darauf.
- Nach jeder Änderung: bauen, passende Tests laufen lassen, bei größeren Änderungen die ganze Testreihe. Erst dann veröffentlichen.
- `docs/chinesisch-projekt.md` bei neuen Funktionen mitpflegen.

## Aufbau

```
zh-app/            Quelle der App
  index.src.html   Vorlage (HTML, CSS, JS); Platzhalter werden beim Bauen ersetzt
  *.part.js        Teile, die in die Seite eingesetzt werden: scenes (Etappen-Bilder/Szenen),
                   fx, pitch (Tonkurven), game (Drachenboot-Rennen)
  *.data.js        Daten: lessons, grammar (Baupläne), dialogs, data, mnemo (Merkhilfen),
                   drill (Satz-Training), texts (kurze Texte)
  index.html       gebaute Seite (wird veröffentlicht)
  audio.js         alle Aufnahmen in einer Datei (Quelle für split_audio.js)
  audio-1..4.js    Aufnahmen in vier Teilen (werden veröffentlicht)
  pinyin.js        Aufnahmen der Pinyin-Tabelle (lädt erst bei Bedarf)
  schreiben.js     Strichdaten (Hanzi Writer)
  img/             Etappen-Bilder als .webp (1280 px) und -640.webp
scripts/           Bau-, Prüf- und Testskripte (siehe unten)
  fake/            künstliche Aufnahmen für die Mikrofon-Tests
dl/                Rohmaterial: audio-cmn (Aufnahmen), audio-pad (mit Stille), pinyin(-src),
                   mmah (Make Me a Hanzi), scenes (Original-PNGs der Bilder), hw (Hanzi Writer, .tgz)
docs/              Projektbeschreibung und Bild-Prompts
```

Erzeugte Ordner (nicht im Repo): `test/` (Test-Build), `test2/`, `shots/`, `audit/`, `node_modules/`, `dl/fonts/npm/node_modules/`.

## Einrichtung (einmal nach dem Klonen)

```
bash scripts/setup.sh
```
Holt die Schriften für die Tests (npm), entpackt Hanzi Writer, installiert eslint und Playwright und legt die Arbeitsordner an. Ist schon ein Chromium da (z. B. in Claude Code im Browser), wird es benutzt; Playwright für Python bekommt dann dieselbe Version wie das vorhandene für Node. Python 3 mit Pillow, Node 18+ und npm werden vorausgesetzt.

## Bauen

```
python3 scripts/build_page.py zh-app                       # -> zh-app/index.html (Produktion)
python3 scripts/build_page.py zh-app test test/index.html  # Test-Build mit window.__t
cp zh-app/audio-?.js zh-app/pinyin.js zh-app/schreiben.js test/ && cp -r zh-app/img test/
```
Der Test-Build hängt das Objekt `window.__t` an (Zugriff auf Zustand und Funktionen, z. B. `getS`, `state`, `startLesson`, `startReview`, `LESSONS`, `WORD` …) und lädt alle vier Audio-Teile sofort. Die Liste der freigegebenen Funktionen steht in `scripts/build_page.py`.

Daten neu erzeugen, wenn ihre Quelle geändert wurde:
- Kurze Texte: `node scripts/build_texts.js` (Quelle `scripts/texts_src.js`)
- Gespräche: `node scripts/build_dialogs.js` (Quelle `scripts/dialogs_src.js`)
- Aufnahmen: `node scripts/build_audio.js zh-app/index.html dl/audio-pad zh-app/audio.js`, danach `node scripts/split_audio.js` (siehe `scripts/AUDIO_README.txt`)

## Testen

- Ganze Testreihe (35–40 Minuten, am besten im Hintergrund): `bash scripts/runall.sh > test/suite.log 2>&1` — fertig, wenn `test/suite_done` existiert. In der Ausgabe nach „FEHLER“ / „Fehler“ suchen.
- Prüfskripte für die Daten (schnell): `node scripts/check_lessons.js zh-app/lessons.data.js dl/audio-cmn`, `node scripts/check_grammar.js zh-app`, `node scripts/check_dialogs.js zh-app`, `node scripts/check_data.js zh-app/index.html`, `node scripts/check_drill.js`
- Einzelne Browser-Tests (Playwright, brauchen den Test-Build): z. B. `python3 scripts/fulltest.py mobile`, `lessontest.py`, `srstest.py`, `r6test.py` …
- Zufallsklicker: `python3 scripts/monkeytest.py <frisch|mitte|alles|still|dunkel|mac> <schritte> <seed>`. Meldungen „hängt … app:#toene“ sind Fehlalarme (Knöpfe der Pinyin-Tabelle).
- eslint: `npx eslint -c scripts/eslint.config.mjs test/index.html` bzw. auf ausgezogene Skripte; Warnungen zu unbenutzten Variablen sind harmlos.
- Die Tests leiten Google Fonts auf lokale Dateien um (`scripts/fontroute.py`). Mikrofon und Spracherkennung werden über Chromium-Flags bzw. `add_init_script` nachgebaut; dabei immer `window.SpeechRecognition` **und** `webkitSpeechRecognition` ersetzen.
- Alle Pfade in den Skripten hängen am Repo-Ordner (`ROOT`, per `ZH_ROOT` überschreibbar).
- Alte Hilfsskripte aus früheren Runden (Bildschirmfotos, einmalige Umbauten, Tonhöhen-Analyse) wurden am 12.11.2026 gelöscht. Sie stehen noch in der Git-Geschichte (erster Commit).

## Veröffentlichen

Die App läuft als Artifact auf claude.ai, weil sie dessen Funktionen nutzt (Datenbank für den Lernstand, Anmeldung, Claude für das freie Gespräch):
- Slug: `eaee8426-2b03-4d48-8ea2-c5919007e2aa`
- Link: https://claude.ai/artifact/W1bszcWm8iBVbNZ4WZE88q
- Stand bei der Übertragung: Version `1794085414-b9b4` (11.11.2026)
- Zuletzt veröffentlicht: Version `1794515919-254b` (12.11.2026, Ton-Duell, hartnäckige Wörter, Tagesrunde nach Pausen; davor `1794494507-d081` Design, `1794085414-b9b4` Übertragung)
- Fähigkeiten: `{db:{}, user:{}, sample:{}}`

Veröffentlicht werden genau diese Dateien: `index.html`, `audio-1.js` … `audio-4.js`, `pinyin.js`, `schreiben.js`, `img/*.webp`. Wenn die Artifact-Werkzeuge (`mcp__claude-artifacts__*`) in der Sitzung da sind: erst `get_artifact` (aktuelle Version), dann `publish_files` mit `slug` und `base_version`, jede Datei mit `as` = Pfad im Artifact. Ohne diese Werkzeuge: Florian veröffentlicht über einen Chat im claude.ai-Projekt „🇨🇳 CHINESISCH“, der das Repo einliest.

Außerhalb von claude.ai (z. B. lokal geöffnet) läuft die App auch, speichert dann aber nur im Browser, und das freie Gespräch geht nicht.

## Lernstand und Erinnerung

- Lernstand in der Artifact-Datenbank: `data/users/u_04twSZJsrC3BKQng2ROkuw/progress` (Felder u. a. `words{zh:{b,d,iv,e}}`, `days{datum:{xp,lessons,reviews}}`, `learn{done,dlg,lsn,txt}`, `pats`, `tips` (Hinweise der Heute-Karte: Datum des ersten Zeigens oder `x` = erledigt), `prefs{goal,tmode}`). Beim Laden bereinigt `normalize()` kaputte Einträge.
- Tägliche Erinnerung: geplante Aufgabe `trig_01AeGnvtRoVbZJpMXkyfiLjg`, jeden Tag 17:38 Uhr (Europe/Budapest), Push aufs Handy (Android). Sie liest den Lernstand aus der Datenbank und nennt fällige Wörter, Punkte von heute, Serie und nächste Lektion; ist das Tagesziel erreicht, nur „Heute schon geübt, nichts zu tun.“

## Etappen-Bilder

5 von 17 sind fertig (01–05). Neue Bilder einbauen:
```
python3 scripts/add_image.py 06 /pfad/zum/06.png
```
Das Skript speichert das Original in `dl/scenes/`, erzeugt beide `.webp`-Größen und trägt die Etappe in `SCENE_IMG` (`zh-app/scenes.part.js`) ein. Danach bauen, `python3 scripts/sweep.py` für die Ansichten, veröffentlichen (die neuen Bilder mit hochladen). Reihenfolge der Etappen: 06 train, 07 bund, 08 water, 09 lane, 10 school, 11 street, 12 garden, 13 lake, 14 restaurant, 15 tower, 16 park, 17 airport. Vorher prüfen: keine Schrift oder Fantasie-Zeichen im Bild.

## Quellen und Lizenzen

- Aufnahmen: audio-cmn (CC BY-SA)
- Strichdaten: Hanzi Writer / Make Me a Hanzi
- Schriften: Google Fonts (über @fontsource nur für die Tests)
