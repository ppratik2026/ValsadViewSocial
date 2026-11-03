"""A different animation for every layout of the viral design, so no two reels move alike.

Each layout gets:
- intro steps (put before the shared ones: the first step that matches an element wins), in the
  [selector, keyframes, start s, duration s, stagger s] form of src/card.ANIM_JS;
- live motion for the rest of the reel ([selector, CSS animation with {start} / {end} / {total}]);
- optionally an overlay (lightning, police lights, TV scan lines ...);
- "spot": how the points are read out one by one (glow, underline sweep, tick, typewriter ...), or None.

All keyframes are in MOTION_CSS. Elements keep their own transform through var(--t0) (set by ANIM_JS).
"""

MOTION_CSS = """
@property --n { syntax: '<integer>'; inherits: false; initial-value: 0; }
@property --p { syntax: '<percentage>'; inherits: false; initial-value: 0%; }
@keyframes typeIn { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
@keyframes typeInR { from { clip-path: inset(0 0 0 100%); } to { clip-path: inset(0 0 0 0); } }
@keyframes printDown { from { clip-path: inset(0 0 72% 0); transform: var(--t0, translate(0)) translateY(-60px); }
  to { clip-path: inset(0 0 0 0); transform: var(--t0, translate(0)); } }
@keyframes flipX { from { transform: var(--t0, translate(0)) perspective(900px) rotateX(-95deg); opacity: 0; }
  to { transform: var(--t0, translate(0)) perspective(900px) rotateX(0); opacity: 1; } }
@keyframes flipY { from { transform: var(--t0, translate(0)) perspective(1200px) rotateY(90deg); }
  to { transform: var(--t0, translate(0)) perspective(1200px) rotateY(0); } }
@keyframes dropBounce { 0% { transform: var(--t0, translate(0)) translateY(-900px); }
  60% { transform: var(--t0, translate(0)) translateY(0); } 75% { transform: var(--t0, translate(0)) translateY(-60px); }
  88% { transform: var(--t0, translate(0)) translateY(0); } 94% { transform: var(--t0, translate(0)) translateY(-14px); }
  100% { transform: var(--t0, translate(0)); } }
@keyframes swingIn { 0% { transform: var(--t0, translate(0)) perspective(900px) rotateX(-100deg); transform-origin: top; }
  60% { transform: var(--t0, translate(0)) perspective(900px) rotateX(18deg); } 80% { transform: var(--t0, translate(0)) perspective(900px) rotateX(-8deg); }
  100% { transform: var(--t0, translate(0)) perspective(900px) rotateX(0); } }
@keyframes slapIn { 0% { transform: var(--t0, translate(0)) scale(3) rotate(-25deg); opacity: 0; }
  60% { transform: var(--t0, translate(0)) scale(.9); opacity: 1; } 100% { transform: var(--t0, translate(0)); } }
@keyframes glitch { 0% { transform: var(--t0, translate(0)) translateX(-40px) skewX(20deg); filter: hue-rotate(90deg) contrast(2); opacity: .3; }
  20% { transform: var(--t0, translate(0)) translateX(30px) skewX(-10deg); filter: hue-rotate(-60deg); opacity: 1; }
  40% { transform: var(--t0, translate(0)) translateX(-12px); filter: none; } 60% { transform: var(--t0, translate(0)) translateX(8px); }
  100% { transform: var(--t0, translate(0)); filter: none; } }
@keyframes flickerOn { 0% { opacity: 0; } 10% { opacity: 1; } 14% { opacity: .1; } 22% { opacity: .9; } 26% { opacity: .2; }
  40% { opacity: 1; } 44% { opacity: .4; } 60%, 100% { opacity: 1; } }
@keyframes notiDrop { 0% { transform: var(--t0, translate(0)) translateY(-160%); opacity: 0; } 70% { transform: var(--t0, translate(0)) translateY(8%); opacity: 1; }
  100% { transform: var(--t0, translate(0)); } }
@keyframes vibrate { 0%, 100% { translate: 0 0; } 20% { translate: -6px 0; } 40% { translate: 6px 0; } 60% { translate: -4px 0; } 80% { translate: 4px 0; } }
@keyframes develop { from { filter: brightness(3) saturate(0) blur(4px); } to { filter: none; } }
@keyframes unfold { from { transform: var(--t0, translate(0)) perspective(1000px) rotateX(-80deg); transform-origin: top; opacity: 0; }
  to { transform: var(--t0, translate(0)) perspective(1000px) rotateX(0); opacity: 1; } }
@keyframes rollIn { from { transform: var(--t0, translate(0)) translateX(700px) rotate(360deg); } to { transform: var(--t0, translate(0)); } }
@keyframes spinY { from { transform: var(--t0, translate(0)) perspective(800px) rotateY(-360deg) scale(.4); } to { transform: var(--t0, translate(0)); } }
@keyframes slideFarL { from { transform: var(--t0, translate(0)) translateX(-1300px); } to { transform: var(--t0, translate(0)); } }
@keyframes slideFarR { from { transform: var(--t0, translate(0)) translateX(1300px); } to { transform: var(--t0, translate(0)); } }
@keyframes riseFar { from { transform: var(--t0, translate(0)) translateY(1400px); } to { transform: var(--t0, translate(0)); } }
@keyframes growY { from { transform: var(--t0, translate(0)) scaleY(0); transform-origin: top; } to { transform: var(--t0, translate(0)) scaleY(1); } }
@keyframes countDown { from { --n: 60; } }
@keyframes countUp { from { --n: 0; } }
@keyframes fillP { from { --p: 0%; } }
@keyframes strobe { 0%, 100% { opacity: 0; } 10%, 30% { opacity: .55; } 20%, 40% { opacity: 0; } }
@keyframes bolt { 0%, 100% { opacity: 0; } 2% { opacity: .95; } 4% { opacity: .1; } 6% { opacity: .8; } 9% { opacity: 0; } }
@keyframes shakeHard { 0%, 100% { translate: 0 0; } 10% { translate: -18px 8px; } 20% { translate: 16px -10px; } 30% { translate: -12px 6px; }
  40% { translate: 10px -4px; } 50% { translate: -6px 2px; } 60% { translate: 0 0; } }
@keyframes sirenL { 0%, 49% { opacity: .55; } 50%, 100% { opacity: 0; } }
@keyframes sirenR { 0%, 49% { opacity: 0; } 50%, 100% { opacity: .55; } }
@keyframes scan { from { background-position: 0 0; } to { background-position: 0 120px; } }
@keyframes filmRun { from { transform: var(--t0, translate(0)) translateX(900px); } to { transform: var(--t0, translate(0)); } }
@keyframes perfs { from { background-position: 0 0; } to { background-position: -144px 0; } }
@keyframes ripple { from { box-shadow: 0 0 0 0 rgba(208,0,0,.6), 0 10px 22px rgba(0,0,0,.35); }
  to { box-shadow: 0 0 0 60px rgba(208,0,0,0), 0 10px 22px rgba(0,0,0,.35); } }
@keyframes sweep { from { background-size: 0% 100%; } to { background-size: 100% 100%; } }
@keyframes tick { 0% { transform: var(--t0, translate(0)) translateX(0); } 30% { transform: var(--t0, translate(0)) translateX(26px); }
  100% { transform: var(--t0, translate(0)) translateX(0); } }
@keyframes inkIn { from { filter: blur(12px); opacity: 0; letter-spacing: 12px; } to { filter: none; opacity: 1; letter-spacing: normal; } }
@keyframes wobble { 0%, 100% { rotate: 0deg; } 25% { rotate: -3deg; } 75% { rotate: 3deg; } }
@keyframes float { 0%, 100% { translate: 0 0; } 50% { translate: 0 -14px; } }
@keyframes halftone { from { background-position: 0 0; } to { background-position: 36px 36px; } }
@keyframes ledBlink { 0%, 100% { text-shadow: 0 0 14px rgba(255,176,0,.8); } 50% { text-shadow: 0 0 30px rgba(255,176,0,1), 0 0 60px rgba(255,120,0,.6); } }
@keyframes highlightSweep { from { background: linear-gradient(90deg, rgba(255,214,10,.55) 0%, transparent 0%); }
  to { background: linear-gradient(90deg, rgba(255,214,10,.55) 100%, transparent 100%); } }
@keyframes tvOn { 0% { transform: var(--t0, translate(0)) scale(1, .01); filter: brightness(4); } 40% { transform: var(--t0, translate(0)) scale(1, .01); filter: brightness(4); }
  70% { transform: var(--t0, translate(0)) scale(1, 1.05); filter: brightness(1.6); } 100% { transform: var(--t0, translate(0)); filter: none; } }
@keyframes drawLine { from { stroke-dashoffset: 2600; } to { stroke-dashoffset: 0; } }
@keyframes rainFall { from { background-position: 0 0; } to { background-position: -40px 360px; } }
@keyframes sprayIn { from { filter: blur(14px); opacity: 0; transform: var(--t0, translate(0)) scale(1.15); } to { filter: none; opacity: 1; transform: var(--t0, translate(0)); } }
@keyframes beamSway { 0%, 100% { transform: translateX(-50%) rotate(-3deg); } 50% { transform: translateX(-50%) rotate(3deg); } }
@keyframes curtainOpenL { from { transform: scaleX(3.5); transform-origin: left; } to { transform: scaleX(1); transform-origin: left; } }
@keyframes curtainOpenR { from { transform: scaleX(3.5); transform-origin: right; } to { transform: scaleX(1); transform-origin: right; } }
@keyframes shatterIn { 0% { transform: var(--t0, translate(0)) scale(1.4) rotate(-6deg); opacity: 0; } 50% { opacity: 1; }
  70% { transform: var(--t0, translate(0)) scale(.96) rotate(1deg); } 100% { transform: var(--t0, translate(0)); } }
@keyframes spinRays { from { transform: rotate(0deg); } to { transform: rotate(40deg); } }
@keyframes ringTurn { from { transform: rotate(0deg); } to { transform: rotate(60deg); } }
@keyframes underline { 0% { box-shadow: inset 0 -6px 0 rgba(255,214,10,0); } 30%, 80% { box-shadow: inset 0 -10px 0 rgba(255,214,10,.9); }
  100% { box-shadow: inset 0 -6px 0 rgba(255,214,10,0); } }
"""

OVERLAY_CSS = """
#fx { position: fixed; inset: 0; z-index: 90; pointer-events: none; }
#fx .bolt { position: absolute; inset: 0; background: radial-gradient(circle at 70% 10%, #fff 0%, rgba(200,220,255,.8) 30%, transparent 70%); opacity: 0; }
#fx .sl { position: absolute; inset: 0; background: radial-gradient(circle at 0% 0%, rgba(255,0,0,.9), transparent 45%); opacity: 0; }
#fx .sr { position: absolute; inset: 0; background: radial-gradient(circle at 100% 0%, rgba(0,80,255,.9), transparent 45%); opacity: 0; }
#fx .scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0 3px, transparent 3px 6px); }
#fx .strobe { position: absolute; inset: 0; background: #d00000; opacity: 0; }
#fx .grain { position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.07) 1px, transparent 1.5px); background-size: 7px 7px; }
"""

# rows that are read out one by one (the same list as src/reel_motion.SPOT)
ROWS = (".pt, .item, .step, .row, .tip, .li, .note, .noti, .nb, .led, .msg, .ev p, .notes p, .lines p, .chap p, .chips span, "
        ".pts p, .black p, .credits p, .cols p, .list p, .stone, .tile:not(.pic), .side, .glass p, .infobox, .myth, .chip, .badge")

M = {
    "police": {
        "intro": [[".v-tag", "slapIn", 0.0, 0.4, 0], [".hazard", "slideFarL", 0.25, 0.35, 0], [".hl div", "slideFarR", 0.3, 0.35, 0.12],
                  [".pt", "slideFarL", 1.2, 0.3, 0.15]],
        "overlay": '<div class="sl"></div><div class="sr"></div>',
        "live": [["#fx .sl", "sirenL .8s steps(1) 0s infinite"], ["#fx .sr", "sirenR .8s steps(1) 0s infinite"]],
        "spot": "glow"},
    "storm": {
        "intro": [[".pin", "dropBounce", 0.0, 0.9, 0], [".hl div", "inkIn", 0.2, 0.6, 0.2], [".when", "slapIn", 1.0, 0.4, 0],
                  [".infobox", "riseFar", 1.3, 0.5, 0]],
        "overlay": '<div class="bolt"></div>',
        "live": [["#fx .bolt", "bolt 3.2s linear .4s infinite"], ["#main", "shakeHard .5s linear .45s 1"],
                 [".bgpic", "kbZoom {end}s linear 0s both"]],
        "spot": None},
    "bignews": {
        "intro": [[".pill", "spinY", 0.0, 0.6, 0], [".hlcard", "flipX", 0.3, 0.5, 0], [".glass p", "typeIn", 0.9, 0.6, 0.4],
                  [".badge", "rollIn", 1.6, 0.6, 0.25]],
        "live": [[".badge", "float 2s ease-in-out {start}s infinite"]],
        "spot": "underline"},
    "tips": {
        "intro": [[".hl div:nth-child(odd)", "slideFarL", 0.0, 0.35, 0.15], [".hl div:nth-child(even)", "slideFarR", 0.1, 0.35, 0.15],
                  [".myth", "slapIn", 0.9, 0.35, 0], [".checkhead", "typeIn", 1.2, 0.4, 0], [".tip", "flipX", 1.5, 0.35, 0.15]],
        "spot": "tick"},
    "card": {
        "intro": [[".head .hl div", "typeIn", 0.0, 0.45, 0.2], [".kick", "slapIn", 0.8, 0.35, 0], [".white", "riseFar", 0.9, 0.5, 0],
                  [".row", "slideFarR", 1.2, 0.35, 0.18]],
        "live": [[".row .circ", "wobble 1.6s ease-in-out {start}s infinite"]],
        "spot": "glow"},
    "tv": {
        "intro": [["#main", "glitch", 0.0, 0.5, 0], [".lower .hl div", "typeIn", 0.6, 0.3, 0.15], [".item", "slideFarL", 1.2, 0.3, 0.15]],
        "overlay": '<div class="scan"></div>',
        "live": [["#fx .scan", "scan 1s linear 0s infinite"], [".screen", "kbPan {end}s ease-in-out 0s both"]],
        "spot": "underline"},
    "paper": {
        "intro": [["#main", "flipY", 0.0, 0.7, 0], [".hl div", "typeIn", 0.6, 0.5, 0.25], [".cols p", "typeIn", 1.5, 0.5, 0.2],
                  [".stamp", "slapIn", 2.0, 0.4, 0]],
        "overlay": '<div class="grain"></div>',
        "spot": "highlight"},
    "quote": {
        "intro": [[".qmark", "slapIn", 0.0, 0.4, 0], [".hl div", "typeIn", 0.3, 0.6, 0.3], [".closeq", "slapIn", 1.2, 0.35, 0],
                  [".who", "slideFarL", 1.4, 0.4, 0]],
        "live": [[".qmark, .closeq", "float 2.4s ease-in-out {start}s infinite"]],
        "spot": "underline"},
    "timeline": {
        "intro": [[".head", "dropBounce", 0.0, 0.8, 0], [".step .dot", "slapIn", 0.9, 0.3, 0.3], [".step p", "typeIn", 1.0, 0.4, 0.3]],
        "spot": "tick"},
    "versus": {
        "intro": [[".side:not(.r)", "slideFarL", 0.4, 0.4, 0], [".side.r", "slideFarR", 0.4, 0.4, 0], [".bolt", "slapIn", 0.9, 0.35, 0]],
        "live": [["#main", "shakeHard .45s linear .95s 1"], [".bolt", "pulse 1.2s ease-in-out {start}s infinite"]],
        "spot": None},
    "alert": {
        "intro": [[".sign", "slapIn", 0.0, 0.4, 0], [".place", "dropBounce", 0.3, 0.7, 0], [".hl div", "flickerOn", 0.6, 0.6, 0.15]],
        "overlay": '<div class="strobe"></div>',
        "live": [["#fx .strobe", "strobe 1.2s linear 0s 2"], [".sign .ic", "wobble .6s ease-in-out 0s infinite"]],
        "spot": "glow"},
    "notice": {
        "intro": [[".band", "growY", 0.0, 0.4, 0], [".hl div", "typeIn", 0.4, 0.45, 0.2], [".row", "typeIn", 1.1, 0.35, 0.2],
                  [".seal", "slapIn", 2.0, 0.4, 0]],
        "spot": "highlight"},
    "stats": {
        "intro": [[".hl div", "inkIn", 0.0, 0.5, 0.15], [".tile", "flipX", 0.7, 0.4, 0.18]],
        "live": [[".tile b", "ledBlink 1.4s ease-in-out {start}s infinite"]],
        "spot": "glow"},
    "polaroid": {
        "intro": [[".pola", "dropBounce", 0.0, 0.8, 0], [".pola .img", "develop", 0.3, 1.6, 0], [".strip", "slideFarR", 0.9, 0.4, 0],
                  [".note", "slapIn", 1.3, 0.35, 0.2]],
        "live": [[".note", "wobble 2.4s ease-in-out {start}s infinite"]],
        "spot": None},
    "magazine": {
        "intro": [[".mast", "inkIn", 0.0, 0.7, 0], [".lines p", "slideFarL", 0.8, 0.35, 0.15], [".hl div", "slideFarL", 0.4, 0.4, 0.15]],
        "live": [[".bgpic", "kbZoom {end}s ease-out 0s both"]],
        "spot": None},
    "chat": {
        "intro": [[".msg", "notiDrop", 0.0, 0.35, 0.9]],
        "spot": None},
    "diagonal": {
        "intro": [[".slant", "slideFarL", 0.0, 0.4, 0], [".li", "slideFarR", 0.8, 0.3, 0.15]],
        "live": [[".toppic", "kbZoom {end}s linear 0s both"]],
        "spot": "tick"},
    "ticket": {
        "intro": [[".tk", "printDown", 0.4, 0.8, 0], [".hl div", "typeIn", 0.0, 0.4, 0.12], [".bar", "typeIn", 1.3, 0.5, 0]],
        "spot": "underline"},
    "map": {
        "intro": [[".pin", "dropBounce", 0.0, 1.0, 0], [".cardm", "riseFar", 0.8, 0.5, 0], [".compass", "spinY", 0.2, 0.8, 0]],
        "live": [[".pin b", "ripple 1.4s ease-out {start}s infinite"]],
        "spot": "tick"},
    "calendar": {
        "intro": [[".cal", "swingIn", 0.0, 0.9, 0], [".cal .d", "flipX", 0.6, 0.5, 0], [".hl div", "typeIn", 1.0, 0.4, 0.15]],
        "live": [[".cal", "wobble 3s ease-in-out {start}s infinite"]],
        "spot": "tick"},
    "receipt": {
        "intro": [[".bill", "printDown", 0.0, 1.4, 0], [".item", "typeIn", 0.9, 0.35, 0.25]],
        "spot": "highlight"},
    "scoreboard": {
        "intro": [[".hl div", "inkIn", 0.0, 0.5, 0.15], [".board", "flipX", 0.5, 0.5, 0], [".led", "flipX", 0.9, 0.35, 0.2]],
        "live": [[".led b", "ledBlink 1s ease-in-out {start}s infinite"]],
        "spot": None},
    "comic": {
        "intro": [[".boom", "slapIn", 0.0, 0.35, 0], [".panel", "slapIn", 0.3, 0.35, 0], [".pic", "slideFarL", 0.6, 0.35, 0],
                  [".say", "slapIn", 0.9, 0.3, 0.3]],
        "live": [["body", "halftone 1.2s linear 0s infinite"], ["#main", "shakeHard .4s linear .32s 1"]],
        "spot": None},
    "neon": {
        "intro": [[".sign", "flickerOn", 0.0, 0.9, 0], [".hl div", "flickerOn", 0.4, 1.0, 0.25], [".nb", "flickerOn", 1.4, 0.8, 0.3]],
        "live": [[".hl div", "flicker 2.6s linear {start}s infinite"], [".sign", "flicker 3.1s linear {start}s infinite"]],
        "spot": None},
    "lockscreen": {
        "intro": [[".clock", "inkIn", 0.0, 0.5, 0], [".noti", "notiDrop", 0.5, 0.4, 0.6]],
        "live": [["#main", "vibrate .3s linear .55s 2"], ["#main", "vibrate .3s linear 1.15s 1"]],
        "spot": None},
    "chalkboard": {
        "intro": [[".topic", "typeIn", 0.0, 0.4, 0], [".hl div", "typeIn", 0.3, 0.7, 0.4], [".pts p", "typeIn", 1.6, 0.5, 0.3]],
        "spot": "underline"},
    "filmstrip": {
        "intro": [[".title", "inkIn", 0.0, 0.6, 0], [".strip", "filmRun", 0.2, 0.9, 0], [".hl div", "inkIn", 1.0, 0.5, 0.15],
                  [".stars", "typeIn", 1.6, 0.6, 0]],
        "live": [[".frame", "kbPan {end}s linear 0s both"]],
        "spot": None},
    "notebook": {
        "intro": [[".topic", "typeIn", 0.0, 0.4, 0], [".hl div", "typeIn", 0.3, 0.5, 0.3], [".clip", "dropBounce", 1.0, 0.7, 0],
                  [".lines p", "typeIn", 1.6, 0.45, 0.3]],
        "spot": "highlight"},
    "billboard": {
        "intro": [[".board", "swingIn", 0.0, 1.0, 0], [".lights i", "flickerOn", 0.9, 0.6, 0.15], [".ground", "riseFar", 1.2, 0.5, 0]],
        "live": [[".cloud", "float 4s ease-in-out 0s infinite"]],
        "spot": None},
    "letter": {
        "intro": [[".env", "slideFarL", 0.0, 0.5, 0], [".stampx", "slapIn", 0.4, 0.35, 0], [".postmark", "slapIn", 0.7, 0.35, 0],
                  [".paper", "unfold", 1.0, 0.7, 0]],
        "spot": "highlight"},
    "crimetape": {
        "intro": [[".tape.a", "slideFarL", 0.0, 0.3, 0], [".tape.b", "slideFarR", 0.25, 0.3, 0], [".case", "slapIn", 0.6, 0.3, 0],
                  [".hl div", "typeIn", 0.8, 0.35, 0.15], [".ev p", "typeIn", 1.5, 0.35, 0.2]],
        "live": [["#main", "shakeHard .4s linear .3s 1"]],
        "spot": "tick"},
    "collage": {
        "intro": [[".grid div", "slapIn", 0.0, 0.35, 0.2], [".torn", "riseFar", 0.7, 0.5, 0], [".chips span", "slapIn", 1.3, 0.3, 0.15]],
        "live": [[".grid div", "kbZoom {end}s linear 0s both"]],
        "spot": "glow"},
    "radio": {
        "intro": [[".ep", "typeIn", 0.0, 0.5, 0], [".player", "riseFar", 0.2, 0.6, 0], [".chap p", "typeIn", 1.2, 0.4, 0.3]],
        "live": [[".ctrl b", "pulse 1s ease-in-out 0s infinite"]],
        "spot": None},
    "countdown": {
        "intro": [[".ring", "spinY", 0.0, 0.7, 0], [".till", "slapIn", 0.8, 0.35, 0], [".hl div", "slideFarR", 1.0, 0.35, 0.12]],
        "live": [[".cnt", "countDown 1.6s ease-out .1s both"], [".ring", "pulse 1s ease-in-out 1.8s infinite"]],
        "spot": "glow"},
    "percent": {
        "intro": [[".hl div", "typeIn", 0.0, 0.4, 0.15], [".chart", "flipX", 0.5, 0.5, 0]],
        "live": [[".donut", "fillP 1.8s ease-out .7s both"], [".pcnt", "countUp 1.8s ease-out .7s both"]],
        "spot": "underline"},
    "folder": {
        "intro": [[".sheet, #main", "riseFar", 0.0, 0.6, 0], [".label", "typeIn", 0.3, 0.5, 0], [".stamp2", "slapIn", 1.2, 0.35, 0],
                  [".notes p", "typeIn", 1.5, 0.4, 0.25]],
        "live": [["#main", "shakeHard .35s linear 1.25s 1"]],
        "spot": "highlight"},
    "roadsign": {
        "intro": [[".sign", "swingIn", 0.0, 1.0, 0], [".stone", "riseFar", 0.9, 0.45, 0.2]],
        "live": [[".road", "perfs 1s linear 0s infinite"]],
        "spot": "tick"},
}

M.update({
    "crackglass": {
        "intro": [[".glass", "fadeIn", 0.0, 0.15, 0], [".shard", "shatterIn", 0.2, 0.5, 0], [".frag p", "slideFarR", 0.9, 0.3, 0.15]],
        "live": [["#main", "shakeHard .4s linear .15s 1"], [".bgpic", "kbZoom {end}s linear 0s both"]],
        "spot": "glow"},
    "spotlight": {
        "intro": [[".curtain.l", "curtainOpenL", 0.0, 0.9, 0], [".curtain.r", "curtainOpenR", 0.0, 0.9, 0], [".star", "inkIn", 0.7, 0.5, 0],
                  [".hl div", "inkIn", 0.9, 0.5, 0.2], [".cards p", "riseFar", 1.5, 0.4, 0.2]],
        "live": [[".beam", "beamSway 3s ease-in-out 0s infinite"]],
        "spot": None},
    "retrotv": {
        "intro": [[".screen", "tvOn", 0.0, 0.8, 0], [".ch", "flickerOn", 0.6, 0.5, 0], [".hl div", "slideFarL", 0.8, 0.35, 0.12],
                  [".pts p", "typeIn", 1.4, 0.4, 0.25]],
        "live": [[".knobs i", "wobble 2s ease-in-out {start}s infinite"]],
        "spot": "underline"},
    "detective": {
        "intro": [[".photo", "settle", 0.0, 0.6, 0], [".clip2", "slapIn", 0.4, 0.35, 0], [".notes p", "slapIn", 1.0, 0.3, 0.2]],
        "live": [[".strings path", "drawLine 2.4s ease-out 1.2s both"]],
        "spot": "highlight"},
    "weatherapp": {
        "intro": [[".loc", "dropIn", 0.0, 0.4, 0], [".big", "spinY", 0.2, 0.6, 0], [".card", "riseFar", 0.7, 0.45, 0], [".day", "flipX", 1.1, 0.35, 0.15]],
        "live": [[".rain", "rainFall .7s linear 0s infinite"], [".big .ic", "float 2s ease-in-out 0s infinite"]],
        "spot": "glow"},
    "graffiti": {
        "intro": [[".tag", "sprayIn", 0.0, 0.5, 0], [".hl div", "sprayIn", 0.3, 0.55, 0.25], [".drips", "growY", 1.1, 0.6, 0],
                  [".paste p", "slapIn", 1.4, 0.3, 0.15]],
        "spot": "tick"},
    "telegram": {
        "intro": [[".head", "typeIn", 0.0, 0.5, 0], [".meta div", "typeIn", 0.4, 0.3, 0.15], [".hl div", "typeIn", 1.0, 0.5, 0.25],
                  [".body p", "typeIn", 1.8, 0.5, 0.3]],
        "live": [[".head span", "pulse 1.2s ease-in-out {start}s infinite"]],
        "spot": "highlight"},
    "flapboard": {
        "intro": [[".board .hl div", "flipX", 0.1, 0.35, 0.18], [".status", "flickerOn", 0.8, 0.5, 0], [".rw", "flipX", 1.2, 0.3, 0.15]],
        "live": [[".status", "blink 1s steps(1) {start}s infinite"]],
        "spot": "glow"},
    "laptop": {
        "intro": [[".lid", "unfold", 0.0, 0.6, 0], [".bar span", "typeIn", 0.5, 0.5, 0], [".page .hl div", "typeIn", 0.9, 0.4, 0.15]],
        "spot": "underline"},
    "openbook": {
        "intro": [[".book", "flipY", 0.0, 0.7, 0], [".ribbon", "growY", 0.6, 0.5, 0], [".right .hl div", "inkIn", 0.8, 0.5, 0.2],
                  [".right p", "typeIn", 1.5, 0.45, 0.25]],
        "spot": "highlight"},
})

M.update({
    "hero3d": {
        "intro": [[".ribbon", "dropIn", 0.0, 0.4, 0], [".hl div", "slapIn", 0.2, 0.4, 0.15], [".fl", "popIn", 0.8, 0.35, 0.15],
                  [".sub", "riseFar", 1.0, 0.4, 0], [".cards p", "slideFarR", 1.3, 0.35, 0.15]],
        "live": [[".rays", "spinRays {end}s linear 0s both"], [".fl", "float 2.2s ease-in-out {start}s infinite"],
                 [".spark", "blink 1.3s steps(1) 0s infinite"], [".bgpic", "kbZoom {end}s linear 0s both"]],
        "spot": "glow"},
    "glass3d": {
        "intro": [[".photo", "settle", 0.0, 0.6, 0], [".tag", "slideFarL", 0.3, 0.4, 0], [".front", "riseFar", 0.5, 0.5, 0],
                  [".gc", "flipX", 1.1, 0.4, 0.15]],
        "live": [[".orb", "float 3s ease-in-out 0s infinite"], [".photo", "kbPan {end}s ease-in-out 0s both"]],
        "spot": "glow"},
    "poppop": {
        "intro": [[".photo", "slapIn", 0.0, 0.4, 0], [".stamp", "slapIn", 0.4, 0.3, 0], [".hl div", "slideFarR", 0.5, 0.3, 0.12],
                  [".bul p", "slapIn", 1.2, 0.3, 0.15]],
        "live": [["#main", "shakeHard .35s linear .45s 1"], [".stamp", "wobble 1.2s ease-in-out {start}s infinite"]],
        "spot": "tick"},
    "cinema": {
        "intro": [[".pre", "inkIn", 0.0, 0.8, 0], [".hl div", "inkIn", 0.6, 0.8, 0.3], [".tagline", "fadeIn", 1.5, 0.5, 0],
                  [".stars", "typeIn", 1.8, 0.6, 0], [".credits p", "fadeIn", 2.0, 0.4, 0.2]],
        "live": [[".bgpic", "kbZoom {end}s ease-out 0s both"]],
        "spot": None},
})

M.update({
    "typo": {"intro": [[".kick", "typeIn", 0.0, 0.3, 0], [".wall span", "slapIn", 0.1, 0.25, 0.12], [".rule", "typeIn", 1.4, 0.4, 0],
                       [".dot", "popIn", 1.6, 0.4, 0], [".lower p", "typeIn", 1.8, 0.4, 0.25], [".sticker", "slapIn", 2.4, 0.3, 0]],
             "spot": None},
    "fullbleed": {"intro": [[".pill", "slideFarL", 0.3, 0.3, 0], [".hl div", "inkIn", 0.5, 0.6, 0.2], [".one", "fadeIn", 1.4, 0.5, 0],
                            [".meta", "fadeIn", 1.7, 0.4, 0], [".sticker", "slapIn", 2.2, 0.3, 0]],
                  "live": [[".bgpic", "kbZoom {end}s ease-out 0s both"]], "spot": None},
    "splitv": {"intro": [[".bar", "growY", 0.0, 0.5, 0], [".stack span", "slideFarR", 0.2, 0.3, 0.1], [".rule", "typeIn", 1.3, 0.3, 0],
                         [".pt2 p", "typeIn", 1.5, 0.4, 0.25], [".sticker", "slapIn", 2.2, 0.3, 0]],
               "live": [[".strip", "kbPan {end}s ease-in-out 0s both"]], "spot": None},
    "ring": {"intro": [[".disc", "popIn", 0.0, 0.5, 0], [".ringsvg", "spinY", 0.3, 0.8, 0], [".kick", "dropIn", 0.2, 0.4, 0],
                       [".under p", "fadeIn", 1.3, 0.4, 0.2], [".sticker", "slapIn", 2.0, 0.3, 0]],
             "live": [[".ringsvg", "ringTurn {end}s linear 0s both"]], "spot": None},
    "cutout": {"intro": [[".snap", "dropBounce", 0.0, 0.7, 0], [".collage span", "slapIn", 0.5, 0.25, 0.13], [".torn p", "slapIn", 1.9, 0.25, 0.15],
                         [".sticker", "slapIn", 2.4, 0.3, 0]],
               "spot": None},
    "droste": {"intro": [[".f2", "settle", 0.0, 0.5, 0], [".f3", "settle", 0.2, 0.5, 0], [".f4", "settle", 0.4, 0.5, 0],
                         [".core .hl div", "slideFarL", 0.8, 0.35, 0.15], [".one", "fadeIn", 1.5, 0.4, 0], [".sticker", "slapIn", 2.0, 0.3, 0]],
               "live": [[".f4", "kbZoom {end}s linear 0s both"], [".f1", "kbZoom {end}s linear 0s both"]], "spot": None},
})

SPOT_ANIM = {
    "glow": "spot {step}s ease-in-out {at}s",
    "underline": "underline {step}s ease-in-out {at}s",
    "tick": "tick {step}s ease-out {at}s",
    "highlight": "highlightSweep {step}s ease-out {at}s both",
}

LIVE_JS = """([start, end, extra, spot, overlay]) => {
  const add = (el, anim) => { el.style.animation = (el.style.animation ? el.style.animation + ', ' : '') + anim; };
  const all = s => [...document.querySelectorAll(s)];
  const total = Math.max(end - start, 1);
  if (overlay) { const fx = document.createElement('div'); fx.id = 'fx'; fx.innerHTML = overlay; document.body.appendChild(fx); }
  for (const [sel, anim] of extra) {
    const a = anim.replaceAll('{start}', start).replaceAll('{end}', end).replaceAll('{total}', total);
    all(sel).forEach(el => add(el, a));
  }
  if (spot) {
    const rows = all(spot.rows).filter(el => el.offsetParent !== null || el.closest('#fx'));
    const step = rows.length ? Math.max(.6, Math.min(1.6, (total - 1.2) / rows.length)) : 0;
    rows.forEach((el, i) => add(el, spot.anim.replaceAll('{step}', step).replaceAll('{at}', start + i * step)));
  }
  document.getAnimations().forEach(a => a.pause());
}"""


def motion(template: str) -> dict:
    return M.get(template, {"intro": [], "live": [], "spot": "glow"})


def add_style_motion(page, template: str, start: float, end: float) -> None:
    """The layout's own live motion, overlay and reading guide (after the shared live motion)."""
    m = motion(template)
    spot = m.get("spot")
    page.add_style_tag(content=OVERLAY_CSS)
    page.evaluate(LIVE_JS, [start, end, m.get("live", []),
                            {"rows": ROWS, "anim": SPOT_ANIM[spot]} if spot else None, m.get("overlay", "")])
