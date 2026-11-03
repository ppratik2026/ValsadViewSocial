"""Six layouts that break the usual poster skeleton (headline, picture, points box, question strip, footer):

  typo      typography only: the words fill the canvas in mixed sizes and weights, the picture only in a small circle
  fullbleed the picture is the poster: a short headline low on it, one line of detail, a small question sticker
  splitv    a tall picture strip on one side, the headline stacked word by word down the other side
  ring      a big round picture in the middle, the headline running around it on a circle
  cutout    every word of the headline cut out of a different paper and pasted at an angle, ransom-note style
  droste    the picture framed inside itself again and again, the headline on the innermost frame

No points box, no question strip and no footer bar: the source and handle are small, the question is a sticker.
"""
import html
import random

from src.designs import esc, highlight_numbers
from src.viral_more import SYM, _bg, _page, _pts
from src.viral_layouts import BASE, _ask

def _base(font, top=40):
    from src.designs import BRUSH_MASK
    return BASE % {"font": font, "mask": BRUSH_MASK, "top": top, "min_top": top}


def _words(story) -> list[str]:
    return story.headline.split()


def _is_hi(word: str, story) -> bool:
    return bool(story.highlight) and (word in story.highlight.split() or word in story.highlight)


MINI = """
  .mini { position: absolute; left: 40px; right: 40px; bottom: 34px; z-index: 8; display: flex; justify-content: space-between;
    font-size: 24px; font-weight: 700; opacity: .85; }
  .sticker { position: absolute; z-index: 8; background: #ffe14d; color: #111; font-size: 34px; font-weight: 800; padding: 14px 24px 18px;
    border-radius: 18px; transform: rotate(-4deg); box-shadow: 0 10px 20px rgba(0,0,0,.35); max-width: 640px; line-height: 1.25; }
  .sticker small { display: block; font-size: 24px; color: #b00000; }
"""


def _mini(story, handle, date, color="#fff"):
    return f'<div class="mini" style="color:{color}"><span>સ્રોત: {esc(story.source_name)}</span><span>{esc(handle)} • {esc(date)}</span></div>'


def _sticker(story, asks, style):
    return f'<div class="sticker" style="{style}">{_ask(story, asks)}<small>👇 કોમેન્ટ કરો</small></div>'


# ------------------------------------------------------------------------------------------------ typo
TYPO_CSS = MINI + """
  body { background: #f4f1ea; color: #111; }
  #main { left: 50px; right: 50px; top: 60px; bottom: 260px; gap: 0; justify-content: space-between; }
  .wall { display: flex; flex-wrap: wrap; align-content: flex-start; gap: 0 22px; line-height: .98; }
  .wall span { font-weight: 800; letter-spacing: -1px; }
  .wall .s1 { font-size: calc(var(--hl) * 1.21); } .wall .s2 { font-size: calc(var(--hl) * 0.89); } .wall .s3 { font-size: calc(var(--hl) * 0.68); font-weight: 500; }
  .wall .hi { color: #e63946; font-size: calc(var(--hl) * 1.53); }
  .wall .o { color: transparent; -webkit-text-stroke: 3px #111; }
  .rule { height: 12px; background: #111; margin: 26px 0; }
  .lower { display: grid; grid-template-columns: 300px 1fr; gap: 30px; align-items: center; }
  .dot { width: 300px; height: 300px; border-radius: 50%; background: #ccc center/cover no-repeat; filter: grayscale(1) contrast(1.2); }
  .lower p { font-size: var(--pt); font-weight: 600; line-height: 1.35; }
  .lower p + p { margin-top: 10px; }
  .lower .num { color: #e63946; font-weight: 800; }
  .kick { font-size: 34px; font-weight: 800; letter-spacing: 6px; color: #e63946; margin-bottom: 10px; }
"""


def typo_page(story, font, image_url, date, handle, place, asks):
    rnd = random.Random(story.headline)
    spans = []
    for w in _words(story):
        if _is_hi(w, story):
            spans.append(f'<span class="hi">{esc(w)}</span>')
        else:
            cls = rnd.choice(["s1", "s1", "s2", "s3"]) + (" o" if rnd.random() < .2 else "")
            spans.append(f'<span class="{cls}">{esc(w)}</span>')
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 2))
    body = f"""<div id="main">
    <div class="kick">{esc(place or story.kicker or "")}</div>
    <div class="wall">{"".join(spans)}</div>
    <div class="rule"></div>
    <div class="lower"><div class="dot"{_bg(image_url)}></div><div>{pts}</div></div>
  </div>
  {_sticker(story, asks, "right:50px;bottom:110px;")}{_mini(story, handle, date, "#111")}"""
    return _page(_base(font) + TYPO_CSS, font, body)


# ------------------------------------------------------------------------------------------- fullbleed
FULL_CSS = MINI + """
  body { background: #000; }
  .bgpic { position: absolute; inset: 0; background: #222 center/cover no-repeat; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.35) 0%, transparent 25%, transparent 45%, rgba(0,0,0,.92) 85%); }
  .sym { top: 30px; left: 30px; right: auto; }
  #main { left: 60px; right: 60px; top: auto; bottom: 120px; height: 900px; justify-content: flex-end; }
  .pill { align-self: flex-start; background: #e50914; color: #fff; font-size: 32px; font-weight: 800; padding: 6px 20px 10px; border-radius: 6px; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 6px; color: #fff; text-shadow: 0 6px 30px rgba(0,0,0,.8); }
  .hl .hi { color: #ffd60a; }
  .one { font-size: var(--pt); font-weight: 600; line-height: 1.35; color: #ddd; max-width: 900px; }
  .one .num { color: #ffd60a; }
  .meta { display: flex; gap: 22px; color: #bbb; font-size: 28px; font-weight: 700; }
  .meta b { color: #46d369; }
"""


def fullbleed_page(story, font, image_url, date, handle, place, asks):
    one = (_pts(story, 1) or [story.subheadline or ""])[0]
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}
  <div id="main">
    <div class="pill">{esc(place or story.kicker or "NEWS")}</div>
    <div class="hl">{"".join(f"<div>{d}</div>" for d in _split_hi(story, 3))}</div>
    {f'<div class="one">{highlight_numbers(one)}</div>' if one else ""}
    <div class="meta"><b>● LIVE</b><span>{esc(date)}</span><span>{esc(story.kicker or "")}</span></div>
  </div>
  {_sticker(story, asks, "right:40px;top:120px;transform:rotate(5deg)")}{_mini(story, handle, date)}"""
    return _page(_base(font) + FULL_CSS, font, body)


def _split_hi(story, n):
    from src.viral_layouts import _hi, _lines
    return [_hi(line, story.highlight) for line in _lines(story.headline, min(n, max(1, len(story.headline) // 14)))]


# ---------------------------------------------------------------------------------------------- splitv
SPLIT_CSS = MINI + """
  body { background: #0f172a; }
  .strip { position: absolute; left: 0; top: 0; bottom: 0; width: 430px; background: #333 center/cover no-repeat; }
  .strip::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent 70%, #0f172a); }
  .strip .sym { bottom: 120px; }
  .bar { position: absolute; left: 430px; top: 0; bottom: 0; width: 14px; background: #f97316; }
  #main { left: 480px; right: 40px; top: 70px; bottom: 120px; gap: 0; }
  .kick { color: #f97316; font-size: 32px; font-weight: 800; letter-spacing: 4px; margin-bottom: 16px; }
  .stack span { display: block; font-size: calc(var(--hl) * 0.84); font-weight: 800; line-height: 1.08; color: #fff; }
  .stack span:nth-child(3n+2) { color: #94a3b8; font-weight: 500; font-size: calc(var(--hl) * 0.73); }
  .stack .hi { color: #f97316 !important; font-size: calc(var(--hl) * 1.00) !important; font-weight: 800 !important; }
  .rule { width: 120px; height: 10px; background: #f97316; margin: 26px 0; }
  .pt2 p { font-size: var(--pt); font-weight: 600; line-height: 1.35; color: #cbd5e1; margin-bottom: 10px; }
  .pt2 .num { color: #f97316; font-weight: 800; }
"""


def splitv_page(story, font, image_url, date, handle, place, asks):
    stack = "".join(f'<span class="{"hi" if _is_hi(w, story) else ""}">{esc(w)}</span>' for w in _words(story))
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 2))
    body = f"""<div class="strip"{_bg(image_url)}>{SYM if image_url else ""}</div><div class="bar"></div>
  <div id="main">
    <div class="kick">{esc(place or story.kicker or "")}</div>
    <div class="stack fit">{stack}</div>
    <div class="rule"></div>
    <div class="pt2">{pts}</div>
  </div>
  {_sticker(story, asks, "left:40px;bottom:110px;transform:rotate(-3deg);max-width:360px;font-size:28px")}{_mini(story, handle, date)}"""
    return _page(_base(font) + SPLIT_CSS, font, body)


# ------------------------------------------------------------------------------------------------ ring
RING_CSS = MINI + """
  body { background: radial-gradient(circle at 50% 42%, #1d3557 0%, #0b132b 70%); }
  .ringsvg { position: absolute; left: 0; top: 160px; width: 1080px; height: 1080px; z-index: 2; }
  .disc { position: absolute; left: 240px; top: 400px; width: 600px; height: 600px; border-radius: 50%; background: #333 center/cover no-repeat;
    border: 14px solid #ffd166; box-shadow: 0 0 0 10px rgba(255,209,102,.25), 0 30px 60px rgba(0,0,0,.6); z-index: 1; }
  .kick { position: absolute; left: 0; right: 0; top: 70px; text-align: center; color: #ffd166; font-size: 40px; font-weight: 800; letter-spacing: 4px; }
  .under { position: absolute; left: 80px; right: 80px; top: 1290px; text-align: center; }
  .under p { font-size: 40px; font-weight: 600; line-height: 1.4; color: #e0e1dd; }
  .under .num { color: #ffd166; font-weight: 800; }
  #main { display: none; }
"""


def ring_page(story, font, image_url, date, handle, place, asks):
    text = story.headline + "  ✦  " + story.headline
    hi = esc(story.highlight) if story.highlight else ""
    t = esc(text)
    if hi:
        t = t.replace(hi, f'<tspan fill="#ffd166">{hi}</tspan>')
    svg = f"""<svg class="ringsvg" viewBox="0 0 1080 1080"><defs><path id="c" d="M540,540 m-400,0 a400,400 0 1,1 800,0 a400,400 0 1,1 -800,0"/></defs>
      <text font-family="{html.escape(font)}, Noto Sans Gujarati" font-weight="800" font-size="70" fill="#fff" letter-spacing="2">
      <textPath href="#c" startOffset="0" textLength="2480" lengthAdjust="spacingAndGlyphs">{t}</textPath></text></svg>"""
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 2))
    body = f"""<div class="kick">{esc(place or story.kicker or "")}</div><div class="disc"{_bg(image_url)}></div>{svg}
  <div class="under">{pts}</div><div id="main"></div>
  {_sticker(story, asks, "left:50%;bottom:110px;transform:translateX(-50%) rotate(-3deg)")}{_mini(story, handle, date)}"""
    return _page(_base(font) + RING_CSS, font, body)


# ---------------------------------------------------------------------------------------------- cutout
CUT_CSS = MINI + """
  body { background: #2b2d42; background-image: radial-gradient(rgba(255,255,255,.05) 2px, transparent 2px); background-size: 30px 30px; }
  #main { left: 40px; right: 40px; top: 60px; bottom: 120px; gap: 26px; }
  .collage { display: flex; flex-wrap: wrap; gap: 18px 14px; justify-content: center; align-content: flex-start; }
  .collage span { display: inline-block; padding: 6px 22px 14px; font-weight: 800; box-shadow: 0 8px 14px rgba(0,0,0,.45); line-height: 1.1; }
  .p1 { background: #fff; color: #111; font-size: calc(var(--hl) * 0.77); } .p2 { background: #ffd60a; color: #111; font-size: calc(var(--hl) * 0.89); }
  .p3 { background: #111; color: #fff; font-size: calc(var(--hl) * 0.71); } .p4 { background: #ef233c; color: #fff; font-size: calc(var(--hl) * 0.81); }
  .p5 { background: #8ecae6; color: #023047; font-size: calc(var(--hl) * 0.74); } .p6 { background: #f1faee; color: #e63946; font-size: calc(var(--hl) * 0.84); font-family: Georgia, serif; }
  .collage .hi { background: #ef233c; color: #ffd60a; font-size: calc(var(--hl) * 1.13); }
  .snap { position: relative; align-self: center; width: 80%; height: 520px; background: #ccc center/cover no-repeat; border: 16px solid #fff;
    transform: rotate(-3deg); box-shadow: 0 16px 30px rgba(0,0,0,.5); }
  .snap::before, .snap::after { content: ""; position: absolute; top: -26px; width: 180px; height: 52px; background: rgba(255,240,180,.85); }
  .snap::before { left: 30px; transform: rotate(-10deg); } .snap::after { right: 30px; transform: rotate(8deg); }
  .snap .sym { bottom: 6px; }
  .torn p { display: inline-block; font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #111; background: #fff; padding: 8px 16px; margin: 0 8px 10px 0;
    transform: rotate(-1deg); }
  .torn p:nth-child(even) { transform: rotate(1.5deg); background: #ffd60a; }
  .torn .num { color: #ef233c; }
"""


def cutout_page(story, font, image_url, date, handle, place, asks):
    rnd = random.Random(story.headline + "x")
    spans = []
    for w in _words(story):
        cls = "hi" if _is_hi(w, story) else rnd.choice(["p1", "p2", "p3", "p4", "p5", "p6"])
        spans.append(f'<span class="{cls}" style="transform:rotate({rnd.uniform(-6, 6):.1f}deg)">{esc(w)}</span>')
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 2))
    body = f"""<div id="main">
    <div class="collage fit">{"".join(spans)}</div>
    <div class="snap"{_bg(image_url)}>{SYM if image_url else ""}</div>
    <div class="torn">{pts}</div>
  </div>
  {_sticker(story, asks, "right:40px;bottom:110px;transform:rotate(4deg)")}{_mini(story, handle, date)}"""
    return _page(_base(font) + CUT_CSS, font, body)


# ---------------------------------------------------------------------------------------------- droste
DROSTE_CSS = MINI + """
  body { background: #111; }
  .f { position: absolute; background: #333 center/cover no-repeat; border: 10px solid #fff; box-shadow: 0 20px 50px rgba(0,0,0,.7); }
  .f1 { inset: 0; border: 0; filter: brightness(.45) saturate(1.2); }
  .f2 { left: 80px; right: 80px; top: 170px; bottom: 300px; transform: rotate(-3deg); filter: brightness(.65); }
  .f3 { left: 170px; right: 170px; top: 360px; bottom: 560px; transform: rotate(3deg); filter: brightness(.85); }
  .f4 { left: 250px; right: 250px; top: 540px; bottom: 820px; transform: rotate(-2deg); }
  .core { position: absolute; left: 60px; right: 60px; bottom: 300px; z-index: 5; }
  .core .hl div { background: #fff; color: #111; padding: 4px 30px 12px; box-shadow: 0 12px 24px rgba(0,0,0,.5); }
  .core .hl div:nth-child(even) { background: #ff006e; color: #fff; }
  .core .hl .hi { color: #ff006e; } .core .hl div:nth-child(even) .hi { color: #ffe14d; }
  .tag { position: absolute; left: 60px; top: 60px; z-index: 6; color: #fff; font-size: 40px; font-weight: 800; letter-spacing: 3px; }
  .one { position: absolute; left: 60px; right: 60px; bottom: 190px; z-index: 6; text-align: center; color: #fff; font-size: 36px; font-weight: 600; line-height: 1.35; }
  .one .num { color: #ffe14d; }
  #main { display: none; }
"""


def droste_page(story, font, image_url, date, handle, place, asks):
    from src.viral_more import _hl
    bg = _bg(image_url)
    one = (_pts(story, 1) or [story.subheadline or ""])[0]
    body = f"""<div class="f f1"{bg}></div><div class="f f2"{bg}></div><div class="f f3"{bg}></div><div class="f f4"{bg}></div>
  <div class="tag">↘ {esc(place or story.kicker or "")}</div>
  <div class="core"><div class="hl">{_hl(story)}</div></div>
  {f'<div class="one">{highlight_numbers(one)}</div>' if one else ""}<div id="main"></div>
  {_sticker(story, asks, "right:40px;top:40px;transform:rotate(5deg)")}{_mini(story, handle, date)}"""
    return _page(_base(font) + DROSTE_CSS, font, body)


BOLD_LAYOUTS = {"typo": typo_page, "fullbleed": fullbleed_page, "splitv": splitv_page, "ring": ring_page,
                "cutout": cutout_page, "droste": droste_page}
