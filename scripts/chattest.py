# Prüft das freie Gespräch mit einem nachgebauten Claude: Szenen, Pinyin aus dem Wörterbuch, Rückmeldung, Fehlerfälle, ohne Claude.
import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import sys, json; sys.path.insert(0, ROOT + "/scripts"); import fontroute
res = []
def ok(c, m): res.append(("OK  " if c else "FEHLER ") + m)
FAKE = """
window.__prompts = []; window.__mode = [];
const R = [
 {ok:null, his_zh:"", fix_zh:"", why_de:"", reply_zh:"你好！你喝什么？", reply_de:"Hallo! Was trinkst du?", hint_zh:"我喝茶。", hint_de:"Ich trinke Tee.", new_words:[]},
 {ok:true, his_zh:"我想喝茶。", fix_zh:"", why_de:"", reply_zh:"好！你要一杯茶吗？", reply_de:"Gut! Möchtest du eine Tasse Tee?", hint_zh:"要，谢谢。", hint_de:"Ja, danke.", new_words:[]},
 {ok:false, his_zh:"", fix_zh:"我很好。", why_de:"Vor einem Adjektiv steht kein 是.", reply_zh:"你喜欢绿茶吗？", reply_de:"Magst du grünen Tee?", hint_zh:"喜欢。", hint_de:"Ja.", new_words:[{zh:"绿茶", py:"lǜ chá", de:"grüner Tee"}]}
];
let k = 0;
const fake = function(){ return Promise.reject({code:"x"}); };
fake.json = function(input){ window.__prompts.push(input); const m = window.__mode.shift();
  if(m) return new Promise((res, rej) => setTimeout(() => rej({code:m}), 50));
  const r = R[Math.min(k++, R.length-1)]; return new Promise(res => setTimeout(() => res(JSON.parse(JSON.stringify(r))), 120)); };
window.claude = {use: (n) => Promise.resolve(n === "sample" ? fake : null)};
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for view, (w, h) in (("mobile", (390, 844)), ("desktop", (1366, 900))):
        ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page(); fontroute.setup(pg); pg.add_init_script(FAKE)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.ZH_AUDIO"); pg.wait_for_timeout(500)
        pg.evaluate("""() => { const T = window.__t, s = T.state(), t = T.today(); T.LESSONS.slice(0, 8).forEach(l => { s.learn.done[l.id] = {at:t, best:100}; l.W.forEach(w => s.words[w.zh] = {b:1, d:T.addDays(t,1)}); }); s.prefs.smode = 'chat'; location.hash='saetze'; }""")
        pg.wait_for_timeout(500)
        ok(pg.locator(".scen").count() == 5, f"{view}: 5 Szenen (frei + 4 geschaffte Etappen) ({pg.locator('.scen').count()})")
        pg.click('[data-scen="4"]'); pg.wait_for_timeout(400)
        pr = pg.evaluate("() => window.__prompts[0]")
        ok("Im Teehaus bestellen" in pr and "咖啡" in pr and "火车站" not in pr and "JSON" in pr, f"{view}: Auftrag nennt Szene und nur gelernte Wörter")
        ok(pg.locator(".chat-log .dl-b.a").count() == 1, f"{view}: Begrüßung erscheint")
        ok("Nǐhǎo! Nǐ hē shénme?" in pg.inner_text(".chat-log .dl-b.a .dl-py"), f"{view}: Pinyin aus dem eigenen Wörterbuch ({pg.inner_text('.chat-log .dl-b.a .dl-py')!r})")
        pg.click('[data-act="chathint"]'); ok(pg.is_visible(".c-hint") and "我喝茶" in pg.inner_text(".c-hint"), f"{view}: Tipp zeigt eine mögliche Antwort")
        pg.fill("#chat-in", "wo xiang he cha"); pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
        me = pg.inner_text(".chat-log .dl-b.me")
        ok("我想喝茶" in me and "Passt" in me, f"{view}: Pinyin-Eingabe wird zu Zeichen, Rückmeldung ✓ ({me[:40]!r})")
        pg.fill("#chat-in", "我是很好"); pg.click('[data-act="chatsend"]'); pg.wait_for_timeout(500)
        last_me = pg.locator(".chat-log .dl-b.me").last.inner_text()
        ok("Besser" in last_me and "我很好" in last_me and "是" in last_me, f"{view}: Fehler wird verbessert und erklärt")
        ok(pg.locator(".c-unk").count() >= 1 and "绿茶" in pg.inner_text(".c-new"), f"{view}: unbekanntes Wort markiert und erklärt")
        ok("lǜ" in pg.locator(".chat-log .dl-b.a").last.inner_text(), f"{view}: Pinyin für neues Wort aus Claudes Angabe")
        pg.evaluate("() => { window.__mode.push('not_granted'); }")
        pg.fill("#chat-in", "谢谢"); pg.keyboard.press("Enter"); pg.wait_for_timeout(400)
        ok("Freigabe" in pg.inner_text("#chat") and pg.input_value("#chat-in") == "谢谢", f"{view}: ohne Freigabe: Hinweis, Text bleibt im Feld")
        pg.evaluate("() => { window.__mode.push('rate_limited'); }")
        pg.keyboard.press("Enter"); pg.wait_for_timeout(400)
        ok("zu viele Anfragen" in pg.inner_text("#chat"), f"{view}: zu viele Anfragen: Hinweis")
        pg.click('[data-act="chatend"]'); pg.wait_for_timeout(200)
        ok(pg.locator(".scen").count() == 5, f"{view}: Beenden führt zur Szenenwahl")
        ok(not errs, f"{view}: keine JS-Fehler {errs[:3]}")
        ctx.close()
    # ohne Claude
    ctx = b.new_context(); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + ROOT + "/test/index.html"); pg.wait_for_function("!!window.__t"); pg.wait_for_timeout(300)
    pg.evaluate("() => { window.__t.state().prefs.smode = 'chat'; location.hash='saetze'; }"); pg.wait_for_timeout(500)
    ok("nur, wenn du die App in Claude öffnest" in pg.inner_text("#chat"), "ohne Claude: verständlicher Hinweis")
    # Pinyin-Helfer
    cases = pg.evaluate("""() => ['我不去。','一个人','一杯茶','你好吗？','这是我爸爸。','我们都是学生。','我要三个苹果。'].map(z => window.__t.pyOf(z).py)""")
    ok(cases == ['Wǒ bú qù.', 'Yí ge rén', 'Yì bēi chá', 'Nǐ_hǎo ma?', 'Zhè shì wǒ bà_ba.', 'Wǒ_men dōu shì xué_sheng.', 'Wǒ yào sān ge píng_guǒ.'], f"Pinyin-Helfer mit Tonwechseln {cases}")
    ok(not errs, f"ohne Claude: keine JS-Fehler {errs}")
    b.close()
print("\n".join(res))
