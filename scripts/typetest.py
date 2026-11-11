# Prüft die Bewertung getippter Antworten
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
CASES = [
 ("谢谢","xie4xie",True,None), ("谢谢","xièxie",True,None), ("谢谢","xie4 xie5",True,None), ("谢谢","Xie4xie0",True,None), ("谢谢","xie4xie4",True,"neutral"),
 ("谢谢","xiexie",False,"notones"), ("谢谢","xie3xie",False,"tones"), ("谢谢","谢谢",True,None), ("谢谢","xie4xi",False,"letters"), ("谢谢","x4iexie",False,"place"),
 ("你好","ni3hao3",True,None), ("你好","ni2hao3",True,"33"), ("你好","nǐ hǎo",True,None), ("你好","ni hao",False,"notones"), ("你好","ni3hao",False,"tones"), ("你好","你号",False,"hzwrong"),
 ("想","yao4",True,"syn"), ("要","xiang3",True,"syn"), ("要","想",True,"syn"), ("是","zai4",False,"letters"), ("是","在",False,"hzwrong"),
 ("一点","yi4dian3",True,None), ("一点","yi1dian3",True,None), ("一点","yi2dian3",False,"tones"), ("一","yi1",True,None), ("一","yi4",False,"tones"),
 ("不","bu4",True,None), ("不","bu2",False,"tones"), ("汉语","Han4yu3",True,None), ("汉语","hàn yǔ",True,None), ("吗","ma",True,None), ("吗","ma5",True,None),
 ("好吃","hao3chi1",True,None), ("好吃","hao3chi",False,"tones"), ("好吃","hǎochī",True,None), ("中国","zhong1guo2",True,None), ("中国","zhongguo",False,"notones"),
 ("火车站","huo3che1zhan4",True,None), ("火车站","huǒchēzhàn",True,None), ("了","le",True,None), ("什么","shen2me",True,None), ("什么","shen2me1",True,"neutral"),
 ("德国","de2 guo2",True,None), ("去","qu4",True,None), ("去","qv4",False,"letters"), ("朋友","peng2you",True,None), ("朋友","péngyou",True,None),
 ("这个","zhe4ge",True,None), ("哪里","na3li3",True,None), ("哪里","na2li3",True,"33"), ("哪里","na3li",False,"tones"), ("", "", False, "empty"),
 ("哪儿","nar3",True,None), ("哪儿","na3r",True,None), ("哪儿","nǎr",True,None), ("哪儿","哪儿",True,None), ("哪儿","na3",False,"letters"),
 ("女儿","nv3er2",True,None), ("女儿","nü3ér",True,None), ("女儿","nu3er2",False,"letters"), ("不客气","bu2ke4qi",True,None), ("不客气","bu4ke4qi",True,None),
 ("对不起","dui4buqi3",True,None), ("对不起","dui4bu4qi3",True,"neutral"), ("个","ge4",True,None), ("个","ge",False,"notones"), ("谁","shei2",True,None),
 ("谁","shui2",True,None), ("喂","wei4",True,None), ("喂","wei2",True,None), ("喂","wei3",False,"tones"), ("怎么样","zen3meyang4",True,None),
 ("出租车","chu1zu1che1",True,None), ("北京","bei3jing1",True,None), ("北京","Beijing",False,"notones"), ("下雨","xia4yu3",True,None), ("我们","wo3men",True,None),
]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO")
    bad = []
    for zh, inp, ok, kind in CASES:
        r = pg.evaluate("([zh, inp]) => { const T = window.__t; return T.checkTyped(T.WORD[zh] || {zh:zh, syls:[], py:''}, inp); }", [zh, inp])
        got_ok = bool(r.get("ok")); got = r.get("kind")
        tag = "syn" if r.get("syn") else ("neutral" if "neutral" in (r.get("notes") or []) else ("33" if "33" in (r.get("notes") or []) else None))
        exp_tag = kind if ok else None
        if got_ok != ok or (not ok and got != kind) or (ok and (tag != exp_tag)):
            bad.append(f"{zh} '{inp}': erwartet {ok}/{kind}, bekommen {got_ok}/{got}/{tag}")
    print(len(CASES), "Fälle,", "Fehler:", bad or "keine")
    b.close()
