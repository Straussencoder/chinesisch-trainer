import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
p = ROOT + "/zh-app/index.src.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, count=1):
    global s
    n = s.count(a); assert n == count, (n, a[:100]); s = s.replace(a, b)
DARK = "--sS:#86a8e0; --sV:#f08a7c; --sO:#6cc79c; --sA:#e2b45c; --sD:#bb9be6; --sT:#6ccbd6; --sL:#d8a07a; --sZ:#e591b6; --sQ:#b9b1a7; --sP:#bdb3a2; --sX:#bccb82;"
rep("    --nav:#0d0b08;\n    color-scheme: dark;\n  }\n}", "    --nav:#0d0b08;\n    " + DARK + "\n    color-scheme: dark;\n  }\n}")
rep("  --nav:#0d0b08;\n  color-scheme: dark;\n}", "  --nav:#0d0b08;\n  " + DARK + "\n  color-scheme: dark;\n}")
orn = lambda rot: ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='34' height='34' fill='none' stroke='%23c4362b' stroke-opacity='.55' stroke-width='1.5'%3E%3Cg transform='rotate(" + str(rot) + " 17 17)'%3E%3Cpath d='M2 32V2h30'/%3E%3Cpath d='M7 32V7h25'/%3E%3Cpath d='M7 14h7V7'/%3E%3Ccircle cx='12' cy='12' r='1.3' fill='%23c4362b' fill-opacity='.55' stroke='none'/%3E%3C/g%3E%3C/svg%3E\")")
rep("  --nav:#1b1814; --nav-ink:#efe6d4; --nav-muted:#a99f8c;",
    "  --nav:#1b1814; --nav-ink:#efe6d4; --nav-muted:#a99f8c;\n"
    "  --sS:#34568b; --sV:#b8352a; --sO:#2b7a57; --sA:#a06c14; --sD:#7a55a0; --sT:#1d7480; --sL:#8a5733; --sZ:#a3456e; --sQ:#5f5852; --sP:#857b6c; --sX:#5f6b2f;\n"
    "  --orn-tl:" + orn(0) + ";\n  --orn-tr:" + orn(90) + ";\n  --orn-br:" + orn(180) + ";\n  --orn-bl:" + orn(270) + ";")
css = r'''
/* ---------- Satzbau ---------- */
.s-S{--c:var(--sS)} .s-V{--c:var(--sV)} .s-O{--c:var(--sO)} .s-A{--c:var(--sA)} .s-D{--c:var(--sD)} .s-T{--c:var(--sT)}
.s-L{--c:var(--sL)} .s-Z{--c:var(--sZ)} .s-Q{--c:var(--sQ)} .s-P{--c:var(--sP)} .s-X{--c:var(--sX)}
.bauplan{display:flex; flex-wrap:wrap; align-items:center; gap:5px 6px}
.bp{display:inline-flex; flex-direction:column; align-items:center; padding:3px 10px 4px; border-radius:9px; background:var(--c); color:#fff; line-height:1.15; box-shadow:inset 0 -2px 0 rgba(0,0,0,.18)}
.bp b{font-size:13px; font-weight:700}
.bp small{font-size:10.5px; opacity:.88; white-space:nowrap}
:root[data-app-theme="dark"] .bp{color:#14110d}
@media (prefers-color-scheme: dark){ :root:not([data-app-theme="light"]) .bp{color:#14110d} }
.bp-plus, .sg-plus{color:var(--muted); font-weight:800; font-size:15px}
.sg-plus{align-self:center}
.bp-hint{display:flex; flex-wrap:wrap; align-items:center; gap:6px 10px; margin:-4px 0 12px}
.bp-cap, .sb-cap, .lg-cap{font-size:11.5px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin:0}
.satz{display:flex; flex-wrap:wrap; align-items:stretch; gap:6px; margin:8px 0 0}
.sg{display:flex; flex-direction:column; border-radius:12px; background:color-mix(in srgb, var(--c) 9%, var(--sheet)); box-shadow:inset 0 0 0 1.5px color-mix(in srgb, var(--c) 42%, transparent); padding:5px 5px 6px; min-width:0}
.sg-l{font-size:10.5px; font-weight:800; letter-spacing:.09em; text-transform:uppercase; color:var(--c); padding:0 5px 2px}
.sg-w{display:flex; flex-wrap:wrap; gap:2px}
.sw{display:flex; flex-direction:column; align-items:center; background:none; border:0; padding:2px 7px 3px; border-radius:9px; cursor:pointer; line-height:1.2; min-width:44px; color:var(--ink); font:inherit}
.sw:hover{background:color-mix(in srgb, var(--c) 15%, transparent)}
.sw-hz{font-family:var(--hanzi); font-size:calc(27px * var(--hz-scale)); line-height:1.25}
.sw-py{font-size:12.5px; font-weight:600}
.sw-gl{font-size:13px; font-weight:700; margin-top:1px}
.sw-wc{font-size:10.5px; color:var(--muted)}
.why{display:flex; gap:10px; align-items:flex-start; background:color-mix(in srgb, var(--gold) 10%, var(--sheet)); border-radius:12px; padding:10px 12px; font-size:14.5px; line-height:1.5; margin:10px 0 0; text-align:left}
.why .seal{flex:none; width:26px; height:26px; font-size:17px; border-radius:7px; background:var(--gold); color:#fff}
.why .hz{font-size:1.15em}
.satzbox{margin-top:18px; padding:12px 12px 14px; border-radius:16px; background:var(--sheet) var(--texture); box-shadow:0 0 0 1px var(--line), 0 12px 24px -20px rgba(31,27,22,.5); animation:inkin .45s cubic-bezier(.2,.8,.2,1)}
.satzbox.in-card{margin:2px 0 0; box-shadow:0 0 0 1px var(--line); text-align:left}
.wc-tag{display:inline-block; font-size:12px; font-weight:800; letter-spacing:.06em; padding:2px 10px; border-radius:999px; border:1.5px solid var(--line); color:var(--ink-2); background:var(--paper-2)}
.oldtag{display:inline-flex; align-items:center; gap:7px; margin:14px 0 -6px; padding:3px 12px 3px 4px; border-radius:999px; background:color-mix(in srgb, var(--gold) 16%, var(--sheet)); color:var(--ink-2); font-size:13px; font-weight:700}
.oldtag .seal{width:22px; height:22px; font-size:14px; border-radius:50%; background:var(--gold); color:#fff}
/* Bauplan als Schriftrolle */
.scroll{margin:14px auto 4px; max-width:640px; filter:drop-shadow(0 16px 22px rgba(31,27,22,.16))}
.sc-rod{position:relative; height:14px; margin:0 -10px; border-radius:7px; background:linear-gradient(#9a6a3f, #6b4424 55%, #4a2d17)}
.sc-rod::before, .sc-rod::after{content:""; position:absolute; top:-3px; width:12px; height:20px; border-radius:5px; background:linear-gradient(#e0bb5e, #a87a2a)}
.sc-rod::before{left:-8px} .sc-rod::after{right:-8px}
.sc-paper{padding:24px 22px 20px; background:var(--orn-tl) top 10px left 10px no-repeat, var(--orn-tr) top 10px right 10px no-repeat, var(--orn-br) bottom 10px right 10px no-repeat, var(--orn-bl) bottom 10px left 10px no-repeat, var(--texture) var(--sheet)}
.sc-kick{display:flex; align-items:center; gap:8px; margin:0 0 4px 22px; color:var(--seal); font-size:12.5px; font-weight:800; letter-spacing:.12em; text-transform:uppercase}
.sc-kick .seal{width:26px; height:26px; font-size:17px; border-radius:7px}
.sc-title{font-family:var(--display); font-weight:600; font-size:26px; line-height:1.2; margin:6px 0 12px; text-wrap:balance}
.sc-title .hz{font-size:1.05em}
.sc-text{font-size:16px; line-height:1.6; margin:14px 0 4px; max-width:58ch}
.sc-text .hz{font-size:1.15em}
.sc-ex{border-top:1px dashed var(--line); padding-top:12px; margin-top:14px}
.sc-de{margin:0; font-size:14.5px; color:var(--ink-2)}
.sc-de .hz{font-size:20px; margin-right:6px}
/* Wortkarte für neue Wörter */
.wordcard{margin:10px auto 0; max-width:520px; padding:22px 16px 20px; border-radius:18px; background:var(--orn-tl) top 10px left 10px no-repeat, var(--orn-tr) top 10px right 10px no-repeat, var(--orn-br) bottom 10px right 10px no-repeat, var(--orn-bl) bottom 10px left 10px no-repeat, var(--texture) var(--sheet); box-shadow:0 0 0 1px var(--line), 0 18px 32px -24px rgba(31,27,22,.55)}
.wordcard .center{margin-top:0}
/* Kopf der Übung */
.s-mid{flex:1; min-width:0; display:flex; flex-direction:column; gap:2px}
.s-ctx{display:flex; align-items:center; gap:7px; font-size:12.5px; font-weight:700; color:var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
.s-place{font-family:var(--brush); color:var(--seal); font-size:17px; line-height:1}
/* Tonkurven */
.tcurve{display:block; width:44px; height:26px; color:var(--ink); margin:1px 0 2px}
.rq-opt.tone .tcurve{width:38px; height:22px}
/* Karteikasten */
.kasten{display:grid; grid-template-columns:repeat(6, minmax(0, 1fr)); margin-top:16px; padding:10px 8px 0; border-radius:14px 14px 10px 10px; background:linear-gradient(#a8743f, #7a4f29); box-shadow:inset 0 2px 0 rgba(255,255,255,.25), inset 0 -3px 0 rgba(0,0,0,.25), 0 16px 28px -18px rgba(60,30,10,.75)}
.fach{position:relative; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; min-height:158px; margin:0 3px; padding:8px 2px 10px; border-radius:7px 7px 0 0; background:linear-gradient(#4a2f18, #33200f 45%); color:#f3e6cc; text-align:center; box-shadow:inset 0 0 0 1px rgba(0,0,0,.25)}
.fach::before{content:""; position:absolute; left:0; right:0; top:0; height:6px; border-radius:7px 7px 0 0; background:linear-gradient(#c4925a, #8d5d31)}
.stack{position:relative; width:78%; height:66px; margin-bottom:8px}
.stack i{position:absolute; left:0; right:0; bottom:calc(var(--i) * 6px); height:42px; border-radius:3px; background:linear-gradient(#fbf6ea 0 7px, #c23a2c 7px 8px, #fbf6ea 8px); box-shadow:0 1px 2px rgba(0,0,0,.45); transform:rotate(calc((var(--i) - 3) * .9deg))}
.fach b{font-family:var(--display); font-size:21px; line-height:1}
.fach span{font-size:11.5px; font-weight:700; margin-top:2px}
.fach small{font-size:10.5px; opacity:.75; line-height:1.2; margin-top:1px}
.fach.leer .stack::after{content:""; position:absolute; left:10%; right:10%; bottom:0; height:3px; border-radius:2px; background:rgba(255,255,255,.12)}
.kasten-sum{margin:12px 0 0; font-size:14.5px; color:var(--ink-2); text-align:center}
.kasten-sum b{font-variant-numeric:tabular-nums}
/* Baupläne-Übersicht */
.smode{margin-top:14px}
.legend-card{margin-top:14px; padding:14px 16px}
.legend{display:flex; flex-wrap:wrap; gap:6px; margin-top:8px}
.plan{margin-top:10px; border-radius:14px; background:var(--sheet) var(--texture); box-shadow:0 0 0 1px var(--line)}
.plan summary{display:flex; align-items:center; gap:10px; padding:13px 14px; cursor:pointer; list-style:none; font-size:16px}
.plan summary::-webkit-details-marker{display:none}
.plan summary b{flex:1; min-width:0}
.plan summary b .hz{font-size:1.1em}
.pl-chev{color:var(--muted); font-size:22px; line-height:1; transition:transform .2s}
.plan[open] .pl-chev{transform:rotate(90deg)}
.pl-n{flex:none; font-size:11.5px; font-weight:800; background:var(--seal); color:#fff; border-radius:6px; padding:2px 6px; font-variant-numeric:tabular-nums}
.plan.locked{display:flex; align-items:center; gap:10px; padding:11px 14px; opacity:.55; box-shadow:0 0 0 1px var(--line) inset; background:none}
.plan.locked b{flex:1; font-weight:600}
.plan.locked small{color:var(--muted); font-size:12.5px; white-space:nowrap}
.plan.locked .pl-n{background:var(--muted)}
.pl-body{padding:0 14px 16px}
.pl-body > p{font-size:15.5px; line-height:1.6; margin:12px 0 0}
.pl-body > p .hz{font-size:1.15em}
.oldsum{width:100%; max-width:560px}
.oldsum .rr-words{justify-content:center}
@media (max-width:520px){
  .fach{min-height:140px; margin:0 2px}
  .fach small{font-size:9.5px}
  .sc-paper{padding:22px 14px 18px}
  .sc-title{font-size:23px}
  .sw{min-width:38px; padding:2px 5px 3px}
}
'''
rep("/* ---------- Wiederholen ---------- */", css + "\n/* ---------- Wiederholen ---------- */")
open(p, "w", encoding="utf-8").write(s)
print("ok")
