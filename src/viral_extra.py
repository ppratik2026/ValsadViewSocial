"""Ten more poster layouts for the viral design, each a different everyday object, so the feed never looks alike:

  ticket      a travel ticket with a tear-off stub: route, date and time fields, barcode
  map         a local map: roads and river, a big pin on the place, the story on a map card
  calendar    a tear-off calendar page with the date huge, the story below
  receipt     a shop bill: items with their amounts on dotted lines, a total, "thank you" footer
  scoreboard  a stadium LED board: amber dot-matrix numbers, team-style rows
  comic       a comic page: halftone panels, a "BOOM!" burst, speech bubbles
  neon        a brick wall with a glowing neon headline and neon outlined boxes
  lockscreen  a phone lock screen: big clock, the story as notifications
  chalkboard  a classroom chalkboard: chalk letters, underlines, doodled arrows
  filmstrip   a film strip: the photo in film frames, the headline as a movie title

Shared contract with src/viral.FIT: #main, .hl div lines, --hl, --pt, --ask, --top, --min-top, .grow.
Brands, logos and real people are never drawn; every Gujarati word is real font text.
"""
import re

from src.designs import esc, highlight_numbers
from src.icons import icon_img
from src.viral_layouts import _ask
from src.viral_more import SYM, _askbar, _base, _bg, _foot, _hl, _page, _pts


def _fact(story, pattern: str, default: tuple[str, str] | None = None) -> tuple[str, str] | None:
    f = next((f for f in story.facts if re.search(pattern, f["label"] + " " + f["value"], re.I)), None)
    return (f["label"], f["value"]) if f else default


# -------------------------------------------------------------------------------------------- ticket
TICKET_CSS = """
  body { background: linear-gradient(160deg, #0f4c81 0%, #062a4d 100%); }
  .handle { top: 30px; right: 30px; }
  .tk { position: relative; display: grid; grid-template-columns: 1fr 230px; background: #fdf6e3; color: #222; border-radius: 30px;
    box-shadow: 0 20px 44px rgba(0,0,0,.5); overflow: hidden; }
  .tk::before, .tk::after { content: ""; position: absolute; left: calc(100% - 248px); width: 36px; height: 36px; border-radius: 50%;
    background: #0a3866; }
  .tk::before { top: -18px; } .tk::after { bottom: -18px; }
  .tk .l { padding: 24px 26px; border-right: 5px dashed #c9b98f; display: flex; flex-direction: column; gap: 14px; }
  .tk .brand { display: flex; justify-content: space-between; align-items: center; background: #e85d04; color: #fff; margin: -24px -26px 0;
    padding: 12px 26px; font-size: 32px; font-weight: 800; }
  .tk .route { display: flex; align-items: center; gap: 16px; font-size: 64px; font-weight: 800; color: #062a4d; line-height: 1.1; }
  .tk .route i { flex: 1; border-top: 6px dotted #e85d04; position: relative; }
  .tk .route i::after { content: "✈"; position: absolute; left: 45%; top: -36px; font-size: 44px; color: #e85d04; font-style: normal; }
  .tk .fields { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 20px; }
  .tk .fields small { display: block; font-size: 24px; font-weight: 800; color: #8a7a55; letter-spacing: 1px; }
  .tk .fields b { font-size: 40px; color: #222; line-height: 1.15; }
  .tk .r { padding: 24px 16px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; gap: 12px;
    background: #f6ebcc; }
  .tk .r .ic { width: 120px; height: 120px; }
  .tk .r small { font-size: 26px; font-weight: 800; color: #8a7a55; text-align: center; }
  .bar { height: 120px; width: 100%; background: repeating-linear-gradient(90deg, #222 0 4px, transparent 4px 7px, #222 7px 9px,
    transparent 9px 14px, #222 14px 20px, transparent 20px 23px); }
  .hl div { color: #fff; text-shadow: 0 6px 18px rgba(0,0,0,.5); }
  .hl .hi { color: #ffb703; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; padding: 12px 20px; border-radius: 16px;
    background: rgba(255,255,255,.1); border-left: 10px solid #ffb703; margin-bottom: 12px; }
  .pts .num { color: #ffb703; }
  .photo { position: relative; height: 380px; border-radius: 26px; background: #062a4d center/cover no-repeat; border: 5px solid #fdf6e3; }
  .photo .sym { bottom: 10px; }
"""


def ticket_page(story, font, image_url, date, handle, place, asks):
    when = _fact(story, r"તારીખ|દિવસ|date|નવેમ્બર|ડિસેમ્બર|જાન્યુ", ("તારીખ", date))
    time = _fact(story, r"સમય|કલાક|વાગ્યે|time", None)
    other = next((f for f in story.facts if (f["label"], f["value"]) not in (when, time)), None)
    fields = [("તારીખ", when[1])] + ([("સમય", time[1])] if time else []) + ([(other["label"], other["value"])] if other else [])
    fields_html = "".join(f"<div><small>{esc(a)}</small><b>{esc(b)}</b></div>" for a, b in fields[:4])
    route_text = story.kicker if " - " in (story.kicker or "") else place
    frm, to = (route_text.split(" - ") + [""])[:2] if route_text else ("વલસાડ", "")
    route = f'{esc(frm)}<i></i>{esc(to or story.kicker or "")}' if (to or story.kicker) else esc(frm)
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="hl">{_hl(story)}</div>
    <div class="tk"><div class="l"><div class="brand"><span>{esc(handle)}</span><span>NEWS PASS</span></div>
      <div class="route">{route}</div><div class="fields">{fields_html}</div></div>
      <div class="r">{icon_img(story.headline)}<small>{esc(story.kicker or "માહિતી")}</small><div class="bar"></div></div></div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 120) + TICKET_CSS, font, body)


# ----------------------------------------------------------------------------------------------- map
MAP_CSS = """
  body { background: #e8efd9; color: #1f2d1a; }
  .map { position: absolute; inset: 0; overflow: hidden;
    background:
      linear-gradient(115deg, transparent 47%, #7cc4e8 47%, #7cc4e8 53%, transparent 53%),
      linear-gradient(20deg, transparent 49%, #fff 49%, #fff 51.5%, transparent 51.5%),
      linear-gradient(95deg, transparent 63%, #fff 63%, #fff 64.5%, transparent 64.5%),
      linear-gradient(170deg, transparent 30%, #ffd166 30%, #ffd166 31.8%, transparent 31.8%),
      repeating-linear-gradient(0deg, transparent 0 118px, rgba(0,0,0,.05) 118px 120px),
      repeating-linear-gradient(90deg, transparent 0 118px, rgba(0,0,0,.05) 118px 120px),
      radial-gradient(circle at 20% 80%, #cfe3b5 0 140px, transparent 141px),
      radial-gradient(circle at 85% 25%, #cfe3b5 0 180px, transparent 181px); }
  .pin { position: absolute; left: 50%; top: 250px; transform: translateX(-50%); z-index: 3; display: flex; flex-direction: column;
    align-items: center; }
  .pin .ic { width: 200px; height: 200px; filter: drop-shadow(0 16px 10px rgba(0,0,0,.35)); }
  .pin b { margin-top: -10px; background: #d00000; color: #fff; font-size: 60px; font-weight: 800; padding: 4px 34px 10px; border-radius: 40px;
    border: 5px solid #fff; box-shadow: 0 10px 22px rgba(0,0,0,.35); white-space: nowrap; }
  .pin::after { content: ""; position: absolute; top: 175px; width: 120px; height: 30px; border-radius: 50%; background: rgba(0,0,0,.2); z-index: -1; }
  .handle { top: 30px; left: 30px; background: #fff; color: #1f2d1a; border-color: #d00000; }
  .compass { position: absolute; right: 40px; top: 30px; width: 130px; height: 130px; border-radius: 50%; background: #fff; border: 5px solid #1f2d1a;
    font: 900 40px/120px Arial, sans-serif; text-align: center; color: #d00000; z-index: 3; }
  .cardm { background: #fff; border-radius: 30px; padding: 20px 24px; box-shadow: 0 18px 40px rgba(0,0,0,.25); border-top: 14px solid #d00000; }
  .cardm .hl div { color: #1f2d1a; }
  .cardm .hl .hi { color: #d00000; }
  .row { display: flex; gap: 16px; align-items: center; padding: 10px 0; border-top: 2px dashed #d6dccb; }
  .row .ic { width: 60px; height: 60px; flex-shrink: 0; }
  .row p { font-size: var(--pt); font-weight: 700; line-height: 1.3; }
  .row .num { color: #d00000; }
  .photo { position: relative; height: 300px; border-radius: 24px; background: #9bb center/cover no-repeat; border: 6px solid #fff;
    box-shadow: 0 10px 24px rgba(0,0,0,.25); }
  .photo .sym { bottom: 10px; }
  .foot { color: #1f2d1a; }
"""


def map_page(story, font, image_url, date, handle, place, asks):
    rows = "".join(f'<div class="row">{icon_img(p)}<p>{highlight_numbers(p)}</p></div>' for p in _pts(story, 3))
    body = f"""<div class="map"></div><div class="handle">{esc(handle)}</div><div class="compass">N</div>
  <div class="pin">{icon_img("pin")}<b>{esc(place or story.kicker or "વલસાડ")}</b></div>
  <div id="main">
    <div class="grow"></div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    <div class="cardm"><div class="hl">{_hl(story)}</div>{rows}</div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 560, 520) + MAP_CSS, font, body)


# ------------------------------------------------------------------------------------------ calendar
CAL_CSS = """
  body { background: linear-gradient(180deg, #ffecd2 0%, #fcb69f 100%); color: #222; }
  .handle { top: 30px; right: 30px; }
  .cal { align-self: center; width: 640px; background: #fff; border-radius: 30px; overflow: hidden; box-shadow: 0 24px 50px rgba(0,0,0,.3);
    position: relative; transform: rotate(-2deg); }
  .cal .rings { position: absolute; top: -26px; left: 0; right: 0; display: flex; justify-content: space-around; }
  .cal .rings i { width: 30px; height: 64px; border-radius: 15px; background: linear-gradient(90deg, #999, #eee, #999); }
  .cal .m { background: #d00000; color: #fff; text-align: center; font-size: 64px; font-weight: 800; padding: 30px 0 14px; }
  .cal .d { text-align: center; font: 900 260px/1.05 'Arial Black', Arial, sans-serif; color: #222; }
  .cal .w { text-align: center; font-size: 44px; font-weight: 800; color: #d00000; padding-bottom: 20px; border-bottom: 4px dashed #eee; }
  .hl div { color: #3d0000; }
  .hl .hi { color: #d00000; }
  .list { background: rgba(255,255,255,.85); border-radius: 26px; padding: 12px 22px; }
  .list p { font-size: var(--pt); font-weight: 700; line-height: 1.3; padding: 10px 0 10px 50px; border-bottom: 2px solid #f3d1c3; position: relative; }
  .list p:last-child { border-bottom: 0; }
  .list p::before { content: "📌"; position: absolute; left: 0; }
  .list .num { color: #d00000; }
  .photo { position: relative; height: 330px; border-radius: 24px; background: #fcb69f center/cover no-repeat; border: 6px solid #fff; }
  .photo .sym { bottom: 10px; }
  .foot { color: #3d0000; }
"""
MONTHS = ["જાન્યુઆરી", "ફેબ્રુઆરી", "માર્ચ", "એપ્રિલ", "મે", "જૂન", "જુલાઈ", "ઓગસ્ટ", "સપ્ટેમ્બર", "ઓક્ટોબર", "નવેમ્બર", "ડિસેમ્બર"]


def calendar_date(story, date: str) -> tuple[str, str, str]:
    """(day number, month, label) from a date fact ('3 નવેમ્બર'), else today's date."""
    f = _fact(story, r"\d+\s*(?:" + "|".join(m[:3] for m in MONTHS) + ")")
    text, label = (f[1], f[0]) if f else (date, "આજે")
    m = re.search(r"(\d{1,2})\s*([઀-૿.]+)", text)
    return (m.group(1), m.group(2), label) if m else ("", text, label)


def calendar_page(story, font, image_url, date, handle, place, asks):
    day, month, label = calendar_date(story, date)
    rows = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="cal"><div class="rings"><i></i><i></i><i></i><i></i></div><div class="m">{esc(month)}</div>
      <div class="d">{esc(day or "!")}</div><div class="w">{esc(label)}</div></div>
    <div class="hl">{_hl(story)}</div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="list">{rows}</div>' if rows else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 70) + CAL_CSS, font, body)


# ------------------------------------------------------------------------------------------- receipt
RECEIPT_CSS = """
  body { background: #2b2d42; }
  .handle { top: 30px; right: 30px; }
  .bill { align-self: center; width: 860px; background: #fff; color: #222; padding: 34px 40px 50px; position: relative;
    font-family: 'Courier New', monospace, '%FONT%'; box-shadow: 0 24px 50px rgba(0,0,0,.5); transform: rotate(1.5deg);
    -webkit-mask: linear-gradient(#000 0 0) top/100% calc(100% - 26px) no-repeat,
      radial-gradient(circle 14px at 14px 100%, transparent 14px, #000 15px) bottom/28px 26px repeat-x; }
  .bill .shop { text-align: center; font-size: 44px; font-weight: 800; font-family: '%FONT%', sans-serif; }
  .bill .meta { display: flex; justify-content: space-between; font-size: 26px; border-bottom: 3px dashed #999; padding: 10px 0 14px; }
  .bill .hl div { color: #222; font-family: '%FONT%', sans-serif; }
  .bill .hl .hi { color: #d00000; }
  .item { display: flex; align-items: baseline; gap: 10px; font-size: var(--pt); font-weight: 700; padding: 8px 0; font-family: '%FONT%', sans-serif; }
  .item span { flex-shrink: 1; }
  .item i { flex: 1; border-bottom: 4px dotted #bbb; transform: translateY(-6px); min-width: 30px; }
  .item b { font-family: 'Courier New', monospace; font-size: calc(var(--pt) * 1.1); white-space: nowrap; }
  .total { display: flex; justify-content: space-between; border-top: 4px double #222; margin-top: 10px; padding-top: 12px;
    font-size: calc(var(--pt) * 1.2); font-weight: 800; font-family: '%FONT%', sans-serif; }
  .total b { color: #d00000; }
  .thanks { text-align: center; font-size: 30px; margin-top: 16px; letter-spacing: 2px; }
  .note p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #edf2f4; border-left: 10px solid #ef233c; padding-left: 16px;
    margin-bottom: 10px; }
  .note .num { color: #ffd60a; }
"""


def receipt_page(story, font, image_url, date, handle, place, asks):
    items = [(f["label"], f["value"]) for f in story.facts[:4]]
    for p in story.points:
        m = re.search(r"(₹\s?[\d,.]+|\d[\d,.]*\s?(?:%|રૂપિયા|કરોડ|લાખ))", p)
        if m and len(items) < 5:
            items.append((p.replace(m.group(1), "").strip(" :,-")[:38], m.group(1)))
    rows = "".join(f'<div class="item"><span>{esc(a)}</span><i></i><b>{esc(b)}</b></div>' for a, b in items)
    used = " ".join(a for a, _ in items)
    note = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3) if p[:20] not in used)[:1200]
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="bill"><div class="shop">🧾 {esc(story.kicker or "ભાવનો હિસાબ")}</div>
      <div class="meta"><span>{esc(place or "વલસાડ")}</span><span>{esc(date)}</span></div>
      <div class="hl">{_hl(story)}</div>
      {rows}
      <div class="thanks">*** {esc(handle)} ***</div></div>
    {f'<div class="note">{note}</div>' if note else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page((_base(font, 90) + RECEIPT_CSS).replace("%FONT%", font), font, body)


# ---------------------------------------------------------------------------------------- scoreboard
SCORE_CSS = """
  body { background: radial-gradient(ellipse at 50% 110%, #1b5e20 0%, #0b2410 45%, #050a06 100%); }
  body::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 600px;
    background: radial-gradient(circle at 15% 0%, rgba(255,255,255,.35) 0 60px, transparent 260px),
      radial-gradient(circle at 85% 0%, rgba(255,255,255,.35) 0 60px, transparent 260px); }
  .handle { top: 30px; left: 50%; transform: translateX(-50%); }
  .board { background: #0a0a0a; border: 12px solid #333; border-radius: 22px; padding: 22px; box-shadow: 0 0 0 4px #555, 0 24px 50px rgba(0,0,0,.6); }
  .board .t { text-align: center; color: #ffb000; font-size: 38px; font-weight: 800; letter-spacing: 2px; border-bottom: 3px solid #333;
    padding-bottom: 10px; margin-bottom: 10px; }
  .led { display: flex; justify-content: space-between; align-items: center; padding: 10px 6px; border-bottom: 2px solid #222; gap: 20px; }
  .led span { color: #e5e5e5; font-size: calc(var(--pt) * 1.05); font-weight: 800; }
  .led b { font: 900 calc(var(--pt) * 1.8)/1 'Courier New', monospace; color: #ffb000; text-shadow: 0 0 14px rgba(255,176,0,.8);
    letter-spacing: 4px; background-image: radial-gradient(rgba(0,0,0,.55) 1px, transparent 1.5px); background-size: 5px 5px;
    -webkit-background-clip: text; }
  .hl div { color: #fff; text-shadow: 0 6px 18px rgba(0,0,0,.6); }
  .hl .hi { color: #ffb000; }
  .photo { position: relative; height: 360px; border-radius: 22px; background: #1b5e20 center/cover no-repeat; border: 5px solid #ffb000; }
  .photo .sym { bottom: 10px; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #fff; padding: 10px 18px; margin-bottom: 10px;
    background: rgba(0,0,0,.45); border-radius: 14px; border-left: 8px solid #ffb000; }
  .pts .num { color: #ffb000; }
"""


def scoreboard_page(story, font, image_url, date, handle, place, asks):
    leds = [(f["label"], f["value"]) for f in story.facts[:4]]
    if not leds:
        leds = [(p[:30], m.group(0)) for p in story.points if (m := re.search(r"\d[\d,./]*", p))][:3]
    leds_html = "".join(f'<div class="led"><span>{esc(a)}</span><b>{esc(b)}</b></div>' for a, b in leds)
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="hl">{_hl(story)}</div>
    {f'<div class="board"><div class="t">★ {esc(story.kicker or place or "સ્કોરબોર્ડ")} ★</div>{leds_html}</div>' if leds_html else ""}
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 110) + SCORE_CSS, font, body)


# --------------------------------------------------------------------------------------------- comic
COMIC_CSS = """
  body { background: #ffe14d; color: #111;
    background-image: radial-gradient(rgba(0,0,0,.18) 22%, transparent 24%); background-size: 18px 18px; }
  .handle { top: 30px; right: 30px; background: #111; }
  .boom { align-self: flex-start; position: relative; padding: 40px 70px; font: 900 96px/1 'Arial Black', Arial, sans-serif; color: #ffe14d;
    -webkit-text-stroke: 5px #111; paint-order: stroke fill; transform: rotate(-8deg); z-index: 1; }
  .boom::before { content: ""; position: absolute; inset: 0; z-index: -1; background: #e10600; border: 6px solid #111;
    clip-path: polygon(50% 0, 61% 22%, 86% 8%, 78% 34%, 100% 42%, 80% 58%, 94% 84%, 66% 76%, 56% 100%, 44% 78%, 18% 94%, 24% 66%, 0 54%, 20% 40%, 8% 14%, 36% 24%); }
  .panel { background: #fff; border: 6px solid #111; box-shadow: 10px 10px 0 #111; padding: 16px 20px; }
  .panel .hl div { color: #111; }
  .panel .hl .hi { color: #e10600; }
  .panels { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
  .pic { position: relative; min-height: 360px; border: 6px solid #111; box-shadow: 10px 10px 0 #111; background: #ccc center/cover no-repeat;
    filter: contrast(1.15) saturate(1.3); }
  .pic .sym { bottom: 8px; }
  .say { position: relative; background: #fff; border: 6px solid #111; border-radius: 40px; padding: 16px 20px; font-size: var(--pt);
    font-weight: 800; line-height: 1.25; box-shadow: 8px 8px 0 #111; }
  .say::after { content: ""; position: absolute; left: 40px; bottom: -34px; border: 18px solid transparent; border-top: 26px solid #111; }
  .say .num { color: #e10600; }
  .sayw { display: flex; flex-direction: column; gap: 40px; }
  .wide { grid-column: 1 / -1; }
  .foot { color: #111; }
  .v-ask .say { border-radius: 0; box-shadow: none; border: 0; }
  .v-ask .say::after { display: none; }
"""


def comic_page(story, font, image_url, date, handle, place, asks):
    word = {"breaking": "BOOM!", "money": "WOW!", "happy": "YAY!"}.get(story.mood, "OMG!")
    says = "".join(f'<div class="say">{highlight_numbers(p)}</div>' for p in _pts(story, 3))
    pic = f'<div class="pic"{_bg(image_url)}>{SYM if image_url else ""}</div>'
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="boom">{word}</div>
    <div class="panel"><div class="hl">{_hl(story)}</div></div>
    <div class="panels">{pic}<div class="sayw">{says}</div></div>
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 40) + COMIC_CSS, font, body)


# ---------------------------------------------------------------------------------------------- neon
NEON_CSS = """
  body { background: #1a1014;
    background-image: linear-gradient(rgba(0,0,0,.35) 2px, transparent 2px), linear-gradient(90deg, rgba(0,0,0,.35) 2px, transparent 2px),
      radial-gradient(circle at 50% 30%, #3a1c2a 0%, #120a0e 70%);
    background-size: 120px 60px, 120px 60px, 100% 100%; background-position: 0 0, 60px 30px, 0 0; }
  .handle { top: 30px; right: 30px; border-color: #00f5d4; }
  .sign { align-self: center; border: 6px solid #ff2e88; border-radius: 30px; padding: 6px 40px 12px; color: #ffd6ec; font-size: 46px; font-weight: 800;
    box-shadow: 0 0 18px #ff2e88, inset 0 0 18px #ff2e88; text-shadow: 0 0 10px #ff2e88, 0 0 30px #ff2e88; }
  .hl div { color: #e0fffb; text-shadow: 0 0 6px #fff, 0 0 18px #00f5d4, 0 0 40px #00f5d4, 0 0 70px #00bbf9; }
  .hl .hi { color: #fff3b0; text-shadow: 0 0 6px #fff, 0 0 18px #ffd60a, 0 0 40px #ff9e00; }
  .photo { position: relative; height: 420px; border-radius: 28px; background: #222 center/cover no-repeat; border: 5px solid #00f5d4;
    box-shadow: 0 0 22px #00f5d4; }
  .photo .sym { bottom: 10px; }
  .nb { border: 4px solid #9b5de5; border-radius: 22px; padding: 14px 20px; font-size: var(--pt); font-weight: 700; line-height: 1.3; color: #f3e8ff;
    box-shadow: 0 0 14px #9b5de5, inset 0 0 12px rgba(155,93,229,.6); margin-bottom: 14px; }
  .nb:nth-child(even) { border-color: #f15bb5; box-shadow: 0 0 14px #f15bb5, inset 0 0 12px rgba(241,91,181,.6); }
  .nb .num { color: #fee440; text-shadow: 0 0 10px #fee440; }
  .v-ask .say { background: #00f5d4; }
"""


def neon_page(story, font, image_url, date, handle, place, asks):
    boxes = "".join(f'<div class="nb">{highlight_numbers(p)}</div>' for p in _pts(story, 3))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="sign">{esc(place or story.kicker or "LIVE NEWS")}</div>
    <div class="hl">{_hl(story)}</div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div>{boxes}</div>' if boxes else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 120) + NEON_CSS, font, body)


# ---------------------------------------------------------------------------------------- lockscreen
LOCK_CSS = """
  body { background: #000; }
  .wall { position: absolute; inset: 0; background: #1d2b64 center/cover no-repeat; filter: blur(6px) brightness(.6); transform: scale(1.08); }
  .wall.none { background: linear-gradient(160deg, #1d2b64, #f8cdda); filter: none; }
  .status { position: absolute; top: 24px; left: 50px; right: 50px; display: flex; justify-content: space-between; font: 700 30px Arial, sans-serif;
    color: #fff; z-index: 5; }
  .clock { text-align: center; color: #fff; font: 300 190px/1 Arial, sans-serif; letter-spacing: -6px; text-shadow: 0 6px 24px rgba(0,0,0,.4); }
  .day { text-align: center; color: #fff; font-size: 40px; font-weight: 700; margin-top: -10px; }
  .noti { background: rgba(255,255,255,.82); color: #111; border-radius: 34px; padding: 18px 24px; backdrop-filter: blur(20px);
    box-shadow: 0 10px 30px rgba(0,0,0,.3); }
  .noti .app { display: flex; align-items: center; gap: 12px; font-size: 26px; font-weight: 800; color: #555; margin-bottom: 6px; }
  .noti .app .ic { width: 44px; height: 44px; border-radius: 10px; background: #d00000; padding: 4px; }
  .noti .app time { margin-left: auto; font-weight: 600; }
  .noti .hl { align-items: flex-start; gap: 0; }
  .noti .hl div { text-align: left; padding: 0 0 4px; color: #111; }
  .noti .hl .hi { color: #d00000; }
  .noti p { font-size: var(--pt); font-weight: 700; line-height: 1.3; }
  .noti .num { color: #d00000; }
  .noti .img { position: relative; height: 340px; border-radius: 20px; margin-top: 12px; background: #999 center/cover no-repeat; }
  .noti .img .sym { bottom: 10px; }
  .unlock { text-align: center; color: #fff; font-size: 32px; font-weight: 700; }
  .unlock i { display: block; width: 300px; height: 10px; border-radius: 5px; background: #fff; margin: 14px auto 0; }
"""


def lockscreen_page(story, font, image_url, date, handle, place, asks):
    pts = _pts(story, 3)
    notes = "".join(f'<div class="noti"><div class="app">{icon_img(p)}<span>{esc(handle)}</span><time>{i + 1} મિ. પહેલાં</time></div>'
                    f'<p>{highlight_numbers(p)}</p></div>' for i, p in enumerate(pts))
    img = f'<div class="img"{_bg(image_url)}>{SYM}</div>' if image_url else ""
    wall = f'<div class="wall"{_bg(image_url)}></div>' if image_url else '<div class="wall none"></div>'
    body = f"""{wall}<div class="status"><span>{esc(handle)}</span><span>5G ▮▮▮ 🔋</span></div>
  <div id="main">
    <div class="clock">10:10</div>
    <div class="day">{esc(date)} • {esc(place or "વલસાડ")}</div>
    <div class="noti"><div class="app">{icon_img("siren")}<span>બ્રેકિંગ • {esc(handle)}</span><time>હમણાં</time></div>
      <div class="hl">{_hl(story)}</div>{img}</div>
    {notes}
    <div class="grow"></div>
    <div class="unlock">{_ask(story, asks)} 👇 કોમેન્ટ કરો<i></i></div>
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 90) + LOCK_CSS, font, body)


# ---------------------------------------------------------------------------------------- chalkboard
CHALK_CSS = """
  body { background: #6b4226; }
  .board { position: absolute; inset: 26px; border-radius: 16px; border: 22px solid #8b5a2b;
    background: radial-gradient(ellipse at 50% 40%, #2f5d46 0%, #1e3d2e 80%); box-shadow: inset 0 0 80px rgba(0,0,0,.5); }
  .board::after { content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.06) 1px, transparent 2px);
    background-size: 9px 9px; }
  #main { left: 80px; right: 80px; top: 80px; bottom: 70px; }
  .handle { top: 60px; right: 70px; background: transparent; border: 3px dashed #fff; }
  .topic { align-self: flex-start; color: #ffe066; font-size: 40px; font-weight: 800; border-bottom: 4px solid #ffe066; transform: rotate(-2deg); }
  .hl div { color: #f8f9fa; text-shadow: 0 0 2px rgba(255,255,255,.7), 2px 2px 0 rgba(255,255,255,.15); }
  .hl .hi { color: #ffe066; text-decoration: underline wavy #ff8fa3; text-underline-offset: 10px; }
  .photo { position: relative; height: 340px; border: 6px solid #f8f9fa; transform: rotate(1.5deg); background: #2f5d46 center/cover no-repeat;
    box-shadow: 0 10px 20px rgba(0,0,0,.4); }
  .photo .sym { bottom: 8px; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.35; color: #f1f3f5; padding: 8px 0 8px 60px; position: relative; }
  .pts p::before { content: "➜"; position: absolute; left: 0; color: #8ce99a; font-size: 1.1em; }
  .pts .num { color: #ffa8a8; }
  .v-ask .say { background: #f8f9fa; color: #1e3d2e; }
  .chalk { position: absolute; right: 140px; bottom: 34px; width: 160px; height: 26px; background: #fff; border-radius: 6px; transform: rotate(-6deg); z-index: 5; }
  .foot { color: #dee2e6; }
"""


def chalkboard_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 4))
    body = f"""<div class="board"></div><div class="chalk"></div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="topic">{esc(story.kicker or place or "આજનો પાઠ")}</div>
    <div class="hl">{_hl(story)}</div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 80) + CHALK_CSS, font, body)


# ----------------------------------------------------------------------------------------- filmstrip
FILM_CSS = """
  body { background: #0d0d0d; }
  .handle { top: 30px; right: 30px; }
  .strip { margin: 0 -30px; background: #111; padding: 40px 20px; position: relative; display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px;
    border-top: 3px solid #222; border-bottom: 3px solid #222; }
  .strip::before, .strip::after { content: ""; position: absolute; left: 0; right: 0; height: 24px;
    background: repeating-linear-gradient(90deg, transparent 0 22px, #f5f5f5 22px 50px, transparent 50px 72px); }
  .strip::before { top: 8px; } .strip::after { bottom: 8px; }
  .frame { position: relative; height: 420px; background: #333 center/cover no-repeat; border-radius: 6px; }
  .frame.b { filter: grayscale(1) contrast(1.2); background-position: 30% center; }
  .frame .sym { bottom: 8px; }
  .title { text-align: center; color: #e9c46a; font: 700 34px/1 Georgia, serif; letter-spacing: 8px; }
  .hl div { color: #fff; text-shadow: 0 4px 0 #9d0208, 0 8px 24px rgba(0,0,0,.7); }
  .hl .hi { color: #e9c46a; }
  .stars { text-align: center; font-size: 46px; letter-spacing: 10px; color: #e9c46a; }
  .credits { text-align: center; }
  .credits p { font-size: var(--pt); font-weight: 700; line-height: 1.35; color: #ddd; padding: 6px 0; }
  .credits p + p { border-top: 1px solid #333; }
  .credits .num { color: #e9c46a; }
  .v-ask .say { background: #e9c46a; }
"""


def filmstrip_page(story, font, image_url, date, handle, place, asks):
    credits = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    bg = _bg(image_url)
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="title">{esc(handle).upper()} PRESENTS</div>
    <div class="strip"><div class="frame"{bg}>{SYM if image_url else ""}</div><div class="frame b"{bg}></div></div>
    <div class="hl">{_hl(story)}</div>
    <div class="stars">★ ★ ★ ★ ★</div>
    {f'<div class="credits">{credits}</div>' if credits else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 100) + FILM_CSS, font, body)


EXTRA_LAYOUTS = {
    "ticket": ticket_page, "map": map_page, "calendar": calendar_page, "receipt": receipt_page,
    "scoreboard": scoreboard_page, "comic": comic_page, "neon": neon_page, "lockscreen": lockscreen_page,
    "chalkboard": chalkboard_page, "filmstrip": filmstrip_page,
}

EXTRA_STEPS = [
    [".tk, .cal, .bill, .board, .panel", "zoomIn", 0.05, 0.45, 0],
    [".pin", "dropIn", 0.0, 0.5, 0],
    [".boom", "slam", 0.1, 0.4, 0],
    [".clock, .sign, .topic, .title", "fadeIn", 0.0, 0.4, 0],
    [".noti", "slideR", 0.4, 0.35, 0.25],
    [".led, .item, .say, .nb, .credits p", "popIn", 1.0, 0.3, 0.14],
    [".cardm, .frame, .stars, .total, .thanks", "fadeIn", 0.8, 0.35, 0.1],
    [".unlock", "riseUp", 2.3, 0.4, 0],
]
