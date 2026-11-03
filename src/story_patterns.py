"""Image-first story reels in the look of the reference posters: the picture shows first, then the headline comes in
word by word in big 3D letters, then the rest of the text arrives one element at a time.

The posters are full and loud like the reference posters: thick 3D letters with outlines, brush-stroke strips,
glowing fact boxes, a 3D icon next to every point, stickers, and the "?" question strip with the red comment tag.
The picture sits in a bordered frame (never stretched or blurred). Six patterns, chosen by the kind of news:

  brk     crime / breaking: black-red, hazard stripes, red brush strips, neon points box, BREAKING bar
  gold    good news / events: royal purple with gold rays, gold 3D letters, medal fact badges
  neon    weather / trending: night purple with sparkles, glowing neon letters and boxes
  stack   money / prices: bright yellow pop-art, huge words in coloured blocks, offset-shadow cards
  card2   government / exams: sky blue, white card, coloured icon circles (like the iPhone poster)
  glitch  politics / viral: black-green cyber, RGB letters, terminal boxes

Every word is real text in a real font, so the spelling is always right.
"""
from src.designs import BRUSH_MASK, esc, highlight_numbers
from src.icons import icon_img
from src.viral_layouts import BASE, _ask, _lines
from src.viral_more import SYM, _bg, _page, _pts

IMG_ONLY = 1.1   # seconds the picture is shown alone

# thick outline + stacked shadows = 3D extruded letters (colour of the depth per pattern)
def _x3d(depth: str, outline: str = "#111") -> str:
    shadows = ", ".join(f"{i}px {i}px 0 {depth}" for i in range(1, 9))
    return (f"-webkit-text-stroke: 4px {outline}; paint-order: stroke fill; "
            f"text-shadow: {shadows}, 10px 16px 18px rgba(0,0,0,.55);")


def _base(font, top=30):
    return BASE % {"font": font, "mask": BRUSH_MASK, "top": top, "min_top": top}


def _hl_words(story, n=None) -> str:
    """Headline lines, every word in its own span (.w) so the words can animate one by one."""
    n = n or (2 if len(story.headline) < 26 else 3 if len(story.headline) < 56 else 4)
    hi = set(story.highlight.split()) if story.highlight else set()
    out = []
    for line in _lines(story.headline, n):
        words = "".join(f'<span class="w{" hi" if w in hi else ""}">{esc(w)}</span> ' for w in line.split())
        out.append(f'<div class="brush">{words.strip()}</div>')
    return f'<div class="hl">{"".join(out)}</div>'


def _facts(story, cls="fact") -> str:
    facts = [f for f in story.facts if len(f["value"]) <= 16][:2]
    return "".join(f'<div class="{cls}">{icon_img(f["label"] + " " + f["value"])}<div><small>{esc(f["label"])}</small>'
                   f'<b>{esc(f["value"])}</b></div></div>' for f in facts)


def _points(story, n=4) -> str:
    return "".join(f'<div class="pt">{icon_img(p)}<span>{highlight_numbers(p)}</span></div>' for p in _pts(story, n))


def _ask_strip(story, asks) -> str:
    return (f'<div class="v-ask"><div class="q">?</div><div class="say brush">{_ask(story, asks)}</div>'
            f'<div class="bubble brush">કોમેન્ટ કરીને<br>જરૂર જણાવો</div></div>')


def _foot(story, date, handle):
    return f'<div class="foot"><span>સ્રોત: {esc(story.source_name)}</span><span>{esc(handle)} • {esc(date)}</span></div>'


# shared look: picture frame that takes the free space, big letters, boxes with icons
KIT = """
  body { color: #fff; }
  #main { gap: 18px; }
  .w { display: inline-block; }
  .pic { position: relative; flex: 1 1 auto; min-height: 560px; border-radius: 28px; background: #333 center/cover no-repeat;
    border: 8px solid var(--frame); box-shadow: 0 16px 34px rgba(0,0,0,.45); }
  .pic .sym { bottom: 12px; }
  .pic .tag { position: absolute; left: -8px; top: 22px; display: flex; box-shadow: 0 8px 18px rgba(0,0,0,.5); }
  .pic .tag b { background: var(--c1); color: #fff; font-size: 34px; padding: 6px 18px 10px; }
  .pic .tag span { background: #111; color: var(--c2); font-size: 42px; font-weight: 800; padding: 2px 22px 8px; }
  .hl { gap: 8px; }
  .hl div { font-size: var(--hl); font-weight: 800; line-height: 1.3; padding: 16px 30px 14px; overflow: visible; }
  .sub { align-self: center; text-align: center; font-size: calc(var(--pt) * 1.12); font-weight: 800; padding: 8px 26px 12px; line-height: 1.3; }
  .facts { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; }
  .fact { display: flex; align-items: center; gap: 12px; border-radius: 24px; padding: 8px 22px 8px 10px; }
  .fact .ic { width: 78px; height: 78px; filter: drop-shadow(0 6px 6px rgba(0,0,0,.35)); }
  .fact small { display: block; font-size: 24px; font-weight: 800; line-height: 1.1; }
  .fact b { display: block; font-size: 48px; font-weight: 800; line-height: 1.1; }
  .box { border-radius: 26px; padding: 10px 20px; }
  .pt { display: flex; gap: 14px; align-items: center; font-size: var(--pt); font-weight: 800; line-height: 1.28; padding: 8px 0; }
  .pt + .pt { border-top: 2px dashed rgba(255,255,255,.22); }
  .pt .ic { width: calc(var(--pt) * 1.5); height: calc(var(--pt) * 1.5); flex-shrink: 0; filter: drop-shadow(0 4px 4px rgba(0,0,0,.35)); }
  .foot { font-size: 24px; opacity: .85; }
"""


# ---------------------------------------------------------------------------------------------------- brk
BRK_CSS = KIT + """
  :root { --frame: #ffe600; --c1: #e10600; --c2: #ffe600; }
  body { background: radial-gradient(circle at 50% 60%, #3a0303 0%, #120202 70%);
    background-image: repeating-linear-gradient(135deg, rgba(255,0,0,.07) 0 30px, transparent 30px 60px), radial-gradient(circle at 50% 60%, #3a0303 0%, #120202 70%); }
  .hazard { height: 26px; margin: 0 -30px; background: repeating-linear-gradient(-45deg, #ffd000 0 34px, #111 34px 68px); }
  .hl div { background: linear-gradient(180deg, #ff1a1a, #9d0000); color: #fff; """ + _x3d("#4a0000") + """ }
  .hl div:nth-child(even) { color: #ffe600; }
  .hl .hi { color: #ffe600; font-size: 1.18em; } .hl div:nth-child(even) .hi { color: #fff; }
  .sub { background: #ffe600; color: #111; transform: rotate(-1.5deg); }
  .sub .num { color: #c00; }
  .fact { background: #fff; color: #111; border: 5px solid #e10600; } .fact b { color: #c00; }
  .box { background: rgba(8,8,18,.92); border: 4px solid #ff2e63; box-shadow: 0 0 26px rgba(255,46,99,.7); }
  .box .num { color: #ffe600; }
  .breaking { display: flex; align-items: center; justify-content: center; gap: 14px; background: #e10600; color: #fff; font-size: 44px; font-weight: 800;
    padding: 6px 0 10px; margin: 0 -30px; border-top: 4px solid #ffe600; border-bottom: 4px solid #ffe600; }
  .breaking .ic { width: 60px; height: 60px; }
"""


def brk_page(story, font, image_url, date, handle, place, asks):
    pts = _points(story)
    facts = _facts(story)
    body = f"""<div class="handle" style="top:22px;right:22px">{esc(handle)}</div>
  <div id="main">
    <div class="pic"{_bg(image_url)}>{SYM if image_url else ""}<div class="tag"><b>🚨 બ્રેકિંગ</b><span>{esc(place or story.kicker or "")}</span></div></div>
    <div class="hazard"></div>
    {_hl_words(story)}
    {f'<div class="sub brush">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="facts">{facts}</div>' if facts else ""}
    {f'<div class="box">{pts}</div>' if pts else ""}
    <div class="breaking">{icon_img("siren")}BREAKING NEWS{icon_img("siren")}</div>
    {_ask_strip(story, asks)}
    {_foot(story, date, handle)}
  </div>"""
    return _page(_base(font) + BRK_CSS, font, body)


# --------------------------------------------------------------------------------------------------- gold
GOLD_CSS = KIT + """
  :root { --frame: #f5c542; --c1: #7b2ff7; --c2: #ffd66b; }
  body { background: radial-gradient(circle at 50% 35%, #5a189a 0%, #240046 55%, #10002b 100%); }
  body::before { content: ""; position: absolute; left: 50%; top: 40%; width: 2400px; height: 2400px; margin: -1200px 0 0 -1200px; opacity: .25;
    background: repeating-conic-gradient(rgba(255,214,107,.6) 0 5deg, transparent 5deg 15deg);
    -webkit-mask-image: radial-gradient(circle, #000 0%, transparent 55%); }
  .ribbon { align-self: center; background: linear-gradient(180deg, #ffd66b, #c9962c); color: #3c096c; font-size: 40px; font-weight: 800; padding: 6px 50px 12px;
    clip-path: polygon(0 0, 100% 0, 95% 50%, 100% 100%, 0 100%, 5% 50%); }
  .hl div { color: #ffd66b; """ + _x3d("#7a5200", "#2b1500") + """ }
  .hl div:nth-child(even) { color: #fff; }
  .hl .hi { color: #ff4fd8; font-size: 1.18em; }
  .sub { background: rgba(255,255,255,.14); border: 3px solid #ffd66b; border-radius: 40px; color: #fff; }
  .sub .num { color: #ffd66b; }
  .fact { background: radial-gradient(circle at 30% 30%, #fff6d5, #f5c542); color: #3c096c; border: 4px solid #fff; border-radius: 60px; }
  .box { background: rgba(255,255,255,.1); border: 3px solid rgba(255,214,107,.8); }
  .box .num { color: #ffd66b; }
"""


def gold_page(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="handle" style="top:22px;right:22px">{esc(handle)}</div>
  <div id="main">
    <div class="ribbon">⭐ {esc(place or story.kicker or "ખુશખબર")} ⭐</div>
    <div class="pic"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {_hl_words(story)}
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="facts">{_facts(story)}</div>' if _facts(story) else ""}
    {f'<div class="box">{_points(story, 3)}</div>' if _points(story, 3) else ""}
    {_ask_strip(story, asks)}
    {_foot(story, date, handle)}
  </div>"""
    return _page(_base(font) + GOLD_CSS, font, body)


# --------------------------------------------------------------------------------------------------- neon
NEON_CSS = KIT + """
  :root { --frame: #00f5d4; --c1: #9b5de5; --c2: #00f5d4; }
  body { background: radial-gradient(circle at 30% 20%, #3c096c 0%, #10002b 60%, #05010f 100%); }
  body::after { content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.7) 1.5px, transparent 2px);
    background-size: 90px 110px; opacity: .35; pointer-events: none; }
  .pic { box-shadow: 0 0 30px #00f5d4; }
  .sign { align-self: center; color: #ff4fd8; border: 5px solid #ff4fd8; border-radius: 20px; padding: 4px 30px 10px; font-size: 40px; font-weight: 800;
    text-shadow: 0 0 10px #ff4fd8, 0 0 30px #ff4fd8; box-shadow: 0 0 18px #ff4fd8, inset 0 0 18px #ff4fd8; }
  .hl div { color: #fff; -webkit-text-stroke: 3px #003b36; paint-order: stroke fill;
    text-shadow: 0 0 8px #fff, 0 0 20px #00f5d4, 0 0 44px #00f5d4, 0 0 80px #00bbf9; }
  .hl div:nth-child(even) { color: #fff6b0; text-shadow: 0 0 8px #fff, 0 0 20px #ffd60a, 0 0 44px #ff9e00; }
  .hl .hi { color: #ff4fd8; }
  .sub { color: #fff; background: #9b5de5; border-radius: 40px; box-shadow: 0 0 20px #9b5de5; }
  .sub .num { color: #fff6b0; }
  .fact { background: rgba(0,0,0,.5); border: 3px solid #00f5d4; box-shadow: 0 0 16px #00f5d4; } .fact b { color: #00f5d4; }
  .box { background: rgba(16,0,43,.85); border: 3px solid #ff4fd8; box-shadow: 0 0 22px #ff4fd8; }
  .box .num { color: #fff6b0; }
"""


def neon_page(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="handle" style="top:22px;right:22px">{esc(handle)}</div>
  <div id="main">
    <div class="sign">📍 {esc(place or story.kicker or "LIVE")}</div>
    <div class="pic"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {_hl_words(story)}
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="facts">{_facts(story)}</div>' if _facts(story) else ""}
    {f'<div class="box">{_points(story, 3)}</div>' if _points(story, 3) else ""}
    {_ask_strip(story, asks)}
    {_foot(story, date, handle)}
  </div>"""
    return _page(_base(font) + NEON_CSS, font, body)


# -------------------------------------------------------------------------------------------------- stack
STACK_CSS = KIT + """
  :root { --frame: #111; --c1: #ff006e; --c2: #ffbe0b; }
  body { background: #ffd60a; background-image: radial-gradient(rgba(0,0,0,.14) 22%, transparent 24%); background-size: 22px 22px; color: #111; }
  .pic { border-width: 10px; box-shadow: 14px 14px 0 #ff006e; transform: rotate(-1.5deg); border-radius: 6px; }
  .hl div { color: #111; padding: 0 10px 6px; }
  .hl .w { padding: 0 16px 8px; margin: 0 3px 6px; border: 4px solid #111; box-shadow: 6px 6px 0 #111; background: #fff; }
  .hl div:nth-child(3n+1) .w:nth-child(odd) { background: #ff006e; color: #fff; }
  .hl div:nth-child(3n+2) .w:nth-child(even) { background: #3a86ff; color: #fff; }
  .hl div:nth-child(3n+3) .w:nth-child(odd) { background: #8338ec; color: #fff; }
  .hl .hi { background: #111 !important; color: #ffd60a !important; transform: rotate(-3deg); font-size: 1.12em; }
  .sub { background: #111; color: #fff; }
  .sub .num { color: #ffd60a; }
  .fact { background: #fff; border: 5px solid #111; box-shadow: 8px 8px 0 #3a86ff; border-radius: 0; } .fact b { color: #ff006e; }
  .box { background: #fff; border: 5px solid #111; box-shadow: 10px 10px 0 #111; border-radius: 0; color: #111; }
  .pt + .pt { border-top-color: rgba(0,0,0,.18); }
  .box .num { color: #ff006e; }
  .foot { color: #111; }
"""


def stack_page(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="handle" style="top:22px;right:22px;background:#111">{esc(handle)}</div>
  <div id="main">
    <div class="pic"{_bg(image_url)}>{SYM if image_url else ""}<div class="tag"><b>💰</b><span>{esc(place or story.kicker or "")}</span></div></div>
    {_hl_words(story)}
    {f'<div class="sub brush">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="facts">{_facts(story)}</div>' if _facts(story) else ""}
    {f'<div class="box">{_points(story, 3)}</div>' if _points(story, 3) else ""}
    {_ask_strip(story, asks)}
    {_foot(story, date, handle)}
  </div>"""
    return _page(_base(font) + STACK_CSS, font, body)


# -------------------------------------------------------------------------------------------------- card2
CARD_CSS = KIT + """
  :root { --frame: #fff; --c1: #1d3fbf; --c2: #ffe600; }
  body { background: linear-gradient(180deg, #0a1f5c 0%, #1d3fbf 50%, #0a1f5c 100%); }
  .hl div:first-child { color: #fff; """ + _x3d("#0a1f5c", "#0a1433") + """ }
  .hl div:nth-child(2) { background: #ffe600; color: #111; transform: rotate(-1.5deg); }
  .hl div:nth-child(n+3) { background: linear-gradient(180deg, #ff1a1a, #9d0000); color: #ffe600; """ + _x3d("#4a0000") + """ }
  .hl .hi { color: #e10600; } .hl div:nth-child(n+3) .hi, .hl div:first-child .hi { color: #ffe600; }
  .sub { background: #111; color: #fff; border: 4px solid #fff; border-radius: 22px; }
  .sub .num { color: #ffe600; }
  .fact { background: #fff; color: #0a1f5c; border: 4px solid #ffe600; } .fact b { color: #e10600; }
  .box { background: linear-gradient(180deg, #ffffff, #eef3ff); color: #1a1a2e; box-shadow: 0 16px 34px rgba(0,0,0,.4); }
  .pt .ic { background: radial-gradient(circle at 35% 30%, #ff6b6b, #c1121f); border-radius: 50%; padding: 10px; border: 4px solid #fff; }
  .pt:nth-child(3n+2) .ic { background: radial-gradient(circle at 35% 30%, #5ee27a, #138a36); }
  .pt:nth-child(3n+3) .ic { background: radial-gradient(circle at 35% 30%, #5b8cff, #1d3fbf); }
  .pt + .pt { border-top-color: #dfe6f5; }
  .box .num { color: #c1121f; }
"""


def card_page(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="handle" style="top:22px;right:22px">{esc(handle)}</div>
  <div id="main">
    <div class="pic"{_bg(image_url)}>{SYM if image_url else ""}<div class="tag"><b>📢</b><span>{esc(place or story.kicker or "")}</span></div></div>
    {_hl_words(story)}
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="facts">{_facts(story)}</div>' if _facts(story) else ""}
    {f'<div class="box">{_points(story, 3)}</div>' if _points(story, 3) else ""}
    {_ask_strip(story, asks)}
    {_foot(story, date, handle)}
  </div>"""
    return _page(_base(font) + CARD_CSS, font, body)


# ------------------------------------------------------------------------------------------------- glitch
GLITCH_CSS = KIT + """
  :root { --frame: #00ff9c; --c1: #ff0050; --c2: #00ff9c; }
  body { background: #050805; background-image: repeating-linear-gradient(0deg, rgba(0,255,156,.06) 0 2px, transparent 2px 6px),
    radial-gradient(circle at 50% 30%, #0b2a1d 0%, #050805 70%); }
  .pic { box-shadow: 0 0 26px rgba(0,255,156,.6); }
  .scan { align-self: flex-start; font: 800 36px/1 'Courier New', monospace; color: #00ff9c; border: 3px solid #00ff9c; padding: 10px 18px; background: rgba(0,0,0,.6); }
  .hl div { color: #fff; -webkit-text-stroke: 3px #000; paint-order: stroke fill;
    text-shadow: 6px 0 0 rgba(255,0,80,.9), -6px 0 0 rgba(0,220,255,.9), 0 10px 16px rgba(0,0,0,.6); }
  .hl .hi { color: #00ff9c; }
  .sub { background: #ff0050; color: #fff; }
  .sub .num { color: #00ff9c; }
  .fact { background: #000; border: 3px solid #00ff9c; } .fact b { color: #00ff9c; }
  .box { background: rgba(0,0,0,.75); border: 3px solid #00ff9c; font-family: 'Courier New', monospace; }
  .box .num { color: #00ff9c; }
"""


def glitch_page(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="handle" style="top:22px;right:22px">{esc(handle)}</div>
  <div id="main">
    <div class="scan">[ {esc(place or story.kicker or "LIVE")} ]</div>
    <div class="pic"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {_hl_words(story)}
    {f'<div class="sub brush">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="facts">{_facts(story)}</div>' if _facts(story) else ""}
    {f'<div class="box">{_points(story, 3)}</div>' if _points(story, 3) else ""}
    {_ask_strip(story, asks)}
    {_foot(story, date, handle)}
  </div>"""
    return _page(_base(font) + GLITCH_CSS, font, body)


def _with_hero(page):
    """The picture fills the whole screen first (image only), then fades into its frame as the text starts."""
    def wrapped(story, font, image_url, date, handle, place, asks):
        html = page(story, font, image_url, date, handle, place, asks)
        if not image_url:
            return html
        hero = (f'<div class="hero" style="position:absolute;inset:0;z-index:60;opacity:0;background:#000 url({image_url}) center/cover no-repeat">'
                '</div>')
        return html.replace("<body>", "<body>" + hero, 1)
    return wrapped


PATTERNS = {name: _with_hero(fn) for name, fn in {"brk": brk_page, "gold": gold_page, "neon": neon_page, "stack": stack_page,
                                                 "card": card_page, "glitch": glitch_page}.items()}

S = IMG_ONLY
_HERO = [".hero", "heroOut", S - 0.25, 0.55, 0]
_REST = [[".sub", "slapIn", S + 2.0, 0.35, 0], [".fact", "popIn", S + 2.4, 0.35, 0.2], [".box", "fadeIn", S + 2.8, 0.25, 0],
         [".pt", "slideFarL", S + 2.9, 0.35, 0.35], [".v-ask", "riseUp", S + 4.3, 0.4, 0], [".foot, .handle", "fadeIn", S + 4.5, 0.4, 0]]
# image first, then the headline word by word, then the rest one element at a time (src/card.ANIM_JS format)
PATTERN_MOTION = {
    "brk": {"intro": [_HERO, [".pic .tag", "slideFarL", S, 0.35, 0], [".hazard", "slideFarR", S + .2, 0.3, 0], [".hl div", "growX", S + .3, 0.3, 0.25],
                      [".hl .w", "slapIn", S + .5, 0.25, 0.1], [".breaking", "slideFarR", S + 4.0, 0.35, 0]] + _REST,
            "live": [[".pic", "kbPan {end}s linear 0s both"], [".pic .tag b", "blink 1s steps(1) {start}s infinite"],
                     [".hazard", "march 1.2s linear 0s infinite"]], "spot": None},
    "gold": {"intro": [_HERO, [".ribbon", "dropIn", S, 0.4, 0], [".hl .w", "wordRise", S + .4, 0.55, 0.13]] + _REST,
             "live": [[".pic", "kbPan {end}s ease-in-out 0s both"]], "spot": None},
    "neon": {"intro": [_HERO, [".sign", "flickerOn", S, 0.8, 0], [".hl .w", "flickerOn", S + .4, 0.7, 0.14]] + _REST,
             "live": [[".pic", "kbPan {end}s linear 0s both"], [".sign", "flicker 3s linear {start}s infinite"]], "spot": None},
    "stack": {"intro": [_HERO, [".pic .tag", "slapIn", S, 0.3, 0], [".hl .w", "dropIn", S + .2, 0.45, 0.13]] + _REST,
              "live": [[".pic", "kbPan {end}s ease-in-out 0s both"]], "spot": None},
    "card": {"intro": [_HERO, [".pic .tag", "slideFarL", S, 0.35, 0], [".hl div", "typeIn", S + .3, 0.55, 0.4]] + _REST,
             "live": [[".pic", "kbPan {end}s linear 0s both"], [".pt .ic", "wobble 1.6s ease-in-out {start}s infinite"]], "spot": None},
    "glitch": {"intro": [_HERO, [".scan", "typeIn", S, 0.5, 0], [".hl div", "glitch", S + .4, 0.45, 0.3]] + _REST,
               "live": [[".pic", "kbPan {end}s linear 0s both"]], "spot": None},
}

EXTRA_KEYFRAMES = """
@keyframes heroOut { 0% { opacity: 1; transform: scale(1.06); } 100% { opacity: 0; transform: scale(1.2); } }
@keyframes growX { from { transform: var(--t0, translate(0)) scaleX(0); transform-origin: left; } to { transform: var(--t0, translate(0)) scaleX(1); transform-origin: left; } }
@keyframes wordRise { from { transform: var(--t0, translate(0)) translateY(60px); filter: blur(10px); opacity: 0; }
  to { transform: var(--t0, translate(0)); filter: none; opacity: 1; } }
@keyframes tickIn { 0% { transform: var(--t0, translate(0)) translateX(-40px); opacity: 0; } 60% { transform: var(--t0, translate(0)) translateX(8px); opacity: 1; }
  100% { transform: var(--t0, translate(0)); } }
"""
