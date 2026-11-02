"""Ten more creative layouts for the viral design (none repeats the 27 before them):

  notebook   a lined notebook page with spiral binding, highlighter marks and a paper clip photo
  billboard  a roadside billboard on poles against the sky, the story on the board
  letter     an envelope with a postage stamp and a letter "પ્રિય વલસાડવાસીઓ,"
  crimetape  yellow police tape across the photo, case-file style points (crime stories)
  collage    a photo collage of four crops of the picture, the headline on a torn paper band
  radio      an audio player: play button, waveform, the points as chapters
  countdown  "N દિવસ બાકી": a big countdown to a date in the story (only when that date is ahead)
  percent    a big ring chart for a percentage in the story (only when there is one)
  folder     a manila case folder with a paper clip, a typed sheet and a "તપાસ ચાલુ" stamp
  roadsign   a green highway sign with white letters, km-stone style facts (roads and travel)

Shared contract with src/viral.FIT: #main, .hl div lines, --hl, --pt, --ask, --top, --min-top, .grow.
No brands, logos or real people are drawn; numbers only ever come from the story itself.
"""
import re
from datetime import date as Date

from src.designs import esc, highlight_numbers
from src.icons import icon_img
from src.viral_layouts import _ask
from src.viral_more import SYM, _askbar, _base, _bg, _foot, _hl, _page, _pts

MONTHS = {"જાન્યુ": 1, "ફેબ્રુ": 2, "માર્ચ": 3, "એપ્રિલ": 4, "મે": 5, "જૂન": 6, "જુલાઈ": 7, "ઓગસ્ટ": 8, "સપ્ટે": 9,
          "ઓક્ટો": 10, "નવે": 11, "ડિસે": 12}


# -------------------------------------------------------------------------------------------- notebook
NOTEBOOK_CSS = """
  body { background: #c9d6df; color: #1b263b; }
  .page { position: absolute; left: 70px; right: 30px; top: 30px; bottom: 30px; background: #fffef8; border-radius: 10px;
    box-shadow: 0 16px 40px rgba(0,0,0,.25);
    background-image: linear-gradient(90deg, transparent 88px, #ff8fa3 88px, #ff8fa3 92px, transparent 92px),
      repeating-linear-gradient(180deg, transparent 0 62px, #a9c7e8 62px 64px); }
  .rings { position: absolute; left: 30px; top: 60px; bottom: 60px; width: 70px; z-index: 3; display: flex; flex-direction: column;
    justify-content: space-between; }
  .rings i { height: 34px; border-radius: 20px; border: 8px solid #6c757d; border-left-color: transparent; }
  #main { left: 190px; right: 60px; top: 70px; bottom: 60px; }
  .handle { top: 50px; right: 60px; background: #1b263b; }
  .topic { align-self: flex-start; font-size: 38px; font-weight: 800; color: #6a4c93; background: linear-gradient(transparent 55%, #ffe066 55%); }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 4px; color: #1b263b; }
  .hl .hi { background: linear-gradient(transparent 50%, #ffadad 50%); color: #c1121f; }
  .clip { position: relative; height: 360px; width: 86%; transform: rotate(-2.5deg); border: 12px solid #fff;
    box-shadow: 0 10px 24px rgba(0,0,0,.25); background: #ccc center/cover no-repeat; }
  .clip::before { content: ""; position: absolute; top: -40px; left: 60px; width: 40px; height: 110px; border: 7px solid #adb5bd;
    border-radius: 20px; z-index: 2; }
  .clip .sym { bottom: 8px; }
  .lines p { font-size: var(--pt); font-weight: 700; line-height: 1.45; padding-left: 50px; position: relative; color: #1b263b; }
  .lines p::before { content: "✔"; position: absolute; left: 0; color: #2a9d8f; }
  .lines .num { background: linear-gradient(transparent 55%, #b9fbc0 55%); }
  .foot { color: #495057; }
"""


def notebook_page(story, font, image_url, date, handle, place, asks):
    lines = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 4))
    body = f"""<div class="page"></div><div class="rings">{"<i></i>" * 14}</div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="topic">{esc(story.kicker or place or "આજની નોંધ")}</div>
    <div class="hl">{_hl(story)}</div>
    <div class="clip"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="lines">{lines}</div>' if lines else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 70) + NOTEBOOK_CSS, font, body)


# ------------------------------------------------------------------------------------------- billboard
BILLBOARD_CSS = """
  body { background: linear-gradient(180deg, #4facfe 0%, #8fd3fe 45%, #f9d29d 75%, #7a9e3d 75%, #5b7f2a 100%); }
  .sun { position: absolute; right: 120px; top: 120px; width: 160px; height: 160px; border-radius: 50%; background: #ffe066;
    box-shadow: 0 0 80px #ffe066; }
  .cloud { position: absolute; height: 60px; border-radius: 40px; background: rgba(255,255,255,.85); }
  .poles { position: absolute; left: 0; right: 0; top: 1150px; height: 600px; display: flex; justify-content: center; gap: 420px; }
  .poles i { width: 34px; background: linear-gradient(90deg, #555, #999, #555); }
  .handle { top: 30px; left: 30px; }
  .board { background: #fff; border: 16px solid #2b2d42; border-radius: 10px; box-shadow: 0 30px 40px rgba(0,0,0,.35); overflow: hidden;
    display: grid; grid-template-columns: 1fr 1fr; position: relative; z-index: 2; }
  .board .img { position: relative; background: #ccc center/cover no-repeat; min-height: 520px; }
  .board .img .sym { bottom: 8px; }
  .board .txt { background: #d00000; padding: 18px 16px; display: flex; flex-direction: column; justify-content: center; gap: 10px; }
  .board .txt .hl div { color: #fff; padding: 0 10px 6px; }
  .board .txt .hl .hi { color: #ffe066; }
  .board .txt small { color: #ffe066; font-size: 32px; font-weight: 800; text-align: center; }
  .lights { display: flex; justify-content: space-around; margin-top: -10px; position: relative; z-index: 3; }
  .lights i { width: 60px; height: 30px; background: #2b2d42; border-radius: 0 0 30px 30px; box-shadow: 0 30px 40px rgba(255,240,150,.5); }
  .ground { background: rgba(255,255,255,.92); border-radius: 26px; padding: 16px 22px; color: #1b4332; margin-top: 380px; }
  .ground p { font-size: var(--pt); font-weight: 700; line-height: 1.3; padding: 6px 0; }
  .ground .num { color: #d00000; }
  .foot { color: #fff; }
"""


def billboard_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>👉 {highlight_numbers(p)}</p>" for p in _pts(story, 2))
    clouds = ('<div class="cloud" style="left:80px;top:300px;width:260px"></div>'
              '<div class="cloud" style="left:560px;top:420px;width:200px"></div>')
    body = f"""<div class="sun"></div>{clouds}<div class="poles"><i></i><i></i></div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="board"><div class="img"{_bg(image_url)}>{SYM if image_url else ""}</div>
      <div class="txt"><small>{esc(place or story.kicker or "")}</small><div class="hl">{_hl(story)}</div></div></div>
    <div class="lights"><i></i><i></i><i></i></div>
    {f'<div class="ground">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 300, 200) + BILLBOARD_CSS, font, body)


# ---------------------------------------------------------------------------------------------- letter
LETTER_CSS = """
  body { background: #e9d8c4; color: #3d2b1f;
    background-image: repeating-linear-gradient(45deg, rgba(0,0,0,.02) 0 10px, transparent 10px 20px); }
  .env { position: absolute; left: 40px; right: 40px; top: 40px; height: 360px; background: #f6e7cf; border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,.2); overflow: hidden; }
  .env::before { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 100%;
    background: linear-gradient(160deg, transparent 49.5%, #e7d2b0 50%), linear-gradient(200deg, transparent 49.5%, #e7d2b0 50%);
    background-size: 50% 100%; background-position: left, right; background-repeat: no-repeat; }
  .env .border { position: absolute; inset: 0; border: 14px solid transparent;
    border-image: repeating-linear-gradient(45deg, #d00000 0 20px, #fff 20px 40px, #1d3fbf 40px 60px, #fff 60px 80px) 14; }
  .stampx { position: absolute; right: 80px; top: 70px; width: 170px; height: 200px; background: #fff; padding: 10px; z-index: 3;
    transform: rotate(6deg); box-shadow: 0 4px 10px rgba(0,0,0,.25); border: 4px dotted #bbb; }
  .stampx div { height: 100%; background: #2a9d8f center/cover no-repeat; }
  .postmark { position: absolute; right: 200px; top: 110px; width: 150px; height: 150px; border-radius: 50%; border: 5px solid rgba(61,43,31,.6);
    color: rgba(61,43,31,.7); display: flex; align-items: center; justify-content: center; text-align: center; font-size: 26px; font-weight: 800;
    z-index: 4; transform: rotate(-12deg); }
  .to { position: absolute; left: 100px; top: 150px; z-index: 3; font-size: 40px; font-weight: 800; line-height: 1.3; }
  .handle { top: 70px; left: 90px; z-index: 5; }
  .paper { background: #fffdf6; border-radius: 10px; padding: 26px 34px; box-shadow: 0 12px 30px rgba(0,0,0,.2);
    background-image: repeating-linear-gradient(180deg, transparent 0 58px, rgba(61,43,31,.08) 58px 60px); }
  .paper .dear { font-size: 40px; font-weight: 800; color: #6b4226; }
  .paper .hl { align-items: flex-start; gap: 0; }
  .paper .hl div { text-align: left; padding: 0 0 4px; color: #3d2b1f; }
  .paper .hl .hi { color: #c1121f; }
  .paper p { font-size: var(--pt); font-weight: 700; line-height: 1.45; }
  .paper .num { color: #c1121f; }
  .paper .sign { text-align: right; font-size: 36px; font-weight: 800; color: #6b4226; margin-top: 12px; }
  .foot { color: #6b4226; }
"""


def letter_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>• {highlight_numbers(p)}</p>" for p in _pts(story, 3))
    who = place.split(" - ")[0] if place else "વલસાડ"
    body = f"""<div class="env"><div class="border"></div></div>
  <div class="stampx"><div{_bg(image_url)}></div></div><div class="postmark">{esc(who)}<br>{esc(date.split(" 20")[0])}</div>
  <div class="to">પ્રતિ,<br>{esc(who)}ના નાગરિકો</div>
  <div id="main">
    <div class="paper"><div class="dear">પ્રિય {esc(who)}વાસીઓ,</div><div class="hl">{_hl(story)}</div>{pts}
      <div class="sign">— {esc(handle)}</div></div>
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 440, 400) + LETTER_CSS, font, body)


# ------------------------------------------------------------------------------------------- crimetape
TAPE_CSS = """
  body { background: #0b0b0b; }
  .bgpic { position: absolute; left: 0; right: 0; top: 0; height: 1000px; background: #222 center/cover no-repeat; filter: saturate(.7) brightness(.8); }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.2), rgba(0,0,0,.1) 50%, #0b0b0b); }
  .tape { position: absolute; left: -100px; right: -100px; height: 90px; background: #ffd000; color: #111; z-index: 3; display: flex;
    align-items: center; overflow: hidden; white-space: nowrap; font: 900 40px/1 'Arial Black', Arial, sans-serif; letter-spacing: 3px;
    box-shadow: 0 10px 20px rgba(0,0,0,.5); }
  .tape.a { top: 260px; transform: rotate(-12deg); }
  .tape.b { top: 470px; transform: rotate(9deg); }
  .sym { top: 30px; left: 30px; right: auto; }
  .handle { top: 30px; right: 30px; }
  .case { display: flex; align-items: center; gap: 16px; }
  .case b { background: #d00000; color: #fff; font-size: 40px; padding: 6px 22px 10px; }
  .case span { color: #ffd000; font-size: 40px; font-weight: 800; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 6px; color: #fff; }
  .hl .hi { color: #ffd000; }
  .facts { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .facts div { border: 3px solid #ffd000; padding: 10px 16px; }
  .facts small { display: block; color: #aaa; font-size: 26px; font-weight: 800; }
  .facts b { color: #fff; font-size: calc(var(--pt) * 1.1); }
  .ev p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #eee; padding: 10px 0 10px 64px; position: relative;
    border-bottom: 1px dashed #444; }
  .ev p::before { content: attr(data-n); position: absolute; left: 0; top: 8px; width: 48px; height: 48px; background: #ffd000; color: #111;
    font: 900 28px/48px Arial, sans-serif; text-align: center; }
  .ev .num { color: #ffd000; }
"""


def crimetape_page(story, font, image_url, date, handle, place, asks):
    words = "POLICE LINE • DO NOT CROSS • " * 6
    facts = "".join(f'<div><small>{esc(f["label"])}</small><b>{esc(f["value"])}</b></div>' for f in story.facts[:2])
    ev = "".join(f'<p data-n="{i}">{highlight_numbers(p)}</p>' for i, p in enumerate(_pts(story, 4), 1))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}
  <div class="tape a">{words}</div><div class="tape b">{words}</div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="case"><b>{esc(story.kicker or "ક્રાઇમ")}</b><span>📍 {esc(place or "વલસાડ")}</span></div>
    <div class="hl">{_hl(story)}</div>
    {f'<div class="facts">{facts}</div>' if facts else ""}
    {f'<div class="ev">{ev}</div>' if ev else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 720, 560) + TAPE_CSS, font, body)


# --------------------------------------------------------------------------------------------- collage
COLLAGE_CSS = """
  body { background: #fdf0d5; color: #222; }
  .grid { position: absolute; left: 0; right: 0; top: 0; height: 900px; display: grid; grid-template-columns: 1.3fr 1fr;
    grid-template-rows: 1fr 1fr; gap: 10px; padding: 10px; }
  .grid div { background: #888 center/cover no-repeat; border-radius: 14px; }
  .grid div:first-child { grid-row: 1 / 3; }
  .grid div:nth-child(2) { background-position: 20% 30%; filter: saturate(1.4); }
  .grid div:nth-child(3) { background-position: 80% 70%; filter: grayscale(1); }
  .sym { top: 860px; }
  .handle { top: 24px; left: 24px; }
  .torn { margin: 0 -30px; background: #fff; padding: 30px 40px 36px; box-shadow: 0 -6px 20px rgba(0,0,0,.25);
    clip-path: polygon(0 6%, 4% 0, 9% 5%, 15% 1%, 22% 6%, 30% 0, 37% 5%, 45% 1%, 52% 6%, 60% 0, 68% 5%, 75% 1%, 83% 6%, 90% 0, 96% 5%, 100% 1%,
      100% 95%, 95% 100%, 88% 95%, 80% 100%, 72% 94%, 64% 100%, 56% 95%, 48% 100%, 40% 94%, 32% 100%, 24% 95%, 16% 100%, 8% 94%, 0 100%); }
  .torn small { display: block; text-align: center; color: #d62828; font-size: 36px; font-weight: 800; }
  .torn .hl div { color: #003049; }
  .torn .hl .hi { color: #d62828; }
  .chips { display: flex; flex-wrap: wrap; gap: 14px; justify-content: center; }
  .chips span { background: #003049; color: #fff; font-size: var(--pt); font-weight: 700; padding: 10px 22px; border-radius: 40px; line-height: 1.25; }
  .chips span:nth-child(even) { background: #d62828; }
  .chips .num { color: #fcbf49; }
  .foot { color: #003049; }
"""


def collage_page(story, font, image_url, date, handle, place, asks):
    tiles = "".join(f"<div{_bg(image_url)}></div>" for _ in range(3))
    chips = "".join(f"<span>{highlight_numbers(p)}</span>" for p in _pts(story, 4))
    body = f"""<div class="grid">{tiles}</div>{SYM if image_url else ""}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="torn"><small>{esc(place or story.kicker or "")}</small><div class="hl">{_hl(story)}</div></div>
    {f'<div class="chips">{chips}</div>' if chips else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 820, 600) + COLLAGE_CSS, font, body)


# ----------------------------------------------------------------------------------------------- radio
RADIO_CSS = """
  body { background: linear-gradient(170deg, #240046 0%, #3c096c 40%, #10002b 100%); }
  .handle { top: 30px; right: 30px; }
  .player { background: rgba(255,255,255,.08); border: 2px solid rgba(255,255,255,.2); border-radius: 40px; padding: 26px; display: flex;
    flex-direction: column; gap: 18px; box-shadow: 0 20px 50px rgba(0,0,0,.4); }
  .cover { position: relative; height: 560px; border-radius: 28px; background: #5a189a center/cover no-repeat; }
  .cover .sym { bottom: 10px; }
  .cover .onair { position: absolute; left: 20px; top: 20px; background: #ff006e; color: #fff; font: 900 32px/1 Arial, sans-serif;
    padding: 10px 18px; border-radius: 10px; }
  .wave { display: flex; align-items: center; gap: 6px; height: 120px; }
  .wave i { flex: 1; background: linear-gradient(180deg, #ff006e, #8338ec); border-radius: 6px; }
  .ctrl { display: flex; align-items: center; justify-content: center; gap: 60px; color: #fff; font-size: 54px; }
  .ctrl b { width: 140px; height: 140px; border-radius: 50%; background: #fff; color: #3c096c; font-size: 70px; line-height: 140px;
    text-align: center; box-shadow: 0 0 40px rgba(255,0,110,.6); }
  .time { display: flex; justify-content: space-between; color: #c8b6ff; font-size: 26px; font-weight: 700; }
  .ep { color: #ff99c8; font-size: 34px; font-weight: 800; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 6px; color: #fff; }
  .hl .hi { color: #ff99c8; }
  .chap p { display: flex; gap: 16px; font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #e0aaff; padding: 8px 0; }
  .chap p b { color: #fff; font-family: 'Courier New', monospace; white-space: nowrap; }
  .chap .num { color: #ffd60a; }
"""


def radio_page(story, font, image_url, date, handle, place, asks):
    heights = [30, 55, 80, 45, 95, 70, 40, 85, 60, 100, 50, 75, 35, 90, 65, 45, 80, 55, 30, 70, 95, 50, 40, 60]
    wave = "".join(f'<i style="height:{h}%"></i>' for h in heights)
    chap = "".join(f"<p><b>0{i}:{(i * 17) % 60:02d}</b><span>{highlight_numbers(p)}</span></p>" for i, p in enumerate(_pts(story, 3), 1))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="ep">🎧 {esc(handle)} • {esc(place or story.kicker or "ન્યૂઝ")}</div>
    <div class="hl">{_hl(story)}</div>
    <div class="player"><div class="cover"{_bg(image_url)}><div class="onair">● ON AIR</div>{SYM if image_url else ""}</div>
      <div class="wave">{wave}</div><div class="time"><span>00:42</span><span>02:15</span></div>
      <div class="ctrl"><span>⏮</span><b>▶</b><span>⏭</span></div></div>
    {f'<div class="chap">{chap}</div>' if chap else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 60) + RADIO_CSS, font, body)


# ------------------------------------------------------------------------------------------- countdown
def days_left(story, today: Date | None = None) -> tuple[int, str] | None:
    """Days from today to the first date in the story's facts ('10 નવેમ્બર'), if it is 1-60 days ahead."""
    today = today or Date.today()
    for f in story.facts:
        m = re.search(r"(\d{1,2})\s*(" + "|".join(MONTHS) + ")", f["value"])
        if not m:
            continue
        month = MONTHS[m.group(2)]
        try:
            target = Date(today.year + (1 if month < today.month - 1 else 0), month, int(m.group(1)))
        except ValueError:
            continue
        n = (target - today).days
        if 1 <= n <= 60:
            return n, f["value"]
    return None


COUNT_CSS = """
  body { background: radial-gradient(circle at 50% 30%, #ff7b00 0%, #d00000 45%, #370617 100%); }
  .handle { top: 30px; right: 30px; }
  .ring { align-self: center; width: 560px; height: 560px; border-radius: 50%; display: flex; flex-direction: column; align-items: center;
    justify-content: center; background: radial-gradient(circle, #fff 0 60%, transparent 61%),
      repeating-conic-gradient(#ffd60a 0 4deg, transparent 4deg 10deg); box-shadow: 0 0 80px rgba(255,214,10,.6); }
  .ring b { font: 900 260px/0.9 'Arial Black', Arial, sans-serif; color: #d00000; }
  .ring span { font-size: 64px; font-weight: 800; color: #370617; }
  .till { align-self: center; background: #370617; color: #ffd60a; font-size: 44px; font-weight: 800; padding: 8px 34px 12px; border-radius: 40px; }
  .hl div { color: #fff; text-shadow: 0 6px 0 rgba(0,0,0,.35); }
  .hl .hi { color: #ffd60a; }
  .photo { position: relative; height: 300px; border-radius: 26px; background: #370617 center/cover no-repeat; border: 6px solid #ffd60a; }
  .photo .sym { bottom: 10px; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #fff; background: rgba(0,0,0,.3); border-radius: 16px;
    padding: 10px 20px; margin-bottom: 10px; }
  .pts .num { color: #ffd60a; }
"""


def countdown_page(story, font, image_url, date, handle, place, asks):
    left = days_left(story)
    n, when = left if left else ("!", "")
    pts = "".join(f"<p>⏳ {highlight_numbers(p)}</p>" for p in _pts(story, 2))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="ring"><b>{n}</b><span>દિવસ બાકી</span></div>
    {f'<div class="till">📅 {esc(when)} સુધી</div>' if when else ""}
    <div class="hl">{_hl(story)}</div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 70) + COUNT_CSS, font, body)


# --------------------------------------------------------------------------------------------- percent
def find_percent(story) -> tuple[float, str] | None:
    """(value, label) of the first percentage in the facts or points, if any (0-100)."""
    for text, label in [(f["value"], f["label"]) for f in story.facts] + [(p, p) for p in story.points]:
        m = re.search(r"(\d{1,3}(?:\.\d+)?)\s?%", text)
        if m and 0 < float(m.group(1)) <= 100:
            return float(m.group(1)), re.sub(r"\d{1,3}(?:\.\d+)?\s?%", "", label).strip(" :,-")[:60]
    return None


PERCENT_CSS = """
  body { background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%); color: #212529; }
  .handle { top: 30px; right: 30px; }
  .kick { align-self: flex-start; background: #4361ee; color: #fff; font-size: 36px; font-weight: 800; padding: 4px 22px 8px; border-radius: 12px; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 6px; color: #212529; }
  .hl .hi { color: #4361ee; }
  .chart { display: flex; align-items: center; gap: 30px; background: #fff; border-radius: 34px; padding: 30px; box-shadow: 0 16px 40px rgba(0,0,0,.12); }
  .donut { width: 420px; height: 420px; flex-shrink: 0; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    background: radial-gradient(circle, #fff 0 56%, transparent 57%), conic-gradient(#4361ee 0 var(--p), #f72585 var(--p) 100%); }
  .donut b { font: 900 120px/1 'Arial Black', Arial, sans-serif; color: #4361ee; }
  .donut b small { font-size: 60px; }
  .legend p { font-size: calc(var(--pt) * 1.05); font-weight: 800; line-height: 1.3; }
  .legend p i { display: inline-block; width: 30px; height: 30px; border-radius: 8px; background: #4361ee; margin-right: 12px; vertical-align: -4px; }
  .legend p + p i { background: #f72585; }
  .photo { position: relative; height: 330px; border-radius: 26px; background: #ccc center/cover no-repeat; }
  .photo .sym { bottom: 10px; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; padding: 10px 0 10px 24px; border-left: 8px solid #4361ee; margin-bottom: 8px; }
  .pts .num { color: #f72585; }
  .foot { color: #495057; }
"""


def percent_page(story, font, image_url, date, handle, place, asks):
    found = find_percent(story)
    value, label = found if found else (0, "")
    shown = f"{value:g}"
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3) if f"{shown}%" not in p.replace(" ", ""))
    chart = (f'<div class="chart"><div class="donut" style="--p:{value}%"><b>{shown}<small>%</small></b></div>'
             f'<div class="legend"><p><i></i>{esc(label)}</p></div></div>') if found else ""
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="kick">{esc(story.kicker or place or "આંકડા")}</div>
    <div class="hl">{_hl(story)}</div>
    {chart}
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 100) + PERCENT_CSS, font, body)


# ---------------------------------------------------------------------------------------------- folder
FOLDER_CSS = """
  body { background: #3d405b; }
  .folder { position: absolute; left: 30px; right: 30px; top: 80px; bottom: 30px; background: #d4a373; border-radius: 0 24px 24px 24px;
    box-shadow: 0 20px 50px rgba(0,0,0,.45); }
  .folder::before { content: ""; position: absolute; left: 0; top: -50px; width: 380px; height: 60px; background: #d4a373; border-radius: 20px 20px 0 0; }
  .label { position: absolute; left: 50px; top: 46px; z-index: 3; background: #fefae0; color: #333; font: 800 30px/1 'Courier New', monospace;
    padding: 12px 20px; border: 2px solid #999; }
  .handle { top: 30px; right: 40px; }
  .sheet { position: absolute; left: 70px; right: 70px; top: 130px; bottom: 60px; background: #fefae0; box-shadow: 0 6px 20px rgba(0,0,0,.2);
    transform: rotate(-1deg); }
  #main { left: 110px; right: 110px; top: 170px; bottom: 90px; }
  .clip { position: absolute; left: 140px; top: 100px; width: 50px; height: 140px; border: 8px solid #adb5bd; border-radius: 26px; z-index: 6; }
  .stamp2 { position: absolute; right: -40px; top: 20px; z-index: 6; background: rgba(254,250,224,.75); border: 7px solid #c1121f; color: #c1121f; font-size: 50px; font-weight: 800;
    padding: 6px 26px 10px; transform: rotate(-12deg); opacity: .85; }
  .typed { font-family: 'Courier New', monospace; font-size: 28px; color: #555; border-bottom: 2px solid #ccc; padding-bottom: 8px; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 6px; color: #222; }
  .hl .hi { color: #c1121f; text-decoration: underline; }
  .pic { position: relative; height: 340px; width: 80%; background: #999 center/cover no-repeat; border: 10px solid #fff;
    box-shadow: 0 6px 16px rgba(0,0,0,.25); transform: rotate(2deg); filter: sepia(.25); }
  .pic .sym { bottom: 8px; }
  .notes p { font-size: var(--pt); font-weight: 700; line-height: 1.35; color: #222; padding: 6px 0 6px 40px; position: relative; }
  .notes p::before { content: "▸"; position: absolute; left: 0; color: #c1121f; }
  .notes .num { color: #c1121f; background: #ffe066; }
  .foot { color: #555; }
"""


def folder_page(story, font, image_url, date, handle, place, asks):
    notes = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 4))
    stamp = "તપાસ ચાલુ" if story.category == "crime" else "મહત્વનું"
    body = f"""<div class="folder"></div><div class="label">FILE: {esc(place or "VALSAD")}</div><div class="handle">{esc(handle)}</div>
  <div class="sheet"></div><div class="clip"></div>
  <div id="main">
    <div class="typed">વિષય: {esc(story.kicker or "અહેવાલ")} • તા. {esc(date)}</div>
    <div class="hl">{_hl(story)}</div>
    <div class="pic"{_bg(image_url)}>{SYM if image_url else ""}<div class="stamp2">{stamp}</div></div>
    {f'<div class="notes">{notes}</div>' if notes else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 170) + FOLDER_CSS, font, body)


# -------------------------------------------------------------------------------------------- roadsign
ROAD_CSS = """
  body { background: linear-gradient(180deg, #87ceeb 0%, #cfe9f5 40%, #6c757d 40%, #495057 100%); }
  .road { position: absolute; left: 0; right: 0; top: 770px; bottom: 0;
    background: linear-gradient(90deg, transparent 48.5%, #fff 48.5%, #fff 51.5%, transparent 51.5%) center/100% 160px; }
  .handle { top: 30px; left: 30px; }
  .sign { background: #00753a; border: 10px solid #fff; outline: 6px solid #00753a; border-radius: 24px; padding: 20px 26px;
    box-shadow: 0 20px 40px rgba(0,0,0,.4); position: relative; z-index: 2; }
  .sign .hl div { color: #fff; font-family: '%FONT%', Arial, sans-serif; }
  .sign .hl .hi { color: #ffe066; }
  .sign .arrow { text-align: center; color: #fff; font: 900 90px/1 Arial, sans-serif; }
  .posts { display: flex; justify-content: space-around; height: 130px; margin-top: -24px; }
  .posts i { width: 30px; background: linear-gradient(90deg, #888, #ddd, #888); }
  .stones { display: flex; gap: 18px; justify-content: center; }
  .stone { width: 300px; background: #fff; border-radius: 120px 120px 10px 10px; overflow: hidden; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,.3); }
  .stone small { display: block; background: #ffd60a; color: #111; font-size: 28px; font-weight: 800; padding: 22px 10px 8px; }
  .stone b { display: block; font-size: calc(var(--pt) * 1.25); color: #111; padding: 14px 8px; line-height: 1.15; }
  .photo { position: relative; height: 300px; border-radius: 22px; background: #555 center/cover no-repeat; border: 6px solid #fff; }
  .photo .sym { bottom: 8px; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #fff; background: rgba(0,0,0,.55); border-radius: 14px;
    padding: 10px 18px; margin-bottom: 10px; }
  .pts .num { color: #ffe066; }
"""


def roadsign_page(story, font, image_url, date, handle, place, asks):
    stones = "".join(f'<div class="stone"><small>{esc(f["label"])}</small><b>{esc(f["value"])}</b></div>'
                     for f in story.facts[:2] if len(f["value"]) <= 16)
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 2))
    body = f"""<div class="road"></div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="sign"><div class="arrow">⬆ {esc(place or "")}</div><div class="hl">{_hl(story)}</div></div>
    <div class="posts"><i></i><i></i></div>
    {f'<div class="stones">{stones}</div>' if stones else ""}
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page((_base(font, 110) + ROAD_CSS).replace("%FONT%", font), font, body)


PLUS_LAYOUTS = {
    "notebook": notebook_page, "billboard": billboard_page, "letter": letter_page, "crimetape": crimetape_page,
    "collage": collage_page, "radio": radio_page, "countdown": countdown_page, "percent": percent_page,
    "folder": folder_page, "roadsign": roadsign_page,
}

PLUS_STEPS = [
    [".tape", "slideL", 0.1, 0.4, 0.2],
    [".board, .sign, .player, .ring, .chart, .paper, .torn", "settle", 0.0, 0.5, 0],
    [".stampx, .postmark, .stamp2", "slam", 0.9, 0.4, 0.15],
    [".wave i", "riseUp", 0.6, 0.3, 0.02],
    [".clip, .pic", "popIn", 0.6, 0.35, 0],
    [".stone, .chips span, .chap p, .ev p, .notes p, .lines p, .ground", "popIn", 1.1, 0.3, 0.12],
    [".till, .case, .typed, .topic, .ep", "fadeIn", 0.2, 0.4, 0],
]
