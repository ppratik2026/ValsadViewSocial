"""Motion graphics laid over a poster reel (src/poster_reel.py), frame by frame:

- a light sweep (diagonal shine) that crosses the frame whenever the camera reaches a new part of the poster;
- twinkling sparkles;
- a short RGB glitch on every cut;
- a glowing border that pulses;
- a red progress bar along the bottom;
- a blinking "● LIVE" badge at the start;
- at the end, a "Follow @handle" pill and a "કોમેન્ટ કરો 👇" bubble pop in with a bounce.

The stickers are drawn once with the browser (real Gujarati text in a real font) as transparent PNGs.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

W, H = 1080, 1920


def _sticker_png(html_body: str, size: tuple[int, int], out: Path) -> Image.Image:
    """Render a small HTML snippet to a transparent PNG (the browser has the Gujarati fonts)."""
    from playwright.sync_api import sync_playwright
    page_html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Baloo+Bhai+2:wght@800&display=block" rel="stylesheet">
<style>html,body{{margin:0;background:transparent;}} body{{font-family:'Baloo Bhai 2','Noto Sans Gujarati',sans-serif;
display:flex;align-items:center;justify-content:center;width:{size[0]}px;height:{size[1]}px;}}</style></head>
<body>{html_body}</body></html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": size[0], "height": size[1]})
        page.set_content(page_html, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(out), omit_background=True)
        browser.close()
    return Image.open(out).convert("RGBA")


class PosterFX:
    def __init__(self, seconds: float, cuts: list[float], handle: str, work: Path, seed: str = ""):
        self.seconds, self.cuts = seconds, sorted(cuts)
        rnd = random.Random(seed or "fx")
        self.sparkles = [(rnd.randint(30, W - 30), rnd.randint(60, H - 120), rnd.uniform(0, 6.28), rnd.uniform(.6, 1.6))
                         for _ in range(26)]
        self.spark = self._spark_sprite()
        self.sweep = self._sweep_sprite()
        self.border = self._border_sprite()
        work.mkdir(parents=True, exist_ok=True)
        self.follow = _sticker_png(
            f'<div style="background:linear-gradient(90deg,#ff0050,#ff7a00);color:#fff;font-size:46px;font-weight:800;'
            f'padding:14px 38px 20px;border-radius:60px;border:5px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.45)">'
            f'➕ Follow {handle}</div>', (760, 160), work / "follow.png")
        self.comment = _sticker_png(
            '<div style="background:#ffe14d;color:#111;font-size:50px;font-weight:800;padding:16px 34px 22px;border-radius:40px;'
            'border:5px solid #111;box-shadow:8px 8px 0 #111">💬 કોમેન્ટ કરો 👇</div>', (620, 170), work / "comment.png")
        self.live = _sticker_png(
            '<div style="background:#e10600;color:#fff;font:900 40px Arial;padding:10px 22px;border-radius:12px;'
            'border:4px solid #fff">● LIVE</div>', (240, 100), work / "live.png")

    @staticmethod
    def _spark_sprite() -> Image.Image:
        s = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
        d = ImageDraw.Draw(s)
        d.ellipse((24, 24, 36, 36), fill=(255, 255, 255, 255))
        d.line((30, 2, 30, 58), fill=(255, 245, 200, 200), width=3)
        d.line((2, 30, 58, 30), fill=(255, 245, 200, 200), width=3)
        return s.filter(ImageFilter.GaussianBlur(1.2))

    @staticmethod
    def _sweep_sprite() -> Image.Image:
        """A soft diagonal white band, 700px wide, as tall as the frame."""
        band = Image.new("L", (700, H * 2), 0)
        d = ImageDraw.Draw(band)
        for x in range(700):
            a = int(140 * math.exp(-((x - 350) / 120) ** 2))
            d.line((x, 0, x, H * 2), fill=a)
        band = band.rotate(-20, expand=True, resample=Image.BILINEAR)
        img = Image.new("RGBA", band.size, (255, 255, 255, 0))
        img.putalpha(band)
        return img

    @staticmethod
    def _border_sprite() -> Image.Image:
        b = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(b)
        for i, a in enumerate((220, 150, 90, 40)):
            d.rounded_rectangle((10 + i * 6, 10 + i * 6, W - 11 - i * 6, H - 11 - i * 6), radius=40, outline=(255, 214, 10, a), width=6)
        return b

    def _since_cut(self, t: float) -> float:
        past = [c for c in self.cuts if c <= t]
        return t - past[-1] if past else 99

    @staticmethod
    def _pop(t: float, start: float) -> float:
        """Scale of a pop-in with a bounce, 0 before start."""
        x = t - start
        if x <= 0:
            return 0
        if x > .5:
            return 1
        return 1 + 0.25 * math.sin(x / .5 * math.pi) if x > .25 else x / .25

    def apply(self, frame: Image.Image, t: float) -> Image.Image:
        f = frame.convert("RGBA")
        dt = self._since_cut(t)
        # RGB glitch for 3 frames after a cut
        if dt < 0.1:
            r, g, b, a = f.split()
            f = Image.merge("RGBA", (ImageChops.offset(r, 14, 0), g, ImageChops.offset(b, -14, 0), a))
        # light sweep crossing the frame after a cut
        if dt < 0.7:
            x = int(-900 + dt / 0.7 * (W + 1400))
            f.alpha_composite(self.sweep, (x, -H // 2))
        # sparkles
        for (x, y, ph, sp) in self.sparkles:
            a = (math.sin(t * 3 * sp + ph) + 1) / 2
            if a > .55:
                s = self.spark.copy()
                s.putalpha(s.getchannel("A").point(lambda v: int(v * (a - .55) / .45)))
                f.alpha_composite(s, (x - 30, y - 30))
        # pulsing border
        glow = self.border.copy()
        k = .45 + .55 * (math.sin(t * 4) + 1) / 2
        glow.putalpha(glow.getchannel("A").point(lambda v: int(v * k)))
        f.alpha_composite(glow)
        # LIVE badge blinking during the first 3 s
        if t < 3 and int(t * 2) % 2 == 0:
            f.alpha_composite(self.live, (30, 40))
        # stickers at the end
        for img, start, pos in ((self.follow, self.seconds - 2.6, (W // 2, 170)), (self.comment, self.seconds - 2.2, (W // 2, H - 260))):
            sc = self._pop(t, start)
            if sc > 0:
                w, h = int(img.width * sc), int(img.height * sc)
                if w > 4 and h > 4:
                    s = img.resize((w, h), Image.BILINEAR)
                    f.alpha_composite(s, (pos[0] - w // 2, pos[1] - h // 2))
        # progress bar
        d = ImageDraw.Draw(f)
        d.rectangle((0, H - 14, W, H), fill=(0, 0, 0, 160))
        d.rectangle((0, H - 14, int(W * min(t / self.seconds, 1)), H), fill=(255, 0, 80, 255))
        return f.convert("RGB")
