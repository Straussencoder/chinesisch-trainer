# Runde 6: Nachsprechen, Bauplan-Wiederholplan, Gespräche hören, kurze Texte, Sprechen, Aufnahmen in Teilen.
import subprocess, sys
T = [["scripts/r6_rectest.py", "scripts/fake/t2.wav", "toene"], ["scripts/r6_rectest.py", "scripts/fake/w13.wav", "intro"], ["scripts/r6_rectest.py", "scripts/fake/silent.wav", "toene"],
     ["scripts/r6_pattest.py"], ["scripts/r6_lsntest.py"], ["scripts/r6_txttest.py"], ["scripts/r6_saytest.py"], ["scripts/r6_audtest.py"], ["scripts/r6_edge2.py"]]
ok = 0
for t in T:
    r = subprocess.run(["python3"] + t, capture_output=True, text=True, timeout=600)
    good = r.returncode == 0 and "errs []" in r.stdout
    ok += good
    print(("OK  " if good else "FEHLER ") + " ".join(t[0:1] + t[2:3]) + ("" if good else "\n" + r.stdout[-800:] + r.stderr[-1200:]))
print(ok, "/", len(T))
