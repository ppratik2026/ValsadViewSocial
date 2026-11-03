"""More layouts for the viral design, each modelled on one of the reference posters the page owner picked:

- storm:    the picture fills the whole poster, a place pin on top, a giant stacked headline (white line, then
            yellow lines on red brush strips), a date strip with a calendar, and a dark info box at the bottom
            (the cyclone poster);
- bignews:  a "BIG NEWS" pill, the headline in a white glowing card, a glass box with the details (numbers in
            yellow), the picture below with round number badges like road signs (the speeding-memo poster);
- tips:     headline strips in four colours, a myth/warning box, "check these N things" and numbered tip cards
            with the values (the petrol pump poster);
- card:     the headline on the picture with a highlighted line, a white card with coloured icon circles for the
            points, and the "?" question strip with a comment bubble (the iPhone poster).

The police poster (photo, place tag, hazard stripes, red strips, neon points box) is in src/viral.py. All of them
use the same fitting script (src/viral.FIT): --hl for the headline lines, --pt for the body text, --top / --min-top
for the picture height, and a .grow spacer that lets the body text grow into free space.
"""
import re

from src.designs import BRUSH_MASK, esc, highlight_numbers
from src.icons import icon_img

BASE = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1080px; height: 1920px; overflow: hidden; }
  body { font-family: '%(font)s', 'Noto Sans Gujarati', 'Noto Color Emoji', sans-serif; position: relative; color: #fff; }
  :root { --top: %(top)spx; --min-top: %(min_top)spx; }
  #main { position: absolute; left: 30px; right: 30px; top: var(--top); bottom: 24px; display: flex;
    flex-direction: column; gap: 22px; z-index: 4; }
  #main > * { flex-shrink: 0; }
  .grow { flex: 1 1 auto; min-height: 0; }
  .brush { -webkit-mask-image: %(mask)s; -webkit-mask-size: 100%% 100%%; mask-image: %(mask)s; mask-size: 100%% 100%%; }
  .hl { display: flex; flex-direction: column; align-items: center; gap: 6px; }
  .hl div { font-size: var(--hl); font-weight: 800; line-height: 1.22; padding: 4px 40px 12px; text-align: center;
    max-width: 100%%; white-space: nowrap; overflow: hidden; }
  .hl .hi { font-size: 1.25em; display: inline-block; line-height: 1; }
  .num { font-weight: 800; }
  .sym { position: absolute; right: 16px; z-index: 3; background: rgba(0,0,0,.55); color: #fff; font-size: 22px;
    font-weight: 700; padding: 4px 14px; border-radius: 12px; }
  .handle { position: absolute; z-index: 6; font-size: 28px; font-weight: 800; padding: 6px 20px; border-radius: 40px;
    background: rgba(0,0,0,.55); border: 3px solid #ffd60a; color: #fff; }
  .foot { display: flex; justify-content: space-between; font-size: 25px; font-weight: 700; color: rgba(255,255,255,.85); }
  .v-ask { display: flex; align-items: center; gap: 16px; }
  .v-ask .q { width: 116px; height: 116px; flex-shrink: 0; border-radius: 50%%; background: #1565ff; color: #fff;
    font: 900 84px/108px Arial, sans-serif; text-align: center; border: 6px solid #fff; box-shadow: 0 10px 24px rgba(0,0,0,.5); }
  .v-ask .say { flex: 1; background: #ffd60a; color: #1a1a1a; font-size: var(--ask); font-weight: 800; line-height: 1.2;
    padding: 14px 30px 20px; text-align: center; }
  .v-ask .say b { color: #c1121f; }
  .v-ask .bubble { flex-shrink: 0; background: #d00000; color: #fff; font-size: calc(var(--ask) * .62); font-weight: 800;
    padding: 14px 20px 18px; text-align: center; line-height: 1.2; transform: rotate(-4deg); }
"""


def _lines(text: str, n: int) -> list[str]:
    """Split text into n lines of similar length, at word boundaries."""
    words = text.split()
    n = max(1, min(n, len(words)))
    target = len(text) / n
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + len(w) > target * 1.15 and len(lines) < n - 1:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


def _hi(line: str, highlight: str) -> str:
    """The line, escaped, with the highlight word (or its number) wrapped in .hi."""
    text = esc(line)
    for word in ([highlight] + sorted(highlight.split(), key=lambda w: not re.search(r"\d", w))) if highlight else []:
        if word and word in line:
            return text.replace(esc(word), f'<span class="hi">{esc(word)}</span>', 1)
    return text


def _n_lines(headline: str) -> int:
    return 2 if len(headline) < 30 else 3 if len(headline) < 62 else 4


def _ask(story, asks: list[str]) -> str:
    import random
    text = story.comment.strip(" 👇") if story.comment and len(story.comment) <= 70 else random.choice(asks)
    return esc(text)


def _date_fact(story) -> dict | None:
    return next((f for f in story.facts if re.search(r"તારીખ|દિવસ|date|સુધી", f["label"] + f["value"], re.I)), None)


def _num_facts(story) -> list[dict]:
    """Facts whose value is a short number (for the round badges)."""
    return [f for f in story.facts if re.search(r"\d", f["value"]) and len(f["value"]) <= 9][:2]


def _page(css: str, font: str, body: str) -> str:
    font_url = font.replace(" ", "+")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={font_url}:wght@500;700;800&display=block" rel="stylesheet">
<style>{css}</style></head><body>{body}</body></html>"""


# ---------------------------------------------------------------- storm (the cyclone poster)
STORM_CSS = """
  body { background: #06101e; }
  .bgpic { position: absolute; inset: 0; background: #0d2a4a center/cover no-repeat; }
  .bgpic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.25) 0%%,
    rgba(0,0,0,.15) 25%%, rgba(4,12,28,.55) 50%%, rgba(4,12,28,.8) 78%%, #040c1c 100%%); }
  .pin { position: absolute; top: 34px; right: 34px; z-index: 6; display: flex; align-items: center; gap: 10px;
    background: #fff; color: #c1121f; font-size: 46px; font-weight: 800; padding: 6px 26px 10px 14px; border-radius: 22px;
    border: 5px solid #c1121f; box-shadow: 0 10px 26px rgba(0,0,0,.5); }
  .pin .ic { width: 60px; height: 60px; }
  .handle { top: 44px; left: 34px; }
  .hl div:first-child { color: #fff; -webkit-text-stroke: 4px #111; paint-order: stroke fill;
    text-shadow: 0 8px 0 rgba(0,0,0,.6); background: none; }
  .hl div + div { background: linear-gradient(180deg, #e10600, #8f0000); color: #ffe600; -webkit-text-stroke: 3px #5a0000;
    paint-order: stroke fill; text-shadow: 0 6px 0 rgba(0,0,0,.55); }
  .hl div:first-child .hi { color: #ffe600; }
  .hl div + div .hi { color: #fff; }
  .when { align-self: center; display: flex; align-items: center; gap: 18px; background: linear-gradient(180deg, #e10600, #8f0000);
    padding: 12px 40px 16px; }
  .when .ic { width: 84px; height: 84px; }
  .when b { color: #ffe600; font-size: calc(var(--hl) * .72); line-height: 1.1; }
  .when span { font-size: calc(var(--hl) * .5); font-weight: 800; }
  .sub { text-align: center; font-size: calc(var(--pt) * 1.1); font-weight: 800; line-height: 1.3;
    text-shadow: 0 3px 10px rgba(0,0,0,.9); }
  .sub .num { color: #ffe600; }
  .infobox { display: flex; gap: 22px; align-items: center; background: rgba(6,16,34,.92); border: 4px solid #ffd60a;
    border-radius: 28px; padding: 20px 26px; box-shadow: 0 16px 34px rgba(0,0,0,.6); }
  .infobox > .ic { width: 130px; height: 130px; flex-shrink: 0; }
  .infobox h3 { color: #ffd60a; font-size: calc(var(--pt) * 1.1); line-height: 1.2; }
  .infobox p { font-size: var(--pt); font-weight: 700; line-height: 1.32; }
  .infobox p .num { color: #ffd60a; }
"""


def storm_page(story, font, image_url, date, handle, places_tag, asks):
    css = BASE % {"font": font, "mask": BRUSH_MASK, "top": 560, "min_top": 300} + STORM_CSS % {}
    lines = _lines(story.headline, _n_lines(story.headline))
    hl = "".join(f'<div class="{"" if i == 0 else "brush"}">{_hi(line, story.highlight)}</div>'
                 for i, line in enumerate(lines))
    fact = _date_fact(story) or (story.facts[0] if story.facts else None)
    when = (f'<div class="when brush">{icon_img("calendar" if _date_fact(story) else fact["label"] + " " + fact["value"])}'
            f'<div><b>{esc(fact["value"])}</b><br><span>{esc(fact["label"])}</span></div></div>') if fact else ""
    sub = f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""
    text = " ".join(story.points[:2]) if story.points else story.summary
    box = (f'<div class="infobox">{icon_img(story.headline + " " + story.summary)}<div>'
           f'<h3>{esc(story.kicker or "મહત્વની માહિતી")}</h3><p>{highlight_numbers(text)}</p></div></div>') if text else ""
    pic = f'<div class="bgpic" style="background-image:url({image_url})"></div>' if image_url else '<div class="bgpic"></div>'
    sym = '<div class="sym" style="top:150px">પ્રતિકાત્મક તસવીર</div>' if image_url else ""
    pin = f'<div class="pin">{icon_img("pin")}<span>{esc(places_tag)}</span></div>' if places_tag else ""
    body = f"""{pic}{sym}<div class="handle">{esc(handle)}</div>{pin}
  <div id="main">
    <div class="hl">{hl}</div>
    {when}
    {sub}
    <div class="grow"></div>
    {box}
    <div class="v-ask"><div class="q">?</div><div class="say brush">{_ask(story, asks)}</div>
      <div class="bubble brush">કોમેન્ટ કરીને<br>જરૂર જણાવો</div></div>
    <div class="foot"><span>સ્રોત: {esc(story.source_name)}</span><span>{esc(date)}</span></div>
  </div>"""
    return _page(css, font, body)


# ---------------------------------------------------------------- bignews (the speeding-memo poster)
BIGNEWS_CSS = """
  body { background: radial-gradient(circle at 30%% 20%%, #4b1d9a 0%%, #22094f 45%%, #12052e 100%%); }
  body::before { content: ""; position: absolute; inset: 0; background-image:
    radial-gradient(circle, rgba(255,255,255,.8) 0 2px, transparent 3px), radial-gradient(circle, rgba(255,214,10,.7) 0 2px, transparent 3px);
    background-size: 170px 190px, 230px 260px; background-position: 20px 40px, 90px 120px; opacity: .45; }
  .handle { top: 30px; right: 30px; }
  .pill { align-self: center; display: flex; align-items: center; gap: 16px; background: linear-gradient(180deg, #5a2bb8, #2e0f74);
    border: 4px solid #c77dff; border-radius: 26px; padding: 8px 36px 12px; box-shadow: 0 0 30px rgba(199,125,255,.6); }
  .pill .ic { width: 70px; height: 70px; }
  .pill b { font: 900 76px/1.05 'Arial Black', Arial, sans-serif; color: #ffd60a; letter-spacing: 1px; }
  .pill b span { color: #fff; }
  .hlcard { background: linear-gradient(180deg, #ffffff, #ece6ff); border: 6px solid #c77dff; border-radius: 40px;
    box-shadow: 0 0 40px rgba(199,125,255,.75), 0 18px 40px rgba(0,0,0,.5); padding: 18px 10px 10px; }
  .hlcard .hl div { color: #2b0a5e; padding: 0 24px 8px; }
  .hlcard .hl .hi { color: #d00000; }
  .glass { background: rgba(255,255,255,.1); border: 3px solid rgba(255,255,255,.55); border-radius: 34px;
    padding: 22px 30px; box-shadow: inset 0 0 40px rgba(199,125,255,.25), 0 16px 34px rgba(0,0,0,.4); text-align: center; }
  .glass p { font-size: var(--pt); font-weight: 700; line-height: 1.5; }
  .glass p + p { margin-top: 8px; }
  .glass .num { color: #ffd60a; }
  .photo { flex: 1 1 auto; min-height: 360px; position: relative; border-radius: 34px; overflow: hidden;
    background: #2e0f74 center/cover no-repeat; border: 4px solid rgba(199,125,255,.8); box-shadow: 0 0 30px rgba(199,125,255,.45); }
  .photo .sym { bottom: 14px; }
  .badges { position: absolute; right: 20px; top: 20px; display: flex; gap: 16px; z-index: 2; }
  .badge { width: 190px; height: 190px; border-radius: 50%%; background: #fff; border: 18px solid #d00000; color: #111;
    display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 12px 26px rgba(0,0,0,.55); }
  .badge b { font: 900 54px/1 'Arial Black', Arial, sans-serif; }
  .badge small { font-size: 22px; font-weight: 800; line-height: 1.1; text-align: center; padding: 0 6px; }
"""


def bignews_page(story, font, image_url, date, handle, places_tag, asks):
    css = BASE % {"font": font, "mask": BRUSH_MASK, "top": 40, "min_top": 40} + BIGNEWS_CSS % {}
    lines = _lines(story.headline, _n_lines(story.headline))
    hl = "".join(f"<div>{_hi(line, story.highlight)}</div>" for line in lines)
    paras = [p for p in story.points[:3] if p not in story.headline] or ([story.summary] if story.summary else [])
    glass = "".join(f"<p>{highlight_numbers(p)}</p>" for p in paras)
    glass = f'<div class="glass">{glass}</div>' if glass else ""
    def _badge(f):   # longer values ("3 નવેમ્બર") get smaller letters so they stay inside the ring
        size = 54 if len(f["value"]) <= 4 else 40 if len(f["value"]) <= 6 else 30
        label = f["label"] if len(f["label"]) <= 22 else f["label"][:20] + "…"
        return f'<div class="badge"><b style="font-size:{size}px">{esc(f["value"])}</b><small>{esc(label)}</small></div>'
    badges = "".join(_badge(f) for f in _num_facts(story))
    style = f' style="background-image:url({image_url})"' if image_url else ""
    sym = '<div class="sym">પ્રતિકાત્મક તસવીર</div>' if image_url else ""
    tag = esc(places_tag or story.kicker or "")
    body = f"""<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="pill">{icon_img("megaphone")}<b>BIG <span>NEWS</span></b></div>
    <div class="hlcard"><div class="hl">{hl}</div></div>
    {glass}
    <div class="photo"{style}><div class="badges">{badges}</div>{sym}</div>
    <div class="foot"><span>સ્રોત: {esc(story.source_name)}{" • " + tag if tag else ""}</span><span>{esc(date)}</span></div>
  </div>"""
    return _page(css, font, body)


# ---------------------------------------------------------------- tips (the petrol pump poster)
TIPS_CSS = """
  body { background: linear-gradient(180deg, #e9f1ff 0%%, #ffffff 60%%, #eef4ff 100%%); color: #111; }
  .toppic { position: absolute; left: 0; right: 0; top: 0; height: calc(var(--top) + 230px); background: #d00000 center/cover no-repeat; }
  .toppic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.15) 0%%,
    rgba(0,0,0,.05) 40%%, rgba(233,241,255,.6) 80%%, #e9f1ff 100%%); }
  .toppic .sym { top: 20px; }
  .handle { top: 24px; left: 24px; }
  .hl { gap: 0; }
  .hl div { box-shadow: 0 8px 18px rgba(0,0,0,.25); }
  .hl div:nth-child(4n+1) { background: #d90429; color: #ffd60a; }
  .hl div:nth-child(4n+2) { background: #fff; color: #111; }
  .hl div:nth-child(4n+3) { background: #1d3fbf; color: #fff; }
  .hl div:nth-child(4n+4) { background: #ffd60a; color: #111; }
  .hl .hi { color: inherit; }
  .hl div:nth-child(4n+2) .hi, .hl div:nth-child(4n+4) .hi { color: #d90429; }
  .myth { display: flex; gap: 18px; align-items: center; background: linear-gradient(180deg, #b5001b, #7a0012); color: #fff;
    border-radius: 26px; padding: 18px 24px; box-shadow: 0 12px 26px rgba(0,0,0,.3); }
  .myth .ic { width: 96px; height: 96px; flex-shrink: 0; }
  .myth p { font-size: calc(var(--pt) * 1.05); font-weight: 800; line-height: 1.3; }
  .myth .num { color: #ffd60a; }
  .checkhead { display: flex; align-items: center; gap: 18px; background: #0b2a8f; color: #fff; border-radius: 22px;
    padding: 10px 24px 14px; }
  .checkhead .ic { width: 90px; height: 90px; flex-shrink: 0; }
  .checkhead b { font-size: calc(var(--pt) * 1.25); line-height: 1.2; }
  .checkhead b span { background: #ffd60a; color: #111; padding: 0 12px; border-radius: 8px; }
  .tips { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .tip { background: #fff; border: 3px solid #c9d6f5; border-radius: 22px; padding: 14px 18px; box-shadow: 0 8px 18px rgba(0,0,0,.12);
    display: flex; gap: 14px; align-items: flex-start; }
  .tip.wide { grid-column: 1 / -1; }
  .tip .n { width: 64px; height: 64px; flex-shrink: 0; border-radius: 50%%; background: #d90429; color: #fff;
    font: 900 40px/58px Arial, sans-serif; text-align: center; border: 3px solid #fff; box-shadow: 0 4px 10px rgba(0,0,0,.3); }
  .tip p { font-size: var(--pt); font-weight: 800; line-height: 1.3; }
  .tip .num { color: #d90429; }
  .tip.val { flex-direction: column; gap: 4px; background: #fff8dc; border-color: #f0d36b; }
  .tip.val small { background: #138a36; color: #fff; font-size: calc(var(--pt) * .8); font-weight: 800; padding: 2px 16px 6px;
    border-radius: 30px; }
  .tip.val b { font: 900 calc(var(--pt) * 1.6)/1.1 'Arial Black', Arial, sans-serif; color: #111; }
  .foot { color: #333; }
  .v-ask .say { background: #ffd60a; }
"""


def tips_page(story, font, image_url, date, handle, places_tag, asks):
    css = BASE % {"font": font, "mask": BRUSH_MASK, "top": 300, "min_top": 150} + TIPS_CSS % {}
    lines = _lines(story.headline, max(3, _n_lines(story.headline)))
    hl = "".join(f'<div class="brush">{_hi(line, story.highlight)}</div>' for line in lines)
    points = [p for p in story.points if p and p not in story.headline][:5]
    myth = ""
    if story.subheadline or story.summary:
        myth = (f'<div class="myth">{icon_img("cross" if re.search(r"નથી|ખોટ|ગેરમાન્ય|ના ", story.subheadline + story.summary) else "warning")}'
                f'<p>{highlight_numbers(story.subheadline or story.summary)}</p></div>')
    n = len(points)
    head = (f'<div class="checkhead">{icon_img("check")}<b>{esc(story.kicker or "મહત્વની વાતો")}: '
            f'<span>આ {n} વાતો</span> જાણો</b></div>') if n else ""
    cards = "".join(f'<div class="tip{" wide" if n % 2 and i == n - 1 else ""}"><div class="n">{i + 1}</div>'
                    f'<p>{highlight_numbers(p)}</p></div>' for i, p in enumerate(points))
    vals = [f for f in story.facts if len(f["value"]) <= 14][:2]
    cards += "".join(f'<div class="tip val{" wide" if len(vals) == 1 else ""}"><small>{esc(f["label"])}</small>'
                     f'<b>{esc(f["value"])}</b></div>' for f in vals)
    tips = f'<div class="tips">{cards}</div>' if cards else ""
    pic = f'<div class="toppic" style="background-image:url({image_url})"><div class="sym">પ્રતિકાત્મક તસવીર</div></div>' \
        if image_url else '<div class="toppic"></div>'
    body = f"""{pic}<div class="handle">{esc(handle)}</div>
  <div id="main">
    <div class="hl">{hl}</div>
    {myth}
    {head}
    {tips}
    <div class="grow"></div>
    <div class="v-ask"><div class="q">?</div><div class="say brush">{_ask(story, asks)}</div>
      <div class="bubble brush">કોમેન્ટ કરીને<br>જરૂર જણાવો</div></div>
    <div class="foot"><span>સ્રોત: {esc(story.source_name)}{" • " + esc(places_tag) if places_tag else ""}</span><span>{esc(date)}</span></div>
  </div>"""
    return _page(css, font, body)


# ---------------------------------------------------------------- card (the iPhone poster)
CARD_CSS = """
  body { background: linear-gradient(180deg, #0a1433 0%%, #0a1433 51%%, #1b3a9a 100%%); }
  .toppic { position: absolute; left: 0; right: 0; top: 0; height: 980px; background: #142a6b center/cover no-repeat; }
  .toppic::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 55%%, #0a1433 98%%),
    linear-gradient(90deg, rgba(5,10,30,.85) 0%%, rgba(5,10,30,.55) 55%%, rgba(5,10,30,.15) 100%%); }
  .toppic .sym { bottom: 120px; }
  .head { display: flex; flex-direction: column; align-items: flex-start; gap: 8px; }
  .head .handle { position: static; align-self: flex-end; margin-bottom: 4px; }
  .head .hl { align-items: flex-start; width: 100%%; }
  .head .hl div { padding: 2px 28px 10px; -webkit-text-stroke: 2px rgba(0,0,0,.5); paint-order: stroke fill;
    text-shadow: 0 5px 0 rgba(0,0,0,.5); }
  .head .hl div:nth-child(1) { color: #fff; padding-left: 0; }
  .head .hl div:nth-child(2) { background: #ffe600; color: #111; -webkit-text-stroke: 0; text-shadow: none; transform: rotate(-1.5deg); }
  .head .hl div:nth-child(n+3) { background: linear-gradient(180deg, #e10600, #8f0000); color: #ffe600; }
  .head .hl .hi { color: #d00000; }
  .head .hl div:nth-child(n+3) .hi, .head .hl div:nth-child(1) .hi { color: #ffe600; }
  .kick { background: #0b0b14; color: #fff; border: 4px solid #fff; border-radius: 24px; font-size: calc(var(--pt) * 1.15);
    font-weight: 800; padding: 6px 30px 10px; display: flex; align-items: center; gap: 12px; }
  .kick .ic { width: 56px; height: 56px; }
  .white { background: linear-gradient(180deg, #ffffff, #eef3ff); border-radius: 34px; padding: 12px 22px; color: #1a1a2e;
    box-shadow: 0 18px 40px rgba(0,0,0,.45); }
  .row { display: flex; gap: 22px; align-items: center; padding: 14px 4px; border-bottom: 2px solid #e1e7f5; }
  .row:last-child { border-bottom: 0; }
  .row .circ { width: 112px; height: 112px; flex-shrink: 0; border-radius: 50%%; display: flex; align-items: center;
    justify-content: center; border: 5px solid #fff; box-shadow: 0 6px 16px rgba(0,0,0,.25); }
  .row:nth-child(3n+1) .circ { background: radial-gradient(circle at 35%% 30%%, #ff6b6b, #c1121f); }
  .row:nth-child(3n+2) .circ { background: radial-gradient(circle at 35%% 30%%, #5ee27a, #138a36); }
  .row:nth-child(3n+3) .circ { background: radial-gradient(circle at 35%% 30%%, #5b8cff, #1d3fbf); }
  .row .circ .ic { width: 70px; height: 70px; }
  .row p { font-size: var(--pt); font-weight: 700; line-height: 1.35; }
  .row:nth-child(3n+1) .num { color: #c1121f; }
  .row:nth-child(3n+2) .num { color: #138a36; }
  .row:nth-child(3n+3) .num { color: #1d3fbf; }
"""


def card_page(story, font, image_url, date, handle, places_tag, asks):
    css = BASE % {"font": font, "mask": BRUSH_MASK, "top": 36, "min_top": 36} + CARD_CSS % {}
    lines = _lines(story.headline, max(3, _n_lines(story.headline)))
    hl = "".join(f'<div class="{"brush" if i else ""}">{_hi(line, story.highlight)}</div>' for i, line in enumerate(lines))
    kick = esc(places_tag or story.kicker or "")
    kick = f'<div class="kick">{icon_img(story.headline)}<span>{kick}</span></div>' if kick else ""
    points = [p for p in story.points if p and p not in story.headline][:4]
    if not points and story.summary:
        points = [s for s in re.split(r"(?<=[.!?।])\s+", story.summary) if s.strip() and story.headline not in s][:3]
    rows = "".join(f'<div class="row"><div class="circ">{icon_img(p)}</div><p>{highlight_numbers(p)}</p></div>'
                   for p in points)
    white = f'<div class="white">{rows}</div>' if rows else ""
    pic = f'<div class="toppic" style="background-image:url({image_url})"><div class="sym">પ્રતિકાત્મક તસવીર</div></div>' \
        if image_url else '<div class="toppic"></div>'
    body = f"""{pic}
  <div id="main">
    <div class="head"><div class="handle">{esc(handle)}</div><div class="hl">{hl}</div>{kick}</div>
    <div class="grow"></div>
    {white}
    <div class="v-ask"><div class="q">?</div><div class="say brush">{_ask(story, asks)}</div>
      <div class="bubble brush">કોમેન્ટ કરીને<br>જરૂર જણાવો</div></div>
    <div class="foot"><span>સ્રોત: {esc(story.source_name)}</span><span>{esc(date)}</span></div>
  </div>"""
    return _page(css, font, body)


LAYOUTS = {"storm": storm_page, "bignews": bignews_page, "tips": tips_page, "card": card_page}

# intro animation steps for these layouts (selectors that do not exist on a page are skipped)
MORE_STEPS = [
    [".pin, .pill", "dropIn", 0.0, 0.4, 0],
    [".hl div", "punchIn", 0.15, 0.4, 0.12],
    [".kick, .when", "slam", 0.8, 0.4, 0],
    [".sub, .glass, .myth", "slideL", 1.0, 0.4, 0],
    [".badge", "popIn", 1.3, 0.35, 0.15],
    [".checkhead", "slideR", 1.3, 0.35, 0],
    [".tip, .row", "popIn", 1.5, 0.3, 0.12],
    [".infobox, .white", "riseUp", 1.4, 0.4, 0],
    [".v-ask", "riseUp", 2.3, 0.45, 0],
    [".foot, .handle", "fadeIn", 2.6, 0.3, 0],
]
