"""Fifteen posters with fifteen different structures (not just other colours): where the picture sits, how the
headline is set, how the facts and points are laid out all change from one layout to the next.

  diagonal  picture cut on a slant, red block below, left-aligned headline
  tv        news channel screen: LIVE logo, BREAKING tab, white headline bar, blue sub bar, ticker
  paper     newspaper front page: masthead, black headline, photo with caption, two columns
  bignum    one giant number filled with the picture, headline above, chips below
  polaroid  instant photo taped on a board, lined-paper note, sticky note with the number
  circle    round picture with glowing rings, centred text, 2x2 point tiles
  magazine  magazine cover: masthead over the picture, cover lines on the left, round price sticker
  sidebar   coloured side band with the place written upwards, picture and numbered points on the right
  quote     a big quotation: giant quote mark, headline as the quote, sub as the attribution
  steps     light page, picture on top, points on a numbered timeline
  bento     a grid of rounded tiles: picture, number, place and date, headline, points
  hazard    yellow warning page with black-yellow stripes, warning sign, picture as a wide band
  film      film strip with sprocket holes around the picture, movie-title headline, points as credits
  dossier   case file: folder, typed sheet, clipped photo, red stamp, form fields
  tape      picture crossed by two "police line" tapes, headline below

All of them keep the src/viral.FIT contract (#main, .hl div lines, --hl, --pt, --ask, --top, --min-top).
"""
import re

from src.designs import esc, highlight_numbers
from src.icons import icon_img
from src.story_patterns import _base
from src.viral_layouts import _ask, _hi, _lines
from src.viral_layouts import _page
from src.viral_more import _pts


def _hl(story, n=None, cls="hl") -> str:
    n = n or (2 if len(story.headline) < 44 else 3)
    return f'<div class="{cls}">' + "".join(f"<div>{_hi(l, story.highlight)}</div>" for l in _lines(story.headline, n)) + "</div>"


def _sub(story, cls="sub") -> str:
    return f'<div class="{cls}">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""


def _num(story):
    """The fact with the most striking number (for the giant number / stickers), or None."""
    for f in story.facts:
        if re.search(r"\d", f["value"]) and len(f["value"]) <= 10:
            return f
    return story.facts[0] if story.facts else None


def _askx(story, asks, icon="💬") -> str:
    return f'<div class="askx"><span class="qi">{icon}</span><span class="qt">{_ask(story, asks)}</span></div>'


def _pic(url):
    return f"background-image:url({url})" if url else "background:linear-gradient(135deg,#334,#112)"


def _pts_html(story, n=4, icons=True, cls="pt") -> str:
    return "".join(f'<div class="{cls}">{icon_img(p) if icons else ""}<span>{highlight_numbers(p)}</span></div>'
                   for p in _pts(story, n))


def _wrap(css, font, body, top, min_top):
    return _page(_base(font, top, min_top) + COMMON + css, font, body)


COMMON = """
  .hl div { padding: 2px 6px 6px; }
  .hl .hi { font-size: 1em; }
  .askx { display: flex; align-items: center; gap: 16px; font-size: var(--ask); font-weight: 800; line-height: 1.25; }
  .askx .qi { flex-shrink: 0; }
  .num { font-weight: 800; }
  .sym { position: absolute; z-index: 7; background: rgba(0,0,0,.55); color: #fff; font-size: 22px; font-weight: 700;
    padding: 4px 14px; border-radius: 12px; }
"""


# 1 ---------------------------------------------------------------------------------------- diagonal
DIAGONAL = """
  body { background: #a30015; }
  .pic { position: absolute; left: 0; right: 0; top: 0; height: 1120px; background: center/cover no-repeat;
    clip-path: polygon(0 0, 100% 0, 100% 78%, 0 100%); z-index: 1; }
  .edge { position: absolute; left: 0; right: 0; top: 0; height: 1140px; background: #ffd60a; z-index: 0;
    clip-path: polygon(0 80%, 100% 78%, 100% 80%, 0 102%); }
  .place { position: absolute; top: 40px; left: 0; z-index: 3; background: #ffd60a; color: #111; font-size: 40px; font-weight: 800;
    padding: 8px 30px 12px 40px; border-radius: 0 40px 40px 0; }
  .sym { right: 20px; top: 40px; }
  #main { left: 50px; right: 50px; gap: 20px; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; font-size: calc(var(--hl) * .92); color: #fff; padding-left: 0; text-shadow: 0 6px 0 #5c000b; }
  .hl .hi { color: #ffd60a; }
  .sub { font-size: calc(var(--hl) * .42); font-weight: 700; color: #ffd0d6; line-height: 1.3; border-left: 8px solid #ffd60a; padding-left: 20px; }
  .pt { display: flex; gap: 16px; align-items: center; font-size: var(--pt); font-weight: 600; color: #fff; line-height: 1.3; }
  .pt .ic { width: calc(var(--pt) * 1.3); height: calc(var(--pt) * 1.3); }
  .grow { flex: 1; }
  .askx { color: #ffd60a; border-top: 3px dashed rgba(255,255,255,.4); padding-top: 18px; }
  .handle2 { font-size: 26px; color: rgba(255,255,255,.8); font-weight: 700; display: flex; justify-content: space-between; }
"""


def diagonal(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="edge"></div><div class="pic" style="{_pic(image_url)}"></div>
  <div class="place">📍 {esc(place or story.kicker)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main">{_hl(story)}{_sub(story)}<div class="pts">{_pts_html(story, 3)}</div><div class="grow"></div>
  {_askx(story, asks, "👉")}<div class="handle2"><span>{esc(handle)}</span><span>{esc(date)} • {esc(story.source_name)}</span></div></div>"""
    return _wrap(DIAGONAL, font, body, 1000, 780)


# 2 ---------------------------------------------------------------------------------------------- tv
TV = """
  body { background: #000; }
  .pic { position: absolute; inset: 0; background: center/cover no-repeat; }
  .pic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(0,0,0,.85) 75%); }
  .logo { position: absolute; top: 36px; left: 36px; z-index: 5; display: flex; align-items: center; gap: 0; }
  .logo b { background: #d00000; color: #fff; font-size: 34px; padding: 10px 20px 14px; border-radius: 10px 0 0 10px; }
  .logo span { background: #fff; color: #d00000; font: 900 30px/1 Arial; padding: 17px 18px; border-radius: 0 10px 10px 0; }
  .sym { right: 30px; top: 40px; }
  #main { left: 0; right: 0; gap: 0; bottom: 0; }
  .tab { align-self: flex-start; background: #d00000; color: #fff; font: 900 38px/1 Arial; letter-spacing: 2px; padding: 16px 30px; margin-left: 36px;
    display: flex; gap: 14px; align-items: center; }
  .tab small { font-family: inherit; font-size: 32px; letter-spacing: 0; background: #ffd60a; color: #111; padding: 2px 14px 6px; }
  .hl { background: #fff; align-items: flex-start; padding: 14px 36px 10px; margin: 0 36px; border-left: 14px solid #d00000; }
  .hl div { text-align: left; color: #0a0a0a; font-size: calc(var(--hl) * .8); padding: 0 0 4px; }
  .hl .hi { color: #d00000; }
  .sub { background: #0039a6; color: #fff; font-size: calc(var(--hl) * .38); font-weight: 700; padding: 12px 36px 16px; margin: 0 36px; line-height: 1.3; }
  .pts { margin: 24px 36px 0; display: flex; flex-direction: column; gap: 10px; }
  .pt { display: flex; gap: 14px; align-items: center; color: #fff; font-size: var(--pt); font-weight: 600; line-height: 1.3; }
  .pt::before { content: "▶"; color: #ffd60a; font-size: .7em; }
  .grow { flex: 1; }
  .ticker { display: flex; background: #ffd60a; color: #111; margin-top: 26px; }
  .ticker .when { background: #111; color: #ffd60a; font: 900 30px/1 Arial; padding: 26px 20px; flex-shrink: 0; }
  .askx { padding: 14px 24px 18px; }
"""


def tv(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="pic" style="{_pic(image_url)}"></div>
  <div class="logo"><b>{esc(handle)}</b><span>● LIVE</span></div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main"><div class="tab">BREAKING NEWS <small>{esc(place or story.kicker)}</small></div>{_hl(story)}{_sub(story)}
  <div class="pts">{_pts_html(story, 3, icons=False)}</div><div class="grow"></div>
  <div class="ticker"><div class="when">{esc(date)}</div>{_askx(story, asks, "🗣️")}</div></div>"""
    return _wrap(TV, font, body, 1080, 820)


# 3 ------------------------------------------------------------------------------------------- paper
PAPER = """
  body { background: #f3eee2; color: #151515; }
  body::before { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.02) 0 2px, transparent 2px 6px); }
  #main { left: 44px; right: 44px; gap: 16px; }
  .mast { text-align: center; font-size: 104px; font-weight: 800; line-height: 1; letter-spacing: 2px; padding-top: 10px; }
  .dateline { display: flex; justify-content: space-between; border-top: 4px solid #151515; border-bottom: 1.5px solid #151515;
    padding: 8px 4px 10px; font-size: 26px; font-weight: 700; }
  .hl div { color: #111; font-size: calc(var(--hl) * .86); padding: 0; }
  .hl .hi { color: #b5001b; }
  .photo { height: 560px; background: center/cover no-repeat; flex-shrink: 0; position: relative; filter: saturate(1.1); }
  .photo .sym { right: 12px; bottom: 12px; }
  .cap { font-size: calc(var(--pt) * .9); font-style: italic; color: #333; border-bottom: 1.5px solid #151515; padding-bottom: 10px; line-height: 1.3; }
  .sub { font-size: calc(var(--hl) * .4); font-weight: 800; color: #b5001b; line-height: 1.3; }
  .cols { column-count: 2; column-gap: 36px; column-rule: 1.5px solid #151515; font-size: var(--pt); line-height: 1.38; font-weight: 600; }
  .cols p { break-inside: avoid; margin-bottom: 10px; }
  .grow { flex: 1; }
  .askx { border: 3px solid #151515; padding: 14px 22px 18px; background: #fff; }
  .askx .qi { background: #151515; color: #f3eee2; font-size: 26px; padding: 6px 14px 10px; }
"""


def paper(story, font, image_url, date, handle, place, asks):
    cols = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 4))
    body = f"""<div id="main"><div class="mast">વલસાડ વ્યૂ</div>
  <div class="dateline"><span>{esc(date)}</span><span>📍 {esc(place or story.kicker)}</span><span>{esc(handle)}</span></div>
  {_hl(story)}{_sub(story)}<div class="photo" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div>
  <div class="cap">સ્રોત: {esc(story.source_name)}</div><div class="cols">{cols}</div><div class="grow"></div>
  {_askx(story, asks, "વાચકોનો સવાલ")}</div>"""
    return _wrap(PAPER, font, body, 24, 24)


# 4 ------------------------------------------------------------------------------------------ bignum
BIGNUM = """
  body { background: #0b0b14; }
  .blur { position: absolute; inset: -40px; background: center/cover no-repeat; filter: blur(30px) brightness(.4) saturate(1.4); }
  #main { left: 50px; right: 50px; gap: 22px; align-items: center; justify-content: center; }
  .place { font-size: 36px; font-weight: 800; color: #0b0b14; background: #00e0b8; padding: 6px 26px 10px; border-radius: 40px; }
  .hl div { font-size: calc(var(--hl) * .72); color: #fff; }
  .hl .hi { color: #00e0b8; }
  .big { font: 900 300px/1 'Arial Black', Arial, sans-serif; letter-spacing: -6px; background: center/cover no-repeat;
    -webkit-background-clip: text; background-clip: text; color: transparent; -webkit-text-stroke: 5px #fff; white-space: nowrap;
    filter: drop-shadow(0 20px 30px rgba(0,224,184,.35)); padding: 0 10px; }
  .biglabel { font-size: calc(var(--pt) * 1.1); font-weight: 800; color: #00e0b8; margin-top: -10px; }
  .sub { text-align: center; font-size: calc(var(--hl) * .38); font-weight: 700; color: #ffe8a3; line-height: 1.3; }
  .chips { display: flex; flex-wrap: wrap; gap: 14px; justify-content: center; }
  .chip { background: rgba(255,255,255,.08); border: 2px solid rgba(255,255,255,.22); color: #fff; font-size: calc(var(--pt) * .85);
    font-weight: 600; padding: 10px 22px 14px; border-radius: 40px; line-height: 1.25; }
  .askx { color: #fff; background: linear-gradient(90deg, #00b894, #0984e3); padding: 16px 30px 20px; border-radius: 60px; }
  .foot2 { font-size: 24px; color: rgba(255,255,255,.6); }
"""


def bignum(story, font, image_url, date, handle, place, asks):
    f = _num(story)
    value, label = (f["value"], f["label"]) if f else (story.highlight or "", "")
    size = 300 if len(value) <= 5 else 220 if len(value) <= 7 else 160
    chips = "".join(f'<div class="chip">{highlight_numbers(p)}</div>' for p in _pts(story, 3))
    body = f"""<div class="blur" style="{_pic(image_url)}"></div>
  <div id="main"><div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}
  <div class="big" style="font-size:{size}px;{_pic(image_url)}">{esc(value)}</div><div class="biglabel">{esc(label)}</div>
  {_sub(story)}<div class="chips">{chips}</div>{_askx(story, asks, "💬")}
  <div class="foot2">{esc(handle)} • {esc(date)} • સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(BIGNUM, font, body, 60, 30)


# 5 ---------------------------------------------------------------------------------------- polaroid
POLAROID = """
  body { background: #2f6f73; background-image: radial-gradient(rgba(255,255,255,.08) 2px, transparent 2px); background-size: 26px 26px; }
  .pola { position: absolute; left: 110px; top: 70px; width: 860px; background: #fff; padding: 30px 30px 100px; transform: rotate(-3deg);
    box-shadow: 0 30px 50px rgba(0,0,0,.45); z-index: 2; }
  .pola .ph { height: 640px; background: center/cover no-repeat; position: relative; }
  .pola .ph .sym { right: 10px; top: 10px; }
  .pola .cap { position: absolute; bottom: 24px; left: 0; right: 0; text-align: center; font-size: 46px; font-weight: 700; color: #1d3557; }
  .tape { position: absolute; width: 230px; height: 64px; background: rgba(255,230,140,.85); z-index: 3; }
  .t1 { left: 70px; top: 60px; transform: rotate(-35deg); } .t2 { right: 70px; top: 50px; transform: rotate(30deg); }
  .sticky { position: absolute; right: 50px; top: 760px; z-index: 4; width: 280px; background: #ffd60a; color: #111; padding: 20px 20px 26px;
    transform: rotate(6deg); box-shadow: 0 16px 24px rgba(0,0,0,.35); text-align: center; }
  .sticky b { display: block; font-size: 64px; line-height: 1.1; } .sticky small { font-size: 26px; font-weight: 700; }
  #main { left: 50px; right: 50px; gap: 14px; background: #fffdf5; padding: 34px 40px 30px; transform: rotate(1deg);
    background-image: repeating-linear-gradient(180deg, transparent 0 62px, #c9dcef 62px 64px); box-shadow: 0 24px 40px rgba(0,0,0,.35);
    bottom: 40px; border-left: 6px solid #e63946; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #1b1b1b; font-size: calc(var(--hl) * .78); padding: 0; }
  .hl .hi { color: #e63946; }
  .sub { font-size: calc(var(--hl) * .38); color: #1d4ed8; font-weight: 700; line-height: 1.3; }
  .pt { display: flex; gap: 14px; color: #222; font-size: var(--pt); font-weight: 600; line-height: 1.32; }
  .pt::before { content: "✔"; color: #2a9d8f; font-weight: 900; }
  .grow { flex: 1; }
  .askx { color: #e63946; }
  .foot2 { font-size: 24px; color: #555; }
"""


def polaroid(story, font, image_url, date, handle, place, asks):
    f = _num(story)
    sticky = f'<div class="sticky"><b>{esc(f["value"])}</b><small>{esc(f["label"])}</small></div>' if f else ""
    body = f"""<div class="pola"><div class="ph" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div>
  <div class="cap">📍 {esc(place or story.kicker)}</div></div><div class="tape t1"></div><div class="tape t2"></div>{sticky}
  <div id="main">{_hl(story)}{_sub(story)}{_pts_html(story, 3, icons=False)}<div class="grow"></div>{_askx(story, asks, "✍️")}
  <div class="foot2">{esc(handle)} • {esc(date)} • {esc(story.source_name)}</div></div>"""
    return _wrap(POLAROID, font, body, 1000, 900)


# 6 ------------------------------------------------------------------------------------------ circle
CIRCLE = """
  body { background: radial-gradient(circle at 50% 22%, #2b2d8f 0%, #10113a 55%, #070720 100%); }
  .rings { position: absolute; left: 50%; top: 380px; width: 1000px; height: 1000px; margin: -500px 0 0 -500px; border-radius: 50%;
    background: repeating-radial-gradient(circle, transparent 0 60px, rgba(255,255,255,.06) 60px 62px); }
  .disc { position: absolute; left: 50%; top: 380px; width: 620px; height: 620px; margin: -310px 0 0 -310px; border-radius: 50%;
    background: center/cover no-repeat; box-shadow: 0 0 0 14px #ff9f1c, 0 0 0 30px rgba(255,159,28,.25), 0 0 120px rgba(255,159,28,.6); z-index: 2; }
  .badge { position: absolute; left: 50%; top: 610px; transform: translateX(150px) rotate(8deg); z-index: 3; background: #ff9f1c; color: #10113a;
    width: 230px; height: 230px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center; border: 8px solid #fff; }
  .badge b { font-size: 50px; line-height: 1.05; } .badge small { font-size: 22px; font-weight: 800; padding: 0 16px; line-height: 1.1; }
  .handle { top: 30px; left: 30px; }
  .sym { right: 30px; top: 30px; }
  #main { left: 50px; right: 50px; gap: 20px; align-items: center; }
  .place { font-size: 36px; font-weight: 800; color: #ff9f1c; letter-spacing: 1px; }
  .hl div { color: #fff; font-size: calc(var(--hl) * .8); }
  .hl .hi { color: #ff9f1c; }
  .sub { text-align: center; font-size: calc(var(--hl) * .38); color: #a5b4fc; font-weight: 700; line-height: 1.3; }
  .tiles { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; width: 100%; }
  .tile { background: rgba(255,255,255,.08); border-radius: 26px; padding: 18px 20px; display: flex; gap: 14px; align-items: center;
    color: #fff; font-size: calc(var(--pt) * .85); font-weight: 600; line-height: 1.28; border-top: 4px solid #ff9f1c; }
  .tile .ic { width: 64px; height: 64px; flex-shrink: 0; }
  .grow { flex: 1; }
  .askx { color: #10113a; background: #fff; padding: 14px 30px 18px; border-radius: 22px; }
"""


def circle(story, font, image_url, date, handle, place, asks):
    f = _num(story)
    badge = f'<div class="badge"><b>{esc(f["value"])}</b><small>{esc(f["label"])}</small></div>' if f else ""
    tiles = "".join(f'<div class="tile">{icon_img(p)}<span>{highlight_numbers(p)}</span></div>' for p in _pts(story, 4))
    body = f"""<div class="rings"></div><div class="disc" style="{_pic(image_url)}"></div>{badge}
  <div class="handle">{esc(handle)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main"><div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}<div class="tiles">{tiles}</div>
  <div class="grow"></div>{_askx(story, asks, "🤔")}</div>"""
    return _wrap(CIRCLE, font, body, 760, 700)


# 7 ---------------------------------------------------------------------------------------- magazine
MAGAZINE = """
  body { background: #000; }
  .pic { position: absolute; inset: 0; background: center/cover no-repeat; }
  .pic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.75) 0%, rgba(0,0,0,.2) 60%, transparent),
    linear-gradient(180deg, rgba(0,0,0,.45) 0%, transparent 25%, transparent 50%, rgba(0,0,0,.85) 100%); }
  .mast { position: absolute; top: 20px; left: 0; right: 0; text-align: center; z-index: 3; font: 900 168px/1 'Arial Black', Arial, sans-serif;
    color: #fff; letter-spacing: -4px; mix-blend-mode: normal; }
  .mast + .tag { position: absolute; top: 190px; left: 0; right: 0; text-align: center; z-index: 3; color: #ffd60a; font-size: 32px;
    font-weight: 800; letter-spacing: 4px; }
  .issue { position: absolute; top: 250px; left: 40px; z-index: 3; color: #fff; font-size: 26px; font-weight: 700; }
  .sticker { position: absolute; right: 40px; top: 300px; z-index: 4; width: 280px; height: 280px; border-radius: 50%; background: #ffd60a;
    color: #c1121f; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; transform: rotate(-10deg);
    box-shadow: 0 12px 30px rgba(0,0,0,.5); }
  .sticker b { font-size: 64px; line-height: 1; } .sticker small { font-size: 24px; color: #111; font-weight: 800; padding: 6px 20px 0; line-height: 1.1; }
  .sym { left: 40px; top: 300px; }
  #main { left: 40px; right: 120px; gap: 16px; }
  .lines { display: flex; flex-direction: column; gap: 12px; margin-bottom: 14px; }
  .line { color: #fff; font-size: calc(var(--pt) * .9); font-weight: 700; line-height: 1.25; border-left: 6px solid #ffd60a; padding-left: 16px; max-width: 640px; }
  .place { color: #ffd60a; font-size: 34px; font-weight: 800; letter-spacing: 2px; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #fff; font-size: calc(var(--hl) * .95); padding: 0; line-height: 1.12; }
  .hl .hi { color: #ffd60a; }
  .sub { font-size: calc(var(--hl) * .36); color: #ffb4a2; font-weight: 700; line-height: 1.3; }
  .askx { color: #fff; font-size: calc(var(--ask) * .9); }
  .askx .qi { background: #c1121f; padding: 4px 14px 8px; border-radius: 8px; font-size: 26px; }
"""


def magazine(story, font, image_url, date, handle, place, asks):
    f = _num(story)
    sticker = f'<div class="sticker"><b>{esc(f["value"])}</b><small>{esc(f["label"])}</small></div>' if f else ""
    lines = "".join(f'<div class="line">{highlight_numbers(p)}</div>' for p in _pts(story, 3))
    body = f"""<div class="pic" style="{_pic(image_url)}"></div><div class="mast">VALSAD</div><div class="tag">VIEW • {esc(handle)}</div>
  <div class="issue">{esc(date)}</div>{sticker}
  <div id="main"><div class="lines">{lines}</div><div class="place">{esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}
  {_askx(story, asks, "તમારો મત")}</div>"""
    return _wrap(MAGAZINE, font, body, 980, 760)


# 8 ----------------------------------------------------------------------------------------- sidebar
SIDEBAR = """
  body { background: #fff; color: #111; }
  .band { position: absolute; left: 0; top: 0; bottom: 0; width: 200px; background: #e63946; z-index: 1; }
  .band .v { position: absolute; left: 50%; bottom: 60px; transform: translateX(-50%) rotate(180deg); writing-mode: vertical-rl;
    font-size: 150px; font-weight: 800; color: #fff; line-height: 1; white-space: nowrap; }
  .band .d { position: absolute; top: 40px; left: 0; right: 0; text-align: center; color: #fff; font-size: 26px; font-weight: 800; line-height: 1.2; }
  .pic { position: absolute; left: 200px; right: 0; top: 0; height: 820px; background: center/cover no-repeat; }
  .sym { right: 20px; top: 20px; }
  .handle { position: absolute; left: 230px; top: 760px; z-index: 3; background: #111; color: #fff; font-size: 28px; font-weight: 800;
    padding: 8px 24px 12px; }
  #main { left: 240px; right: 40px; gap: 18px; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #111; font-size: calc(var(--hl) * .8); padding: 0; }
  .hl .hi { color: #e63946; }
  .sub { font-size: calc(var(--hl) * .37); color: #1d3557; font-weight: 700; line-height: 1.3; }
  .np { display: flex; gap: 18px; align-items: flex-start; font-size: var(--pt); font-weight: 600; line-height: 1.3; color: #222; }
  .np b { font: 900 calc(var(--pt) * 1.5)/1 'Arial Black', Arial, sans-serif; color: #e63946; flex-shrink: 0; min-width: 1.6em; }
  .grow { flex: 1; }
  .askx { background: #1d3557; color: #fff; padding: 16px 26px 20px; }
  .foot2 { font-size: 22px; color: #666; }
"""


def sidebar(story, font, image_url, date, handle, place, asks):
    pts = "".join(f'<div class="np"><b>{i:02d}</b><span>{highlight_numbers(p)}</span></div>' for i, p in enumerate(_pts(story, 3), 1))
    body = f"""<div class="band"><div class="d">{esc(date)}</div><div class="v">{esc((place or story.kicker).split(" - ")[0])}</div></div>
  <div class="pic" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div><div class="handle">{esc(handle)}</div>
  <div id="main">{_hl(story)}{_sub(story)}{pts}<div class="grow"></div>{_askx(story, asks, "❓")}
  <div class="foot2">સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(SIDEBAR, font, body, 870, 840)


# 9 ------------------------------------------------------------------------------------------- quote
QUOTE = """
  body { background: #120c06; }
  .pic { position: absolute; inset: 0; background: center/cover no-repeat; filter: brightness(.35) sepia(.4) saturate(1.3); }
  .handle { top: 30px; left: 30px; }
  .sym { right: 30px; top: 30px; }
  .mark { position: absolute; left: 50px; top: 250px; font: 900 520px/1 Georgia, serif; color: #f4a261; opacity: .9; z-index: 2; }
  #main { left: 70px; right: 70px; gap: 26px; justify-content: center; }
  .place { color: #f4a261; font-size: 34px; font-weight: 800; letter-spacing: 3px; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #fff; font-size: calc(var(--hl) * .82); padding: 0; font-style: italic; }
  .hl .hi { color: #f4a261; }
  .sub { font-size: calc(var(--hl) * .38); color: #f4a261; font-weight: 700; line-height: 1.3; }
  .sub::before { content: "— "; }
  .line { height: 3px; background: linear-gradient(90deg, #f4a261, transparent); }
  .pt { display: flex; gap: 14px; font-size: calc(var(--pt) * .9); color: #e9dccb; font-weight: 500; line-height: 1.35; }
  .pt::before { content: "•"; color: #f4a261; }
  .askx { color: #120c06; background: #f4a261; padding: 16px 28px 20px; border-radius: 0 40px 40px 0; margin-left: -70px; padding-left: 70px; }
  .foot2 { font-size: 24px; color: rgba(255,255,255,.55); }
"""


def quote(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="pic" style="{_pic(image_url)}"></div><div class="handle">{esc(handle)}</div>
  <div class="sym">પ્રતિકાત્મક તસવીર</div><div class="mark">“</div>
  <div id="main"><div class="place">{esc(place or story.kicker)}</div>{_hl(story, 3)}{_sub(story)}<div class="line"></div>
  {_pts_html(story, 3, icons=False)}{_askx(story, asks, "🗨️")}<div class="foot2">{esc(date)} • સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(QUOTE, font, body, 640, 560)


# 10 ------------------------------------------------------------------------------------------ steps
STEPS = """
  body { background: #f6f8fc; color: #0f172a; }
  .pic { position: absolute; left: 0; right: 0; top: 0; height: 760px; background: center/cover no-repeat; }
  .pic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 55%, #f6f8fc 100%); }
  .handle { top: 30px; left: 30px; }
  .sym { right: 30px; top: 30px; }
  #main { left: 50px; right: 50px; gap: 16px; }
  .place { align-self: flex-start; background: #2563eb; color: #fff; font-size: 32px; font-weight: 800; padding: 6px 24px 10px; border-radius: 12px; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #0f172a; font-size: calc(var(--hl) * .8); padding: 0; }
  .hl .hi { color: #2563eb; }
  .sub { font-size: calc(var(--hl) * .37); color: #ea580c; font-weight: 700; line-height: 1.3; }
  .tl { position: relative; padding-left: 80px; display: flex; flex-direction: column; gap: 16px; margin-top: 6px; }
  .tl::before { content: ""; position: absolute; left: 28px; top: 20px; bottom: 20px; width: 6px; background: #c7d2fe; border-radius: 6px; }
  .st { position: relative; background: #fff; border-radius: 20px; padding: 16px 22px 18px; font-size: var(--pt); font-weight: 600; line-height: 1.3;
    box-shadow: 0 8px 20px rgba(15,23,42,.08); }
  .st i { position: absolute; left: -80px; top: 50%; transform: translateY(-50%); width: 62px; height: 62px; border-radius: 50%; background: #2563eb;
    color: #fff; font: 900 30px/62px Arial; text-align: center; font-style: normal; border: 5px solid #f6f8fc; }
  .grow { flex: 1; }
  .askx { background: #0f172a; color: #fff; padding: 16px 26px 20px; border-radius: 22px; }
  .foot2 { font-size: 22px; color: #64748b; }
"""


def steps(story, font, image_url, date, handle, place, asks):
    sts = "".join(f'<div class="st"><i>{i}</i>{highlight_numbers(p)}</div>' for i, p in enumerate(_pts(story, 4), 1))
    body = f"""<div class="pic" style="{_pic(image_url)}"></div><div class="handle">{esc(handle)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main"><div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}<div class="tl">{sts}</div>
  <div class="grow"></div>{_askx(story, asks, "💭")}<div class="foot2">{esc(date)} • સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(STEPS, font, body, 640, 560)


# 11 ------------------------------------------------------------------------------------------ bento
BENTO = """
  body { background: #0e0e10; }
  #main { left: 30px; right: 30px; top: 30px; bottom: 30px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px;
    grid-template-rows: 700px auto auto auto 1fr auto; }
  #main > * { border-radius: 34px; }
  .t-pic { grid-column: 1 / 3; background: center/cover no-repeat; position: relative; }
  .t-pic .sym { right: 18px; top: 18px; }
  .t-pic .handle { left: 18px; top: 18px; }
  .t-num { background: #ffd60a; color: #111; padding: 22px 26px; display: flex; flex-direction: column; justify-content: center; }
  .t-num b { font: 900 86px/1 'Arial Black', Arial, sans-serif; } .t-num small { font-size: 26px; font-weight: 800; margin-top: 8px; }
  .t-place { background: #3a86ff; color: #fff; padding: 22px 26px; display: flex; flex-direction: column; justify-content: center; }
  .t-place b { font-size: 56px; line-height: 1.1; } .t-place small { font-size: 26px; font-weight: 700; opacity: .9; }
  .hl { grid-column: 1 / 3; background: #fff; padding: 20px 20px 16px; }
  .hl div { color: #111; font-size: calc(var(--hl) * .72); }
  .hl .hi { color: #ff006e; }
  .sub { grid-column: 1 / 3; background: #ff006e; color: #fff; padding: 16px 26px 20px; font-size: calc(var(--hl) * .34); font-weight: 700;
    line-height: 1.3; text-align: center; }
  .t-pts { grid-column: 1 / 3; background: #1c1c22; padding: 18px 26px; display: flex; flex-direction: column; gap: 8px; justify-content: center; }
  .pt { display: flex; gap: 14px; align-items: center; color: #eee; font-size: calc(var(--pt) * .9); font-weight: 600; line-height: 1.3; }
  .pt .ic { width: 52px; height: 52px; }
  .askx { grid-column: 1 / 3; background: #8338ec; color: #fff; padding: 18px 28px 22px; }
"""


def bento(story, font, image_url, date, handle, place, asks):
    f = _num(story)
    num = f'<div class="t-num"><b>{esc(f["value"])}</b><small>{esc(f["label"])}</small></div>' if f else '<div class="t-num"><b>!</b></div>'
    body = f"""<div id="main"><div class="t-pic" style="{_pic(image_url)}"><div class="handle">{esc(handle)}</div>
  <div class="sym">પ્રતિકાત્મક તસવીર</div></div>{num}
  <div class="t-place"><b>📍 {esc((place or story.kicker).split(" - ")[0])}</b><small>{esc(date)}</small></div>
  {_hl(story)}{_sub(story)}<div class="t-pts">{_pts_html(story, 3)}</div>{_askx(story, asks, "💬")}</div>"""
    return _wrap(BENTO, font, body, 30, 30)


# 12 ----------------------------------------------------------------------------------------- hazard
HAZARD = """
  body { background: #ffd60a; color: #111; }
  .stripe { position: absolute; left: 0; right: 0; height: 60px; background: repeating-linear-gradient(-45deg, #111 0 40px, #ffd60a 40px 80px); z-index: 3; }
  .s1 { top: 0; } .s2 { bottom: 0; }
  .warn { position: absolute; top: 90px; left: 50px; z-index: 3; display: flex; align-items: center; gap: 20px; }
  .tri { width: 0; height: 0; border-left: 80px solid transparent; border-right: 80px solid transparent; border-bottom: 140px solid #111; position: relative; }
  .tri::after { content: "!"; position: absolute; left: -20px; top: 30px; color: #ffd60a; font: 900 96px/1 Arial; width: 40px; text-align: center; }
  .warn b { font: 900 64px/1 'Arial Black', Arial; } .warn small { display: block; font-size: 34px; font-weight: 800; margin-top: 8px; }
  .handle { top: 100px; right: 40px; left: auto; background: #111; border-color: #111; }
  #main { left: 50px; right: 50px; gap: 18px; bottom: 90px; }
  .hl div { color: #111; font-size: calc(var(--hl) * .82); }
  .hl .hi { color: #c1121f; }
  .band { margin: 0 -50px; height: 520px; background: center/cover no-repeat; position: relative; flex-shrink: 0; }
  .band .sym { right: 20px; bottom: 20px; }
  .sub { background: #111; color: #ffd60a; margin: -18px -50px 0; padding: 16px 50px 20px; font-size: calc(var(--hl) * .37); font-weight: 700;
    line-height: 1.3; text-align: center; }
  .pt { display: flex; gap: 14px; align-items: center; font-size: var(--pt); font-weight: 700; line-height: 1.3; }
  .pt::before { content: "⚠"; font-size: 1.1em; }
  .grow { flex: 1; }
  .askx { border: 5px solid #111; padding: 14px 24px 18px; background: #fff; }
"""


def hazard(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="stripe s1"></div><div class="stripe s2"></div>
  <div class="warn"><div class="tri"></div><div><b>ALERT</b><small>📍 {esc(place or story.kicker)}</small></div></div>
  <div class="handle">{esc(handle)}</div>
  <div id="main">{_hl(story)}<div class="band" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div>{_sub(story)}
  {_pts_html(story, 3, icons=False)}<div class="grow"></div>{_askx(story, asks, "📢")}</div>"""
    return _wrap(HAZARD, font, body, 290, 270)


# 13 ------------------------------------------------------------------------------------------- film
FILM = """
  body { background: radial-gradient(ellipse at 50% 60%, #2a1a0a 0%, #050505 70%); }
  .spot { position: absolute; left: 50%; top: 860px; width: 1300px; height: 1100px; margin-left: -650px;
    background: radial-gradient(ellipse at 50% 0%, rgba(255,214,140,.25), transparent 60%); }
  .strip { position: absolute; left: -20px; right: -20px; top: 150px; height: 680px; background: #111; transform: rotate(-3deg); z-index: 2;
    padding: 70px 0; box-shadow: 0 30px 60px rgba(0,0,0,.6); }
  .strip::before, .strip::after { content: ""; position: absolute; left: 0; right: 0; height: 40px;
    background: repeating-linear-gradient(90deg, transparent 0 22px, #eee 22px 56px, transparent 56px 78px); background-size: 78px 28px;
    background-repeat: repeat-x; background-position: 0 6px; }
  .strip::before { top: 12px; } .strip::after { bottom: 12px; }
  .frame { height: 100%; background: center/cover no-repeat; margin: 0 50px; position: relative; }
  .frame .sym { right: 14px; top: 14px; }
  .handle { top: 40px; left: 40px; }
  .scene { position: absolute; top: 50px; right: 40px; color: #f5d08a; font: 700 28px/1 'Courier New', monospace; z-index: 3; }
  #main { left: 60px; right: 60px; gap: 20px; align-items: center; }
  .place { color: #f5d08a; font-size: 32px; font-weight: 700; letter-spacing: 8px; }
  .hl div { font-size: calc(var(--hl) * .82); background: linear-gradient(180deg, #fff6d5 0%, #f5c46b 55%, #b8761f 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent; filter: drop-shadow(0 6px 10px rgba(0,0,0,.8)); }
  .hl .hi { color: transparent; }
  .sub { text-align: center; font-size: calc(var(--hl) * .36); color: #fff; font-style: italic; font-weight: 500; line-height: 1.3; }
  .credits { display: flex; flex-direction: column; gap: 6px; text-align: center; }
  .credits p { font-size: calc(var(--pt) * .85); color: #cbbfa8; line-height: 1.3; letter-spacing: 1px; }
  .grow { flex: 1; }
  .askx { color: #050505; background: #f5c46b; padding: 14px 30px 18px; border-radius: 8px; }
  .foot2 { font-size: 22px; color: #7d7466; letter-spacing: 2px; }
"""


def film(story, font, image_url, date, handle, place, asks):
    credits = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="spot"></div><div class="strip"><div class="frame" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div></div>
  <div class="handle">{esc(handle)}</div><div class="scene">SCENE • {esc(date)}</div>
  <div id="main"><div class="place">{esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}<div class="credits">{credits}</div>
  <div class="grow"></div>{_askx(story, asks, "🎬")}<div class="foot2">સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(FILM, font, body, 920, 880)


# 14 ---------------------------------------------------------------------------------------- dossier
DOSSIER = """
  body { background: #b08a57; background-image: linear-gradient(135deg, rgba(255,255,255,.08) 25%, transparent 25%); background-size: 8px 8px; }
  .tabf { position: absolute; top: 40px; left: 60px; background: #c9a46c; color: #4a3417; font-size: 34px; font-weight: 800; padding: 14px 40px 30px;
    border-radius: 18px 18px 0 0; }
  .sheet { position: absolute; left: 40px; right: 40px; top: 110px; bottom: 40px; background: #fbf7ee; box-shadow: 0 20px 40px rgba(0,0,0,.35); }
  .clip { position: absolute; right: 70px; top: 150px; width: 470px; height: 380px; background: center/cover no-repeat; transform: rotate(4deg);
    box-shadow: 0 14px 26px rgba(0,0,0,.35); z-index: 3; }
  .clip::before { content: ""; position: absolute; left: 40px; top: -30px; width: 40px; height: 110px; border: 7px solid #8d99ae; border-radius: 20px; }
  .clip .sym { right: 8px; bottom: 8px; font-size: 18px; }
  .stamp { position: absolute; left: 90px; top: 430px; z-index: 4; border: 8px solid #c1121f; color: #c1121f; font: 900 58px/1 'Arial Black', Arial;
    padding: 12px 26px; transform: rotate(-12deg); opacity: .85; letter-spacing: 3px; }
  .fields { position: absolute; left: 90px; top: 170px; width: 420px; z-index: 3; display: flex; flex-direction: column; gap: 22px; }
  .fld small { display: block; font: 700 22px/1 'Courier New', monospace; color: #6b5a3e; }
  .fld b { display: block; font-size: 40px; line-height: 1.2; color: #1a1a1a; border-bottom: 2px solid #1a1a1a; padding-bottom: 4px; }
  #main { left: 90px; right: 90px; gap: 22px; bottom: 80px; justify-content: center; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #1a1a1a; font-size: calc(var(--hl) * .76); padding: 0; }
  .hl .hi { color: #c1121f; }
  .sub { font-size: calc(var(--hl) * .38); font-weight: 700; line-height: 1.35; color: #1d3557; }
  .pt { display: flex; gap: 14px; font-size: calc(var(--pt) * .92); color: #222; line-height: 1.35; font-weight: 600; }
  .pt::before { content: "▸"; color: #c1121f; }
  .grow { flex: 1; }
  .askx { border-top: 3px solid #1a1a1a; padding-top: 16px; color: #1a1a1a; }
  .handle { top: 40px; right: 60px; left: auto; }
"""


def dossier(story, font, image_url, date, handle, place, asks):
    fl = [("સ્થળ", place or story.kicker), ("તારીખ", date)] + [(f["label"], f["value"]) for f in story.facts[:1]]
    fields = "".join(f'<div class="fld"><small>{esc(a)}</small><b>{esc(b)}</b></div>' for a, b in fl if b)
    stamp = {"breaking": "BREAKING", "happy": "GOOD NEWS"}.get(story.mood, "IMPORTANT")
    body = f"""<div class="tabf">કેસ ફાઇલ</div><div class="sheet"></div><div class="handle">{esc(handle)}</div>
  <div class="clip" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div><div class="fields">{fields}</div>
  <div class="stamp">{stamp}</div>
  <div id="main">{_hl(story)}{_sub(story)}{_pts_html(story, 4, icons=False)}{_askx(story, asks, "✏️")}</div>"""
    return _wrap(DOSSIER, font, body, 720, 640)


# 15 ------------------------------------------------------------------------------------------- tape
TAPE = """
  body { background: #0a0a0a; }
  .pic { position: absolute; left: 0; right: 0; top: 0; height: 1100px; background: center/cover no-repeat; filter: saturate(1.2) contrast(1.1); }
  .pic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.2) 0%, transparent 30%, rgba(10,10,10,.6) 75%, #0a0a0a 100%); }
  .tp { position: absolute; left: -100px; right: -100px; height: 92px; background: #ffd60a; z-index: 3; overflow: hidden; white-space: nowrap;
    color: #111; font: 900 46px/92px 'Arial Black', Arial, sans-serif; letter-spacing: 3px; box-shadow: 0 10px 20px rgba(0,0,0,.5);
    border-top: 6px solid #111; border-bottom: 6px solid #111; }
  .tp1 { top: 560px; transform: rotate(-9deg); } .tp2 { top: 620px; transform: rotate(7deg); background: #ffbe0b; }
  .handle { top: 30px; left: 30px; }
  .sym { right: 30px; top: 30px; }
  #main { left: 50px; right: 50px; gap: 18px; }
  .place { align-self: center; color: #ffd60a; font-size: 34px; font-weight: 800; letter-spacing: 2px; }
  .hl div { color: #fff; font-size: calc(var(--hl) * .85); text-shadow: 0 6px 0 #000; }
  .hl .hi { color: #ffd60a; }
  .sub { text-align: center; font-size: calc(var(--hl) * .38); color: #ff8fa3; font-weight: 700; line-height: 1.3; }
  .pts { display: flex; flex-direction: column; gap: 8px; border-top: 2px solid #333; padding-top: 16px; }
  .pt { display: flex; gap: 14px; align-items: center; color: #ddd; font-size: calc(var(--pt) * .92); font-weight: 600; line-height: 1.3; }
  .pt .ic { width: 54px; height: 54px; }
  .askx { color: #111; background: #ffd60a; padding: 14px 28px 18px; clip-path: polygon(0 0, 100% 0, 97% 100%, 3% 100%); justify-content: center; }
  .foot2 { font-size: 22px; color: #777; text-align: center; }
"""


def tape(story, font, image_url, date, handle, place, asks):
    word = {"breaking": "BREAKING", "happy": "GOOD NEWS"}.get(story.mood, "LATEST NEWS")
    t = (f" {word} • {handle} •" * 6)
    body = f"""<div class="pic" style="{_pic(image_url)}"></div><div class="tp tp1">{esc(t)}</div><div class="tp tp2">{esc(t)}</div>
  <div class="handle">{esc(handle)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main"><div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}<div class="pts">{_pts_html(story, 3)}</div>
  {_askx(story, asks, "👇")}<div class="foot2">{esc(date)} • સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(TAPE, font, body, 1000, 900)


# registered as x<name> (several older layouts already use these names)
LAYOUTS15 = {"x" + f.__name__: f for f in (diagonal, tv, paper, bignum, polaroid, circle, magazine, sidebar, quote, steps, bento,
                                     hazard, film, dossier, tape)}
