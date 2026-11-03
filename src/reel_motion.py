"""Motion for the whole reel (viral design), not only its first seconds.

After the intro (elements fly / punch in, src/card.ANIM_JS), the poster keeps moving until the reel ends, like the
animated news reels of popular pages:

- the picture slowly pans / zooms (Ken Burns), so the frame is never frozen;
- the points light up one after another, as if someone is reading them out (a "reading guide");
- the highlight word pulses, LIVE / ON AIR dots and sirens blink, hazard stripes and police tape march, the
  ticker scrolls, the waveform bounces, neon flickers;
- the question strip bounces at the end, so viewers comment.

The frames are captured the same way as the intro (every animation is seeked to the frame's time), so the
video is smooth and the same every time.
"""

LIVE_CSS = """
@keyframes kbZoom { from { transform: scale(1); } to { transform: scale(1.09); } }
@keyframes kbPan { from { background-position: 35% 40%; } to { background-position: 65% 60%; } }
@keyframes pulse { 0%, 100% { transform: var(--t0, translate(0)) scale(1); } 50% { transform: var(--t0, translate(0)) scale(1.08); } }
@keyframes glowHi { 0%, 100% { filter: none; } 50% { filter: brightness(1.35) drop-shadow(0 0 14px rgba(255,230,0,.9)); } }
@keyframes blink { 0%, 45% { opacity: 1; } 50%, 95% { opacity: .25; } 100% { opacity: 1; } }
@keyframes march { from { background-position: 0 0; } to { background-position: 136px 0; } }
@keyframes scrollX { from { transform: translateX(0); } to { transform: translateX(-60%); } }
@keyframes eq { 0%, 100% { transform: scaleY(1); } 50% { transform: scaleY(.35); } }
@keyframes flicker { 0%, 18%, 22%, 62%, 66%, 100% { opacity: 1; } 20%, 64% { opacity: .55; } }
@keyframes spot { 0% { transform: var(--t0, translate(0)) scale(1); filter: none; }
  25% { transform: var(--t0, translate(0)) scale(1.045); filter: brightness(1.12) drop-shadow(0 0 18px rgba(255,214,10,.85)); }
  75% { transform: var(--t0, translate(0)) scale(1.045); filter: brightness(1.12) drop-shadow(0 0 18px rgba(255,214,10,.85)); }
  100% { transform: var(--t0, translate(0)) scale(1); filter: none; } }
@keyframes bounce { 0%, 100% { transform: var(--t0, translate(0)) translateY(0); } 30% { transform: var(--t0, translate(0)) translateY(-26px); }
  55% { transform: var(--t0, translate(0)) translateY(0); } 75% { transform: var(--t0, translate(0)) translateY(-10px); } }
@keyframes wiggle { 0%, 100% { rotate: 0deg; } 25% { rotate: -6deg; } 75% { rotate: 6deg; } }
@keyframes tapeMove { from { text-indent: 0; } to { text-indent: -420px; } }
"""

# the full-bleed picture layers zoom; the framed pictures pan inside their frame
ZOOM = ".v-pic, .bgpic, .toppic, .wall, .grid div"
PAN = ".photo, .screen, .cover, .img, .frame, .pic, .clip, .tile.pic, .board .img, .stampx div"
# rows that light up one after another, in reading order
SPOT = (".pt, .item, .step, .row, .tip, .li, .note, .noti, .nb, .led, .say:not(.v-ask .say), .msg, .ev p, .notes p, "
        ".lines p, .chap p, .chips span, .pts p, .black p, .credits p, .cols p, .list p, .stone, .tile:not(.pic), .side, "
        ".glass p, .infobox, .myth, .item, .chip, .badge")

LIVE_JS = """([start, end, sel]) => {
  const add = (el, anim) => { el.style.animation = (el.style.animation ? el.style.animation + ', ' : '') + anim; };
  const all = s => [...document.querySelectorAll(s)];
  const total = Math.max(end - start, 1);
  all(sel.zoom).forEach(el => add(el, `kbZoom ${end}s linear 0s both`));
  all(sel.pan).forEach(el => add(el, `kbPan ${end}s ease-in-out 0s both`));
  all('.hl .hi').forEach(el => add(el, `glowHi 1.4s ease-in-out ${start}s infinite`));
  all('.live i, .onair, .v-tag .t1 .ic, .pin .ic, .sign .ic').forEach(el => add(el, `blink 1s steps(1) ${start * 0}s infinite`));
  all('.hazard').forEach(el => add(el, `march 1.2s linear 0s infinite`));
  all('.ticker em').forEach(el => add(el, `scrollX ${total}s linear ${start}s both`));
  all('.tape').forEach(el => add(el, `tapeMove ${end}s linear 0s both`));
  all('.wave i').forEach((el, i) => add(el, `eq ${0.5 + (i % 5) * 0.12}s ease-in-out ${i * 0.05}s infinite`));
  all('.ring, .boom, .bolt').forEach(el => add(el, `pulse 1.6s ease-in-out ${start}s infinite`));
  all('.neon-on, body .sign').forEach(el => { if (getComputedStyle(el).boxShadow.includes('rgb(255, 46, 136)')) add(el, `flicker 2.4s linear ${start}s infinite`); });
  // the call to comment: the "?" bounces and the bubble wiggles in the last seconds
  const askAt = Math.max(start, end - 2.4);
  all('.v-ask .q').forEach(el => add(el, `bounce .9s ease-out ${askAt}s 2`));
  all('.v-ask .bubble, .typebar b, .unlock').forEach(el => add(el, `wiggle .5s ease-in-out ${askAt + .3}s 3`));
  document.getAnimations().forEach(a => a.pause());
}"""

SELECTORS = {"zoom": ZOOM, "pan": PAN, "spot": SPOT}


def add_live_motion(page, start: float, end: float) -> None:
    """Add the whole-reel motion to a rendered poster page (after the intro animation was set up)."""
    page.add_style_tag(content=LIVE_CSS)
    page.evaluate(LIVE_JS, [start, end, SELECTORS])
