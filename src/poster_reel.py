"""Turn a finished poster image (PNG/JPG, e.g. one made in the Gemini app) into an animated 9:16 news reel.

    python tools/poster_to_reel.py poster.jpg out.mp4 [--style auto|scan|punch|zigzag|focus] [--music file.mp3]

The poster is split into its bands (headline, picture, points, bottom strip) by looking at where the picture
changes most from row to row, and a "camera" moves over it like a news editor reading it out:

  scan    starts close on the headline with a punch-in, glides down band by band, then pulls back to the whole poster
  punch   whole poster first, then quick punch-ins on every band with a flash, back out at the end
  zigzag  diagonal moves left-right while going down, with a slight tilt
  focus   whole poster, then each band is lit up in turn while the rest is dimmed (no zoom)

Every reel opens with a short flash and ends on the full poster (the last seconds are what people re-read).
"""
import argparse
import math
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

W, H, FPS = 1080, 1920, 30


def _ease(t: float) -> float:
    return t * t * (3 - 2 * t)


def bands(img: Image.Image, n_max: int = 6) -> list[tuple[int, int]]:
    """(top, bottom) of the poster's main bands: cut where neighbouring rows differ the least."""
    small = img.convert("L").resize((90, 160))
    px = small.load()
    rows = [[px[x, y] for x in range(90)] for y in range(160)]
    change = [sum(abs(a - b) for a, b in zip(rows[y], rows[y - 1])) for y in range(1, 160)]
    # quiet rows are band edges; pick well-spaced ones
    order = sorted(range(10, 150), key=lambda y: change[y - 1])
    cuts = []
    for y in order:
        if all(abs(y - c) >= 22 for c in cuts):
            cuts.append(y)
        if len(cuts) >= n_max - 1:
            break
    edges = [0] + sorted(cuts) + [160]
    scale = img.height / 160
    return [(int(a * scale), int(b * scale)) for a, b in zip(edges, edges[1:]) if b - a >= 14]


def _fit(img: Image.Image) -> Image.Image:
    """The poster at 1080 wide, padded or cropped to 9:16 (blurred fill behind a shorter poster)."""
    img = img.convert("RGB")
    img = img.resize((W, round(img.height * W / img.width)))
    if img.height >= H:
        top = (img.height - H) // 2
        return img.crop((0, top, W, top + H))
    bg = img.resize((W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(.5)
    bg.paste(img, (0, (H - img.height) // 2))
    return bg


def _view(img: Image.Image, cx: float, cy: float, zoom: float, tilt: float = 0) -> Image.Image:
    """The frame seen by the camera at (cx, cy) with this zoom (1 = whole poster)."""
    w, h = W / zoom, H / zoom
    x0 = min(max(cx - w / 2, 0), W - w)
    y0 = min(max(cy - h / 2, 0), H - h)
    frame = img.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize((W, H), Image.BILINEAR)
    if tilt:
        frame = frame.rotate(tilt, resample=Image.BILINEAR, expand=False, fillcolor=(0, 0, 0)).resize((W, H))
        frame = frame.crop((30, 54, W - 30, H - 54)).resize((W, H))
    return frame


def keyframes(style: str, bnds: list[tuple[int, int]], seconds: float) -> list[tuple[float, float, float, float, float]]:
    """(time, cx, cy, zoom, tilt) points the camera passes through."""
    whole = (W / 2, H / 2, 1.0, 0.0)
    centres = [(W / 2, (a + b) / 2, max(1.12, min(1.32, H / max(b - a, 1) * .45))) for a, b in bnds]
    end_hold = 2.6
    t_move = seconds - end_hold - 0.6
    keys = []
    if style == "scan":
        first = centres[0]
        keys.append((0.0, first[0], first[1], first[2] * 1.15, 0))
        step = t_move / max(len(centres), 1)
        for i, (cx, cy, z) in enumerate(centres):
            keys.append((0.4 + i * step, cx, cy, z, 0))
        keys.append((seconds - end_hold, *whole))
    elif style == "punch":
        keys.append((0.0, *whole))
        step = t_move / max(len(centres), 1)
        for i, (cx, cy, z) in enumerate(centres):
            t = 0.8 + i * step
            keys += [(t, cx, cy, z * 1.1, 0), (t + step * .8, cx, cy, z, 0)]
        keys.append((seconds - end_hold, *whole))
    elif style == "zigzag":
        step = t_move / max(len(centres), 1)
        keys.append((0.0, W * .42, centres[0][1], 1.3, -2))
        for i, (cx, cy, z) in enumerate(centres):
            keys.append((0.4 + i * step, W * (.44 if i % 2 else .56), cy, max(z, 1.25), 2 if i % 2 else -2))
        keys.append((seconds - end_hold, *whole))
    else:   # focus: no camera move
        keys = [(0.0, *whole), (seconds, *whole)]
    keys.append((seconds, *whole))
    return keys


def _at(keys, t):
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            k = _ease((t - t0) / (t1 - t0)) if t1 > t0 else 1
            return [x + (y - x) * k for x, y in zip(a, b)]
    return keys[-1][1:]


def render(poster: Path, out: Path, style: str = "auto", music: Path | None = None, seconds: float = 12.0) -> Path:
    img = _fit(Image.open(poster))
    bnds = bands(img)
    if style == "auto":
        style = random.choice(["scan", "punch", "zigzag", "focus"])
    print(f"   {poster.name}: style {style}, {len(bnds)} bands")
    keys = keyframes(style, bnds, seconds)
    tmp = Path(tempfile.mkdtemp())
    dim = ImageEnhance.Brightness(img).enhance(.35)
    n = int(seconds * FPS)
    focus_step = (seconds - 3.4) / max(len(bnds), 1)
    for i in range(n):
        t = i / FPS
        cx, cy, zoom, tilt = _at(keys, t)
        if style == "focus" and 0.8 <= t < seconds - 2.6:
            k = min(int((t - 0.8) / focus_step), len(bnds) - 1)
            a, b = bnds[k]
            frame = dim.copy()
            frame.paste(img.crop((0, a, W, b)), (0, a))
            base = frame
        else:
            base = img
        frame = _view(base, cx, cy, zoom, tilt)
        if t < 0.25:   # opening flash
            frame = Image.blend(frame, Image.new("RGB", (W, H), "white"), 1 - t / 0.25)
        if style == "punch":   # small flash on every punch-in
            phase = ((t - 0.8) / ((seconds - 3.4) / max(len(bnds), 1))) % 1 if t > 0.8 else 1
            if phase < 0.06:
                frame = ImageEnhance.Brightness(frame).enhance(1.6 - phase * 10)
        if t > seconds - 2.6:   # gentle "breathing" on the full poster at the end
            s = 1 + 0.015 * math.sin((t - seconds + 2.6) * 5)
            frame = _view(frame, W / 2, H / 2, s)
        frame.save(tmp / f"f{i:04d}.jpg", quality=90)
    args = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%04d.jpg")]
    if music:
        args += ["-ss", "20", "-i", str(music), "-filter_complex",
                 f"[1:a]afade=t=in:d=0.5,afade=t=out:st={seconds - 1.5}:d=1.5[a]", "-map", "0:v", "-map", "[a]"]
    args += ["-t", str(seconds), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
             "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)]
    result = subprocess.run(args, capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("poster", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--style", default="auto", choices=["auto", "scan", "punch", "zigzag", "focus"])
    ap.add_argument("--music", type=Path)
    ap.add_argument("--seconds", type=float, default=12)
    a = ap.parse_args()
    sys.exit(0 if render(a.poster, a.out, a.style, a.music, a.seconds) else 1)


if __name__ == "__main__":
    main()
