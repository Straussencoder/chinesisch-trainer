import os as _os; ROOT = _os.environ.get("ZH_ROOT") or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import re
p = ROOT + "/zh-app/index.src.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:90])
    s = s.replace(a, b)

# ---------- A: Schriften ----------
rep("family=Noto+Serif+Display:wght@600;700&", "family=Bodoni+Moda:opsz,wght@6..96,500;6..96,600;6..96,700&")
# ---------- B: Farben und Schrift-Variablen ----------
rep('  --display:"Noto Serif Display", "Noto Serif SC", Georgia, serif;', '  --display:"Bodoni Moda", "Noto Serif SC", Georgia, serif;\n  --nav:#1b1814; --nav-ink:#efe6d4; --nav-muted:#a99f8c;')
rep("    --shadow:0 1px 0 rgba(0,0,0,.4), 0 8px 22px -12px rgba(0,0,0,.7);\n    color-scheme: dark;\n  }\n}", "    --shadow:0 1px 0 rgba(0,0,0,.4), 0 8px 22px -12px rgba(0,0,0,.7);\n    --nav:#0d0b08;\n    color-scheme: dark;\n  }\n}")
rep("  --shadow:0 1px 0 rgba(0,0,0,.4), 0 8px 22px -12px rgba(0,0,0,.7);\n  color-scheme: dark;\n}", "  --shadow:0 1px 0 rgba(0,0,0,.4), 0 8px 22px -12px rgba(0,0,0,.7);\n  --nav:#0d0b08;\n  color-scheme: dark;\n}")

# ---------- C: Grundgerüst ----------
a = s.index("/* ---------- Grundgerüst ---------- */"); b = s.index("/* ---------- Bausteine ---------- */")
s = s[:a] + r'''/* ---------- Grundgerüst ---------- */
.app{min-height:100%; display:grid; grid-template-columns:minmax(0, 1fr)}
.sidebar{display:none}
.topbar{position:sticky; top:0; z-index:20; display:flex; align-items:center; justify-content:space-between; gap:10px; padding:10px 14px; background:color-mix(in srgb, var(--paper) 88%, transparent); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px)}
.topbar::after{content:""; position:absolute; left:0; right:0; bottom:-6px; height:6px; background:var(--huiwen) repeat-x; background-size:12px 12px; opacity:.5}
.logo{display:flex; align-items:center; gap:10px; text-decoration:none; color:inherit}
.seal{display:inline-grid; place-items:center; background:var(--seal); color:var(--seal-ink); border-radius:7px; font-family:var(--brush); line-height:1; box-shadow:inset 0 0 0 2px color-mix(in srgb, var(--seal-ink) 35%, transparent), inset 0 0 0 4px var(--seal)}
.logo .seal{width:40px; height:40px; font-size:28px; transform:rotate(-3deg)}
.logo-t{display:flex; flex-direction:column; line-height:1.15}
.logo-t b{font-family:var(--display); font-weight:600; font-size:18px; white-space:nowrap}
.logo-t span{font-size:12.5px; color:var(--muted)}
.chips-top{display:flex; gap:6px; align-items:center}
.stat-chip{display:inline-flex; align-items:center; gap:6px; background:var(--sheet); border-radius:999px; padding:3px 10px 3px 4px; font-weight:600; font-size:14px; font-variant-numeric:tabular-nums; white-space:nowrap; box-shadow:0 0 0 1px var(--line)}
.stat-chip .seal{width:24px; height:24px; font-size:16px; border-radius:50%}
.stat-chip.goal .seal{background:var(--gold)}
.gear{width:34px; height:34px; border-radius:50%; display:grid; place-items:center; background:var(--sheet); box-shadow:0 0 0 1px var(--line); color:var(--ink-2)}
.gear[aria-current="page"]{background:var(--seal); color:#fff; box-shadow:none}

main{min-width:0; padding:18px 16px calc(104px + env(safe-area-inset-bottom)); max-width:780px; width:100%; margin:0 auto}
.view{display:none}
.view.on{display:block; animation:inkin .55s cubic-bezier(.2,.8,.2,1)}
@keyframes inkin{from{opacity:0; transform:translateY(10px); filter:blur(4px)} to{opacity:1; transform:none; filter:none}}

.tabbar{position:fixed; left:10px; right:10px; bottom:calc(10px + env(safe-area-inset-bottom)); z-index:20; display:grid; grid-template-columns:repeat(5,1fr); gap:2px; background:var(--nav); border-radius:22px; padding:6px; box-shadow:0 14px 34px -12px rgba(0,0,0,.6), inset 0 0 0 1px rgba(255,255,255,.06)}
.navlink{position:relative; display:flex; flex-direction:column; align-items:center; padding:5px 2px 4px; text-decoration:none; border-radius:16px; font-size:11px; font-weight:600; line-height:1.2; color:var(--nav-muted); transition:background .25s, color .25s, transform .2s}
.navlink .ni{font-family:var(--hanzi); font-size:19px; font-weight:700; line-height:1.35}
.tabbar .navlink[aria-current="page"]{color:#fff; background:var(--seal); transform:translateY(-1px)}
.navlink .badge{position:absolute; top:-2px; right:calc(50% - 28px); min-width:18px; height:18px; padding:0 5px; border-radius:999px; background:var(--gold); color:#1b1814; font-size:11px; font-weight:800; line-height:18px; text-align:center; font-variant-numeric:tabular-nums}
.side-art{display:none}

@media (min-width:880px){
  .app{grid-template-columns:264px minmax(0, 1fr)}
  .topbar,.tabbar{display:none}
  .sidebar{display:flex; flex-direction:column; gap:22px; position:sticky; top:0; height:100vh; padding:26px 18px; background:var(--nav); color:var(--nav-ink); overflow:hidden}
  .sidebar .logo-t span{color:var(--nav-muted)}
  .sidebar nav{display:flex; flex-direction:column; gap:3px; position:relative; z-index:1}
  .sidebar .navlink{flex-direction:row; gap:12px; font-size:15.5px; padding:9px 10px; justify-content:flex-start; border-radius:12px}
  .sidebar .navlink .ni{min-width:46px; text-align:center; font-size:18px; padding:3px 0; border-radius:9px; transition:background .25s}
  .sidebar .navlink:hover{color:var(--nav-ink); background:rgba(255,255,255,.05)}
  .sidebar .navlink[aria-current="page"]{color:var(--nav-ink); background:rgba(255,255,255,.08)}
  .sidebar .navlink[aria-current="page"] .ni{color:#fff; background:var(--seal)}
  .sidebar .navlink .badge{position:static; margin-left:auto}
  .side-day{position:relative; z-index:1; padding:14px; border-radius:14px; background:rgba(255,255,255,.05); box-shadow:inset 0 0 0 1px rgba(255,255,255,.07)}
  .side-day .muted{color:var(--nav-muted)}
  .side-day .ring circle:first-child{stroke:rgba(255,255,255,.14)}
  .side-day .ring text{fill:var(--nav-ink)}
  .side-day .wd{color:var(--nav-muted)}
  .side-day .wd i{border-color:rgba(255,255,255,.22)}
  .side-day .wd i.today{box-shadow:0 0 0 2px var(--nav), 0 0 0 3.5px var(--gold)}
  .side-art{display:block; position:absolute; left:0; right:0; bottom:0; height:220px; pointer-events:none; opacity:.9}
  .side-art svg{width:100%; height:100%; display:block}
  main{padding:36px 40px 70px}
}

''' + s[b:]

# ---------- D: Bausteine ----------
rep("h1.title{font-family:var(--display); font-size:30px; line-height:1.15; margin:0; font-weight:700; text-wrap:balance; letter-spacing:-.005em}",
    "h1.title{font-family:var(--display); font-size:31px; line-height:1.15; margin:0; font-weight:600; text-wrap:balance}")
rep("h2.sec{display:flex; align-items:center; gap:10px; font-family:var(--display); font-size:20px; margin:34px 0 12px; font-weight:700}",
    "h2.sec{display:flex; align-items:center; gap:10px; font-family:var(--display); font-size:21px; margin:34px 0 12px; font-weight:600}")
rep(".card{background:var(--sheet); border:1px solid var(--line); border-radius:16px; box-shadow:var(--shadow)}",
    ".card{background:var(--sheet) var(--texture); border:0; border-radius:14px; box-shadow:0 0 0 1px color-mix(in srgb, var(--line) 75%, transparent), 0 14px 30px -20px rgba(31,27,22,.4)}")

# ---------- E: neue Bausteine vor der Sitzung ----------
new_css = r'''/* ---------- Titelbild ---------- */
.hero{position:relative; margin:-18px -16px 0; height:min(64vh, 440px); min-height:340px; overflow:hidden; background:#efe2c8; isolation:isolate}
.hero-art{position:absolute; inset:-36px 0 0 0; will-change:transform}
.hero-art .scene-svg{width:100%; height:100%; display:block}
.hero::after{content:""; position:absolute; left:0; right:0; bottom:0; height:46%; z-index:1; pointer-events:none; background:linear-gradient(to bottom, rgba(239,226,200,0), color-mix(in srgb, var(--paper) 82%, transparent) 72%, var(--paper))}
.hero .cl{position:absolute; z-index:1; width:130px; color:rgba(255,251,242,.92); animation:drift linear infinite; filter:drop-shadow(0 2px 4px rgba(120,100,70,.18))}
@keyframes drift{from{transform:translateX(-160px)} to{transform:translateX(min(110vw, 1100px))}}
.birds{position:absolute; z-index:1; top:14%; left:0; width:70px; animation:fly 28s linear infinite}
.birds path{animation:flap .45s ease-in-out infinite alternate; transform-box:fill-box; transform-origin:center}
.birds path:nth-child(2){animation-delay:.15s} .birds path:nth-child(3){animation-delay:.3s}
@keyframes fly{from{transform:translate(-90px, 30px)} to{transform:translate(min(105vw, 1000px), -50px)}}
@keyframes flap{to{transform:scaleY(.35)}}
.hero-ink{position:absolute; z-index:2; top:16px; left:14px; display:flex; gap:8px; align-items:flex-start}
.hero-hello{margin:0; writing-mode:vertical-rl; font-family:var(--brush); font-weight:400; font-size:clamp(58px, 16vw, 92px); line-height:1; color:#1d1a16; text-shadow:0 0 22px rgba(246,236,214,.95), 0 0 6px rgba(246,236,214,.9); animation:write 1.3s cubic-bezier(.6,.1,.3,1) both}
@keyframes write{from{clip-path:inset(0 0 100% 0)} to{clip-path:inset(0 0 0 0)}}
.name-seal{display:block; writing-mode:vertical-rl; width:48px; height:48px; padding:5px 4px; background:#c23a2c; color:#fbefdc; font-family:var(--brush); font-size:18px; line-height:19px; text-align:center; letter-spacing:0; border-radius:5px; box-shadow:inset 0 0 0 2px rgba(251,239,220,.55), 0 3px 8px rgba(120,30,20,.3); transform:rotate(4deg); animation:stamp .5s cubic-bezier(.2,1.6,.4,1) 1.1s both}
.hero-date{position:absolute; z-index:2; top:16px; right:14px; font-size:12.5px; font-weight:600; color:#3b352d; background:rgba(251,246,234,.78); padding:4px 10px; border-radius:999px; backdrop-filter:blur(6px)}
.hero-ribbon{position:absolute; z-index:3; left:12px; right:12px; bottom:14px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px 14px; padding:12px 14px; border-radius:18px; background:color-mix(in srgb, var(--sheet) 80%, transparent); backdrop-filter:blur(14px) saturate(1.2); -webkit-backdrop-filter:blur(14px) saturate(1.2); box-shadow:0 16px 34px -18px rgba(0,0,0,.5), inset 0 0 0 1px rgba(255,255,255,.25)}
.hr-step{display:block; font-size:11.5px; text-transform:uppercase; letter-spacing:.14em; color:var(--muted); font-weight:700}
.hr-name{display:block; font-family:var(--display); font-weight:600; font-size:21px; line-height:1.2}
.hr-name .brush{color:var(--seal); font-size:1.15em; margin-right:4px}
.mini-route{display:flex; gap:4px; margin-top:7px}
.mini-route i{width:20px; height:5px; border-radius:3px; background:var(--line)}
.mini-route i.on{background:var(--seal)}
.mini-route i.cur{background:linear-gradient(90deg, var(--seal) var(--p), var(--line) var(--p)); box-shadow:0 0 0 2px color-mix(in srgb, var(--seal) 25%, transparent)}
.hr-go{flex-direction:column; align-items:flex-start; gap:1px; padding:10px 18px; text-align:left}
.hr-go small{font-weight:600; font-size:12.5px; opacity:.92}
.statline{display:flex; flex-wrap:wrap; justify-content:center; gap:8px 20px; margin:16px 0 0; font-size:14px; color:var(--ink-2)}
.statline > span{display:inline-flex; align-items:center; gap:7px}
.statline b{font-variant-numeric:tabular-nums; font-size:15.5px; color:var(--ink)}
.statline .seal{width:26px; height:26px; font-size:17px; border-radius:50%}
.tiles2{display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:16px}
.tile{position:relative; overflow:hidden; display:flex; flex-direction:column; justify-content:flex-end; gap:1px; min-height:156px; padding:14px; border-radius:18px; text-decoration:none; color:inherit; border:0; cursor:pointer; text-align:left; font:inherit; transition:transform .3s cubic-bezier(.2,.9,.3,1.3), box-shadow .3s; box-shadow:0 14px 30px -18px rgba(31,27,22,.55)}
.tile:hover{transform:translateY(-4px) rotate(-.6deg)}
.tile:disabled{cursor:default; opacity:.7}
.tile b{font-size:16.5px; position:relative; z-index:1}
.tile small{font-size:12.5px; opacity:.85; position:relative; z-index:1}
.tile-rev{background:var(--nav); color:#efe6d4}
.tile-rev .big{position:absolute; right:-8px; top:-18px; font-family:var(--brush); font-size:104px; line-height:1; color:rgba(239,230,212,.1)}
.tile-rev .count{font-family:var(--display); font-weight:600; font-size:38px; line-height:1; color:#fff; position:relative}
.tile-rev .count em{font-style:normal; font-size:15px; font-family:var(--body); font-weight:600; color:var(--gold); margin-left:4px}
.tile-game{background:#e9dcc0; color:#1d1a16}
.tile-game canvas{position:absolute; inset:0; width:100%; height:100%; display:block}
.tile-game::after{content:""; position:absolute; inset:45% 0 0 0; background:linear-gradient(to bottom, rgba(233,220,192,0), rgba(246,239,224,.96) 62%)}
.tile-game .tz{position:relative; z-index:1; font-family:var(--brush); font-size:28px; color:#c23a2c; line-height:1}
.booklet{margin-top:30px}
.bk-head{display:flex; align-items:baseline; justify-content:space-between; gap:10px; margin-bottom:10px}
.bk-head b{font-family:var(--display); font-weight:600; font-size:21px}
.bk-head b .brush{color:var(--seal); margin-right:6px}
.bk{display:grid; grid-template-columns:1fr 1fr; padding:6px; border-radius:12px; background:linear-gradient(135deg, #8a2620, #5e1612); box-shadow:0 18px 34px -20px rgba(60,10,8,.7)}
.bk-page{position:relative; display:grid; grid-template-columns:1fr 1fr; gap:12px; padding:16px 12px 18px; background:#f6efdf var(--texture); overflow:hidden}
.bk-page:first-child{border-radius:7px 0 0 7px; box-shadow:inset -16px 0 20px -16px rgba(0,0,0,.4)}
.bk-page:last-child{border-radius:0 7px 7px 0; box-shadow:inset 16px 0 20px -16px rgba(0,0,0,.4)}
.bk-page::before{content:attr(data-wm); position:absolute; inset:0; display:grid; place-items:center; font-family:var(--brush); font-size:120px; color:rgba(194,58,44,.05); pointer-events:none}
.bk .stamp{color:#c23a2c}
.bk .stamp.got{border-color:#c23a2c; background:rgba(194,58,44,.05)}
.bk .stamp.open{color:#9a8f7c; border-color:#d9ccb2}
.stamp.got:hover{transform:rotate(0deg) scale(1.06); transition:transform .25s}
.journey-head{display:flex; align-items:flex-end; gap:14px; margin:44px 0 0}
.journey-head .brush{font-size:60px; color:var(--seal); line-height:.85}
.journey-head h2{font-family:var(--display); font-weight:600; font-size:24px; margin:0; line-height:1.15}
.journey-head p{margin:2px 0 0; color:var(--muted); font-size:14px}
.stage2{position:relative; z-index:1; margin:24px 0 2px}
.st-art{position:relative; height:196px; background:#f3ead6; -webkit-mask-image:radial-gradient(ellipse 74% 70% at 50% 50%, #000 56%, transparent 100%); mask-image:radial-gradient(ellipse 74% 70% at 50% 50%, #000 56%, transparent 100%); transition:transform .8s cubic-bezier(.2,.8,.2,1)}
.stage2:hover .st-art{transform:scale(1.03)}
.st-art .scene-svg{width:100%; height:100%; display:block}
.st-vname{position:absolute; z-index:2; top:8px; left:4px; writing-mode:vertical-rl; font-family:var(--brush); font-size:48px; line-height:1.02; color:#c23a2c; text-shadow:0 0 14px var(--paper), 0 0 4px var(--paper), 0 0 2px var(--paper)}
.st-done{position:absolute; z-index:2; top:14px; right:10px; width:58px; height:58px; border-radius:50%; border:3px double #c23a2c; color:#c23a2c; display:grid; place-items:center; font-family:var(--brush); font-size:34px; transform:rotate(-12deg); background:rgba(251,246,234,.75)}
.st-info{text-align:center; margin-top:-4px; padding:0 8px}
.st-num{display:block; font-size:11.5px; text-transform:uppercase; letter-spacing:.14em; color:var(--muted); font-weight:700}
.st-info h3{font-family:var(--display); font-weight:600; font-size:23px; margin:2px 0 2px; line-height:1.2}
.st-info p{margin:0 auto; max-width:46ch; color:var(--muted); font-size:14px}
.st-prog{display:inline-block; margin-top:6px; font-size:12.5px; font-weight:700; color:var(--ink-2); background:var(--paper-2); padding:2px 10px; border-radius:999px}
.vbanner{position:relative; margin:-18px -16px 8px; height:172px; overflow:hidden; background:#efe2c8; isolation:isolate}
.vbanner .vb-art{position:absolute; inset:0}
.vbanner .scene-svg{width:100%; height:100%; display:block}
.vbanner::after{content:""; position:absolute; left:0; right:0; bottom:0; height:62%; z-index:1; background:linear-gradient(to bottom, rgba(239,226,200,0), color-mix(in srgb, var(--paper) 86%, transparent) 70%, var(--paper))}
.vb-text{position:absolute; z-index:2; left:16px; right:16px; bottom:10px; display:flex; align-items:flex-end; gap:12px}
.vb-text .brush{font-size:56px; color:#c23a2c; line-height:.9; text-shadow:0 0 14px var(--paper)}
.vb-text h1{font-family:var(--display); font-weight:600; font-size:28px; margin:0; line-height:1.1}
/* Spielhalle */
.lobby-hero{position:relative; margin:-18px -16px 10px; height:250px; overflow:hidden; background:#efe0c3}
.lobby-hero canvas{width:100%; height:100%; display:block}
.lobby-hero::after{content:""; position:absolute; left:0; right:0; bottom:0; height:30%; background:linear-gradient(to bottom, transparent, var(--paper))}
.lobby-title{position:absolute; z-index:1; left:16px; top:12px; display:flex; flex-direction:column}
.lobby-title .brush{font-size:60px; color:#c23a2c; line-height:1; text-shadow:0 0 16px rgba(246,234,211,.95)}
.lt-de{font-family:var(--display); font-weight:600; font-size:22px; color:#1d1a16; text-shadow:0 0 10px rgba(246,234,211,.95)}
.lobby-facts{display:flex; flex-wrap:wrap; gap:6px 18px; margin:12px 0 0; font-size:14px; color:var(--ink-2)}
.lobby-facts b{font-size:18px; margin-right:3px; color:var(--ink); font-variant-numeric:tabular-nums}
.rivals{display:grid; gap:14px}
.rival{display:flex; gap:14px; padding:14px; border-radius:18px; background:var(--sheet) var(--texture); box-shadow:0 0 0 1px color-mix(in srgb, var(--line) 75%, transparent), 0 14px 30px -20px rgba(31,27,22,.45); transition:transform .3s cubic-bezier(.2,.9,.3,1.3)}
.rival:hover{transform:translateY(-4px)}
.rv-face{flex:none}
.rv-face svg{width:84px; height:84px; display:block}
.rv-body{min-width:0}
.rv-name .hz{font-size:22px} .rv-py{font-size:14px; font-weight:600}
.rv-de{font-size:14px; color:var(--muted); display:flex; gap:8px; align-items:center; flex-wrap:wrap}
.stars{display:inline-flex; gap:4px} .stars i{width:8px; height:8px; transform:rotate(45deg); background:var(--line)} .stars i.on{background:var(--seal)}
.rv-intro{font-size:14px; margin:6px 0 4px}
.rv-rec{font-size:12.5px; color:var(--muted); margin-bottom:10px}
@media (min-width:700px){ .rivals{grid-template-columns:repeat(3, 1fr)} .rival{flex-direction:column; align-items:center; text-align:center} .rv-de{justify-content:center} }
/* Rennen */
.game{position:fixed; inset:0; z-index:56; display:flex; flex-direction:column; background:var(--paper) var(--texture); overflow-y:auto; -webkit-overflow-scrolling:touch}
.race-top{display:flex; align-items:center; gap:12px; padding:12px 14px; max-width:920px; width:100%; margin:0 auto}
.race-hud{flex:1; min-width:0}
.hud-track{position:relative; height:8px; border-radius:4px; background:var(--paper-2); box-shadow:inset 0 0 0 1px var(--line)}
.hud-track i{position:absolute; top:50%; width:15px; height:15px; margin:-7.5px 0 0 -7.5px; border-radius:50%; border:2.5px solid var(--sheet); box-shadow:0 1px 3px rgba(0,0,0,.3)}
.hud-me{background:var(--seal); z-index:2}
.hud-num{display:flex; justify-content:space-between; gap:8px; font-size:12.5px; margin-top:5px; font-variant-numeric:tabular-nums}
.combo{min-width:74px; text-align:right; font-weight:800; color:var(--gold); font-size:15px; white-space:nowrap}
.combo.hot{color:var(--seal); animation:hot .5s ease-in-out infinite alternate}
@keyframes hot{to{transform:scale(1.12)}}
.race-stage{position:relative; width:100%; max-width:920px; margin:0 auto; height:min(38vh, 320px); min-height:220px; flex:none}
.race-stage canvas{width:100%; height:100%; display:block}
.race-count{position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; pointer-events:none}
.race-count b{font-size:104px; color:#c23a2c; text-shadow:0 0 24px rgba(246,234,211,.95); line-height:1}
.race-count small{font-weight:700; font-size:16px; color:#1d1a16; background:rgba(251,246,234,.88); padding:2px 12px; border-radius:8px}
.race-count.go b{animation:countin .8s cubic-bezier(.2,1.6,.4,1)}
@keyframes countin{from{transform:scale(2.4) rotate(-8deg); opacity:0} 45%{transform:scale(.94); opacity:1} to{transform:none}}
.race-say{display:flex; align-items:center; gap:10px; max-width:920px; width:100%; margin:8px auto 0; padding:0 14px}
.race-say .panda svg{width:46px; height:46px; display:block}
.race-say p{margin:0; flex:1; background:var(--sheet); border-radius:14px; padding:8px 12px; font-size:14.5px; position:relative; box-shadow:0 0 0 1px var(--line); min-height:40px}
.race-say p::before{content:""; position:absolute; left:-7px; top:50%; margin-top:-6px; border:6px solid transparent; border-left:0; border-right-color:var(--sheet)}
.race-say p.pop{animation:sayin .35s cubic-bezier(.2,1.4,.4,1)}
@keyframes sayin{from{transform:scale(.94); opacity:.4}}
.race-q{max-width:920px; width:100%; margin:0 auto; padding:10px 14px calc(18px + env(safe-area-inset-bottom))}
.rq-head{display:flex; align-items:center; gap:14px; min-height:76px}
.rq-k{display:block; font-size:13px; font-weight:700; color:var(--muted)}
.rq-zi{font-size:calc(46px * var(--hz-scale)); line-height:1.15; background:var(--sheet); border:0; border-radius:14px; padding:4px 14px; box-shadow:0 0 0 1px var(--line); cursor:pointer; flex:none}
.rq-play{width:64px; height:64px; border-radius:50%; border:0; background:var(--seal); color:#fff; display:grid; place-items:center; cursor:pointer; flex:none; box-shadow:0 4px 0 color-mix(in srgb, var(--seal) 60%, #000)}
.rq-de{display:block; font-family:var(--display); font-weight:600; font-size:25px; line-height:1.2}
.rq-py{display:block; font-size:18px; font-weight:600}
.rq-timer{height:4px; border-radius:2px; background:var(--paper-2); overflow:hidden; margin:6px 0 10px}
.rq-timer i{display:block; height:100%; background:linear-gradient(90deg, var(--gold), var(--seal)); transform-origin:left; animation:bonus 3.2s linear forwards}
@keyframes bonus{from{transform:scaleX(1)} to{transform:scaleX(0)}}
.rq-opts{display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:4px}
.rq-opt{position:relative; min-height:64px; padding:10px; border-radius:14px; border:2px solid var(--line); border-bottom-width:4px; background:var(--sheet); font-weight:600; font-size:16px; cursor:pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; line-height:1.25; text-align:center; transition:transform .08s}
.rq-opt:active:not(:disabled){transform:translateY(2px)}
.rq-opt:hover:not(:disabled){border-color:var(--ink-2)}
.rq-opt .k{position:absolute; top:5px; left:8px; font-size:11px; color:var(--muted)}
.rq-opt.zh .hz{font-size:calc(30px * var(--hz-scale)); font-weight:500}
.rq-opt.zh small{font-size:13px}
.rq-opt.tone .mk{font-size:28px; color:var(--tc); line-height:1.1}
.rq-opt.tone small{font-size:12.5px; color:var(--muted)}
.rq-opt.right{border-color:var(--ok); background:var(--ok-bg)}
.rq-opt.wrong{border-color:var(--bad); background:var(--bad-bg); animation:shake .32s}
.rq-opt.dim{opacity:.45}
.rq-fix{margin:10px 0 0; font-size:15px} .rq-fix .hz{font-size:20px}
.rq-wait{text-align:center; padding:34px 10px; color:var(--muted); font-weight:600}
.rr-head{display:flex; gap:14px; align-items:center}
.rr-seal{flex:none; width:74px; height:74px; border-radius:14px; display:grid; place-items:center; background:var(--seal); color:#fff; font-family:var(--brush); font-size:52px; transform:rotate(-6deg); animation:stamp .5s cubic-bezier(.2,1.6,.4,1); box-shadow:inset 0 0 0 3px rgba(255,255,255,.35)}
.rr-seal.lost{background:var(--ink-2); color:var(--paper)}
.rr-title{display:block; font-family:var(--display); font-weight:600; font-size:29px; line-height:1.15}
.rr-sub{font-size:14px; color:var(--muted)}
.rr-stats{display:grid; grid-template-columns:repeat(4, 1fr); gap:8px; margin:14px 0}
.rr-stats span{background:var(--sheet); border-radius:12px; padding:8px 4px; text-align:center; font-size:12px; color:var(--muted); box-shadow:0 0 0 1px var(--line)}
.rr-stats b{display:block; font-size:19px; color:var(--ink); font-variant-numeric:tabular-nums}
.rr-words{display:flex; flex-wrap:wrap; gap:6px}
.rr-w{display:inline-flex; align-items:center; gap:6px; border:0; box-shadow:0 0 0 1px var(--line); background:var(--sheet); border-radius:999px; padding:4px 11px; font-size:13.5px; cursor:pointer}
.rr-w .m{color:var(--ok); font-weight:800} .rr-w.bad .m{color:var(--bad)} .rr-w .hz{font-size:17px}
.rr-actions{display:flex; flex-wrap:wrap; gap:10px; margin-top:16px}
.fxlayer{position:fixed; inset:0; pointer-events:none; z-index:80}
.pbrush{flex:1; height:20px; display:block; overflow:visible}
.pbrush .fillrect{transform-box:fill-box; transform-origin:left center; transition:transform .55s cubic-bezier(.3,.9,.3,1)}
@media (min-width:880px){
  .hero{margin:-36px -40px 0; height:460px}
  .hero-ribbon{left:28px; right:28px; bottom:22px}
  .hero-ink{left:28px; top:26px}
  .hero-date{right:28px; top:26px}
  .vbanner{margin:-36px -40px 10px; height:210px}
  .vb-text{left:32px}
  .lobby-hero{margin:-36px -40px 14px; height:320px}
  .lobby-title{left:32px; top:24px}
  .st-art{height:250px}
  .st-vname{font-size:60px}
  .tile{min-height:180px}
}
@media (max-width:520px){
  .rr-stats{grid-template-columns:repeat(2, 1fr)}
  .race-count b{font-size:84px}
}

'''
rep("/* ---------- Sitzung (Lektion, Wiederholung) ---------- */", new_css + "/* ---------- Sitzung (Lektion, Wiederholung) ---------- */")
rep(".lessons::before{", ".lessons-x::before{", 0) if ".lessons::before{" not in s else None
# Knoten: Animation nur rückwärts füllen, damit Hover-Effekte greifen
rep("box-shadow:inset 0 0 0 4px var(--sheet), inset 0 0 0 5.5px var(--line), 0 5px 0 var(--line); animation:pop .45s cubic-bezier(.2,1.5,.4,1) both; animation-delay:var(--d)}",
    "box-shadow:inset 0 0 0 4px var(--sheet), inset 0 0 0 5.5px var(--line), 0 5px 0 var(--line); animation:pop .45s cubic-bezier(.2,1.5,.4,1) backwards; animation-delay:var(--d); transition:transform .25s cubic-bezier(.2,.9,.3,1.4)}\n.node:not(:disabled):hover{transform:translateY(-3px) scale(1.05)}")

# ---------- G: HTML ----------
rep('''    <div class="card" style="padding:14px 14px 12px" id="side-day"></div>
  </aside>''', '''    <div class="side-day" id="side-day"></div>
    <div class="side-art" id="side-art" aria-hidden="true"></div>
  </aside>''')
rep('''    <section class="view" id="view-toene" aria-labelledby="h-toene">
      <h1 class="title" id="h-toene"><span class="brush">声调</span> Töne hören</h1>
      <p class="subtitle">''', '''    <section class="view" id="view-toene" aria-labelledby="h-toene">
      <header class="vbanner"><div class="vb-art" data-scene="wall"></div><div class="vb-text"><span class="brush" aria-hidden="true">声调</span><h1 id="h-toene">Töne hören</h1></div></header>
      <p class="subtitle">''')
rep('''    <section class="view" id="view-saetze" aria-labelledby="h-saetze">
      <h1 class="title" id="h-saetze"><span class="brush">句子</span> Reisesätze</h1>
      <p class="subtitle">''', '''    <section class="view" id="view-saetze" aria-labelledby="h-saetze">
      <header class="vbanner"><div class="vb-art" data-scene="market"></div><div class="vb-text"><span class="brush" aria-hidden="true">句子</span><h1 id="h-saetze">Reisesätze</h1></div></header>
      <p class="subtitle">''')
rep('''    <section class="view" id="view-einstellungen" aria-labelledby="h-set"></section>''',
    '''    <section class="view" id="view-einstellungen" aria-labelledby="h-set"></section>
    <!-- SPIEL -->
    <section class="view" id="view-spiel" aria-label="Drachenboot-Rennen"></section>''')
rep('''<div class="session tc" id="session" hidden role="dialog" aria-modal="true" aria-label="Übung"></div>''',
    '''<div class="session tc" id="session" hidden role="dialog" aria-modal="true" aria-label="Übung"></div>
<div class="game tc" id="game" hidden role="dialog" aria-modal="true" aria-label="Drachenboot-Rennen"></div>''')

# ---------- H: JavaScript ----------
rep("/*SCENES*/\n", "/*SCENES*/\n/*FX*/\n")
rep("/* ================= Übungen erzeugen ================= */", "/*GAME*/\n\n/* ================= Übungen erzeugen ================= */")
# Zustand
rep("learn:{done:{}}, words:{}, prefs:defaults()};", "learn:{done:{}}, words:{}, game:{played:0, wins:{}, best:{}}, prefs:defaults()};")
rep("learn:{done:(s.learn && s.learn.done) || {}}, words:s.words||{}, prefs:Object.assign(defaults(), s.prefs||{})};",
    "learn:{done:(s.learn && s.learn.done) || {}}, words:s.words||{}, game:Object.assign({played:0, wins:{}, best:{}}, s.game||{}), prefs:Object.assign(defaults(), s.prefs||{})};")
rep("function emptyDay(){ return {tones:0, toneOk:0, cards:0, neu:0, xp:0, lessons:0, reviews:0}; }",
    "function emptyDay(){ return {tones:0, toneOk:0, cards:0, neu:0, xp:0, lessons:0, reviews:0, games:0}; }")
# Navigation
rep('''  {id:"wiederholen", hz:"复习", name:"Wiederholen"},
  {id:"toene", hz:"声调", name:"Töne"},''', '''  {id:"wiederholen", hz:"复习", name:"Wiederholen"},
  {id:"spiel", hz:"龙舟", name:"Spiel"},
  {id:"toene", hz:"声调", name:"Töne"},''')
rep('''  $("#side-nav").innerHTML = html;
  $("#tab-nav").innerHTML = html;''', '''  $("#side-nav").innerHTML = html;
  $("#tab-nav").innerHTML = NAV.filter(function(n){ return n.id!=="einstellungen"; }).map(function(n){
    return '<a class="navlink" href="#'+n.id+'" data-view="'+n.id+'"'+(n.id===currentView ? ' aria-current="page"' : '')+'><span class="ni" aria-hidden="true">'+n.hz+'</span><span>'+n.name+'</span>'+
      (n.id==="wiederholen" && due ? '<span class="badge" aria-label="'+due+' fällig">'+due+'</span>' : '')+'</a>';
  }).join("");''')
rep('''    '<span class="stat-chip goal" title="Tagesziel"><span class="seal" aria-hidden="true">今</span>'+Math.min(d.xp, goal)+'/'+goal+'</span>';''',
    '''    '<span class="stat-chip goal" title="Tagesziel"><span class="seal" aria-hidden="true">今</span>'+Math.min(d.xp, goal)+'/'+goal+'</span>'+
    '<a class="gear" href="#einstellungen" aria-label="Einstellungen"'+(currentView==="einstellungen" ? ' aria-current="page"' : '')+'><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm8.4 4.6-.1-1.1 2-1.6-2-3.4-2.4.9a8 8 0 0 0-1.9-1.1L15.6 3h-4l-.4 2.6a8 8 0 0 0-1.9 1.1l-2.4-.9-2 3.4 2 1.6a8 8 0 0 0 0 2.2l-2 1.6 2 3.4 2.4-.9a8 8 0 0 0 1.9 1.1l.4 2.6h4l.4-2.6a8 8 0 0 0 1.9-1.1l2.4.9 2-3.4z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg></a>';''')
rep('''  if(currentView==="einstellungen") renderSettings();
}
window.addEventListener("hashchange"''', '''  if(currentView==="einstellungen") renderSettings();
  if(currentView==="spiel") renderLobby();
}
window.addEventListener("hashchange"''')
rep('''function route(){
  if(S){ return; }''', '''function route(){
  if(S || G){ return; }''')
rep('''window.addEventListener("hashchange", function(){ if(!S){ route(); window.scrollTo(0,0); } });''',
    '''window.addEventListener("hashchange", function(){ if(!S && !G){ route(); window.scrollTo(0,0); } });''')
open(p, "w", encoding="utf-8").write(s)
print("Teil 1 ok")
