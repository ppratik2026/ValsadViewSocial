"""Twelve more poster layouts for the viral design, each with its own look (none repeats the five in
src/viral.py / src/viral_layouts.py):

  tv        TV news screen: LIVE bar, the picture as the screen, lower-third headline bars, a ticker
  paper     newspaper front page: masthead, serif headline, sepia photo with caption, two text columns, stamp
  quote     a statement: giant quote marks, the words in big letters, speaker tag (never a face)
  timeline  step by step: picture with a slanted edge, numbered timeline of the points
  versus    before / after or this / that: two big panels with a VS bolt
  alert     warning sign: yellow-black hazard poster, big ⚠ and "સાવધાન!"
  notice    public notice: paper with a navy band, numbered rows, a round stamp
  stats     numbers dashboard: big number tiles with icons
  polaroid  pin board: tilted photo with tape, headline on a paper strip, sticky notes
  magazine  magazine cover: full photo, big masthead, cover lines down the side
  chat      chat screen: the news told as message bubbles, with a photo message
  diagonal  photo cut diagonally, headline on a slanted red band, points on white

Every layout keeps the shared contract of src/viral.FIT (#main, .hl div lines, --hl, --pt, --ask, --top,
--min-top, .grow). Every Gujarati word is real font text, so the spelling is always right.
"""
import re

from src.designs import BRUSH_MASK, esc, highlight_numbers
from src.icons import icon_img
from src.viral_layouts import BASE, _ask, _date_fact, _hi, _lines, _n_lines, _page


def _base(font: str, top: int, min_top: int | None = None) -> str:
    return BASE % {"font": font, "mask": BRUSH_MASK, "top": top, "min_top": top if min_top is None else min_top}


def _pts(story, n: int = 4) -> list[str]:
    points = [p for p in story.points if p and p.strip() and p not in story.headline][:n]
    if not points and story.summary:
        points = [s.strip() for s in re.split(r"(?<=[.!?।])\s+", story.summary)
                  if s.strip() and story.headline not in s][:n]
    return points


def _hl(story, n: int | None = None, cls=lambda i: "") -> str:
    lines = _lines(story.headline, n or _n_lines(story.headline))
    return "".join(f'<div class="{cls(i)}">{_hi(line, story.highlight)}</div>' for i, line in enumerate(lines))


def _askbar(story, asks, cls: str = "") -> str:
    return (f'<div class="v-ask {cls}"><div class="q">?</div><div class="say brush">{_ask(story, asks)}</div>'
            f'<div class="bubble brush">કોમેન્ટ કરીને<br>જરૂર જણાવો</div></div>')


def _foot(story, date: str, extra: str = "") -> str:
    return (f'<div class="foot"><span>સ્રોત: {esc(story.source_name)}{" • " + esc(extra) if extra else ""}</span>'
            f'<span>{esc(date)}</span></div>')


def _bg(image_url: str | None) -> str:
    return f' style="background-image:url({image_url})"' if image_url else ""


SYM = '<div class="sym">પ્રતિકાત્મક તસવીર</div>'


# ------------------------------------------------------------------------------------------------ tv
TV_CSS = """
  body { background: linear-gradient(180deg, #050b1f 0%, #0b1f4d 100%); }
  .bar { display: flex; align-items: center; gap: 16px; }
  .live { background: #e10600; color: #fff; font: 900 40px/1 Arial, sans-serif; padding: 12px 22px; border-radius: 10px;
    display: flex; align-items: center; gap: 12px; }
  .live i { width: 22px; height: 22px; border-radius: 50%; background: #fff; box-shadow: 0 0 14px #fff; }
  .chan { flex: 1; background: #fff; color: #0b1f4d; font-size: 40px; font-weight: 800; padding: 6px 24px 10px; border-radius: 10px; }
  .clock { background: #ffd60a; color: #111; font-size: 32px; font-weight: 800; padding: 10px 18px; border-radius: 10px; }
  .screen { position: relative; height: 640px; border-radius: 26px; overflow: hidden; border: 8px solid #1c2c5e;
    background: #1c2c5e center/cover no-repeat; box-shadow: 0 0 0 4px #4a6cff, 0 20px 40px rgba(0,0,0,.6); }
  .screen .sym { top: 16px; }
  .screen .tag { position: absolute; left: 0; bottom: 26px; background: #e10600; color: #fff; font-size: 44px; font-weight: 800;
    padding: 6px 30px 10px 24px; clip-path: polygon(0 0, 100% 0, 94% 100%, 0 100%); }
  .lower .hl { align-items: flex-start; gap: 0; }
  .lower .hl div { background: #fff; color: #0b1f4d; padding: 4px 28px 10px; text-align: left; border-left: 16px solid #e10600; }
  .lower .hl div:nth-child(even) { background: #0b1f4d; color: #fff; border-left-color: #ffd60a; }
  .lower .hl .hi { color: #e10600; }
  .lower .hl div:nth-child(even) .hi { color: #ffd60a; }
  .items { display: flex; flex-direction: column; gap: 12px; }
  .item { display: flex; gap: 16px; align-items: flex-start; background: rgba(255,255,255,.08); border-radius: 14px;
    padding: 12px 18px; border-left: 8px solid #ffd60a; }
  .item b { color: #ffd60a; font-size: var(--pt); line-height: 1.3; }
  .item p { font-size: var(--pt); font-weight: 700; line-height: 1.3; }
  .item .num { color: #ffd60a; }
  .ticker { display: flex; margin: 0 -30px; background: #ffd60a; color: #111; font-size: 34px; font-weight: 800; }
  .ticker b { background: #e10600; color: #fff; padding: 12px 22px; white-space: nowrap; }
  .ticker span { padding: 12px 18px; white-space: nowrap; overflow: hidden; }
"""


def tv_page(story, font, image_url, date, handle, place, asks):
    pts = _pts(story, 3)
    items = "".join(f'<div class="item"><b>▶</b><p>{highlight_numbers(p)}</p></div>' for p in pts)
    tick = " ✦ ".join([story.subheadline or story.summary or story.headline] + pts)[:160]
    body = f"""<div id="main">
    <div class="bar"><div class="live"><i></i>LIVE</div><div class="chan">{esc(handle)} ન્યૂઝ</div><div class="clock">{esc(date)}</div></div>
    <div class="screen"{_bg(image_url)}>{SYM if image_url else ""}<div class="tag">{esc(place or story.kicker or "બ્રેકિંગ ન્યૂઝ")}</div></div>
    <div class="lower"><div class="hl">{_hl(story)}</div></div>
    <div class="items">{items}</div>
    <div class="grow"></div>
    {_askbar(story, asks)}
    <div class="ticker"><b>તાજા સમાચાર</b><span>{esc(tick)}</span></div>
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 40) + TV_CSS, font, body)


# --------------------------------------------------------------------------------------------- paper
PAPER_CSS = """
  body { background: #f3ead6; color: #1a1a1a;
    background-image: repeating-linear-gradient(0deg, rgba(0,0,0,.025) 0 2px, transparent 2px 6px); }
  .mast { text-align: center; border-top: 6px double #1a1a1a; border-bottom: 6px double #1a1a1a; padding: 6px 0 10px; }
  .mast b { display: block; font-size: 96px; font-weight: 800; letter-spacing: 2px; line-height: 1.1; }
  .mast small { display: flex; justify-content: space-between; font-size: 26px; font-weight: 700; border-top: 2px solid #1a1a1a;
    padding-top: 6px; }
  .kick { align-self: flex-start; background: #b5001b; color: #fff; font-size: 34px; font-weight: 800; padding: 4px 22px 8px; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { padding: 0 0 6px; text-align: left; color: #111; }
  .hl .hi { color: #b5001b; }
  .sub { font-size: calc(var(--pt) * 1.1); font-weight: 700; color: #444; line-height: 1.3; border-left: 8px solid #b5001b; padding-left: 16px; }
  .photo { position: relative; height: 460px; background: #c8b99a center/cover no-repeat; filter: sepia(.35) contrast(1.05);
    border: 3px solid #1a1a1a; }
  .photo .sym { bottom: 10px; }
  .cols { column-count: 2; column-gap: 34px; column-rule: 2px solid #1a1a1a; font-size: var(--pt); line-height: 1.4; font-weight: 600; }
  .cols p { margin-bottom: 10px; break-inside: avoid; }
  .cols .num { color: #b5001b; }
  .stamp { position: absolute; right: 20px; top: 20px; z-index: 8; width: 200px; height: 200px; border-radius: 50%;
    border: 8px solid #b5001b; color: #b5001b; display: flex; align-items: center; justify-content: center; text-align: center;
    font-size: 40px; font-weight: 800; line-height: 1.1; transform: rotate(-14deg); opacity: .85; background: rgba(243,234,214,.6); }
  .foot { color: #333; }
  .v-ask .say { background: #1a1a1a; color: #fff; }
"""


def paper_page(story, font, image_url, date, handle, place, asks):
    pts = _pts(story, 4)
    cols = "".join(f"<p>{highlight_numbers(p)}</p>" for p in pts)
    body = f"""<div id="main">
    <div class="mast"><b>વલસાડ વ્યૂ</b><small><span>{esc(handle)}</span><span>{esc(place or "દક્ષિણ ગુજરાત")}</span><span>{esc(date)}</span></small></div>
    {f'<div class="kick">{esc(story.kicker)}</div>' if story.kicker else ""}
    <div class="hl">{_hl(story)}</div>
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}<div class="stamp">તાજા<br>સમાચાર</div></div>
    {f'<div class="cols">{cols}</div>' if cols else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 34) + PAPER_CSS, font, body)


# --------------------------------------------------------------------------------------------- quote
QUOTE_CSS = """
  body { background: radial-gradient(circle at 80% 10%, #6a040f 0%, #370617 45%, #12020a 100%); }
  .bgpic { position: absolute; left: 0; right: 0; bottom: 0; height: 900px; background: #370617 center/cover no-repeat; opacity: .55; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, #12020a 0%, rgba(18,2,10,.2) 45%, #12020a 100%); }
  .handle { top: 34px; right: 34px; }
  .qmark { font: 900 320px/0.8 Georgia, serif; color: #ffd60a; height: 190px; text-shadow: 0 10px 0 rgba(0,0,0,.4); }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { padding: 0 0 8px; text-align: left; color: #fff; text-shadow: 0 6px 18px rgba(0,0,0,.6); }
  .hl .hi { color: #ffd60a; }
  .who { display: flex; align-items: center; gap: 16px; align-self: flex-start; }
  .who i { width: 90px; height: 6px; background: #ffd60a; }
  .who b { background: #ffd60a; color: #370617; font-size: calc(var(--pt) * 1.1); padding: 6px 24px 10px; border-radius: 12px; }
  .sub { font-size: calc(var(--pt) * 1.05); font-weight: 700; line-height: 1.35; color: #ffe8d6; }
  .sub .num { color: #ffd60a; }
  .pts { display: flex; flex-direction: column; gap: 12px; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; background: rgba(0,0,0,.45); border-left: 8px solid #ffd60a;
    padding: 10px 18px; border-radius: 0 14px 14px 0; }
  .pts .num { color: #ffd60a; }
  .closeq { align-self: flex-end; font: 900 220px/0.5 Georgia, serif; color: #ffd60a; height: 90px; }
"""


def quote_page(story, font, image_url, date, handle, place, asks):
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    who = story.kicker or place or "નિવેદન"
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{('<div class="sym" style="top:30px;left:30px;right:auto">પ્રતિકાત્મક તસવીર</div>' if image_url else "")}
  <div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="qmark">“</div>
    <div class="hl">{_hl(story)}</div>
    <div class="closeq">”</div>
    <div class="who"><i></i><b>{esc(who)}</b></div>
    {f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""}
    <div class="grow"></div>
    {f'<div class="pts">{pts}</div>' if pts else ""}
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 150) + QUOTE_CSS, font, body)


# ------------------------------------------------------------------------------------------ timeline
TIMELINE_CSS = """
  body { background: linear-gradient(180deg, #e6fffa 0%, #ffffff 50%, #e6fffa 100%); color: #0b3c49; }
  .toppic { position: absolute; left: 0; right: 0; top: 0; height: 620px; background: #0f766e center/cover no-repeat;
    clip-path: polygon(0 0, 100% 0, 100% 82%, 0 100%); }
  .toppic .sym { top: 20px; }
  .handle { top: 24px; left: 24px; }
  .head { background: #0f766e; border-radius: 30px; padding: 16px 10px 10px; box-shadow: 0 16px 34px rgba(0,0,0,.3); }
  .head .kick { text-align: center; color: #99f6e4; font-size: 34px; font-weight: 800; }
  .head .hl div { color: #fff; }
  .head .hl .hi { color: #ffd60a; }
  .tl { position: relative; display: flex; flex-direction: column; gap: 18px; padding-left: 20px; }
  .tl::before { content: ""; position: absolute; left: 62px; top: 30px; bottom: 30px; width: 8px; background: #14b8a6; border-radius: 4px; }
  .step { position: relative; display: flex; gap: 22px; align-items: center; }
  .step .dot { width: 92px; height: 92px; flex-shrink: 0; border-radius: 50%; background: #0f766e; color: #fff; z-index: 1;
    font: 900 50px/80px Arial, sans-serif; text-align: center; border: 6px solid #fff; box-shadow: 0 6px 14px rgba(0,0,0,.25); }
  .step p { flex: 1; background: #fff; border: 3px solid #99f6e4; border-radius: 22px; padding: 14px 20px; font-size: var(--pt);
    font-weight: 700; line-height: 1.3; box-shadow: 0 8px 18px rgba(0,0,0,.1); }
  .step .num { color: #e11d48; }
  .foot { color: #0b3c49; }
"""


def timeline_page(story, font, image_url, date, handle, place, asks):
    steps = "".join(f'<div class="step"><div class="dot">{i}</div><p>{highlight_numbers(p)}</p></div>'
                    for i, p in enumerate(_pts(story, 5), 1))
    body = f"""<div class="toppic"{_bg(image_url)}>{SYM if image_url else ""}</div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="head"><div class="kick">{esc(place or story.kicker or "")}</div><div class="hl">{_hl(story)}</div></div>
    {f'<div class="tl">{steps}</div>' if steps else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 460, 300) + TIMELINE_CSS, font, body)


# -------------------------------------------------------------------------------------------- versus
VERSUS_CSS = """
  body { background: linear-gradient(90deg, #7a0012 0%, #7a0012 50%, #0b5d20 50%, #0b5d20 100%); }
  .bgpic { position: absolute; inset: 0; background: center/cover no-repeat; opacity: .22; }
  .handle { top: 30px; left: 50%; transform: translateX(-50%); }
  .hl div { background: #111; color: #fff; }
  .hl div:nth-child(even) { background: #ffd60a; color: #111; }
  .hl .hi { color: #ffd60a; }
  .hl div:nth-child(even) .hi { color: #d00000; }
  .vs { position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: 70px; }
  .side { background: #fff; color: #111; border-radius: 30px; padding: 22px 16px; text-align: center; border: 8px solid #ffb3b3;
    box-shadow: 0 16px 34px rgba(0,0,0,.4); display: flex; flex-direction: column; gap: 10px; align-items: center; }
  .side.r { border-color: #a7f3c0; }
  .side small { font-size: calc(var(--pt) * .95); font-weight: 800; color: #fff; background: #b5001b; padding: 4px 20px 8px; border-radius: 30px; }
  .side.r small { background: #138a36; }
  .side b { font: 900 calc(var(--pt) * 1.7)/1.1 'Arial Black', Arial, sans-serif; word-break: break-word; }
  .side .ic { width: 110px; height: 110px; }
  .bolt { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%) rotate(-8deg); z-index: 2; width: 150px; height: 150px;
    border-radius: 50%; background: #ffd60a; color: #d00000; font: 900 70px/138px 'Arial Black', Arial, sans-serif; text-align: center;
    border: 6px solid #111; box-shadow: 0 10px 24px rgba(0,0,0,.5); }
  .chg { align-self: center; background: #ffd60a; color: #111; font-size: calc(var(--pt) * 1.2); font-weight: 800; padding: 8px 34px 12px;
    border-radius: 40px; border: 4px solid #111; }
  .pts p { font-size: var(--pt); font-weight: 700; line-height: 1.3; background: rgba(0,0,0,.45); padding: 10px 20px; border-radius: 16px;
    margin-bottom: 10px; }
  .pts .num { color: #ffd60a; }
"""


def versus_parts(story):
    """(left label, left value, right label, right value, change) from the story's before/after, or its first two facts."""
    c = story.compare or {}
    if c.get("before") and c.get("after"):
        return "પહેલાં", c["before"], "હવે", c["after"], c.get("change", "")
    if len(story.facts) >= 2:
        a, b = story.facts[0], story.facts[1]
        return a["label"], a["value"], b["label"], b["value"], ""
    return None


def versus_page(story, font, image_url, date, handle, place, asks):
    parts = versus_parts(story) or ("પહેલાં", "—", "હવે", "—", "")
    la, va, lb, vb, chg = parts
    pts = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="hl">{_hl(story, cls=lambda i: "brush")}</div>
    <div class="vs">
      <div class="side">{icon_img("drop_down" if "પહેલાં" in la else la + " " + va)}<small>{esc(la)}</small><b>{esc(va)}</b></div>
      <div class="side r">{icon_img("drop_up" if "હવે" in lb else lb + " " + vb)}<small>{esc(lb)}</small><b>{esc(vb)}</b></div>
      <div class="bolt">VS</div>
    </div>
    {f'<div class="chg">{esc(chg)}</div>' if chg else ""}
    {f'<div class="pts">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date, place)}
  </div>"""
    return _page(_base(font, 110) + VERSUS_CSS, font, body)


# --------------------------------------------------------------------------------------------- alert
ALERT_CSS = """
  body { background: #ffd000; color: #111; }
  body::before { content: ""; position: absolute; inset: 0; border: 34px solid transparent;
    border-image: repeating-linear-gradient(-45deg, #111 0 40px, #ffd000 40px 80px) 34; }
  .handle { top: 52px; right: 52px; }
  #main { left: 60px; right: 60px; top: 60px; bottom: 50px; }
  .sign { align-self: center; display: flex; align-items: center; gap: 20px; }
  .sign .ic { width: 170px; height: 170px; filter: drop-shadow(0 8px 0 rgba(0,0,0,.25)); }
  .sign b { font-size: 120px; font-weight: 800; color: #d00000; -webkit-text-stroke: 4px #111; paint-order: stroke fill; line-height: 1.1; }
  .place { align-self: center; background: #111; color: #ffd000; font-size: 44px; font-weight: 800; padding: 4px 30px 10px; border-radius: 12px; }
  .hl div { color: #111; }
  .hl .hi { color: #d00000; }
  .photo { position: relative; height: 420px; border-radius: 24px; border: 8px solid #111; background: #333 center/cover no-repeat; }
  .photo .sym { bottom: 10px; }
  .black { background: #111; color: #fff; border-radius: 24px; padding: 18px 24px; display: flex; flex-direction: column; gap: 8px; }
  .black p { font-size: var(--pt); font-weight: 700; line-height: 1.3; display: flex; gap: 14px; }
  .black p::before { content: "⚠"; color: #ffd000; }
  .black .num { color: #ffd000; }
  .foot { color: #111; }
  .v-ask .say { background: #111; color: #ffd000; }
"""


def alert_page(story, font, image_url, date, handle, place, asks):
    word = "ચેતવણી!" if re.search(r"એલર્ટ|ચેતવણી|આગાહી|alert", story.headline + story.summary, re.I) else "સાવધાન!"
    pts = "".join(f"<p><span>{highlight_numbers(p)}</span></p>" for p in _pts(story, 4))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="sign">{icon_img("warning")}<b>{word}</b></div>
    {f'<div class="place">{esc(place)}</div>' if place else ""}
    <div class="hl">{_hl(story)}</div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}</div>
    {f'<div class="black">{pts}</div>' if pts else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 60) + ALERT_CSS, font, body)


# -------------------------------------------------------------------------------------------- notice
NOTICE_CSS = """
  body { background: #dfe7f5; color: #10204a; }
  .sheet { position: absolute; inset: 26px; background: #fffdf7; border-radius: 18px; box-shadow: 0 10px 40px rgba(0,0,0,.25);
    border: 3px solid #10204a; }
  #main { left: 56px; right: 56px; top: 56px; bottom: 50px; }
  .band { display: flex; align-items: center; gap: 18px; background: #10204a; color: #fff; border-radius: 14px; padding: 10px 22px; }
  .band .ic { width: 90px; height: 90px; }
  .band b { font-size: 54px; line-height: 1.1; }
  .band small { display: block; font-size: 28px; color: #ffd60a; }
  .photo { position: relative; height: 330px; border-radius: 14px; background: #10204a center/cover no-repeat; border: 3px solid #10204a; }
  .photo .sym { bottom: 10px; }
  .hl div { color: #10204a; }
  .hl .hi { color: #c1121f; }
  .rows { border: 3px solid #10204a; border-radius: 14px; overflow: hidden; }
  .row { display: flex; border-bottom: 2px solid #c7d2ea; }
  .row:last-child { border-bottom: 0; }
  .row:nth-child(even) { background: #eef2fb; }
  .row b { width: 90px; flex-shrink: 0; background: #10204a; color: #ffd60a; font: 900 40px/1 Arial, sans-serif; display: flex;
    align-items: center; justify-content: center; }
  .row p { padding: 12px 18px; font-size: var(--pt); font-weight: 700; line-height: 1.3; }
  .row p em { font-style: normal; color: #c1121f; font-weight: 800; }
  .row .num { color: #c1121f; }
  .seal { position: absolute; right: 24px; top: 20px; z-index: 6; width: 210px; height: 210px; border-radius: 50%; border: 8px double #138a36;
    color: #138a36; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 42px; font-weight: 800;
    transform: rotate(12deg); opacity: .8; line-height: 1.1; }
  .foot { color: #10204a; }
  .v-ask .say { background: #10204a; color: #fff; }
"""


def notice_page(story, font, image_url, date, handle, place, asks):
    rows = [f'<em>{esc(f["label"])}:</em> {esc(f["value"])}' for f in story.facts[:2]]
    rows += [highlight_numbers(p) for p in _pts(story, 4)]
    rows_html = "".join(f'<div class="row"><b>{i}</b><p>{r}</p></div>' for i, r in enumerate(rows[:5], 1))
    body = f"""<div class="sheet"></div>
  <div id="main">
    <div class="band">{icon_img("govt")}<div><b>{esc(story.kicker or "જાહેર માહિતી")}</b><small>{esc(place or "દક્ષિણ ગુજરાત")} • {esc(handle)}</small></div></div>
    <div class="photo"{_bg(image_url)}>{SYM if image_url else ""}<div class="seal">મહત્વની<br>માહિતી</div></div>
    <div class="hl">{_hl(story)}</div>
    {f'<div class="rows">{rows_html}</div>' if rows_html else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 56) + NOTICE_CSS, font, body)


# --------------------------------------------------------------------------------------------- stats
STATS_CSS = """
  body { background: radial-gradient(circle at 50% 0%, #1e3a8a 0%, #0b1026 60%); }
  .handle { top: 30px; right: 30px; }
  .kick { align-self: flex-start; color: #38bdf8; font-size: 36px; font-weight: 800; letter-spacing: 1px; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 6px; color: #fff; }
  .hl .hi { color: #38bdf8; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  .tile { position: relative; border-radius: 26px; padding: 22px; min-height: 230px; background: linear-gradient(160deg, #1e293b, #0f172a);
    border: 3px solid #334155; display: flex; flex-direction: column; justify-content: flex-end; overflow: hidden; }
  .tile.pic { grid-column: 1 / -1; min-height: 420px; background: #1e293b center/cover no-repeat; border-color: #38bdf8; }
  .tile.pic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(11,16,38,.9)); }
  .tile.pic > * { position: relative; z-index: 1; }
  .tile .ic { position: absolute; right: 16px; top: 16px; width: 80px; height: 80px; opacity: .9; }
  .tile b { font: 900 calc(var(--pt) * 2)/1 'Arial Black', Arial, sans-serif; color: #fde047; }
  .tile small { font-size: var(--pt); font-weight: 700; color: #cbd5e1; line-height: 1.2; margin-top: 8px; }
  .tile:nth-child(3n) b { color: #4ade80; }
  .tile:nth-child(3n+1) b { color: #f472b6; }
  .note { font-size: var(--pt); font-weight: 700; line-height: 1.35; color: #e2e8f0; border-left: 8px solid #38bdf8; padding-left: 18px; }
  .note .num { color: #fde047; }
"""


def _numbers(story) -> list[tuple[str, str]]:
    """(value, label) pairs: the facts, then numbers found in the points."""
    out = [(f["value"], f["label"]) for f in story.facts if re.search(r"\d", f["value"]) and len(f["value"]) <= 12]
    for p in story.points:
        m = re.search(r"(₹?\s?[\d,.]+\s?(?:%|કરોડ|લાખ|કિમી|km|KMPH)?)", p)
        digits = re.sub(r"\D", "", m.group(1)) if m else ""
        if m and digits and len(out) < 4 and not any(digits == re.sub(r"\D", "", o[0]) for o in out):
            out.append((m.group(1).strip(), p.replace(m.group(1), "").strip(" :,-")[:40]))
    return out[:4]


def stats_page(story, font, image_url, date, handle, place, asks):
    nums = _numbers(story)
    tiles = "".join(f'<div class="tile">{icon_img(l + " " + v)}<b>{esc(v)}</b><small>{esc(l)}</small></div>' for v, l in nums)
    pic = (f'<div class="tile pic"{_bg(image_url)}>{SYM if image_url else ""}'
           f'<small>{highlight_numbers(story.subheadline or story.summary)[:160]}</small></div>')
    note = next((p for p in _pts(story, 3) if not re.search(r"\d", p)), "")
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="kick">{esc(place or story.kicker or "આંકડામાં સમાચાર")}</div>
    <div class="hl">{_hl(story)}</div>
    <div class="grid">{pic}{tiles}</div>
    {f'<div class="note">{highlight_numbers(note)}</div>' if note else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 100) + STATS_CSS, font, body)


# ------------------------------------------------------------------------------------------ polaroid
POLAROID_CSS = """
  body { background: #b07a4a; color: #1a1a1a;
    background-image: radial-gradient(rgba(0,0,0,.12) 1.5px, transparent 2px), radial-gradient(rgba(255,255,255,.08) 1.5px, transparent 2px);
    background-size: 22px 22px, 31px 31px; }
  .handle { top: 30px; left: 30px; }
  .pola { align-self: center; position: relative; background: #fff; padding: 22px 22px 80px; transform: rotate(-3deg);
    box-shadow: 0 20px 40px rgba(0,0,0,.45); width: 820px; }
  .pola .img { position: relative; height: 520px; background: #ddd center/cover no-repeat; }
  .pola .img .sym { bottom: 10px; }
  .pola .cap { position: absolute; left: 0; right: 0; bottom: 14px; text-align: center; font-size: 40px; font-weight: 800; color: #444; }
  .tape { position: absolute; top: -26px; width: 200px; height: 60px; background: rgba(255,240,180,.85); }
  .tape.l { left: 40px; transform: rotate(-12deg); } .tape.r { right: 40px; transform: rotate(10deg); }
  .strip { background: #fff; padding: 12px 10px 4px; transform: rotate(1deg); box-shadow: 0 12px 26px rgba(0,0,0,.35); }
  .strip .hl div { color: #1a1a1a; }
  .strip .hl .hi { color: #d00000; background: #fff176; padding: 0 10px; }
  .notes { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
  .note { position: relative; padding: 30px 20px 18px; font-size: var(--pt); font-weight: 700; line-height: 1.3;
    box-shadow: 0 10px 20px rgba(0,0,0,.3); }
  .note:nth-child(4n+1) { background: #fff176; transform: rotate(-2deg); }
  .note:nth-child(4n+2) { background: #f8bbd0; transform: rotate(2deg); }
  .note:nth-child(4n+3) { background: #b9f6ca; transform: rotate(1.5deg); }
  .note:nth-child(4n+4) { background: #b3e5fc; transform: rotate(-1.5deg); }
  .note.wide { grid-column: 1 / -1; }
  .note::before { content: ""; position: absolute; top: 8px; left: 50%; width: 28px; height: 28px; margin-left: -14px; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #ff6b6b, #b00020); box-shadow: 0 3px 4px rgba(0,0,0,.4); }
  .note .num { color: #d00000; }
  .foot { color: #fff; }
"""


def polaroid_page(story, font, image_url, date, handle, place, asks):
    pts = _pts(story, 4)
    notes = "".join(f'<div class="note{" wide" if len(pts) % 2 and i == len(pts) - 1 else ""}">{highlight_numbers(p)}</div>'
                    for i, p in enumerate(pts))
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="pola"><div class="tape l"></div><div class="tape r"></div><div class="img"{_bg(image_url)}>{SYM if image_url else ""}</div>
      <div class="cap">{esc(place or story.kicker or date)}</div></div>
    <div class="strip"><div class="hl">{_hl(story)}</div></div>
    {f'<div class="notes">{notes}</div>' if notes else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 70) + POLAROID_CSS, font, body)


# ------------------------------------------------------------------------------------------ magazine
MAGAZINE_CSS = """
  body { background: #111; }
  .bgpic { position: absolute; inset: 0; background: #333 center/cover no-repeat; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.45) 0%, rgba(0,0,0,0) 22%,
    rgba(0,0,0,.1) 45%, rgba(0,0,0,.85) 75%, #000 100%); }
  .mast { text-align: center; font: 900 150px/0.95 'Arial Black', Arial, sans-serif; color: #fff; letter-spacing: -4px;
    text-shadow: 0 8px 24px rgba(0,0,0,.5); }
  .mast span { color: #ff1744; }
  .issue { display: flex; justify-content: space-between; font-size: 28px; font-weight: 800; color: #fff; border-top: 3px solid #fff;
    border-bottom: 3px solid #fff; padding: 4px 6px 8px; }
  .lines { display: flex; flex-direction: column; gap: 16px; width: 62%; }
  .lines p { font-size: var(--pt); font-weight: 800; line-height: 1.25; color: #fff; text-shadow: 0 3px 10px rgba(0,0,0,.9);
    border-left: 10px solid #ffd60a; padding-left: 14px; }
  .lines .num { color: #ffd60a; }
  .kick { align-self: flex-start; background: #ff1744; color: #fff; font-size: 38px; font-weight: 800; padding: 4px 22px 8px; }
  .hl { align-items: flex-start; gap: 0; }
  .hl div { text-align: left; padding: 0 0 6px; color: #fff; text-shadow: 0 6px 20px rgba(0,0,0,.8); }
  .hl .hi { color: #ffd60a; }
  .sym { top: 300px; }
"""


def magazine_page(story, font, image_url, date, handle, place, asks):
    lines = "".join(f"<p>{highlight_numbers(p)}</p>" for p in _pts(story, 3))
    body = f"""<div class="bgpic"{_bg(image_url)}></div>{SYM if image_url else ""}
  <div id="main">
    <div class="mast">VALSAD<span>VIEW</span></div>
    <div class="issue"><span>{esc(handle)}</span><span>{esc(place or "દક્ષિણ ગુજરાત")}</span><span>{esc(date)}</span></div>
    <div class="grow"></div>
    {f'<div class="lines">{lines}</div>' if lines else ""}
    {f'<div class="kick">{esc(story.kicker)}</div>' if story.kicker else ""}
    <div class="hl">{_hl(story)}</div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 40) + MAGAZINE_CSS, font, body)


# ---------------------------------------------------------------------------------------------- chat
CHAT_CSS = """
  body { background: #e5ddd5; color: #111;
    background-image: radial-gradient(rgba(0,0,0,.05) 2px, transparent 2px); background-size: 28px 28px; }
  .top { position: absolute; left: 0; right: 0; top: 0; height: 150px; background: #075e54; display: flex; align-items: center;
    gap: 20px; padding: 0 30px; z-index: 6; color: #fff; }
  .top .av { width: 96px; height: 96px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; }
  .top .av .ic { width: 70px; height: 70px; }
  .top b { font-size: 44px; display: block; line-height: 1.1; }
  .top small { font-size: 28px; color: #b2dfdb; }
  .msg { max-width: 86%; padding: 14px 22px 30px; border-radius: 22px; position: relative; font-size: var(--pt); font-weight: 700;
    line-height: 1.3; box-shadow: 0 2px 4px rgba(0,0,0,.18); }
  .msg.in { align-self: flex-start; background: #fff; border-top-left-radius: 0; }
  .msg.out { align-self: flex-end; background: #dcf8c6; border-top-right-radius: 0; }
  .msg time { position: absolute; right: 16px; bottom: 6px; font-size: 22px; color: #667; }
  .msg.out time::after { content: " ✓✓"; color: #34b7f1; }
  .msg .num { color: #075e54; }
  .msg.big { max-width: 100%; align-self: stretch; padding-top: 10px; }
  .msg.big .hl div { color: #111; padding: 0 10px 6px; }
  .msg.big .hl .hi { color: #d00000; }
  .msg.photo { padding: 10px 10px 34px; width: 80%; }
  .msg.photo .img { position: relative; height: 420px; border-radius: 16px; background: #999 center/cover no-repeat; }
  .msg.photo .img .sym { bottom: 10px; }
  .typebar { display: flex; align-items: center; gap: 16px; }
  .typebar span { flex: 1; background: #fff; border-radius: 50px; padding: 18px 30px; font-size: 34px; color: #777; font-weight: 700; }
  .typebar b { width: 96px; height: 96px; border-radius: 50%; background: #128c7e; color: #fff; font: 900 54px/96px Arial, sans-serif;
    text-align: center; }
  .foot { color: #555; }
"""


def chat_page(story, font, image_url, date, handle, place, asks):
    t = ["10:01", "10:02", "10:02", "10:03", "10:03", "10:04"]
    pts = _pts(story, 3)
    msgs = [f'<div class="msg in">{esc(place + " માં શું થયું? 👀" if place else "શું થયું? 👀")}<time>{t[0]}</time></div>',
            f'<div class="msg out big"><div class="hl">{_hl(story)}</div><time>{t[1]}</time></div>']
    if image_url:
        msgs.append(f'<div class="msg out photo"><div class="img"{_bg(image_url)}>{SYM}</div><time>{t[2]}</time></div>')
    msgs += [f'<div class="msg out">{highlight_numbers(p)}<time>{t[3 + min(i, 2)]}</time></div>' for i, p in enumerate(pts)]
    body = f"""<div class="top"><div class="av">{icon_img("megaphone")}</div><div><b>{esc(handle)}</b><small>online • {esc(date)}</small></div></div>
  <div id="main">
    {"".join(msgs)}
    <div class="grow"></div>
    <div class="typebar"><span>{_ask(story, asks)} કોમેન્ટ કરો...</span><b>➤</b></div>
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 180) + CHAT_CSS, font, body)


# ------------------------------------------------------------------------------------------ diagonal
DIAGONAL_CSS = """
  body { background: #f5f5f5; color: #111; }
  .toppic { position: absolute; left: 0; right: 0; top: 0; height: 820px; background: #333 center/cover no-repeat;
    clip-path: polygon(0 0, 100% 0, 100% 70%, 0 100%); }
  .toppic .sym { top: 20px; }
  .handle { top: 24px; right: 24px; }
  .slant { margin: 0 -60px; padding: 18px 70px 22px; background: linear-gradient(90deg, #d00000, #ff3d00); transform: rotate(-5deg);
    box-shadow: 0 16px 34px rgba(0,0,0,.35); }
  .slant .kick { display: inline-block; background: #111; color: #ffd60a; font-size: 34px; font-weight: 800; padding: 2px 18px 6px;
    margin-bottom: 6px; }
  .slant .hl div { color: #fff; text-shadow: 0 5px 0 rgba(0,0,0,.35); }
  .slant .hl .hi { color: #ffd60a; }
  .list { display: flex; flex-direction: column; gap: 14px; margin-top: 30px; }
  .li { display: flex; gap: 18px; align-items: center; background: #fff; border-radius: 20px; padding: 12px 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,.12); border-left: 14px solid #d00000; }
  .li:nth-child(even) { border-left-color: #111; }
  .li .ic { width: 70px; height: 70px; flex-shrink: 0; }
  .li p { font-size: var(--pt); font-weight: 700; line-height: 1.3; }
  .li .num { color: #d00000; }
  .foot { color: #333; }
"""


def diagonal_page(story, font, image_url, date, handle, place, asks):
    items = "".join(f'<div class="li">{icon_img(p)}<p>{highlight_numbers(p)}</p></div>' for p in _pts(story, 4))
    kick = esc(place or story.kicker or "")
    body = f"""<div class="toppic"{_bg(image_url)}>{SYM if image_url else ""}</div><div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="slant">{f'<div class="kick">{kick}</div>' if kick else ""}<div class="hl">{_hl(story)}</div></div>
    {f'<div class="list">{items}</div>' if items else ""}
    <div class="grow"></div>
    {_askbar(story, asks)}
    {_foot(story, date)}
  </div>"""
    return _page(_base(font, 560, 380) + DIAGONAL_CSS, font, body)


MORE_LAYOUTS = {
    "tv": tv_page, "paper": paper_page, "quote": quote_page, "timeline": timeline_page, "versus": versus_page,
    "alert": alert_page, "notice": notice_page, "stats": stats_page, "polaroid": polaroid_page,
    "magazine": magazine_page, "chat": chat_page, "diagonal": diagonal_page,
}

MORE_STEPS2 = [
    [".live, .mast, .sign, .band, .qmark, .top", "dropIn", 0.0, 0.4, 0],
    [".screen, .pola, .photo", "zoomIn", 0.1, 0.45, 0],
    [".slant", "slideL", 0.15, 0.45, 0],
    [".side", "slideAlt", 0.9, 0.4, 0.1],
    [".bolt, .stamp, .seal", "slam", 1.2, 0.4, 0],
    [".msg", "popIn", 0.2, 0.3, 0.25],
    [".item, .step, .tile, .note, .li, .row, .lines p, .cols p, .pts p, .black p", "popIn", 1.2, 0.3, 0.12],
    [".ticker, .typebar, .who, .chg, .strip", "riseUp", 1.0, 0.4, 0],
]
