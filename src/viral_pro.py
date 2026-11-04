"""Premium layouts for the viral design, made to look as rich as AI-made posters while every word stays real text:

  hero3d      full-bleed picture, light rays and sparkles, a giant tilted 3D extruded headline, floating 3D icons
  glass3d     blurred picture with glowing orbs, frosted glass cards floating at 3D angles, the headline card in front
  poppop      bold pop-art: duotone picture, a giant faded word behind, slanted colour blocks, neon outline frames
  cinema      a movie poster: graded picture, metallic gold bevelled title, tagline, credits block, glowing frame

Shared contract with src/viral.FIT: #main, .hl div lines, --hl, --pt, --ask, --top, --min-top, .grow.
"""
import re

from src.designs import esc, highlight_numbers
from src.icons import icon_img
from src.viral_more import SYM, _askbar, _base, _bg, _foot, _hl, _page, _pts

# extruded 3D letters: a solid face, a thick outline and a stack of shadows that builds the depth
X3D = ("-webkit-text-stroke: 3px #1a0500; paint-order: stroke fill; text-shadow: 1px 1px 0 #7a1d00, 2px 2px 0 #7a1d00, "
       "3px 3px 0 #6b1900, 4px 4px 0 #5c1600, 5px 5px 0 #4d1200, 6px 6px 0 #3e0f00, 7px 7px 0 #2f0b00, 8px 8px 0 #200800, "
       "10px 14px 18px rgba(0,0,0,.6);")


def _icons(story, n=3) -> list[str]:
    """Up to n icons that fit the story (for the floating 3D stickers)."""
    texts = [story.headline] + list(story.points) + [f["label"] + " " + f["value"] for f in story.facts]
    seen, out = set(), []
    for t in texts:
        img = icon_img(t, "fl")
        if img not in seen:
            seen.add(img)
            out.append(img)
        if len(out) == n:
            break
    return out


# --------------------------------------------------------------------------------------------- hero3d
HERO_CSS = """
  body { background: #0b0420; }
  .bgpic { position: absolute; inset: 0; background: #1a0b3d center/cover no-repeat; }
  .bgpic::after { content: ""; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(11,4,32,.15) 0%, rgba(11,4,32,.0) 25%, rgba(11,4,32,.65) 50%, #0b0420 78%); }
  .rays { position: absolute; left: 50%; top: 44%; width: 2400px; height: 2400px; margin: -1200px 0 0 -1200px; z-index: 1; opacity: .35;
    background: repeating-conic-gradient(from 0deg, rgba(255,214,10,.55) 0deg 6deg, transparent 6deg 18deg);
    -webkit-mask-image: radial-gradient(circle, #000 0%, transparent 55%); mask-image: radial-gradient(circle, #000 0%, transparent 55%); }
  .spark { position: absolute; z-index: 2; width: 10px; height: 10px; border-radius: 50%; background: #fff;
    box-shadow: 0 0 12px 4px rgba(255,230,120,.9); }
  .handle { top: 30px; right: 30px; z-index: 6; }
  .sym { top: 30px; left: 30px; right: auto; }
  .ribbon { align-self: center; position: relative; background: linear-gradient(180deg, #ff2e2e, #b00000); color: #fff; font-size: 44px; font-weight: 800;
    padding: 8px 60px 14px; clip-path: polygon(0 0, 100% 0, 94% 50%, 100% 100%, 0 100%, 6% 50%); box-shadow: 0 10px 20px rgba(0,0,0,.5); }
  .hl { transform: rotate(-4deg); gap: 0; }
  .hl div { color: #ffe14d; """ + X3D + """ padding: 0 30px 14px; }
  .hl div:nth-child(even) { color: #ffffff; }
  .hl .hi { color: #ff3b3b; font-size: 1.3em; }
  .floaters { position: relative; height: 0; }
  .fl { position: absolute; width: 170px; height: 170px; z-index: 5; filter: drop-shadow(0 20px 16px rgba(0,0,0,.55)); }
  .sub { align-self: center; background: rgba(0,0,0,.55); border: 3px solid #ffe14d; border-radius: 50px; color: #fff; font-size: calc(var(--pt) * 1.05);
    font-weight: 800; padding: 10px 34px 14px; text-align: center; line-height: 1.3; }
  .sub .num { color: #ffe14d; }
  .cards { display: flex; flex-direction: column; gap: 14px; }
  .cards p { display: flex; gap: 16px; align-items: center; font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #fff;
    background: linear-gradient(90deg, rgba(255,255,255,.16), rgba(255,255,255,.04)); border: 2px solid rgba(255,255,255,.35); border-radius: 22px;
    padding: 12px 20px; box-shadow: 0 10px 24px rgba(0,0,0,.35); }
  .cards p .ic { width: 64px; height: 64px; flex-shrink: 0; }
  .cards .num { color: #ffe14d; }
"""


def hero3d_page(story, font, image_url, date, handle, place, asks):
    import random
    rnd = random.Random(story.headline)
    sparks = "".join(f'<i class="spark" style="left:{rnd.randint(40, 1040)}px;top:{rnd.randint(500, 1500)}px;'
                     f'transform:scale({rnd.uniform(.4, 1.3):.2f})"></i>' for _ in range(16))
    fl = _icons(story)
    spots = [("left:-20px;top:-200px;transform:rotate(-14deg)"), ("right:-20px;top:-230px;transform:rotate(12deg)"),
             ("left:420px;top:-260px;transform:rotate(-8deg) scale(.6)")]
    floaters = "".join(img.replace('class="fl"', f'class="fl" style="{s}"') for img, s in zip(fl, spots))
    cards = "".join(f"<p>{icon_img(p)}<span>{highlight_numbers(p)}</span></p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div><div class="rays"></div>{sparks}{SYM if image_url else ""}
  <div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="ribbon">{esc(place or story.kicker or "મોટા સમાચાર")}</div>
    <div class="floaters">{floaters}</div>
    <div class="hl">{_hl(story)}</div>
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    <div class="grow"></div>
    {f'<div class="cards">{cards}</div>' if cards else ""}
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 560, 420) + HERO_CSS, font, body)


# --------------------------------------------------------------------------------------------- glass3d
GLASS_CSS = """
  body { background: #0d1b2a; }
  .bgpic { position: absolute; inset: -40px; background: #1b263b center/cover no-repeat; filter: blur(14px) saturate(1.4) brightness(.7); }
  .orb { position: absolute; border-radius: 50%; filter: blur(40px); opacity: .75; z-index: 1; }
  .handle { top: 30px; right: 30px; z-index: 6; }
  #main { perspective: 1400px; }
  .photo { position: relative; height: 560px; border-radius: 40px; background: #333 center/cover no-repeat; transform: rotateY(-12deg) rotateX(4deg);
    box-shadow: -30px 40px 60px rgba(0,0,0,.6), 0 0 0 4px rgba(255,255,255,.5); }
  .photo .sym { bottom: 14px; }
  .tag { position: absolute; left: -10px; top: 30px; background: linear-gradient(90deg, #ff006e, #ff7b00); color: #fff; font-size: 38px; font-weight: 800;
    padding: 8px 26px 12px; border-radius: 0 40px 40px 0; box-shadow: 0 10px 20px rgba(0,0,0,.4); }
  .front { background: rgba(255,255,255,.18); border: 2px solid rgba(255,255,255,.55); border-radius: 40px; padding: 22px 20px 16px;
    backdrop-filter: blur(18px); box-shadow: 0 30px 60px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.6); transform: rotateY(6deg) translateZ(40px);
    margin-top: -90px; position: relative; z-index: 3; }
  .front .hl div { color: #fff; text-shadow: 0 4px 18px rgba(0,0,0,.45); }
  .front .hl .hi { color: #ffd60a; -webkit-text-stroke: 2px #5a2a00; paint-order: stroke fill; }
  .stack { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  .gc { background: rgba(255,255,255,.14); border: 2px solid rgba(255,255,255,.4); border-radius: 30px; padding: 18px; backdrop-filter: blur(12px);
    box-shadow: 0 20px 40px rgba(0,0,0,.4); color: #fff; font-size: var(--pt); font-weight: 700; line-height: 1.3; }
  .gc:nth-child(odd) { transform: rotateY(10deg); } .gc:nth-child(even) { transform: rotateY(-10deg); }
  .gc.wide { grid-column: 1 / -1; transform: none; }
  .gc .ic { width: 70px; height: 70px; display: block; margin-bottom: 8px; filter: drop-shadow(0 8px 8px rgba(0,0,0,.4)); }
  .gc .num { color: #ffd60a; }
  .v-ask .say { background: linear-gradient(90deg, #ffd60a, #ff9e00); }
"""


def glass3d_page(story, font, image_url, date, handle, place, asks):
    pts = _pts(story, 4)
    cards = "".join(f'<div class="gc{" wide" if len(pts) % 2 and i == len(pts) - 1 else ""}">{icon_img(p)}{highlight_numbers(p)}</div>'
                    for i, p in enumerate(pts))
    orbs = ('<div class="orb" style="left:-120px;top:200px;width:520px;height:520px;background:#ff006e"></div>'
            '<div class="orb" style="right:-160px;top:820px;width:600px;height:600px;background:#3a86ff"></div>'
            '<div class="orb" style="left:200px;bottom:-200px;width:500px;height:500px;background:#ffbe0b"></div>')
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{orbs}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}<div class="tag">{esc(place or story.kicker or "સમાચાર")}</div></div>
    <div class="front"><div class="hl">{_hl(story)}</div></div>
    {f'<div class="stack">{cards}</div>' if cards else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 60) + GLASS_CSS, font, body)


# ---------------------------------------------------------------------------------------------- poppop
POP_CSS = """
  body { background: #ffde00; overflow: hidden; }
  .giant { position: absolute; left: -40px; top: 620px; z-index: 0; font: 900 420px/0.8 'Arial Black', Arial, sans-serif; color: transparent;
    -webkit-text-stroke: 6px rgba(0,0,0,.12); transform: rotate(-90deg) translate(-40%, 0); transform-origin: left top; white-space: nowrap; }
  .blockA { position: absolute; left: -100px; right: -100px; top: 980px; height: 520px; background: #ff006e; transform: rotate(-8deg); z-index: 0; }
  .blockB { position: absolute; left: -100px; right: -100px; top: 1430px; height: 600px; background: #111; transform: rotate(-8deg); z-index: 0; }
  .handle { top: 30px; right: 30px; background: #111; border-color: #ff006e; }
  .photo { position: relative; height: 640px; background: #333 center/cover no-repeat; border: 10px solid #111; transform: rotate(3deg);
    box-shadow: 18px 18px 0 #ff006e; filter: contrast(1.15) saturate(1.3); }
  .photo::after { content: ""; position: absolute; inset: 0; background: radial-gradient(rgba(0,0,0,.25) 22%, transparent 24%) 0 0/14px 14px;
    mix-blend-mode: multiply; }
  .photo .sym { bottom: 10px; z-index: 2; }
  .stamp { position: absolute; right: -30px; top: -40px; z-index: 3; background: #00f5d4; color: #111; font: 900 46px/1 'Arial Black', Arial, sans-serif;
    padding: 18px 26px; border: 6px solid #111; transform: rotate(10deg); box-shadow: 8px 8px 0 #111; }
  .hl { gap: 4px; }
  .hl div { background: #111; color: #fff; padding: 2px 30px 12px; transform: rotate(-3deg); box-shadow: 10px 10px 0 #ff006e; }
  .hl div:nth-child(even) { background: #fff; color: #111; box-shadow: 10px 10px 0 #111; transform: rotate(2deg); }
  .hl .hi { color: #ffde00; } .hl div:nth-child(even) .hi { color: #ff006e; }
  .bul { display: flex; flex-direction: column; gap: 14px; }
  .bul p { font-size: var(--pt); font-weight: 800; line-height: 1.25; color: #111; background: #fff; border: 5px solid #111; padding: 10px 18px;
    box-shadow: 8px 8px 0 #00f5d4; }
  .bul p:nth-child(even) { box-shadow: 8px 8px 0 #ffde00; }
  .bul .num { color: #ff006e; }
  .foot { color: #fff; }
  .v-ask .say { background: #00f5d4; }
"""


def poppop_page(story, font, image_url, date, handle, place, asks):
    word = {"breaking": "ALERT", "money": "PRICE", "happy": "WOW"}.get(story.mood, "NEWS")
    bul = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="giant">{word} {word}</div><div class="blockA"></div><div class="blockB"></div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}<div class="stamp">{esc(place or word)}</div></div>
    <div class="hl">{_hl(story)}</div>
    {f'<div class="bul">{bul}</div>' if bul else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 70) + POP_CSS, font, body)


# ---------------------------------------------------------------------------------------------- cinema
CINEMA_CSS = """
  body { background: #050505; }
  .bgpic { position: absolute; left: 0; right: 0; top: 0; height: 1250px; background: #222 center/cover no-repeat;
    filter: contrast(1.2) saturate(1.2) sepia(.15); }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 22%,
    rgba(0,0,0,.2) 55%, #050505 100%), radial-gradient(ellipse at 50% 40%, transparent 40%, rgba(0,0,0,.7) 100%); }
  .frame { position: absolute; inset: 22px; border: 3px solid rgba(233,196,106,.7); z-index: 4; pointer-events: none;
    box-shadow: inset 0 0 0 10px rgba(233,196,106,.12); }
  .handle { top: 40px; right: 46px; z-index: 6; }
  .sym { top: 44px; left: 46px; right: auto; }
  .pre { text-align: center; color: #e9c46a; font: 700 32px/1.3 Georgia, serif; letter-spacing: 10px; text-transform: uppercase; }
  .hl { gap: 0; }
  .hl div { background: linear-gradient(180deg, #fff6d5 0%, #f2c14e 40%, #b8860b 55%, #ffe8a3 75%, #c9962c 100%); -webkit-background-clip: text;
    background-clip: text; color: transparent; filter: drop-shadow(0 4px 0 #5c3d00) drop-shadow(0 10px 18px rgba(0,0,0,.8)); padding: 0 20px 10px; }
  .tagline { text-align: center; color: #f1faee; font: italic 600 calc(var(--pt) * 1.05)/1.35 Georgia, '%FONT%', serif; }
  .tagline .num { color: #e9c46a; font-style: normal; }
  .stars { text-align: center; color: #e9c46a; font-size: 48px; letter-spacing: 12px; }
  .credits { display: flex; flex-direction: column; gap: 6px; text-align: center; border-top: 2px solid rgba(233,196,106,.5);
    border-bottom: 2px solid rgba(233,196,106,.5); padding: 14px 10px; }
  .credits p { font-size: calc(var(--pt) * .9); font-weight: 600; line-height: 1.35; color: #d8d8d8; letter-spacing: .5px; }
  .credits .num { color: #e9c46a; }
  .date { text-align: center; color: #fff; font: 800 44px/1 Georgia, serif; letter-spacing: 6px; }
  .v-ask .say { background: linear-gradient(90deg, #f2c14e, #e9c46a); }
  .foot { color: #bbb; }
"""


def cinema_page(story, font, image_url, date, handle, place, asks):
    credits = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div><div class="frame"></div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="pre">{esc(handle)} presents</div>
    <div class="grow"></div>
    <div class="hl">{_hl(story)}</div>
    {f'<div class="tagline">“{highlight_numbers(story.subheadline)}”</div>' if story.subheadline else ""}
    <div class="stars">★ ★ ★ ★ ★</div>
    {f'<div class="credits">{credits}</div>' if credits else ""}
    <div class="date">{esc(place or "VALSAD")} • {esc(date)}</div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page((_base(font, 120) + CINEMA_CSS).replace("%FONT%", font), font, body)


PRO_LAYOUTS = {"hero3d": hero3d_page, "glass3d": glass3d_page, "poppop": poppop_page, "cinema": cinema_page}
