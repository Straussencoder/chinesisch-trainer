import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import json, re, unicodedata
from pypinyin import pinyin, Style
items = json.load(open(ROOT + "/audit/items.json"))
def syls_of(py):
    out = []
    for w in py.split(" "):
        for s in w.split("_"):
            s = re.sub(r"[^\w']", "", s, flags=re.UNICODE).replace("'", "")
            if s: out.append(s.lower())
    return out
def han(s): return [c for c in s if '一' <= c <= '鿿']
def strip_tone(s): return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").replace("ü","v")
def tone(s):
    d = unicodedata.normalize("NFD", s)
    for c, t in (("̄",1),("́",2),("̌",3),("̀",4)):
        if c in d: return t
    return 0
rows = []
for it in items:
    hz = "".join(han(it["zh"]))
    mine = syls_of(it["py"])
    ref = [p[0] for p in pinyin(hz, style=Style.TONE)]
    from pypinyin import lazy_pinyin
    ref_s = lazy_pinyin(hz, style=Style.TONE, tone_sandhi=True)
    if len(mine) != len(ref):
        rows.append((it["src"], it["zh"], it["py"], " ".join(ref), "SILBENZAHL")); continue
    for i,(m, r, rs) in enumerate(zip(mine, ref, ref_s)):
        if m == r.lower(): continue
        if strip_tone(m) != strip_tone(r.lower()) and not (strip_tone(m)=="r" ):
            kind = "ANDERE SILBE"
        elif m == rs.lower(): kind = "Tonwechsel (Sandhi) wie Wörterbuch mit Sandhi"
        elif tone(m)==0: kind = "bei mir neutral"
        elif tone(r)==0: kind = "Wörterbuch neutral"
        else: kind = "ANDERER TON"
        rows.append((it["src"], it["zh"], it["py"], " ".join(ref), f"{hz[i] if i < len(hz) else '?'}: {m} vs {r} → {kind}"))
for r in rows: print(" | ".join(r))
print(len(items), "Einträge geprüft,", len(rows), "Abweichungen")
