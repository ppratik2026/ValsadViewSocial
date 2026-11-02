"""Viral design, modelled on the popular Gujarati news posters (Gemini-made) that the page owner picked:

- a big picture (realistic AI picture or stock photo, never a real person's face) filling the top of the poster,
  or the whole poster behind the text;
- a "BREAKING NEWS | વાપી - વલસાડ" bar with the place of the story;
- the headline in heavy letters on red brush strips, every other line in yellow, the key word extra big;
- fact chips (date, amount ...) and a box of points with icons;
- a yellow brush strip at the bottom with a question to the viewers and "comment" call.

Every Gujarati word is real text in a real font, so the spelling is always right (image AIs break Gujarati letters).
"""
import os
import random
import re

from src.bulletin import _headline
from src.designs import BRUSH_MASK, esc, highlight_numbers
from src.icons import icon_img

# shrink the headline until each strip fits on one line, then the points until everything fits
# 1) shrink the headline until each strip fits on one line; 2) with too much text, make the picture smaller
# (down to MIN_TOP); 3) only then shrink the text; 4) with space left over, grow the points a little
FIT = """() => {
  const root = document.documentElement.style;
  const top0 = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--top'));
  const minTop = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--min-top'));
  const v = {hl: 124, pt: 44, chip: 44, ask: 50, top: top0};
  const set = () => { for (const k in v) root.setProperty('--' + k, v[k] + 'px'); };
  set();
  const wide = () => [...document.querySelectorAll('.hl div')].some(el => el.scrollWidth > el.clientWidth + 2);
  while (wide() && v.hl > 54) { v.hl -= 2; set(); }
  const main = document.getElementById('main');
  const over = () => main.scrollHeight > main.clientHeight + 4;
  while (over() && v.top > minTop) { v.top -= 10; set(); }
  while (over() && (v.pt > 28 || v.hl > 60)) {
    if (v.pt > 28) v.pt -= 1;
    if (v.pt <= 36 && v.hl > 60) v.hl -= 2;
    v.chip = Math.max(30, v.chip - 1); v.ask = Math.max(36, v.ask - 1); set();
  }
  const grow = document.querySelector('.grow');
  while (!over() && grow && grow.clientHeight > 60 && v.pt < 54) { v.pt += 1; set(); }
  if (over()) { v.pt -= 1; set(); }
  return !over();
}"""

# page colours, headline strips, highlight colour, points box and bottom strip, per look
PALETTES = {
    # night police / crime poster: black-red with neon box and hazard stripes
    "red": {"bg": "#0d0203", "bg2": "#2a0507", "strip": "#e10600", "strip2": "#8f0000", "hl": "#ffffff",
            "hl2": "#ffe600", "box": "rgba(8,8,18,.88)", "box_text": "#ffffff", "box_border": "#ff2e63",
            "num": "#ffe600", "ask": "#ffe600", "ask_text": "#7a0000", "tag": "#ffe600", "hazard": True},
    # info / rule: deep purple with neon glow
    "purple": {"bg": "#12062e", "bg2": "#2b0f63", "strip": "#7b2ff7", "strip2": "#4a12b8", "hl": "#ffffff",
               "hl2": "#ffd60a", "box": "rgba(30,16,70,.9)", "box_text": "#ffffff", "box_border": "#c77dff",
               "num": "#ffd60a", "ask": "#ffd60a", "ask_text": "#3c096c", "tag": "#ffd60a", "hazard": False},
    # money / prices: navy with red strips and a white box
    "navy": {"bg": "#061a4d", "bg2": "#0b2d7a", "strip": "#d90429", "strip2": "#9b0019", "hl": "#ffffff",
             "hl2": "#ffd000", "box": "rgba(255,255,255,.96)", "box_text": "#0b1d4d", "box_border": "#ffd000",
             "num": "#d90429", "ask": "#ffd000", "ask_text": "#9b0019", "tag": "#ffd000", "hazard": False},
    # weather / alert: dark storm blue with red strips
    "storm": {"bg": "#04101f", "bg2": "#0d2a4a", "strip": "#c1121f", "strip2": "#780000", "hl": "#ffffff",
              "hl2": "#ffea00", "box": "rgba(4,16,31,.88)", "box_text": "#ffffff", "box_border": "#ffea00",
              "num": "#ffea00", "ask": "#ffea00", "ask_text": "#780000", "tag": "#ffea00", "hazard": False},
    # good news: green with gold
    "green": {"bg": "#032b17", "bg2": "#0b5d2e", "strip": "#138a36", "strip2": "#0b5d20", "hl": "#ffffff",
              "hl2": "#ffe14d", "box": "rgba(255,255,255,.96)", "box_text": "#0b3d1e", "box_border": "#ffe14d",
              "num": "#d9480f", "ask": "#ffe14d", "ask_text": "#0b5d20", "tag": "#ffe14d", "hazard": False},
}

# top tag text and the looks that fit, per mood
MOOD_LOOK = {
    "breaking": ("બ્રેકિંગ ન્યૂઝ", ["red", "storm"]),
    "money": ("મહત્વના સમાચાર", ["navy", "red"]),
    "info": ("મહત્વના સમાચાર", ["purple", "navy", "storm"]),
    "happy": ("ખુશખબર", ["green", "purple"]),
}
WEATHER = re.compile(r"વરસાદ|માવઠ|વાવાઝોડ|આગાહી|ચક્રવાત|હવામાન|ઠંડી|ગરમી|પૂર|દરિયો|દરિયા|rain|cyclone|weather", re.I)

# stock photo searches when the AI gave none (or as extra tries): English, places and objects, never people's names
STOCK_SEARCHES = {
    "crime": ["police checkpoint night", "police car lights night", "police barricade road"],
    "politics": ["election rally crowd india", "microphones podium speech", "indian parliament"],
    "government": ["indian government office", "official documents stamp", "india road construction"],
    "trending": ["india city street traffic", "crowd india street", "smartphone news"],
    "good_news": ["indian students celebrating", "trophy medal winner", "indian festival celebration"],
}
WEATHER_SEARCHES = ["monsoon rain storm", "dark storm clouds sea", "cyclone waves coast"]
MONEY_SEARCHES = ["indian rupee notes", "petrol pump fuel", "market vegetables india"]


def stock_keywords(story) -> list[str]:
    """What to search for on the stock photo sites: the AI's own searches first, then ones for the topic."""
    text = f"{story.headline} {story.summary}"
    extra = (WEATHER_SEARCHES if WEATHER.search(text)
             else MONEY_SEARCHES if re.search(r"₹|ભાવ|પેટ્રોલ|ડીઝલ|price", text, re.I)
             else STOCK_SEARCHES.get(story.category, STOCK_SEARCHES["trending"]))
    own = [k for k in story.image_keywords if k and k.lower() not in ("gujarat", "valsad", "india news")]
    return own[:3] + extra


ASKS = ["તમારું શું માનવું છે?", "તમારો મત શું છે?", "આ વિશે તમે શું કહેશો?"]

CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1080px; height: 1920px; overflow: hidden; }
  body { font-family: '%(font)s', 'Noto Sans Gujarati', 'Noto Color Emoji', sans-serif; position: relative;
    color: #fff; background: radial-gradient(circle at 50%% 70%%, %(bg2)s 0%%, %(bg)s 75%%); }
  :root { --top: %(main_top)spx; --min-top: %(min_top)spx; }
  .v-pic { position: absolute; left: 0; right: 0; top: 0; height: %(pic_h)s; background: %(bg2)s center/cover no-repeat; }
  .v-pic::after { content: ""; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,.35) 0%%, transparent 22%%, transparent %(fade_at)s%%, %(bg)s 100%%); }
  .v-pic .sym { position: absolute; right: 18px; top: calc(var(--top) - 60px); z-index: 2; background: rgba(0,0,0,.55);
    color: #fff; font-size: 22px; font-weight: 700; padding: 4px 14px; border-radius: 12px; }
  .v-top { position: absolute; left: 34px; right: 34px; top: 34px; display: flex; justify-content: space-between;
    align-items: center; z-index: 5; }
  .v-handle { background: rgba(0,0,0,.55); border: 3px solid %(tag)s; color: #fff; font-size: 30px; font-weight: 800;
    padding: 6px 22px; border-radius: 40px; }
  .v-date { background: %(strip)s; color: #fff; font-size: 30px; font-weight: 800; padding: 6px 22px; border-radius: 40px;
    border: 3px solid #fff; }
  #main { position: absolute; left: 30px; right: 30px; top: var(--top); bottom: 26px; display: flex;
    flex-direction: column; gap: 22px; z-index: 4; }
  #main > * { flex-shrink: 0; }
  .v-tag { display: flex; align-items: stretch; align-self: center; border-radius: 22px; overflow: hidden;
    border: 4px solid #fff; box-shadow: 0 12px 30px rgba(0,0,0,.55); max-width: 100%%; }
  .v-tag .t1 { background: linear-gradient(180deg, %(strip)s, %(strip2)s); color: #fff; font-size: 34px; font-weight: 800;
    line-height: 1.05; padding: 10px 22px; display: flex; align-items: center; gap: 12px; text-align: center; }
  .v-tag .t1 .ic { width: 58px; height: 58px; }
  .v-tag .t2 { background: rgba(10,10,25,.92); color: %(tag)s; font-size: 70px; font-weight: 800; line-height: 1.15;
    padding: 6px 34px 12px; white-space: nowrap; text-shadow: 0 4px 0 rgba(0,0,0,.6); }
  .hazard { height: 26px; margin: 0 -30px; background: repeating-linear-gradient(-45deg, #ffd000 0 34px, #111 34px 68px);
    box-shadow: 0 6px 14px rgba(0,0,0,.5); }
  .hl { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .hl div { -webkit-mask-image: %(mask)s; -webkit-mask-size: 100%% 100%%; mask-image: %(mask)s; mask-size: 100%% 100%%;
    background: linear-gradient(180deg, %(strip)s, %(strip2)s); color: %(hl)s; font-size: var(--hl); font-weight: 800;
    line-height: 1.24; padding: 6px 44px 14px; text-align: center; max-width: 100%%; white-space: nowrap; overflow: hidden;
    -webkit-text-stroke: 3px rgba(0,0,0,.55); paint-order: stroke fill; text-shadow: 0 6px 0 rgba(0,0,0,.55); }
  .hl div:nth-child(even) { color: %(hl2)s; }
  .hl .hi { font-size: 1.3em; color: %(hl2)s; display: inline-block; line-height: 1; }
  .hl div:nth-child(even) .hi { color: #fff; }
  .sub { text-align: center; font-size: calc(var(--pt) * 1.05); font-weight: 800; color: #fff; line-height: 1.3;
    text-shadow: 0 3px 8px rgba(0,0,0,.8); }
  .sub .num { color: %(hl2)s; }
  .chips { display: flex; justify-content: center; gap: 18px; flex-wrap: wrap; }
  .chip { display: flex; align-items: center; gap: 14px; background: #fff; color: #111; border-radius: 26px;
    padding: 8px 26px 8px 10px; border: 5px solid %(strip)s; box-shadow: 0 10px 24px rgba(0,0,0,.45); }
  .chip .ic { width: 70px; height: 70px; }
  .chip small { display: block; font-size: calc(var(--chip) * .6); font-weight: 800; color: #555; line-height: 1.1; }
  .chip b { display: block; font-size: var(--chip); font-weight: 800; color: %(strip2)s; line-height: 1.15; }
  .box { background: %(box)s; color: %(box_text)s; border-radius: 30px; border: 4px solid %(box_border)s;
    box-shadow: 0 0 26px %(box_border)s, 0 16px 34px rgba(0,0,0,.5); padding: 18px 28px; display: flex;
    flex-direction: column; gap: 4px; }
  .box h3 { align-self: flex-start; background: %(hl2)s; color: #1a1a1a; font-size: calc(var(--pt) * .95); font-weight: 800;
    padding: 2px 22px 6px; border-radius: 14px; margin-bottom: 6px; }
  .pt { display: flex; gap: 16px; align-items: flex-start; font-size: var(--pt); font-weight: 700; line-height: 1.32;
    padding: 8px 0; border-bottom: 2px dashed rgba(127,127,127,.35); }
  .pt:last-child { border-bottom: 0; }
  .pt .ic { width: calc(var(--pt) * 1.25); height: calc(var(--pt) * 1.25); flex-shrink: 0; margin-top: 2px; }
  .pt .num, .pt b { color: %(num)s; font-weight: 800; }
  .grow { flex: 1 1 auto; min-height: 0; }
  .v-ask { display: flex; align-items: center; gap: 18px; }
  .v-ask .q { width: 120px; height: 120px; flex-shrink: 0; border-radius: 50%%; background: #1565ff; color: #fff;
    font: 900 86px/112px Arial, sans-serif; text-align: center; border: 6px solid #fff; box-shadow: 0 10px 24px rgba(0,0,0,.5); }
  .v-ask .say { flex: 1; -webkit-mask-image: %(mask)s; -webkit-mask-size: 100%% 100%%; mask-image: %(mask)s;
    mask-size: 100%% 100%%; background: %(ask)s; color: %(ask_text)s; font-size: var(--ask); font-weight: 800; line-height: 1.2;
    padding: 14px 34px 20px; text-align: center; }
  .v-ask .say small { display: block; font-size: calc(var(--ask) * .72); color: #1a1a1a; }
  .foot { display: flex; justify-content: space-between; font-size: 25px; font-weight: 700; color: rgba(255,255,255,.85); }
"""


def _place_tag(story, places: list[str]) -> str:
    """'વાપી - વલસાડ': the page's places named in the story (at most two), or '' if none."""
    text = " ".join([story.headline, story.subheadline, story.summary, *story.points])
    found = sorted({p for p in places if p in text}, key=text.index)
    return " - ".join(found[:2])


def _points(story) -> list[str]:
    points = [p for p in story.points if p.strip()][:5]
    if len(points) < 2 and story.summary:   # no points: the summary, one sentence per row
        points = [s.strip() for s in re.split(r"(?<=[.!?।])\s+", story.summary) if s.strip()][:4]
    return [p for p in points if story.headline not in p]   # never the headline a second time


def _chips(story) -> str:
    """Up to two short facts (date, amount, place ...) as white chips with an icon."""
    facts = [f for f in story.facts if len(f.get("value", "")) <= 18][:2]
    return "".join(f'<div class="chip">{icon_img(f["label"] + " " + f["value"])}<div><small>{esc(f["label"])}</small>'
                   f'<b>{esc(f["value"])}</b></div></div>' for f in facts)


# which layouts fit which kind of story (the first ones fit best); every story can also use the general ones
TEMPLATE_RULES = [
    ("weather", ["storm", "alert", "magazine"]),
    ("crime", ["police", "tv", "diagonal", "alert"]),
    ("politics", ["quote", "tv", "paper"]),
    ("government", ["notice", "timeline", "card", "paper"]),
    ("money", ["tips", "stats", "versus"]),
    ("numbers", ["bignews", "stats"]),
    ("compare", ["versus"]),
    ("good_news", ["polaroid", "magazine", "card"]),
    ("trending", ["chat", "magazine", "tv", "diagonal"]),
    ("steps", ["timeline", "tips"]),
]
GENERAL = ["card", "diagonal", "paper", "chat", "polaroid"]
ALL_TEMPLATES = ["police", "storm", "bignews", "tips", "card", "tv", "paper", "quote", "timeline", "versus", "alert",
                 "notice", "stats", "polaroid", "magazine", "chat", "diagonal"]


def _kinds(story, mood: str) -> set[str]:
    text = f"{story.headline} {story.summary}"
    kinds = {story.category}
    if WEATHER.search(text):
        kinds.add("weather")
    if mood == "breaking":
        kinds.add("crime" if story.category == "crime" else "trending")
    if mood == "money" or re.search(r"₹|ભાવ|પેટ્રોલ|ડીઝલ", text):
        kinds.add("money")
    if any(re.search(r"\d", f["value"]) and len(f["value"]) <= 9 for f in story.facts):
        kinds.add("numbers")
    if (story.compare or {}).get("before") or len(story.facts) >= 2:
        kinds.add("compare")
    if len([p for p in story.points if p]) >= 3:
        kinds.add("steps")
    return kinds


def choose_template(story, mood: str, allowed: list[str] | None = None) -> str:
    """Which layout this story gets: one that fits the story, not one of the last few posts' layouts (so the
    profile grid keeps changing), favouring the layouts whose reels did better. VIRAL_TEMPLATE forces one."""
    forced = os.environ.get("VIRAL_TEMPLATE", "")
    if forced:
        return forced
    allowed = [t for t in (allowed or ALL_TEMPLATES) if t in ALL_TEMPLATES] or ALL_TEMPLATES
    kinds = _kinds(story, mood)
    fitting = []
    for kind, names in TEMPLATE_RULES:
        if kind in kinds:
            fitting += [n for n in names if n not in fitting]
    if not _from_compare(story):
        fitting = [t for t in fitting if t != "versus"]
    fitting = [t for t in fitting if t in allowed] + [t for t in GENERAL if t in allowed and t not in fitting]
    from src.history import load_history
    recent = [(p.get("style") or {}).get("template") for p in load_history()[-4:]]
    fresh = [t for t in fitting if t not in recent] or fitting
    if random.random() < 0.5:
        return fresh[0]
    from src.analytics import weighted_choice
    return weighted_choice(fresh[:6], "template")


def _from_compare(story) -> bool:
    from src.viral_more import versus_parts
    return versus_parts(story) is not None


def viral_page(story, font: str, image_url: str | None, date: str, handle: str, mood: str,
               places: list[str] | None = None, allowed: list[str] | None = None) -> str:
    template = choose_template(story, mood, allowed)
    story.style["template"] = template
    if template != "police":
        from src.viral_layouts import LAYOUTS
        from src.viral_more import MORE_LAYOUTS
        page = {**LAYOUTS, **MORE_LAYOUTS}.get(template)
        if page:
            return page(story, font, image_url, date, handle, _place_tag(story, places or []), ASKS)
    tag_text, looks = MOOD_LOOK.get(mood, MOOD_LOOK["info"])
    weather = bool(WEATHER.search(f"{story.headline} {story.summary}"))
    if weather:
        looks = ["storm"] + [x for x in looks if x != "storm"]
    forced = os.environ.get("CARD_PALETTE", "")
    from src.analytics import weighted_choice
    name = forced if forced in PALETTES else weighted_choice(looks, "palette")
    pal = PALETTES[name]
    # layout: picture on the top part, or the picture behind the whole poster (the cyclone-style poster)
    layout = os.environ.get("VIRAL_LAYOUT") or weighted_choice(["top", "full"], "layout")
    story.style.update({"palette": name, "layout": layout})
    if layout == "full":
        pic_h, fade_at, main_top, min_top = "1920px", 30, 640, 420
    else:   # the picture ends a little below where the text starts, fading into the page colour
        pic_h, fade_at, main_top, min_top = "calc(var(--top) + 170px)", 55, 690, 470
    css = CSS % {**pal, "font": font, "mask": BRUSH_MASK, "pic_h": pic_h, "fade_at": fade_at, "main_top": main_top,
                 "min_top": min_top}
    if layout == "full":   # text sits on the picture: darken it more
        css += ".v-pic::after { background: linear-gradient(180deg, rgba(0,0,0,.35) 0%, rgba(0,0,0,.05) 18%, " \
               f"rgba(0,0,0,.55) 38%, {pal['bg']}e6 70%, {pal['bg']} 100%); }}"

    place = _place_tag(story, places or [])
    siren = icon_img("siren" if mood == "breaking" else ("trophy" if mood == "happy" else "megaphone"))
    tag = (f'<div class="v-tag"><div class="t1">{siren}<span>{esc(tag_text).replace(" ", "<br>", 1)}</span></div>'
           f'<div class="t2">{esc(place or story.kicker or tag_text)}</div></div>')
    hazard = '<div class="hazard"></div>' if pal["hazard"] else ""
    sub = f'<div class="sub">{highlight_numbers(story.subheadline)}</div>' if story.subheadline else ""
    chips = _chips(story)
    chips = f'<div class="chips">{chips}</div>' if chips else ""
    points = _points(story)
    bullet = "check" if mood == "happy" else ("alert" if mood == "breaking" else "pin")
    rows = "".join(f'<div class="pt">{icon_img(bullet)}<span>{highlight_numbers(p)}</span></div>' for p in points)
    box = f'<div class="box"><h3>{esc(story.kicker or "મુખ્ય મુદ્દા")}</h3>{rows}</div>' if rows else ""
    ask = esc(story.comment.strip(" 👇") if story.comment and len(story.comment) <= 70 else random.choice(ASKS))
    if image_url:
        sym = '<div class="sym">પ્રતિકાત્મક તસવીર</div>'
        pic = f'<div class="v-pic" style="background-image:url({image_url})">{sym}</div>'
    else:
        pic = '<div class="v-pic"></div>'

    font_url = font.replace(" ", "+")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={font_url}:wght@500;700;800&display=block" rel="stylesheet">
<style>{css}</style></head><body>
  {pic}
  <div class="v-top"><div class="v-handle">{esc(handle)}</div><div class="v-date">{esc(date)}</div></div>
  <div id="main">
    {tag}
    {hazard}
    <div class="hl">{_headline(story)}</div>
    {sub}
    {chips}
    {box}
    <div class="grow"></div>
    <div class="v-ask"><div class="q">?</div><div class="say">{ask}<small>કોમેન્ટ કરીને જરૂર જણાવો 👇</small></div></div>
    <div class="foot"><span>સ્રોત: {esc(story.source_name)}</span><span>{esc(handle)}</span></div>
  </div></body></html>"""


# intro animation of the reel: the picture is there from the very first frame (a blank start makes people scroll
# on), then tag, headline, facts, points and the question pop in
VIRAL_STEPS = [
    [".v-tag", "dropIn", 0.0, 0.4, 0],
    [".hazard", "slideL", 0.2, 0.35, 0],
    [".hl div", "punchIn", 0.2, 0.4, 0.12],
    [".sub", "fadeIn", 1.0, 0.3, 0],
    [".chip", "popIn", 1.15, 0.35, 0.15],
    [".box", "fadeIn", 1.4, 0.25, 0],
    [".pt", "slideL", 1.5, 0.35, 0.14],
    [".v-ask", "riseUp", 2.3, 0.45, 0],
    [".foot, .v-top", "fadeIn", 2.6, 0.3, 0],
]
from src.viral_layouts import MORE_STEPS  # noqa: E402  (the other layouts' elements)
from src.viral_more import MORE_STEPS2  # noqa: E402
VIRAL_STEPS = VIRAL_STEPS + MORE_STEPS2 + MORE_STEPS
