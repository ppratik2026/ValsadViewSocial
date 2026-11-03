"""Ten more creative object-style layouts for the viral design (after the ticket / map / calendar family):

  crackglass   the photo behind cracked glass: the headline on a sharp shard, a bullet-hole style crack
  spotlight    a theatre stage: red velvet curtains, a spotlight beam on the headline, points on stage cards
  retrotv      an old wooden CRT television with knobs: the photo on the curved screen, headline on the cabinet
  detective    an investigation board: photo and notes pinned on cork, joined by red strings
  weatherapp   a weather app screen: big temperature-style number, condition icon, forecast cards (weather news)
  graffiti     a brick wall with the headline sprayed in paint with drips, points on paste-up posters
  telegram     an old telegram form: stamped header, typed headline in capitals style, "STOP" separators
  flapboard    an airport split-flap departure board: every line on flipping tiles, points as board rows
  laptop       a laptop with a browser-like news page open (no real site or brand): photo, headline, points
  openbook     an open book: photo on the left page, the story on the right page, a ribbon bookmark

Shared contract with src/viral.FIT: #main, .hl div lines, --hl, --pt, --ask, --top, --min-top, .grow.
No brands, logos or real people are drawn; numbers only come from the story.
"""
import re

from src.designs import esc, highlight_numbers
from src.icons import icon_img
from src.viral_more import SYM, _askbar, _base, _bg, _foot, _hl, _page, _pts


# ------------------------------------------------------------------------------------------ crackglass
CRACK_CSS = """
  body { background: #05070d; }
  .bgpic { position: absolute; inset: 0; background: #222 center/cover no-repeat; filter: saturate(1.1) brightness(.75); }
  .glass { position: absolute; inset: 0; z-index: 1;
    background:
      linear-gradient(32deg, transparent 49.6%, rgba(255,255,255,.75) 49.8%, transparent 50.2%) 0 0/100% 100%,
      linear-gradient(118deg, transparent 49.6%, rgba(255,255,255,.65) 49.8%, transparent 50.2%) 0 0/100% 100%,
      linear-gradient(74deg, transparent 49.7%, rgba(255,255,255,.55) 49.85%, transparent 50.1%) 0 0/100% 100%,
      linear-gradient(160deg, transparent 49.7%, rgba(255,255,255,.5) 49.85%, transparent 50.1%) 0 0/100% 100%,
      radial-gradient(circle at 62% 30%, rgba(255,255,255,.9) 0 6px, rgba(255,255,255,.25) 7px 26px, transparent 60px),
      repeating-conic-gradient(from 10deg at 62% 30%, transparent 0 22deg, rgba(255,255,255,.35) 22deg 22.6deg);
    mix-blend-mode: screen; }
  .shade { position: absolute; inset: 0; z-index: 1; background: linear-gradient(180deg, rgba(0,0,0,.2) 0%, rgba(0,0,0,.15) 30%, rgba(5,7,13,.92) 62%); }
  .handle { top: 30px; right: 30px; }
  .sym { top: 30px; left: 30px; right: auto; }
  .shard { background: linear-gradient(135deg, rgba(255,255,255,.95), rgba(220,235,255,.85)); color: #0b1020; padding: 24px 30px 30px;
    clip-path: polygon(0 8%, 22% 0, 100% 4%, 96% 92%, 70% 100%, 3% 95%); box-shadow: 0 20px 40px rgba(0,0,0,.5); }
  .shard small { display: block; color: #d00000; font-size: 36px; font-weight: 800; }
  .shard .hl div { color: #0b1020; }
  .shard .hl .hi { color: #d00000; }
  .frag { display: flex; flex-direction: column; gap: 14px; }
  .frag p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #fff; padding: 12px 22px; background: rgba(255,255,255,.08);
    border: 2px solid rgba(255,255,255,.35); clip-path: polygon(0 0, 100% 6%, 98% 100%, 2% 92%); }
  .frag .num { color: #ffd60a; }
"""


def crackglass_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div><div class="glass"></div><div class="shade"></div>{SYM if image_url else ""}
  <div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="grow"></div>
    <div class="shard"><small>⚡ {esc(place or story.kicker or "બ્રેકિંગ")}</small><div class="hl">{_hl(story)}</div></div>
    {f'<div class="frag">{pts}</div>' if pts else ""}
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 520, 300) + CRACK_CSS, font, body)


# ------------------------------------------------------------------------------------------- spotlight
SPOT_CSS = """
  body { background: #0a0004; }
  .curtain { position: absolute; top: 0; bottom: 0; width: 170px; z-index: 3;
    background: repeating-linear-gradient(90deg, #6a040f 0 30px, #9d0208 30px 50px, #370617 50px 64px); box-shadow: 0 0 40px #000; }
  .curtain.l { left: 0; border-radius: 0 0 60% 0; } .curtain.r { right: 0; border-radius: 0 0 0 60%; }
  .valance { position: absolute; left: 0; right: 0; top: 0; height: 110px; z-index: 4;
    background: radial-gradient(circle at 50% 0, #9d0208 0 60px, transparent 61px) 0 0/120px 110px repeat-x, #6a040f;
    border-bottom: 8px solid #e9c46a; }
  .beam { position: absolute; left: 50%; top: 0; width: 900px; height: 1500px; transform: translateX(-50%); z-index: 1;
    background: radial-gradient(ellipse at 50% 100%, rgba(255,244,200,.55) 0%, rgba(255,244,200,.12) 45%, transparent 70%);
    clip-path: polygon(44% 0, 56% 0, 100% 100%, 0 100%); }
  .floor { position: absolute; left: 0; right: 0; bottom: 0; height: 560px; z-index: 0;
    background: repeating-linear-gradient(90deg, #3a1f0f 0 90px, #4a2a14 90px 180px); }
  #main { left: 190px; right: 190px; top: 140px; z-index: 5; }
  .handle { top: 22px; right: 30px; z-index: 7; }
  .star { align-self: center; color: #e9c46a; font-size: 34px; font-weight: 800; letter-spacing: 6px; }
  .hl div { color: #fff8e1; text-shadow: 0 0 20px rgba(255,240,180,.7), 0 6px 0 rgba(0,0,0,.4); }
  .hl .hi { color: #ffd60a; }
  .photo { position: relative; height: 420px; border-radius: 50% 50% 20px 20px / 18% 18% 20px 20px; background: #333 center/cover no-repeat;
    border: 8px solid #e9c46a; box-shadow: 0 0 50px rgba(255,240,180,.5); }
  .photo .sym { bottom: 10px; }
  .cards p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #2b1400; background: #fff3c4; border-radius: 12px;
    padding: 12px 18px; margin-bottom: 12px; box-shadow: 0 8px 18px rgba(0,0,0,.5); }
  .cards p:nth-child(odd) { transform: rotate(-1.2deg); } .cards p:nth-child(even) { transform: rotate(1.2deg); }
  .cards .num { color: #9d0208; }
  .v-ask .q { width: 90px; height: 90px; font-size: 64px; line-height: 80px; }
"""


def spotlight_page(story, font, image_url, date, handle, place, asks):
    cards = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="floor"></div><div class="beam"></div><div class="curtain l"></div><div class="curtain r"></div><div class="valance"></div>
  <div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="star">★ {esc(place or story.kicker or "")} ★</div>
    <div class="hl">{_hl(story)}</div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="cards">{cards}</div>' if cards else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 140) + SPOT_CSS, font, body)


# --------------------------------------------------------------------------------------------- retrotv
RETRO_CSS = """
  body { background: radial-gradient(circle at 50% 30%, #f4a261 0%, #e76f51 50%, #6d2e1f 100%); }
  .handle { top: 30px; right: 30px; }
  .tv { position: relative; background: linear-gradient(180deg, #8b5a2b, #5c3a1a); border-radius: 40px; padding: 30px 30px 26px;
    box-shadow: inset 0 0 0 8px #3e2510, 0 26px 50px rgba(0,0,0,.5); display: grid; grid-template-columns: 1fr 150px; gap: 22px; }
  .tv::before, .tv::after { content: ""; position: absolute; top: -70px; width: 8px; height: 110px; background: #333; }
  .tv::before { left: 38%; transform: rotate(-30deg); } .tv::after { left: 55%; transform: rotate(30deg); }
  .screen { position: relative; height: 560px; border-radius: 60px / 40px; overflow: hidden; background: #222 center/cover no-repeat;
    border: 14px solid #1b1b1b; box-shadow: inset 0 0 60px rgba(0,0,0,.8); }
  .screen::after { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.2) 0 3px, transparent 3px 6px),
    radial-gradient(ellipse at 30% 20%, rgba(255,255,255,.25), transparent 50%); }
  .screen .sym { bottom: 12px; z-index: 2; }
  .knobs { display: flex; flex-direction: column; align-items: center; gap: 30px; padding-top: 20px; }
  .knobs i { width: 100px; height: 100px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #ddd, #555); border: 6px solid #222; }
  .knobs b { width: 110px; height: 160px; background: repeating-linear-gradient(0deg, #222 0 6px, #5c3a1a 6px 12px); border-radius: 12px; }
  .ch { position: absolute; left: 70px; top: 54px; z-index: 3; background: rgba(0,0,0,.6); color: #7CFC00; font: 800 34px/1 'Courier New', monospace;
    padding: 8px 14px; }
  .hl div { color: #fff; text-shadow: 0 5px 0 #6d2e1f; }
  .hl .hi { color: #ffe66d; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #3e2510; background: #fdf0d5; border-left: 12px solid #e76f51;
    padding: 10px 18px; border-radius: 10px; margin-bottom: 12px; }
  .pts .num { color: #c1121f; }
"""


def retrotv_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="tv"><div class="screen"{_bg(image_url)}>{SYM if image_url else ""}</div><div class="knobs"><i></i><i></i><b></b></div>
      <div class="ch">CH-1 • {esc(place or "LIVE")}</div></div>
    <div class="hl">{_hl(story)}</div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 110) + RETRO_CSS, font, body)


# ------------------------------------------------------------------------------------------- detective
DET_CSS = """
  body { background: #a0703f; background-image: radial-gradient(rgba(0,0,0,.15) 1.5px, transparent 2px), radial-gradient(rgba(255,255,255,.08) 1px, transparent 2px);
    background-size: 18px 18px, 27px 27px; }
  .strings { position: absolute; inset: 0; z-index: 3; pointer-events: none; }
  .handle { top: 30px; right: 30px; }
  .case { align-self: flex-start; background: #fff; color: #111; font: 800 34px/1.1 'Courier New', monospace; padding: 10px 20px; transform: rotate(-3deg);
    box-shadow: 0 8px 16px rgba(0,0,0,.35); }
  .case b { color: #c1121f; }
  .top2 { display: flex; flex-direction: column; gap: 26px; }
  .photo { position: relative; height: 420px; width: 78%; align-self: center; background: #ccc center/cover no-repeat; border: 14px solid #fff; border-bottom-width: 50px;
    transform: rotate(-4deg); box-shadow: 0 14px 26px rgba(0,0,0,.4); }
  .photo .sym { bottom: -40px; background: none; color: #444; }
  .pin::before { content: ""; position: absolute; top: -14px; left: 50%; width: 30px; height: 30px; margin-left: -15px; border-radius: 50%; z-index: 4;
    background: radial-gradient(circle at 35% 35%, #ff6b6b, #8b0000); box-shadow: 0 4px 6px rgba(0,0,0,.5); }
  .clip2 { position: relative; background: #fffbe6; padding: 22px 20px; transform: rotate(3deg); box-shadow: 0 12px 24px rgba(0,0,0,.4); }
  .clip2 .hl { align-items: flex-start; gap: 0; }
  .clip2 .hl div { color: #111; text-align: left; padding: 0 0 4px; }
  .clip2 .hl .hi { color: #c1121f; background: #ffe066; }
  .notes { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }
  .notes p { position: relative; font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #111; background: #fff; padding: 22px 16px 14px;
    box-shadow: 0 10px 20px rgba(0,0,0,.35); }
  .notes p:nth-child(odd) { transform: rotate(-2deg); background: #fff3b0; } .notes p:nth-child(even) { transform: rotate(2.5deg); }
  .notes p.wide { grid-column: 1 / -1; }
  .notes .num { color: #c1121f; }
  .foot { color: #fff; }
"""


def detective_page(story, font, image_url, date, handle, place, asks):
    pts = _pts(story, 4)
    notes = "".join(f'<p class="pin{" wide" if len(pts) % 2 and i == len(pts) - 1 else ""}">{highlight_numbers(p)}</p>'
                    for i, p in enumerate(pts))
    strings = ('<svg class="strings" viewBox="0 0 1080 1920" preserveAspectRatio="none">'
               '<path d="M290 330 L800 360 L520 1150 L240 1420 M800 360 L820 1420" stroke="#c1121f" stroke-width="5" fill="none" '
               'stroke-dasharray="2600"/></svg>')
    body = f"""{strings}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="case">CASE FILE • <b>{esc(place or "વલસાડ")}</b></div>
    <div class="top2"><div class="photo pin"{_bg(image_url)}>{SYM if image_url else ""}</div>
      <div class="clip2 pin"><div class="hl">{_hl(story)}</div></div></div>
    {f'<div class="notes">{notes}</div>' if notes else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 120) + DET_CSS, font, body)


# ------------------------------------------------------------------------------------------ weatherapp
WEATHER_CSS = """
  body { background: linear-gradient(180deg, #1e3c72 0%, #2a5298 45%, #6a85b6 100%); }
  .rain { position: absolute; inset: 0; background-image: linear-gradient(105deg, transparent 48%, rgba(255,255,255,.35) 50%, transparent 52%);
    background-size: 26px 90px; opacity: .5; }
  .handle { top: 30px; right: 30px; }
  .loc { text-align: center; color: #fff; font-size: 46px; font-weight: 800; }
  .big { display: flex; align-items: center; justify-content: center; gap: 20px; color: #fff; }
  .big .ic { width: 220px; height: 220px; filter: drop-shadow(0 16px 20px rgba(0,0,0,.35)); }
  .big b { font: 200 200px/1 'Arial', sans-serif; letter-spacing: -6px; }
  .cond { text-align: center; color: #dbe7ff; font-size: 40px; font-weight: 700; }
  .card { background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.35); border-radius: 34px; padding: 18px 22px; backdrop-filter: blur(8px); }
  .card .hl div { color: #fff; }
  .card .hl .hi { color: #ffd60a; }
  .row { display: flex; gap: 14px; }
  .day { flex: 1; text-align: center; background: rgba(255,255,255,.14); border-radius: 26px; padding: 14px 8px; color: #fff; }
  .day .ic { width: 70px; height: 70px; }
  .day small { display: block; font-size: 26px; font-weight: 700; color: #dbe7ff; }
  .day b { display: block; font-size: 30px; line-height: 1.2; }
  .alerts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #fff; padding: 10px 18px; border-radius: 18px; background: rgba(208,0,0,.55);
    margin-bottom: 10px; }
  .alerts .num { color: #ffd60a; }
  .photo { position: relative; height: 280px; border-radius: 30px; background: #2a5298 center/cover no-repeat; }
  .photo .sym { bottom: 10px; }
"""


def weatherapp_page(story, font, image_url, date, handle, place, asks):
    text = f"{story.headline} {story.summary}"
    icon = "storm" if re.search(r"વાવાઝોડ|ચક્રવાત|cyclone", text) else "rain" if re.search(r"વરસાદ|માવઠ|rain", text) else "sun"
    num = next((f["value"] for f in story.facts if re.search(r"\d", f["value"]) and len(f["value"]) <= 6), "")
    days = "".join(f'<div class="day"><small>{esc(f["label"])[:16]}</small>{icon_img(icon)}<b>{esc(f["value"])}</b></div>'
                   for f in story.facts[:3])
    alerts = "".join(f"<p>⚠ {highlight_numbers(p)}</p>" for p in _pts(story, 2))
    body = f"""<div class="rain"></div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="loc">📍 {esc(place or "વલસાડ")}</div>
    <div class="big">{icon_img(icon)}{f"<b>{esc(num)}</b>" if num else ""}</div>
    <div class="cond">{esc(story.kicker or "હવામાન અપડેટ")}</div>
    <div class="card"><div class="hl">{_hl(story)}</div></div>
    {f'<div class="row">{days}</div>' if days else ""}
    {f'<div class="alerts">{alerts}</div>' if alerts else ""}
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 90) + WEATHER_CSS, font, body)


# -------------------------------------------------------------------------------------------- graffiti
GRAFFITI_CSS = """
  body { background: #7a3b2e;
    background-image: linear-gradient(0deg, rgba(0,0,0,.35) 4px, transparent 4px), linear-gradient(90deg, rgba(0,0,0,.35) 4px, transparent 4px),
      linear-gradient(90deg, rgba(0,0,0,.35) 4px, transparent 4px);
    background-size: 160px 70px, 160px 140px, 160px 140px; background-position: 0 0, 0 0, 80px 70px; }
  body::after { content: ""; position: absolute; inset: 0; background: radial-gradient(circle at 50% 30%, transparent 30%, rgba(0,0,0,.55) 100%); }
  .handle { top: 30px; right: 30px; z-index: 6; }
  .tag { align-self: flex-start; font: 900 52px/1 'Arial Black', Arial, sans-serif; color: #00f5d4; transform: rotate(-6deg);
    text-shadow: 0 0 8px #00f5d4, 3px 3px 0 #000; }
  .hl div { color: #ffe600; -webkit-text-stroke: 4px #111; paint-order: stroke fill; text-shadow: 6px 6px 0 #ff006e;
    filter: url(#rough); }
  .hl div:nth-child(even) { color: #fff; text-shadow: 6px 6px 0 #3a86ff; }
  .hl .hi { color: #ff006e; text-shadow: 6px 6px 0 #ffe600; }
  .drips { height: 50px; margin-top: -26px; background: radial-gradient(circle at 10px 40px, #ffe600 0 9px, transparent 10px) 0 0/90px 50px,
    linear-gradient(90deg, transparent 0 6px, #ffe600 6px 14px, transparent 14px) 0 0/90px 40px; opacity: .85; }
  .paste { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .paste p { font-size: var(--pt); font-weight: 800; line-height: 1.3; color: #111; background: #f1faee; padding: 16px; transform: rotate(-2deg);
    box-shadow: 0 8px 16px rgba(0,0,0,.45); }
  .paste p:nth-child(even) { transform: rotate(2deg); background: #ffd6e0; }
  .paste p.wide { grid-column: 1 / -1; }
  .paste .num { color: #d00000; }
  .photo { position: relative; height: 380px; background: #333 center/cover no-repeat; border: 10px solid #f1faee; transform: rotate(1.5deg);
    box-shadow: 0 12px 24px rgba(0,0,0,.5); }
  .photo .sym { bottom: 8px; }
  .foot { color: #fff; }
"""


def graffiti_page(story, font, image_url, date, handle, place, asks):
    pts = _pts(story, 4)
    paste = "".join(f'<p class="{"wide" if len(pts) % 2 and i == len(pts) - 1 else ""}">{highlight_numbers(p)}</p>'
                    for i, p in enumerate(pts))
    rough = ('<svg width="0" height="0" style="position:absolute"><filter id="rough"><feTurbulence baseFrequency=".04" numOctaves="2"/>'
             '<feDisplacementMap in="SourceGraphic" scale="4"/></filter></svg>')
    body = f"""{rough}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="tag">#{esc((place or "Valsad").split(" - ")[0])}</div>
    <div class="hl">{_hl(story)}</div>
    <div class="drips"></div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="paste">{paste}</div>' if paste else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 80) + GRAFFITI_CSS, font, body)


# -------------------------------------------------------------------------------------------- telegram
TELE_CSS = """
  body { background: #c9b79c; }
  .form { position: absolute; left: 40px; right: 40px; top: 40px; bottom: 40px; background: #f5ecd7; box-shadow: 0 14px 40px rgba(0,0,0,.35);
    background-image: repeating-linear-gradient(180deg, transparent 0 68px, rgba(120,90,50,.18) 68px 70px); }
  #main { left: 80px; right: 80px; top: 80px; bottom: 70px; }
  .head { display: flex; justify-content: space-between; align-items: center; border-bottom: 6px double #5c4033; padding-bottom: 10px; }
  .head b { font: 900 70px/1 'Courier New', monospace; letter-spacing: 10px; color: #5c4033; }
  .head span { border: 5px solid #b5001b; color: #b5001b; font: 800 30px/1.1 'Courier New', monospace; padding: 8px 14px; transform: rotate(8deg); text-align: center; }
  .meta { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 20px; font: 700 28px/1.3 'Courier New', monospace; color: #5c4033; }
  .meta i { font-style: normal; color: #111; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { color: #111; text-align: left; padding: 0 0 4px; }
  .hl .hi { color: #b5001b; }
  .body p { font-size: var(--pt); font-weight: 700; line-height: 1.45; color: #222; }
  .body p::after { content: "  — STOP —"; font: 800 26px 'Courier New', monospace; color: #b5001b; }
  .body .num { color: #b5001b; }
  .photo { position: relative; height: 320px; width: 70%; align-self: flex-end; background: #999 center/cover no-repeat; border: 10px solid #fff;
    transform: rotate(3deg); filter: sepia(.4); box-shadow: 0 8px 16px rgba(0,0,0,.3); }
  .photo .sym { bottom: 8px; }
  .foot { color: #5c4033; }
  .v-ask .say { background: #5c4033; color: #f5ecd7; }
"""


def telegram_page(story, font, image_url, date, handle, place, asks):
    body_pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="form"></div>
  <div id="main">
    <div class="head"><b>TELEGRAM</b><span>તાત્કાલિક<br>URGENT</span></div>
    <div class="meta"><div>FROM: <i>{esc(handle)}</i></div><div>TO: <i>{esc(place or "વલસાડ")}</i></div><div>DATE: <i>{esc(date)}</i></div>
      <div>SUBJ: <i>{esc(story.kicker or "સમાચાર")}</i></div></div>
    <div class="hl">{_hl(story)}</div>
    {f'<div class="body">{body_pts}</div>' if body_pts else ""}
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 80) + TELE_CSS, font, body)


# ------------------------------------------------------------------------------------------- flapboard
FLAP_CSS = """
  body { background: #101418; }
  .handle { top: 30px; right: 30px; }
  .board { background: #1b1f24; border: 10px solid #2b3036; border-radius: 18px; padding: 20px; box-shadow: 0 20px 40px rgba(0,0,0,.6); }
  .board .t { display: flex; justify-content: space-between; color: #ffcc00; font: 800 32px/1 'Courier New', monospace; padding-bottom: 14px;
    border-bottom: 3px solid #2b3036; margin-bottom: 12px; }
  .board .hl div { color: #fff; background: linear-gradient(180deg, #2a2f35 0 49%, #111 49% 51%, #22272c 51%); border-radius: 8px;
    margin-bottom: 6px; padding: 6px 24px 12px; }
  .board .hl .hi { color: #ffcc00; }
  .rows { display: flex; flex-direction: column; gap: 10px; }
  .rw { display: grid; grid-template-columns: 90px 1fr; gap: 12px; align-items: center; background: #1b1f24; border-radius: 10px; padding: 10px 12px; }
  .rw b { background: #ffcc00; color: #111; font: 900 34px/56px 'Courier New', monospace; text-align: center; border-radius: 8px; }
  .rw p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #e6e6e6; }
  .rw .num { color: #ffcc00; }
  .photo { position: relative; height: 380px; border-radius: 18px; background: #333 center/cover no-repeat; border: 6px solid #2b3036; }
  .photo .sym { bottom: 10px; }
  .status { align-self: center; background: #2ecc71; color: #062; font: 900 34px/1 'Courier New', monospace; padding: 12px 26px; border-radius: 10px; }
"""


def flapboard_page(story, font, image_url, date, handle, place, asks):
    rows = "".join(f'<div class="rw"><b>{i:02d}</b><p>{highlight_numbers(p)}</p></div>' for i, p in enumerate(_pts(story, 4), 1))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="board"><div class="t"><span>✈ {esc(place or "VALSAD")}</span><span>{esc(date)}</span></div><div class="hl">{_hl(story)}</div></div>
    <div class="status">● {esc(story.kicker or "ON TIME")}</div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="rows">{rows}</div>' if rows else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 100) + FLAP_CSS, font, body)


# ---------------------------------------------------------------------------------------------- laptop
LAPTOP_CSS = """
  body { background: linear-gradient(180deg, #e0e7ef 0%, #c3cfe2 100%); }
  .handle { top: 30px; right: 30px; }
  .lid { background: #1f2933; border-radius: 30px 30px 0 0; padding: 22px 22px 16px; box-shadow: 0 20px 40px rgba(0,0,0,.3); }
  .scr { background: #fff; border-radius: 10px; overflow: hidden; }
  .bar { display: flex; align-items: center; gap: 10px; background: #e5e7eb; padding: 10px 14px; }
  .bar i { width: 18px; height: 18px; border-radius: 50%; background: #ef4444; } .bar i:nth-child(2) { background: #f59e0b; } .bar i:nth-child(3) { background: #22c55e; }
  .bar span { flex: 1; background: #fff; border-radius: 30px; padding: 6px 18px; font: 600 24px/1.2 Arial, sans-serif; color: #555; margin-left: 10px; }
  .page { padding: 18px 22px; display: flex; flex-direction: column; gap: 12px; }
  .page small { color: #d00000; font-size: 30px; font-weight: 800; }
  .page .hl { align-items: flex-start; gap: 0; }
  .page .hl div { color: #111; text-align: left; padding: 0 0 4px; }
  .page .hl .hi { color: #d00000; }
  .img { position: relative; height: 380px; background: #ccc center/cover no-repeat; border-radius: 8px; }
  .img .sym { bottom: 8px; }
  .page p { font-size: var(--pt); font-weight: 600; line-height: 1.35; color: #333; padding-left: 18px; border-left: 6px solid #d00000; }
  .page .num { color: #d00000; font-weight: 800; }
  .base { height: 46px; margin: 0 -40px; background: linear-gradient(180deg, #cbd2d9, #9aa5b1); border-radius: 0 0 40px 40px; }
  .foot { color: #333; }
"""


def laptop_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="lid"><div class="scr"><div class="bar"><i></i><i></i><i></i><span>🔒 {esc(handle.lstrip("@"))}.news / {esc(place or "valsad")}</span></div>
      <div class="page"><small>{esc(story.kicker or "તાજા સમાચાર")}</small><div class="hl">{_hl(story)}</div>
        <div class="img"{_bg(image_url)}>{SYM if image_url else ""}</div>{pts}</div></div></div>
    <div class="base"></div>
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 90) + LAPTOP_CSS, font, body)


# -------------------------------------------------------------------------------------------- openbook
BOOK_CSS = """
  body { background: radial-gradient(circle at 50% 40%, #5e3023 0%, #2b1510 100%); }
  .handle { top: 30px; right: 30px; }
  .title { text-align: center; color: #e9c46a; font: 700 40px/1.2 Georgia, serif; letter-spacing: 4px; }
  .book { position: relative; display: grid; grid-template-columns: 0.85fr 1.15fr; background: #fdf6e3; border-radius: 10px 10px 20px 20px;
    box-shadow: 0 0 0 10px #6b2d1a, 0 30px 50px rgba(0,0,0,.6); min-height: 1000px; }
  .book::before { content: ""; position: absolute; left: 50%; top: 0; bottom: 0; width: 60px; margin-left: -30px;
    background: linear-gradient(90deg, transparent, rgba(0,0,0,.18), transparent); }
  .ribbon { position: absolute; right: 120px; top: -10px; width: 46px; height: 260px; background: #c1121f; z-index: 2;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 88%, 0 100%); }
  .left, .right { padding: 34px 26px; display: flex; flex-direction: column; gap: 16px; min-width: 0; }
  .left .img { position: relative; flex: 1; min-height: 520px; background: #ccc center/cover no-repeat; border: 8px solid #fff; box-shadow: 0 8px 16px rgba(0,0,0,.2); }
  .left .img .sym { bottom: 8px; }
  .left small { font: italic 700 30px/1.3 Georgia, serif; color: #6b2d1a; text-align: center; }
  .right .hl { align-items: flex-start; gap: 0; }
  .right .hl div { color: #2b1510; text-align: left; padding: 0 0 4px; }
  .right .hl .hi { color: #c1121f; }
  .right p { font-size: var(--pt); font-weight: 600; line-height: 1.45; color: #3d2b1f; }
  .right p:first-of-type::first-line { font-weight: 800; }
  .right .num { color: #c1121f; font-weight: 800; }
  .pg { margin-top: auto; text-align: center; font: 700 24px Georgia, serif; color: #8a7a55; }
  .foot { color: #e9c46a; }
"""


def openbook_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="title">📖 {esc(place or "વલસાડ")}ની વાત</div>
    <div class="book"><div class="ribbon"></div>
      <div class="left"><div class="img"{_bg(image_url)}>{SYM if image_url else ""}</div><small>{esc(story.kicker or "")}</small><div class="pg">— ૧ —</div></div>
      <div class="right"><div class="hl">{_hl(story, max(3, len(story.headline) // 7))}</div>{pts}<div class="pg">— ૨ —</div></div></div>
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 80) + BOOK_CSS, font, body)


NEW_LAYOUTS = {
    "crackglass": crackglass_page, "spotlight": spotlight_page, "retrotv": retrotv_page, "detective": detective_page,
    "weatherapp": weatherapp_page, "graffiti": graffiti_page, "telegram": telegram_page, "flapboard": flapboard_page,
    "laptop": laptop_page, "openbook": openbook_page,
}
