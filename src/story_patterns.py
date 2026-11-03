"""Image-first story reels: the picture shows alone first, then the headline animates in word by word in big
styled letters, then the rest of the text comes in slowly, one element after another. Six patterns, each with its
own composition and its own animation:

  brk     breaking: red brush strips grow across the picture, the words slam onto them, a dark box of points
  gold    cinematic: gold 3D words rise out of a blur at the bottom, glass fact chips, points fade in
  neon    night: the words switch on like neon signs one by one, points are typed
  stack   bold: huge coloured words drop and bounce into a stack, fact chips slam in
  card    card: a white card slides up over the picture, the headline is typed in, points tick in with checks
  glitch  glitch: each line glitches in with an RGB split, a scanning place tag, points slide in

Timeline (all patterns): 0-1.1 s picture alone (slow zoom) -> headline word by word -> sub line -> facts ->
points one by one -> question -> hold. Every word is real text in a real font.
"""
import re

from src.designs import esc, highlight_numbers
from src.icons import icon_img
from src.viral_layouts import BASE, _ask, _lines
from src.viral_more import SYM, _bg, _page, _pts

IMG_ONLY = 1.1   # seconds the picture is shown alone


def _base(font, top=40):
    from src.designs import BRUSH_MASK
    return BASE % {"font": font, "mask": BRUSH_MASK, "top": top, "min_top": top}


def _hl_words(story, n=None, line_cls=lambda i: "") -> str:
    """Headline lines, every word in its own span (.w) so the words can animate one by one."""
    n = n or (2 if len(story.headline) < 28 else 3 if len(story.headline) < 60 else 4)
    hi = set(story.highlight.split()) if story.highlight else set()
    out = []
    for i, line in enumerate(_lines(story.headline, n)):
        words = "".join(f'<span class="w{" hi" if w in hi else ""}">{esc(w)}</span> ' for w in line.split())
        out.append(f'<div class="{line_cls(i)}">{words.strip()}</div>')
    return f'<div class="hl">{"".join(out)}</div>'


COMMON = """
  .bgpic { position: absolute; inset: 0; background: #222 center/cover no-repeat; }
  .sym { top: 24px; right: 24px; }
  .w { display: inline-block; }
  .handle { top: 26px; left: 26px; z-index: 7; }
  .foot2 { position: absolute; left: 34px; right: 34px; bottom: 22px; z-index: 7; display: flex; justify-content: space-between;
    font-size: 24px; font-weight: 700; color: rgba(255,255,255,.85); }
  .ask2 { align-self: center; background: #ffe14d; color: #111; font-size: calc(var(--pt) * 1.05); font-weight: 800; padding: 12px 30px 16px;
    border-radius: 40px; box-shadow: 0 10px 24px rgba(0,0,0,.4); text-align: center; line-height: 1.25; }
  .ask2 small { display: block; font-size: .7em; color: #b00000; }
"""


def _foot(story, date, handle):
    return f'<div class="foot2"><span>સ્રોત: {esc(story.source_name)}</span><span>{esc(handle)} • {esc(date)}</span></div>'


def _ask2(story, asks):
    return f'<div class="ask2">{_ask(story, asks)}<small>કોમેન્ટ કરીને જરૂર જણાવો 👇</small></div>'


# ---------------------------------------------------------------------------------------------------- brk
BRK_CSS = COMMON + """
  body { background: #120202; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.1) 0%, rgba(0,0,0,.05) 30%, rgba(18,2,2,.75) 55%, #120202 85%); }
  #main { top: 700px; }
  .tag { align-self: flex-start; display: flex; border: 4px solid #fff; box-shadow: 0 10px 24px rgba(0,0,0,.5); }
  .tag b { background: #e10600; color: #fff; font-size: 36px; padding: 6px 18px 10px; }
  .tag span { background: #111; color: #ffe600; font-size: 44px; font-weight: 800; padding: 2px 24px 8px; }
  .hl { align-items: flex-start; gap: 8px; }
  .hl div { background: linear-gradient(180deg, #e10600, #8f0000); color: #fff; padding: 4px 26px 12px; -webkit-mask-image: %MASK%;
    -webkit-mask-size: 100% 100%; text-align: left; }
  .hl div:nth-child(even) { color: #ffe600; }
  .hl .hi { color: #ffe600; font-size: 1.2em; } .hl div:nth-child(even) .hi { color: #fff; }
  .sub { align-self: flex-start; background: #ffe600; color: #111; font-size: calc(var(--pt) * 1.05); font-weight: 800; padding: 6px 20px 10px; }
  .sub .num { color: #c00; }
  .box { background: rgba(10,10,20,.9); border: 3px solid #ff2e63; border-radius: 22px; padding: 12px 20px; box-shadow: 0 0 22px rgba(255,46,99,.6); }
  .box p { font-size: var(--pt); font-weight: 700; line-height: 1.32; color: #fff; padding: 6px 0 6px 38px; position: relative; }
  .box p::before { content: "▶"; position: absolute; left: 0; color: #ffe600; }
  .box .num { color: #ffe600; }
"""


def brk_page(story, font, image_url, date, handle, place, asks):
    from src.designs import BRUSH_MASK
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 4))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="tag"><b>🚨 બ્રેકિંગ</b><span>{esc(place or story.kicker or "")}</span></div>
    {_hl_words(story)}
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="box">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_ask2(story, asks)}
  </div>{_foot(story, date, handle)}"""
    return _page(_base(font, 700).replace("top: var(--top)", "top: var(--top)") + BRK_CSS.replace("%MASK%", BRUSH_MASK), font, body)


# --------------------------------------------------------------------------------------------------- gold
GOLD_CSS = COMMON + """
  body { background: #070707; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.35) 0%, transparent 25%, rgba(7,7,7,.6) 52%, #070707 82%); }
  #main { top: 820px; }
  .pre { text-align: center; color: #e9c46a; font-size: 34px; font-weight: 800; letter-spacing: 6px; }
  .hl { gap: 0; }
  .hl div { padding: 0 16px 8px; color: #ffd66b; -webkit-text-stroke: 2px #4a2c00; paint-order: stroke fill;
    text-shadow: 0 2px 0 #b8860b, 0 4px 0 #8a6200, 0 6px 0 #5c4100, 0 12px 22px rgba(0,0,0,.8); }
  .hl .hi { color: #fff; }
  .tagline { text-align: center; color: #f1faee; font-size: calc(var(--pt) * 1.05); font-weight: 600; font-style: italic; line-height: 1.35; }
  .tagline .num { color: #ffd66b; }
  .chips { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; }
  .chip { background: rgba(255,255,255,.12); border: 2px solid rgba(255,214,107,.7); border-radius: 22px; padding: 10px 22px; text-align: center; }
  .chip small { display: block; color: #ccc; font-size: 24px; font-weight: 700; }
  .chip b { color: #ffd66b; font-size: 44px; }
  .lines p { text-align: center; font-size: var(--pt); font-weight: 600; color: #e5e5e5; line-height: 1.4; }
  .lines .num { color: #ffd66b; }
  .ask2 { background: linear-gradient(90deg, #ffd66b, #e9c46a); }
"""


def gold_page(story, font, image_url, date, handle, place, asks):
    chips = "".join(f'<div class="chip"><small>{esc(f["label"])}</small><b>{esc(f["value"])}</b></div>'
                    for f in story.facts[:2] if len(f["value"]) <= 14)
    lines = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="pre">{esc(place or story.kicker or "")}</div>
    {_hl_words(story)}
    {f'<div class="tagline">“{highlight_numbers(story.subheadline)}”</div>' if story.subheadline else ""}
    {f'<div class="chips">{chips}</div>' if chips else ""}
    {f'<div class="lines">{lines}</div>' if lines else ""}
    <div class="grow"></div>
    {_ask2(story, asks)}
  </div>{_foot(story, date, handle)}"""
    return _page(_base(font, 820) + GOLD_CSS, font, body)


# --------------------------------------------------------------------------------------------------- neon
NEON_CSS = COMMON + """
  body { background: #05010f; }
  .bgpic { filter: brightness(.45) saturate(1.3) hue-rotate(-10deg); }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 30%, rgba(5,1,15,.85) 65%); }
  #main { top: 640px; }
  .sign { align-self: center; color: #ff4fd8; border: 5px solid #ff4fd8; border-radius: 20px; padding: 4px 30px 10px; font-size: 40px; font-weight: 800;
    text-shadow: 0 0 10px #ff4fd8, 0 0 30px #ff4fd8; box-shadow: 0 0 18px #ff4fd8, inset 0 0 18px #ff4fd8; }
  .hl div { color: #eafffb; text-shadow: 0 0 6px #fff, 0 0 18px #00f5d4, 0 0 40px #00f5d4, 0 0 80px #00bbf9; }
  .hl .hi { color: #fff6b0; text-shadow: 0 0 6px #fff, 0 0 18px #ffd60a, 0 0 40px #ff9e00; }
  .sub { text-align: center; color: #c8b6ff; font-size: var(--pt); font-weight: 700; }
  .typed p { font: 600 var(--pt)/1.4 'Courier New', '%FONT%', monospace; color: #b9fbc0; text-shadow: 0 0 8px rgba(185,251,192,.7);
    border-left: 4px solid #00f5d4; padding-left: 16px; margin-bottom: 10px; }
  .typed .num { color: #fff6b0; }
  .ask2 { background: #00f5d4; box-shadow: 0 0 24px #00f5d4; }
"""


def neon_page(story, font, image_url, date, handle, place, asks):
    typed = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="sign">{esc(place or story.kicker or "LIVE")}</div>
    {_hl_words(story)}
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="typed">{typed}</div>' if typed else ""}
    <div class="grow"></div>
    {_ask2(story, asks)}
  </div>{_foot(story, date, handle)}"""
    return _page(_base(font, 640) + NEON_CSS.replace("%FONT%", font), font, body)


# -------------------------------------------------------------------------------------------------- stack
STACK_CSS = COMMON + """
  body { background: #fff4e0; }
  .bgpic { bottom: 50%; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 70%, #fff4e0 100%); }
  #main { top: 880px; }
  .hl { gap: 6px; }
  .hl div { color: #111; }
  .hl .w { padding: 2px 14px 8px; margin: 0 2px; }
  .hl div:nth-child(3n+1) .w:nth-child(odd) { background: #ff006e; color: #fff; }
  .hl div:nth-child(3n+2) .w:nth-child(even) { background: #3a86ff; color: #fff; }
  .hl div:nth-child(3n+3) .w:nth-child(odd) { background: #ffbe0b; color: #111; }
  .hl .hi { background: #111 !important; color: #ffbe0b !important; transform: rotate(-3deg); }
  .chips { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; }
  .chip { background: #fff; border: 5px solid #111; box-shadow: 6px 6px 0 #111; padding: 6px 20px 10px; display: flex; gap: 12px; align-items: center; }
  .chip .ic { width: 60px; height: 60px; }
  .chip small { display: block; font-size: 24px; font-weight: 800; color: #555; }
  .chip b { font-size: 42px; color: #ff006e; }
  .bul p { font-size: var(--pt); font-weight: 800; line-height: 1.3; color: #111; background: #fff; border: 4px solid #111; padding: 8px 16px; margin-bottom: 10px;
    box-shadow: 6px 6px 0 #3a86ff; }
  .bul .num { color: #ff006e; }
  .foot2 { color: #333; }
  .ask2 { border: 4px solid #111; box-shadow: 6px 6px 0 #111; border-radius: 0; }
"""


def stack_page(story, font, image_url, date, handle, place, asks):
    chips = "".join(f'<div class="chip">{icon_img(f["label"] + " " + f["value"])}<div><small>{esc(f["label"])}</small><b>{esc(f["value"])}</b></div></div>'
                    for f in story.facts[:2] if len(f["value"]) <= 14)
    bul = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    {_hl_words(story)}
    {f'<div class="chips">{chips}</div>' if chips else ""}
    {f'<div class="bul">{bul}</div>' if bul else ""}
    <div class="grow"></div>
    {_ask2(story, asks)}
  </div>{_foot(story, date, handle)}"""
    return _page(_base(font, 880) + STACK_CSS, font, body)


# --------------------------------------------------------------------------------------------------- card
CARD_CSS = COMMON + """
  body { background: #0b1d3a; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.25), transparent 30%, rgba(11,29,58,.4) 60%); }
  #main { top: 760px; }
  .sheet { background: #fff; border-radius: 40px; padding: 26px 26px 18px; box-shadow: 0 -10px 40px rgba(0,0,0,.4); display: flex; flex-direction: column; gap: 14px; }
  .sheet small { color: #e63946; font-size: 32px; font-weight: 800; }
  .sheet .hl { align-items: flex-start; gap: 0; }
  .sheet .hl div { color: #0b1d3a; text-align: left; padding: 0 0 6px; }
  .sheet .hl .hi { color: #e63946; }
  .sheet .sub { font-size: var(--pt); font-weight: 700; color: #457b9d; line-height: 1.3; }
  .ticks p { display: flex; gap: 14px; align-items: flex-start; font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #1d3557; padding: 6px 0; }
  .ticks p .ic { width: calc(var(--pt) * 1.2); height: calc(var(--pt) * 1.2); flex-shrink: 0; }
  .ticks .num { color: #e63946; }
"""


def card_page(story, font, image_url, date, handle, place, asks):
    ticks = "".join(f"<p>{icon_img('check')}<span>{highlight_numbers(p)}</span></p>" for p in _pts(story, 4))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="sheet"><small>📍 {esc(place or story.kicker or "")}</small>{_hl_words(story)}
      {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
      {f'<div class="ticks">{ticks}</div>' if ticks else ""}</div>
    <div class="grow"></div>
    {_ask2(story, asks)}
  </div>{_foot(story, date, handle)}"""
    return _page(_base(font, 760) + CARD_CSS, font, body)


# ------------------------------------------------------------------------------------------------- glitch
GLITCH_CSS = COMMON + """
  body { background: #000; }
  .bgpic { filter: saturate(1.3) contrast(1.1); }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0 3px, transparent 3px 6px),
    linear-gradient(180deg, transparent 35%, rgba(0,0,0,.88) 68%); }
  #main { top: 720px; }
  .scan { align-self: flex-start; font: 800 34px/1 'Courier New', monospace; color: #00ff9c; border: 2px solid #00ff9c; padding: 10px 16px;
    background: rgba(0,0,0,.6); }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { color: #fff; text-align: left; padding: 0 0 6px; text-shadow: 4px 0 0 rgba(255,0,80,.8), -4px 0 0 rgba(0,220,255,.8); }
  .hl .hi { color: #00ff9c; }
  .sub { font-size: var(--pt); font-weight: 700; color: #ddd; border-left: 6px solid #ff0050; padding-left: 14px; }
  .rows p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #fff; background: rgba(255,255,255,.08); border: 1px solid rgba(0,255,156,.5);
    padding: 10px 16px; margin-bottom: 10px; }
  .rows .num { color: #00ff9c; }
  .ask2 { background: #00ff9c; }
"""


def glitch_page(story, font, image_url, date, handle, place, asks):
    rows = "".join(f"<p>&gt; {highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="scan">[ {esc(place or story.kicker or "LIVE")} ]</div>
    {_hl_words(story)}
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="rows">{rows}</div>' if rows else ""}
    <div class="grow"></div>
    {_ask2(story, asks)}
  </div>{_foot(story, date, handle)}"""
    return _page(_base(font, 720) + GLITCH_CSS, font, body)


PATTERNS = {"brk": brk_page, "gold": gold_page, "neon": neon_page, "stack": stack_page, "card": card_page, "glitch": glitch_page}

S = IMG_ONLY
# image first, then the headline word by word, then the rest one element at a time (src/card.ANIM_JS format)
PATTERN_MOTION = {
    "brk": {"intro": [[".tag", "slideFarL", S, 0.35, 0], [".hl div", "growX", S + .3, 0.3, 0.25], [".hl .w", "slapIn", S + .5, 0.25, 0.1],
                      [".sub", "slideFarL", S + 2.0, 0.35, 0], [".box", "fadeIn", S + 2.4, 0.3, 0], [".box p", "slideFarL", S + 2.5, 0.35, 0.35],
                      [".ask2", "slapIn", S + 4.0, 0.35, 0], [".foot2, .handle", "fadeIn", S + 4.2, 0.4, 0]],
            "live": [[".bgpic", "kbZoom {end}s linear 0s both"], [".tag b", "blink 1s steps(1) {start}s infinite"]], "spot": None},
    "gold": {"intro": [[".pre", "inkIn", S, 0.6, 0], [".hl .w", "wordRise", S + .4, 0.55, 0.14], [".tagline", "fadeIn", S + 2.2, 0.6, 0],
                       [".chip", "popIn", S + 2.7, 0.35, 0.2], [".lines p", "fadeIn", S + 3.2, 0.5, 0.35],
                       [".ask2", "riseUp", S + 4.4, 0.4, 0], [".foot2, .handle", "fadeIn", S + 4.6, 0.4, 0]],
             "live": [[".bgpic", "kbZoom {end}s ease-out 0s both"]], "spot": None},
    "neon": {"intro": [[".sign", "flickerOn", S, 0.8, 0], [".hl .w", "flickerOn", S + .5, 0.7, 0.16], [".sub", "fadeIn", S + 2.3, 0.5, 0],
                       [".typed p", "typeIn", S + 2.7, 0.6, 0.5], [".ask2", "flickerOn", S + 4.4, 0.6, 0], [".foot2, .handle", "fadeIn", S + 4.6, 0.4, 0]],
             "live": [[".bgpic", "kbZoom {end}s linear 0s both"], [".sign", "flicker 3s linear {start}s infinite"]], "spot": None},
    "stack": {"intro": [[".hl .w", "dropBounce", S, 0.6, 0.15], [".chip", "slapIn", S + 2.2, 0.3, 0.2], [".bul p", "slideFarR", S + 2.8, 0.35, 0.3],
                        [".ask2", "slapIn", S + 4.2, 0.3, 0], [".foot2, .handle", "fadeIn", S + 4.4, 0.4, 0]],
              "live": [[".bgpic", "kbPan {end}s ease-in-out 0s both"]], "spot": None},
    "card": {"intro": [[".sheet", "riseFar", S, 0.6, 0], [".sheet small", "typeIn", S + .5, 0.4, 0], [".sheet .hl div", "typeIn", S + .8, 0.6, 0.45],
                       [".sheet .sub", "fadeIn", S + 2.4, 0.4, 0], [".ticks p", "tickIn", S + 2.8, 0.4, 0.35],
                       [".ask2", "riseUp", S + 4.3, 0.4, 0], [".foot2, .handle", "fadeIn", S + 4.5, 0.4, 0]],
             "live": [[".bgpic", "kbZoom {end}s linear 0s both"]], "spot": None},
    "glitch": {"intro": [[".scan", "typeIn", S, 0.5, 0], [".hl div", "glitch", S + .4, 0.45, 0.3], [".sub", "slideFarL", S + 1.9, 0.35, 0],
                         [".rows p", "glitch", S + 2.4, 0.4, 0.35], [".ask2", "glitch", S + 4.0, 0.4, 0], [".foot2, .handle", "fadeIn", S + 4.2, 0.4, 0]],
               "live": [[".bgpic", "kbZoom {end}s linear 0s both"]], "spot": None},
}

EXTRA_KEYFRAMES = """
@keyframes growX { from { transform: var(--t0, translate(0)) scaleX(0); transform-origin: left; } to { transform: var(--t0, translate(0)) scaleX(1); transform-origin: left; } }
@keyframes wordRise { from { transform: var(--t0, translate(0)) translateY(60px); filter: blur(10px); opacity: 0; }
  to { transform: var(--t0, translate(0)); filter: none; opacity: 1; } }
@keyframes tickIn { 0% { transform: var(--t0, translate(0)) translateX(-40px); opacity: 0; } 60% { transform: var(--t0, translate(0)) translateX(8px); opacity: 1; }
  100% { transform: var(--t0, translate(0)); } }
"""
