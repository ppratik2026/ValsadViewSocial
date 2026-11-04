"""Fifteen posters with fifteen different structures (not just other colours), and no frame round any picture: its
edges fade out. Where the picture sits, how the headline is set, how the facts and points are laid out all change.

  diagonal  picture cut on a slant, red block below, left-aligned headline
  tv        news channel screen: LIVE logo, BREAKING tab, white headline bar, blue sub bar, ticker
  paper     newspaper front page: masthead, black headline, photo with caption, two columns
  bignum    one giant number filled with the picture, headline above, chips below
  glass     blurred picture as the page, a frosted glass card with the sharp picture fading into it
  place     the place name in giant letters behind and in front of the picture
  magazine  magazine cover: masthead over the picture, headline and cover lines at the bottom, round price sticker
  topline   headline first on a light page, picture in the middle, three icon cards
  quote     a big quotation: giant quote mark, headline as the quote, sub as the attribution
  steps     light page, picture on top, points on a numbered timeline
  bento     picture fading into a dark page, headline on it, then rounded tiles: number, place, points
  ribbon    the headline on a folded ribbon banner, points as chat bubbles
  film      sprocket holes over a soft-edged picture, movie-title headline, points as credits
  infographic  stat cards with bars over a blurred picture
  tape      picture crossed by two "police line" tapes, headline below

All of them keep the src/viral.FIT contract (#main, .hl div lines, --hl, --pt, --ask, --top, --min-top).
"""
import re

from src.designs import esc, highlight_numbers
from src.icons import icon_img
from src.story_patterns import _base, _with_hero
from src.viral_layouts import _ask, _lines
from src.viral_layouts import _page
from src.viral_more import _pts


def _hl(story, n=None, cls="hl") -> str:
    """Headline in 2 lines (3 when long); every word is its own span (.w) so the reel can bring the words in one by one,
    the highlight words also get .hi."""
    n = n or (2 if len(story.headline) < 44 else 3)
    hi = set(story.highlight.split()) if story.highlight else set()
    lines = []
    for line in _lines(story.headline, n):
        words = " ".join(f'<span class="w{" hi" if w in hi else ""}">{esc(w)}</span>' for w in line.split())
        lines.append(f"<div>{words}</div>")
    return f'<div class="{cls}">{"".join(lines)}</div>'


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
  .w { display: inline-block; }
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
  .pic { position: absolute; left: 0; right: 0; top: 0; height: 1180px; background: center/cover no-repeat; z-index: 1;
    -webkit-mask-image: linear-gradient(172deg, #000 55%, transparent 88%); }
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
    body = f"""<div class="pic" style="{_pic(image_url)}"></div>
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
  .photo { height: 600px; margin: 0 -44px; background: center/cover no-repeat; flex-shrink: 0; position: relative; filter: saturate(1.1);
    -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 14%, #000 82%, transparent 100%); }
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
  .lines { display: flex; flex-direction: column; gap: 10px; margin: 6px 0 8px; }
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
  <div id="main"><div class="place">{esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}<div class="lines">{lines}</div>
  {_askx(story, asks, "તમારો મત")}</div>"""
    return _wrap(MAGAZINE, font, body, 1000, 760)



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
  body { background: #0e0e12; }
  .pic { position: absolute; left: 0; right: 0; top: 0; height: 980px; background: center/cover no-repeat;
    -webkit-mask-image: linear-gradient(180deg, #000 60%, transparent 100%); }
  .handle { top: 30px; left: 30px; }
  .sym { right: 30px; top: 30px; }
  #main { left: 36px; right: 36px; gap: 16px; justify-content: flex-end; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #fff; font-size: calc(var(--hl) * .8); padding: 0; text-shadow: 0 4px 20px rgba(0,0,0,.8); }
  .hl .hi { color: #ffd60a; }
  .sub { font-size: calc(var(--hl) * .36); color: #9ad1ff; font-weight: 700; line-height: 1.3; margin-bottom: 6px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .tile { border-radius: 32px; padding: 22px 24px; position: relative; overflow: hidden; }
  .tile .lbl { font-size: 24px; font-weight: 800; letter-spacing: 1px; opacity: .8; }
  .t-num { background: linear-gradient(135deg, #ffd60a, #ff9f1c); color: #1a1200; }
  .t-num b { display: block; font: 900 74px/1.05 'Arial Black', Arial, sans-serif; margin-top: 6px; white-space: nowrap; }
  .t-place { background: linear-gradient(135deg, #3a86ff, #4361ee); color: #fff; }
  .t-place b { display: block; font-size: 52px; line-height: 1.15; margin-top: 6px; }
  .tile .bigic { position: absolute; right: -14px; bottom: -14px; width: 120px; height: 120px; opacity: .35; }
  .t-pts { grid-column: 1 / 3; background: #1b1b24; border: 2px solid #2b2b38; display: flex; flex-direction: column; gap: 10px; }
  .pt { display: flex; gap: 16px; align-items: center; color: #eee; font-size: calc(var(--pt) * .88); font-weight: 600; line-height: 1.3; }
  .pt .ic { width: 54px; height: 54px; flex-shrink: 0; background: #2b2b38; border-radius: 16px; padding: 6px; }
  .askx { border-radius: 32px; background: linear-gradient(90deg, #8338ec, #ff006e); color: #fff; padding: 20px 28px 24px; }
  .foot2 { font-size: 22px; color: #777; display: flex; justify-content: space-between; }
"""


def bento(story, font, image_url, date, handle, place, asks):
    f = _num(story)
    num = (f'<div class="tile t-num"><div class="lbl">{esc(f["label"])}</div><b>{esc(f["value"])}</b>{icon_img(f["label"] + " " + f["value"], "bigic")}</div>'
           if f else f'<div class="tile t-num"><div class="lbl">ખાસ</div><b>!</b></div>')
    where = esc((place or story.kicker).split(" - ")[0])
    body = f"""<div class="pic" style="{_pic(image_url)}"></div><div class="handle">{esc(handle)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main">{_hl(story)}{_sub(story)}<div class="grid">{num}
  <div class="tile t-place"><div class="lbl">{esc(date)}</div><b>📍 {where}</b>{icon_img("pin", "bigic")}</div>
  <div class="tile t-pts">{_pts_html(story, 3)}</div></div>{_askx(story, asks, "💬")}
  <div class="foot2"><span>{esc(handle)}</span><span>સ્રોત: {esc(story.source_name)}</span></div></div>"""
    return _wrap(BENTO, font, body, 820, 600)

# 13 ------------------------------------------------------------------------------------------- film
FILM = """
  body { background: radial-gradient(ellipse at 50% 60%, #2a1a0a 0%, #050505 70%); }
  .spot { position: absolute; left: 50%; top: 860px; width: 1300px; height: 1100px; margin-left: -650px;
    background: radial-gradient(ellipse at 50% 0%, rgba(255,214,140,.25), transparent 60%); }
  .strip { position: absolute; left: -20px; right: -20px; top: 130px; height: 760px; transform: rotate(-3deg); z-index: 2; padding: 0; }
  .strip::before, .strip::after { content: ""; position: absolute; left: 0; right: 0; height: 40px;
    background: repeating-linear-gradient(90deg, transparent 0 22px, #eee 22px 56px, transparent 56px 78px); background-size: 78px 28px;
    background-repeat: repeat-x; background-position: 0 6px; }
  .strip::before { top: 12px; } .strip::after { bottom: 12px; }
  .frame { height: 100%; background: center/cover no-repeat; position: relative;
    -webkit-mask-image: radial-gradient(ellipse 62% 58% at 50% 50%, #000 60%, transparent 100%); }
  .strip::before, .strip::after { opacity: .5; z-index: 3; }
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


# 5 ------------------------------------------------------------------------------------------- glass
GLASS = """
  body { background: #0b1020; }
  .blur { position: absolute; inset: -60px; background: center/cover no-repeat; filter: blur(36px) saturate(1.5) brightness(.75); }
  .handle { top: 30px; left: 30px; }
  #main { left: 60px; right: 60px; top: var(--top); bottom: 60px; gap: 18px; padding: 0 36px 34px; border-radius: 48px;
    background: rgba(255,255,255,.14); backdrop-filter: blur(24px); border: 2px solid rgba(255,255,255,.35);
    box-shadow: 0 30px 80px rgba(0,0,0,.45); }
  .ph { margin: 0 -36px; height: 640px; background: center/cover no-repeat; position: relative; border-radius: 48px 48px 0 0; flex-shrink: 0;
    -webkit-mask-image: linear-gradient(180deg, #000 72%, transparent 100%); }
  .ph .sym { right: 20px; top: 20px; }
  .place { align-self: center; margin-top: -40px; font-size: 32px; font-weight: 800; color: #fff; background: rgba(0,0,0,.35);
    padding: 6px 24px 10px; border-radius: 30px; backdrop-filter: blur(8px); }
  .hl div { color: #fff; font-size: calc(var(--hl) * .72); text-shadow: 0 4px 18px rgba(0,0,0,.4); }
  .hl .hi { color: #ffe066; }
  .sub { text-align: center; font-size: calc(var(--hl) * .34); color: #c8f7ff; font-weight: 700; line-height: 1.3; }
  .pt { display: flex; gap: 14px; align-items: center; color: #fff; font-size: calc(var(--pt) * .85); font-weight: 600; line-height: 1.3; }
  .pt .ic { width: 50px; height: 50px; }
  .grow { flex: 1; }
  .askx { justify-content: center; color: #0b1020; background: #fff; padding: 14px 26px 18px; border-radius: 30px; font-size: calc(var(--ask) * .85); }
  .foot2 { position: absolute; bottom: 16px; left: 0; right: 0; text-align: center; font-size: 22px; color: rgba(255,255,255,.8); }
"""


def glass(story, font, image_url, date, handle, place, asks):
    body = f"""<div class="blur" style="{_pic(image_url)}"></div><div class="handle">{esc(handle)}</div>
  <div id="main"><div class="ph" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div>
  <div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}{_pts_html(story, 3)}<div class="grow"></div>
  {_askx(story, asks, "💬")}</div><div class="foot2">{esc(date)} • સ્રોત: {esc(story.source_name)}</div>"""
    return _wrap(GLASS, font, body, 110, 90)


# 6 -------------------------------------------------------------------------------------------- place
PLACE = """
  body { background: #101418; }
  .giant { position: absolute; top: 40px; left: -20px; right: -20px; text-align: center; z-index: 1; font-size: 330px; font-weight: 800;
    line-height: 1; color: transparent; -webkit-text-stroke: 4px rgba(255,255,255,.35); white-space: nowrap; letter-spacing: -4px; }
  .pic { position: absolute; left: 0; right: 0; top: 240px; height: 900px; background: center/cover no-repeat; z-index: 2;
    -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 22%, #000 62%, transparent 100%); }
  .giant2 { position: absolute; top: 40px; left: -20px; right: -20px; text-align: center; z-index: 3; font-size: 330px; font-weight: 800;
    line-height: 1; color: #ff7b00; white-space: nowrap; letter-spacing: -4px; -webkit-mask-image: linear-gradient(180deg, #000 50%, transparent 72%); }
  .handle { top: 30px; left: 30px; z-index: 6; }
  .sym { right: 30px; top: 30px; }
  #main { left: 50px; right: 50px; gap: 18px; }
  .hl div { color: #fff; font-size: calc(var(--hl) * .82); }
  .hl .hi { color: #ff7b00; }
  .sub { text-align: center; font-size: calc(var(--hl) * .37); color: #ffd6a5; font-weight: 700; line-height: 1.3; }
  .row { display: flex; gap: 14px; }
  .cell { flex: 1; text-align: center; border-top: 4px solid #ff7b00; padding-top: 14px; color: #eee; font-size: calc(var(--pt) * .78);
    font-weight: 600; line-height: 1.28; }
  .cell .ic { display: block; margin: 0 auto 10px; width: 70px; height: 70px; }
  .grow { flex: 1; }
  .askx { justify-content: center; color: #fff; border: 3px solid #ff7b00; border-radius: 60px; padding: 14px 26px 18px; }
  .foot2 { font-size: 22px; color: #888; text-align: center; }
"""


def place_big(story, font, image_url, date, handle, place, asks):
    word = esc((place or story.kicker or "").split(" - ")[0].split(" • ")[0])
    cells = "".join(f'<div class="cell">{icon_img(p)}{highlight_numbers(p)}</div>' for p in _pts(story, 3))
    body = f"""<div class="giant">{word}</div><div class="pic" style="{_pic(image_url)}"></div><div class="giant2">{word}</div>
  <div class="handle">{esc(handle)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main">{_hl(story)}{_sub(story)}<div class="row">{cells}</div><div class="grow"></div>{_askx(story, asks, "👇")}
  <div class="foot2">{esc(date)} • સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(PLACE, font, body, 1050, 960)


# 8 ------------------------------------------------------------------------------------------ topline
TOPLINE = """
  body { background: #fff7e6; color: #1b1b1b; }
  .handle { top: 30px; right: 30px; left: auto; }
  #main { left: 50px; right: 50px; top: 30px; gap: 18px; }
  .place { font-size: 34px; font-weight: 800; color: #d62828; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #1b1b1b; font-size: calc(var(--hl) * .9); padding: 0; line-height: 1.15; }
  .hl .hi { color: #d62828; }
  .sub { font-size: calc(var(--hl) * .37); color: #00798c; font-weight: 700; line-height: 1.3; }
  .ph { margin: 0 -50px; flex: 1 1 auto; min-height: 520px; background: center/cover no-repeat; position: relative;
    -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 12%, #000 85%, transparent 100%); }
  .ph .sym { right: 30px; top: 70px; }
  .row { display: flex; gap: 16px; }
  .cell { flex: 1; background: #fff; border-radius: 26px; padding: 18px 16px 20px; text-align: center; box-shadow: 0 10px 24px rgba(0,0,0,.08);
    font-size: calc(var(--pt) * .75); font-weight: 600; line-height: 1.28; }
  .cell .ic { display: block; margin: 0 auto 10px; width: 66px; height: 66px; }
  .askx { justify-content: center; background: #d62828; color: #fff; padding: 16px 26px 20px; border-radius: 24px; }
  .foot2 { font-size: 22px; color: #777; display: flex; justify-content: space-between; }
"""


def topline(story, font, image_url, date, handle, place, asks):
    cells = "".join(f'<div class="cell">{icon_img(p)}{highlight_numbers(p)}</div>' for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main"><div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}
  <div class="ph" style="{_pic(image_url)}"><div class="sym">પ્રતિકાત્મક તસવીર</div></div><div class="row">{cells}</div>
  {_askx(story, asks, "🙋")}<div class="foot2"><span>{esc(date)}</span><span>સ્રોત: {esc(story.source_name)}</span></div></div>"""
    return _wrap(TOPLINE, font, body, 30, 30)


# 12 ----------------------------------------------------------------------------------------- ribbon
RIBBON = """
  body { background: #1a0633; }
  .pic { position: absolute; inset: 0 0 640px 0; background: center/cover no-repeat;
    -webkit-mask-image: linear-gradient(180deg, #000 60%, transparent 100%); }
  .handle { top: 30px; left: 30px; }
  .sym { right: 30px; top: 30px; }
  #main { left: 0; right: 0; gap: 22px; }
  .place { align-self: center; color: #ffd166; font-size: 34px; font-weight: 800; }
  .hl { position: relative; background: linear-gradient(180deg, #ef476f, #c9184a); margin: 0 70px; padding: 18px 20px 14px;
    box-shadow: 0 16px 30px rgba(0,0,0,.4); }
  .hl::before, .hl::after { content: ""; position: absolute; top: 34px; bottom: -34px; width: 110px; background: #a4133c; z-index: -1;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 30% 50%); }
  .hl::before { left: -80px; } .hl::after { right: -80px; transform: scaleX(-1); }
  .hl div { color: #fff; font-size: calc(var(--hl) * .72); }
  .hl .hi { color: #ffd166; }
  .sub { text-align: center; margin: 22px 60px 0; font-size: calc(var(--hl) * .36); color: #ffd166; font-weight: 700; line-height: 1.3; }
  .bubbles { display: flex; flex-direction: column; gap: 16px; padding: 0 50px; }
  .bb { position: relative; align-self: flex-start; max-width: 88%; background: #fff; color: #1a0633; border-radius: 30px; padding: 14px 26px 18px;
    font-size: calc(var(--pt) * .88); font-weight: 600; line-height: 1.3; }
  .bb:nth-child(even) { align-self: flex-end; background: #ffd166; }
  .grow { flex: 1; }
  .askx { justify-content: center; color: #fff; margin: 0 50px; border-bottom: 4px solid #ef476f; padding-bottom: 14px; }
  .foot2 { font-size: 22px; color: #a99bc0; text-align: center; padding-bottom: 6px; }
"""


def ribbon(story, font, image_url, date, handle, place, asks):
    bubbles = "".join(f'<div class="bb">{highlight_numbers(p)}</div>' for p in _pts(story, 3))
    body = f"""<div class="pic" style="{_pic(image_url)}"></div><div class="handle">{esc(handle)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main"><div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}<div class="bubbles">{bubbles}</div>
  <div class="grow"></div>{_askx(story, asks, "💬")}<div class="foot2">{esc(date)} • સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(RIBBON, font, body, 980, 860)


# 14 ------------------------------------------------------------------------------------- infographic
INFO = """
  body { background: #04141f; }
  .blur { position: absolute; inset: -60px; background: center/cover no-repeat; filter: blur(28px) brightness(.45) saturate(1.3); }
  .pic { position: absolute; left: 0; right: 0; top: 0; height: 760px; background: center/cover no-repeat;
    -webkit-mask-image: linear-gradient(180deg, #000 55%, transparent 100%); }
  .handle { top: 30px; left: 30px; }
  .sym { right: 30px; top: 30px; }
  #main { left: 50px; right: 50px; gap: 20px; }
  .place { align-self: flex-start; color: #2ec4b6; font-size: 34px; font-weight: 800; }
  .hl { align-items: flex-start; }
  .hl div { text-align: left; color: #fff; font-size: calc(var(--hl) * .8); padding: 0; }
  .hl .hi { color: #2ec4b6; }
  .sub { font-size: calc(var(--hl) * .36); color: #ffbf69; font-weight: 700; line-height: 1.3; }
  .stats { display: flex; gap: 18px; }
  .stat { flex: 1; background: rgba(255,255,255,.08); border: 2px solid rgba(46,196,182,.5); border-radius: 26px; padding: 18px 22px; }
  .stat b { display: block; font: 900 64px/1.05 'Arial Black', Arial, sans-serif; color: #2ec4b6; white-space: nowrap; }
  .stat small { display: block; font-size: 24px; font-weight: 700; color: #cde; margin-top: 6px; line-height: 1.2; }
  .bar { height: 14px; border-radius: 10px; background: rgba(255,255,255,.12); overflow: hidden; margin-top: 12px; }
  .bar i { display: block; height: 100%; background: linear-gradient(90deg, #2ec4b6, #ffbf69); }
  .pt { display: flex; gap: 14px; align-items: center; color: #e6f1f5; font-size: calc(var(--pt) * .85); font-weight: 600; line-height: 1.3; }
  .pt .ic { width: 50px; height: 50px; }
  .grow { flex: 1; }
  .askx { color: #04141f; background: #2ec4b6; padding: 14px 26px 18px; border-radius: 18px; }
  .foot2 { font-size: 22px; color: #7a98a8; }
"""


def infographic(story, font, image_url, date, handle, place, asks):
    facts = [f for f in story.facts if len(f["value"]) <= 10][:2]
    widths = [82, 58]
    stats = "".join(f'<div class="stat"><b>{esc(f["value"])}</b><small>{esc(f["label"])}</small><div class="bar"><i style="width:{w}%"></i></div></div>'
                    for f, w in zip(facts, widths))
    body = f"""<div class="blur" style="{_pic(image_url)}"></div><div class="pic" style="{_pic(image_url)}"></div>
  <div class="handle">{esc(handle)}</div><div class="sym">પ્રતિકાત્મક તસવીર</div>
  <div id="main"><div class="place">📍 {esc(place or story.kicker)}</div>{_hl(story)}{_sub(story)}
  {f'<div class="stats">{stats}</div>' if stats else ""}{_pts_html(story, 3)}<div class="grow"></div>{_askx(story, asks, "📊")}
  <div class="foot2">{esc(date)} • સ્રોત: {esc(story.source_name)}</div></div>"""
    return _wrap(INFO, font, body, 700, 600)


# registered as x<name> (several older layouts already use these names); every one shows the picture alone first
LAYOUTS15 = {"x" + f.__name__: _with_hero(f) for f in (diagonal, tv, paper, bignum, glass, place_big, magazine, topline, quote,
                                                     steps, bento, ribbon, film, infographic, tape)}

# ---------------------------------------------------------------------------------------------- motion
# image first (S seconds), then the headline word by word, then the rest one element at a time, in each layout's own way
# (steps in the src/card.ANIM_JS format: selector, animation, start, duration, stagger)
S = 1.1
_HERO = [".hero", "heroOut", S - 0.25, 0.55, 0]
_ZOOM = [[".pic, .blur, .ph, .photo, .frame", "kbZoom {end}s linear 0s both"]]


def _m(*steps, live=None):
    return {"intro": [_HERO] + [list(x) for x in steps], "live": _ZOOM + (live or []), "spot": None}


LAYOUT_MOTION = {
    "xdiagonal": _m((".place", "slideFarL", S, .35, 0), (".hl .w", "slapIn", S + .3, .3, .11), (".sub", "slideFarL", S + 1.9, .4, 0),
                    (".pt", "slideFarL", S + 2.4, .35, .3), (".askx", "riseUp", S + 3.6, .4, 0), (".handle2", "fadeIn", S + 3.9, .4, 0)),
    "xtv": _m((".logo", "dropIn", S, .4, 0), (".tab", "slideFarL", S + .2, .35, 0), (".hl", "growX", S + .5, .4, 0),
              (".hl .w", "fadeIn", S + .8, .2, .08), (".sub", "growX", S + 2.0, .4, 0), (".pt", "slideFarR", S + 2.5, .35, .3),
              (".ticker", "riseUp", S + 3.6, .4, 0), live=[[".logo span", "blink 1s steps(1) {start}s infinite"]]),
    "xpaper": _m((".mast", "dropIn", S, .45, 0), (".dateline", "growX", S + .3, .4, 0), (".hl .w", "inkIn", S + .6, .45, .1),
                 (".sub", "fadeIn", S + 1.9, .4, 0), (".photo", "develop", S + 2.2, .8, 0), (".cap", "fadeIn", S + 2.6, .4, 0),
                 (".cols p", "fadeIn", S + 2.9, .4, .3), (".askx", "popIn", S + 4.0, .35, 0)),
    "xbignum": _m((".place", "popIn", S, .35, 0), (".hl .w", "wordRise", S + .3, .45, .1), (".big", "slam", S + 1.6, .6, 0),
                  (".biglabel", "fadeIn", S + 2.1, .3, 0), (".sub", "fadeIn", S + 2.4, .4, 0), (".chip", "popIn", S + 2.8, .3, .25),
                  (".askx", "riseUp", S + 3.8, .4, 0), (".foot2", "fadeIn", S + 4.1, .4, 0)),
    "xglass": _m((".ph", "fadeIn", S - .1, .5, 0), (".place", "popIn", S + .3, .35, 0), (".hl .w", "wordRise", S + .5, .5, .1),
                 (".sub", "fadeIn", S + 1.9, .4, 0), (".pt", "slideFarL", S + 2.3, .35, .3), (".askx", "popIn", S + 3.5, .35, 0),
                 (".foot2", "fadeIn", S + 3.8, .4, 0)),
    "xplace_big": _m((".giant", "fadeIn", S, .5, 0), (".giant2", "dropBounce", S + .1, .8, 0), (".hl .w", "dropIn", S + .8, .4, .1),
                     (".sub", "fadeIn", S + 2.1, .4, 0), (".cell", "popIn", S + 2.5, .35, .3), (".askx", "riseUp", S + 3.6, .4, 0),
                     (".foot2", "fadeIn", S + 3.9, .4, 0)),
    "xmagazine": _m((".mast", "flipX", S, .6, 0), (".tag, .issue", "fadeIn", S + .4, .4, 0), (".sticker", "popIn", S + .7, .4, 0),
                    (".place", "slideFarL", S + 1.0, .35, 0), (".hl .w", "slideFarL", S + 1.2, .4, .09), (".sub", "fadeIn", S + 2.4, .4, 0),
                    (".line", "slideFarL", S + 2.8, .35, .3), (".askx", "fadeIn", S + 3.9, .4, 0),
                    live=[[".sticker", "wobble 1.6s ease-in-out {start}s infinite"]]),
    "xtopline": _m((".place", "fadeIn", S, .4, 0), (".hl .w", "wordRise", S + .2, .45, .1), (".sub", "fadeIn", S + 1.6, .4, 0),
                   (".ph", "develop", S + 1.9, .7, 0), (".cell", "popIn", S + 2.5, .35, .3), (".askx", "riseUp", S + 3.6, .4, 0),
                   (".foot2", "fadeIn", S + 3.9, .4, 0)),
    "xquote": _m((".mark", "dropBounce", S, .8, 0), (".place", "fadeIn", S + .5, .4, 0), (".hl .w", "fadeIn", S + .7, .5, .14),
                 (".sub", "slideFarL", S + 2.4, .4, 0), (".line", "growX", S + 2.8, .4, 0), (".pt", "fadeIn", S + 3.1, .4, .3),
                 (".askx", "slideFarL", S + 4.1, .4, 0), (".foot2", "fadeIn", S + 4.4, .4, 0)),
    "xsteps": _m((".place", "popIn", S, .35, 0), (".hl .w", "wordRise", S + .3, .45, .1), (".sub", "fadeIn", S + 1.7, .4, 0),
                 (".st", "slideFarR", S + 2.1, .4, .35), (".askx", "riseUp", S + 3.7, .4, 0), (".foot2", "fadeIn", S + 4.0, .4, 0)),
    "xbento": _m((".hl .w", "popIn", S + .1, .35, .09), (".sub", "fadeIn", S + 1.4, .4, 0), (".tile", "popIn", S + 1.8, .4, .3),
                 (".askx", "riseUp", S + 3.2, .4, 0), (".foot2", "fadeIn", S + 3.5, .4, 0),
                 live=[[".bigic", "float 2s ease-in-out {start}s infinite"]]),
    "xribbon": _m((".place", "dropIn", S, .4, 0), (".hl", "unfold", S + .3, .5, 0), (".hl .w", "fadeIn", S + .7, .25, .08),
                  (".sub", "fadeIn", S + 1.9, .4, 0), (".bb", "popIn", S + 2.3, .35, .45), (".askx", "riseUp", S + 3.8, .4, 0),
                  (".foot2", "fadeIn", S + 4.1, .4, 0)),
    "xfilm": _m((".scene", "typeIn", S, .5, 0), (".place", "flickerOn", S + .3, .6, 0), (".hl .w", "flickerOn", S + .6, .6, .12),
                (".sub", "fadeIn", S + 2.2, .5, 0), (".credits p", "riseUp", S + 2.6, .45, .35), (".askx", "popIn", S + 3.9, .35, 0),
                (".foot2", "fadeIn", S + 4.2, .4, 0)),
    "xinfographic": _m((".place", "slideFarL", S, .35, 0), (".hl .w", "wordRise", S + .3, .45, .1), (".sub", "fadeIn", S + 1.7, .4, 0),
                       (".stat", "popIn", S + 2.0, .35, .25), (".bar i", "growX", S + 2.4, .8, .25), (".pt", "slideFarL", S + 2.9, .35, .3),
                       (".askx", "riseUp", S + 4.0, .4, 0), (".foot2", "fadeIn", S + 4.3, .4, 0)),
    "xtape": _m((".tp1", "slideFarL", S, .4, 0), (".tp2", "slideFarR", S + .2, .4, 0), (".place", "fadeIn", S + .5, .3, 0),
                (".hl .w", "slapIn", S + .7, .3, .1), (".sub", "fadeIn", S + 2.0, .4, 0), (".pt", "slideFarL", S + 2.4, .35, .3),
                (".askx", "riseUp", S + 3.6, .4, 0), (".foot2", "fadeIn", S + 3.9, .4, 0)),
}

# which layouts fit which kind of news (src/viral._pattern_for picks the first one not used in the last posts)
LAYOUT_PRIORITY = [
    ("crime", ["xtape", "xtv", "xdiagonal", "xbento"]),
    ("weather", ["xtv", "xglass", "xplace_big", "xfilm"]),
    ("money", ["xbignum", "xinfographic", "xbento", "xpaper"]),
    ("prices", ["xbignum", "xinfographic", "xbento", "xpaper"]),
    ("good_news", ["xmagazine", "xribbon", "xglass", "xquote"]),
    ("event", ["xfilm", "xribbon", "xmagazine", "xplace_big"]),
    ("government", ["xsteps", "xtopline", "xpaper", "xinfographic"]),
    ("education", ["xsteps", "xtopline", "xquote", "xglass"]),
    ("politics", ["xquote", "xpaper", "xtv", "xdiagonal"]),
    ("trending", ["xplace_big", "xglass", "xribbon", "xfilm"]),
    ("viral", ["xribbon", "xtape", "xbignum", "xplace_big"]),
]
LAYOUT_DEFAULT = ["xtopline", "xbento", "xglass", "xplace_big"]
