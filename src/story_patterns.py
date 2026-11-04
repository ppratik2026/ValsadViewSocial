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


def _base(font, top=30, min_top=None):
    return BASE % {"font": font, "mask": BRUSH_MASK, "top": top, "min_top": top if min_top is None else min_top}


def _hl_words(story, n=None) -> str:
    """Headline in 2 full lines (3 when long), every word in its own span (.w) so the words can animate one by one.
    The highlight phrase is coloured as a whole (.hi), with no strip behind it."""
    n = n or (2 if len(story.headline) < 44 else 3)
    hi = set(story.highlight.split()) if story.highlight else set()
    out = []
    for line in _lines(story.headline, n):
        words = "".join(f'<span class="w{" hi" if w in hi else ""}">{esc(w)}</span> ' for w in line.split())
        out.append(f'<div>{words.strip()}</div>')
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


# shared look: the picture fills the whole poster (no frame, no border) and darkens towards the bottom, where the
# text sits straight on it: big 3D letters with outlines and shadows, no label behind every line
KIT = """
  body { color: #fff; background: #000; }
  .bgpic { position: absolute; inset: 0; background: #222 center 30%/cover no-repeat; filter: saturate(1.3) contrast(1.12) brightness(1.04); }
  .bgpic::after { content: ""; position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 25%, transparent 45%, rgba(0,0,0,.35) 100%),
      linear-gradient(180deg, rgba(0,0,0,.3) 0%, rgba(0,0,0,0) 12%, rgba(0,0,0,0) 34%, var(--shade1) 50%, var(--shade2) 66%, var(--shade2) 100%); }
  .sym { top: 24px; right: 24px; }
  #main { gap: 18px; justify-content: flex-end; }
  .w { display: inline-block; }
  .place { align-self: center; font-size: 36px; font-weight: 800; color: #fff; letter-spacing: 1px;
    text-shadow: 0 3px 0 #000, 0 0 18px rgba(0,0,0,.9); }
  .place b { color: var(--accent); }
  .hl { gap: 0; }
  .hl div { font-size: var(--hl); font-weight: 800; line-height: 1.24; padding: 10px 12px 2px; overflow: visible; }
  .hl .hi { color: var(--accent) !important; }
  .rule { align-self: center; width: 46%; height: 6px; border-radius: 6px; background: linear-gradient(90deg, transparent, var(--accent), transparent); }
  .sub { align-self: center; text-align: center; max-width: 96%; font-size: calc(var(--hl) * .48); font-weight: 800; line-height: 1.3;
    color: var(--subc); text-shadow: 0 3px 0 #000, 0 0 16px rgba(0,0,0,.95); }
  .sub .num { color: #fff; }
  .facts { display: flex; justify-content: center; gap: 22px; flex-wrap: wrap; }
  .fact { display: flex; align-items: center; gap: 14px; padding: 10px 26px 10px 14px; border-radius: 22px;
    background: rgba(255,255,255,.1); border: 2px solid rgba(255,255,255,.28); backdrop-filter: blur(8px); }
  .fact .ic { width: 76px; height: 76px; filter: drop-shadow(0 6px 8px rgba(0,0,0,.6)); }
  .fact small { display: block; font-size: 24px; font-weight: 700; line-height: 1.1; color: #ddd; }
  .fact b { display: block; font-size: 50px; font-weight: 800; line-height: 1.1; color: var(--accent); }
  .pts { display: flex; flex-direction: column; gap: 4px; padding: 18px 26px 18px 22px; border-radius: 26px;
    background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04)); border: 2px solid rgba(255,255,255,.2);
    border-left: 10px solid var(--accent); backdrop-filter: blur(10px); box-shadow: 0 18px 40px rgba(0,0,0,.45); }
  .pt { display: flex; gap: 16px; align-items: center; font-size: calc(var(--pt) * .92); font-weight: 600; line-height: 1.32; padding: 6px 0;
    color: #f2f2f2; }
  .pt + .pt { border-top: 1px dashed rgba(255,255,255,.22); }
  .pt .num { color: var(--accent); font-weight: 800; }
  .pt .ic { width: calc(var(--pt) * 1.3); height: calc(var(--pt) * 1.3); flex-shrink: 0; filter: drop-shadow(0 4px 6px rgba(0,0,0,.6)); }
  .foot { font-size: 24px; opacity: .85; }
"""


def _x3d_style(face: str, depth: str) -> str:
    return f"color: {face}; " + _x3d(depth, "#000")


def _poster(story, font, image_url, date, handle, place, asks, css: str, top_extra: str = "") -> str:
    """The shared composition: full picture, then (at the bottom) place, headline, sub line, facts, points, question."""
    facts = _facts(story)
    pts = _points(story, 3)
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}<div class="handle" style="top:22px;left:22px">{esc(handle)}</div>
  {top_extra}
  <div id="main">
    <div class="place">📍 <b>{esc(place or "")}</b>{" • " + esc(story.kicker) if place and story.kicker and place not in story.kicker else "" if place else esc(story.kicker or "")}</div>
    {_hl_words(story)}
    <div class="rule"></div>
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    {f'<div class="facts">{facts}</div>' if facts else ""}
    {f'<div class="pts">{pts}</div>' if pts else ""}
    {_ask_strip(story, asks)}
    {_foot(story, date, handle)}
  </div>"""
    # the text starts at 560 px; with a long story it may climb up to 240 px before any letter gets smaller
    return _page(_base(font, 560, 240) + (KIT + css).replace("%MASK%", BRUSH_MASK), font, body)


# crime / breaking: white and yellow letters with deep red 3D depth, the key word on a red brush stroke
BRK_CSS = """
  :root { --shade1: rgba(40,0,0,.6); --shade2: rgba(25,0,0,.94); --accent: #ffe600; --brush: #e10600; --subc: #ffb3a7; }
  .hl div { """ + _x3d_style("#fff", "#7a0000") + """ }
  .alarm { position: absolute; right: 30px; top: 110px; z-index: 5; font: 900 34px/1 Arial, sans-serif; color: #fff; letter-spacing: 2px;
    text-shadow: 0 0 12px #e10600, 0 0 24px #e10600; }
"""


def brk_page(story, font, image_url, date, handle, place, asks):
    return _poster(story, font, image_url, date, handle, place, asks, BRK_CSS, '<div class="alarm">🚨 BREAKING</div>')


# good news / events: gold letters with brown depth, warm light
GOLD_CSS = """
  :root { --shade1: rgba(40,20,0,.55); --shade2: rgba(30,12,40,.94); --accent: #ffd66b; --brush: #7b2ff7; --subc: #9ff0ff; }
  .hl div { """ + _x3d_style("#ffd66b", "#6b4300") + """ }
  .glow { position: absolute; left: 50%; top: 52%; width: 1400px; height: 1400px; margin: -700px 0 0 -700px; z-index: 1; opacity: .35;
    background: repeating-conic-gradient(rgba(255,214,107,.7) 0 4deg, transparent 4deg 14deg);
    -webkit-mask-image: radial-gradient(circle, #000 0%, transparent 60%); pointer-events: none; }
"""


def gold_page(story, font, image_url, date, handle, place, asks):
    return _poster(story, font, image_url, date, handle, place, asks, GOLD_CSS, '<div class="glow"></div>')


# weather / trending: glowing neon letters
NEON_CSS = """
  :root { --shade1: rgba(16,0,43,.55); --shade2: rgba(10,0,30,.95); --accent: #00f5d4; --brush: #ff4fd8; --subc: #ffd6ff; }
  .hl div { color: #fff; -webkit-text-stroke: 3px #002b27; paint-order: stroke fill;
    text-shadow: 0 0 8px #fff, 0 0 22px #00f5d4, 0 0 46px #00f5d4, 0 0 90px #00bbf9; }
"""


def neon_page(story, font, image_url, date, handle, place, asks):
    return _poster(story, font, image_url, date, handle, place, asks, NEON_CSS)


# money / prices: bold white letters with pink and blue 3D depth, yellow numbers
STACK_CSS = """
  :root { --shade1: rgba(20,0,40,.5); --shade2: rgba(15,0,35,.94); --accent: #ffd60a; --brush: #ff006e; --subc: #7df9ff; }
  .hl div { """ + _x3d_style("#fff", "#ff006e") + """ }
"""


def stack_page(story, font, image_url, date, handle, place, asks):
    return _poster(story, font, image_url, date, handle, place, asks, STACK_CSS)


# government / exams: white letters with navy depth, yellow key word, coloured icon circles for the points
CARD_CSS = """
  :root { --shade1: rgba(5,20,60,.55); --shade2: rgba(5,18,55,.95); --accent: #ffe600; --brush: #1d3fbf; --subc: #a8e6ff; }
  .hl div { """ + _x3d_style("#fff", "#0a1f5c") + """ }
  .pt .ic { background: radial-gradient(circle at 35% 30%, #ff6b6b, #c1121f); border-radius: 50%; padding: 10px; border: 3px solid #fff; }
  .pt:nth-child(3n+2) .ic { background: radial-gradient(circle at 35% 30%, #5ee27a, #138a36); }
  .pt:nth-child(3n+3) .ic { background: radial-gradient(circle at 35% 30%, #5b8cff, #1d3fbf); }
"""


def card_page(story, font, image_url, date, handle, place, asks):
    return _poster(story, font, image_url, date, handle, place, asks, CARD_CSS)


# politics / viral: white letters split into red and cyan, green accents
GLITCH_CSS = """
  :root { --shade1: rgba(0,15,8,.55); --shade2: rgba(0,10,5,.95); --accent: #00ff9c; --brush: #ff0050; --subc: #ffe066; }
  .hl div { color: #fff; -webkit-text-stroke: 3px #000; paint-order: stroke fill;
    text-shadow: 6px 0 0 rgba(255,0,80,.9), -6px 0 0 rgba(0,220,255,.9), 0 10px 16px rgba(0,0,0,.7); }
"""


def glitch_page(story, font, image_url, date, handle, place, asks):
    return _poster(story, font, image_url, date, handle, place, asks, GLITCH_CSS)


def _with_hero(page):
    """The picture alone (no darkening, no text) first; it fades into the poster as the text starts."""
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
_REST = [[".rule", "growX", S + 1.8, 0.4, 0], [".sub", "fadeIn", S + 2.0, 0.45, 0], [".pts", "fadeIn", S + 2.6, 0.3, 0], [".fact", "popIn", S + 2.4, 0.35, 0.2],
         [".pt", "slideFarL", S + 2.8, 0.35, 0.35], [".v-ask", "riseUp", S + 4.3, 0.4, 0], [".foot, .handle", "fadeIn", S + 4.5, 0.4, 0]]
_LIVE = [[".bgpic", "kbZoom {end}s linear 0s both"]]
# image first, then the headline word by word, then the rest one element at a time (src/card.ANIM_JS format)
PATTERN_MOTION = {
    "brk": {"intro": [_HERO, [".alarm", "flickerOn", S, 0.5, 0], [".place", "slideFarL", S + .1, 0.35, 0],
                      [".hl .w", "slapIn", S + .4, 0.25, 0.1]] + _REST,
            "live": _LIVE + [[".alarm", "blink 1s steps(1) {start}s infinite"]], "spot": None},
    "gold": {"intro": [_HERO, [".glow", "fadeIn", S, 0.8, 0], [".place", "fadeIn", S + .1, 0.5, 0],
                       [".hl .w", "wordRise", S + .4, 0.55, 0.13]] + _REST,
             "live": _LIVE + [[".glow", "spinRays {end}s linear 0s both"]], "spot": None},
    "neon": {"intro": [_HERO, [".place", "flickerOn", S, 0.6, 0], [".hl .w", "flickerOn", S + .3, 0.7, 0.14]] + _REST,
             "live": _LIVE, "spot": None},
    "stack": {"intro": [_HERO, [".place", "slapIn", S, 0.3, 0], [".hl .w", "dropIn", S + .2, 0.45, 0.13]] + _REST,
              "live": _LIVE, "spot": None},
    "card": {"intro": [_HERO, [".place", "slideFarL", S, 0.35, 0], [".hl div", "typeIn", S + .3, 0.55, 0.4]] + _REST,
             "live": _LIVE + [[".pt .ic", "wobble 1.6s ease-in-out {start}s infinite"]], "spot": None},
    "glitch": {"intro": [_HERO, [".place", "typeIn", S, 0.5, 0], [".hl div", "glitch", S + .4, 0.45, 0.3]] + _REST,
               "live": _LIVE, "spot": None},
}

EXTRA_KEYFRAMES = """
@keyframes heroOut { 0% { opacity: 1; transform: scale(1.06); } 100% { opacity: 0; transform: scale(1.2); } }
@keyframes growX { from { transform: var(--t0, translate(0)) scaleX(0); transform-origin: left; } to { transform: var(--t0, translate(0)) scaleX(1); transform-origin: left; } }
@keyframes wordRise { from { transform: var(--t0, translate(0)) translateY(60px); filter: blur(10px); opacity: 0; }
  to { transform: var(--t0, translate(0)); filter: none; opacity: 1; } }
@keyframes tickIn { 0% { transform: var(--t0, translate(0)) translateX(-40px); opacity: 0; } 60% { transform: var(--t0, translate(0)) translateX(8px); opacity: 1; }
  100% { transform: var(--t0, translate(0)); } }
"""
