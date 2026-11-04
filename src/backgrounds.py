"""Image for the news card: a free Wikimedia Commons photo, a Pexels or Openverse photo, a free AI illustration
(Pollinations) or Gemini, else none."""
import os
import random
import re
import time
import urllib.parse
from pathlib import Path

import requests
from google import genai
from google.genai import types

PEXELS_PHOTOS = "https://api.pexels.com/v1/search"


def generate_ai_background(prompt: str, model: str, out_path: Path) -> Path | None:
    """Create a 9:16 illustration with a Gemini image model. Returns None if nothing was generated."""
    try:
        response = genai.Client(http_options={"timeout": 150_000}).models.generate_content(
            model=model,
            contents=(
                f"{prompt}\n\nVertical 9:16 background for a Gujarati news reel. Bold colours, cinematic lighting, "
                "keep the top quarter and bottom third simpler so text can sit on top. "
                "Absolutely no text, letters, numbers, watermarks or logos."
            ),
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="9:16"),
            ),
        )
    except Exception as e:  # image generation is a nice-to-have, never fail the run for it
        print(f"AI background failed: {e}")
        return None

    for candidate in response.candidates or []:
        for part in (candidate.content.parts if candidate.content else None) or []:
            if part.inline_data and part.inline_data.data:
                out_path.write_bytes(part.inline_data.data)
                print("Background: AI illustration (Gemini)")
                return out_path
    print("AI background: no image returned.")
    return None


def fetch_stock_background(keywords: list[str], out_path: Path) -> Path | None:
    """Download a portrait stock photo from Pexels. None if no API key or no result."""
    api_key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not api_key:
        return None

    for keyword in keywords:
        resp = requests.get(
            PEXELS_PHOTOS,
            headers={"Authorization": api_key},
            params={"query": keyword, "orientation": "portrait", "per_page": 15},
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"Pexels search failed for {keyword!r}: {resp.status_code}")
            continue
        photos = resp.json().get("photos", [])
        if not photos:
            continue
        photo = random.choice(photos[:8])
        with requests.get(photo["src"]["portrait"], timeout=60) as dl:
            dl.raise_for_status()
            out_path.write_bytes(dl.content)
        print(f"Background: Pexels photo for {keyword!r} by {photo.get('photographer')}")
        return out_path
    return None


OPENVERSE = "https://api.openverse.org/v1/images/"


def fetch_openverse_photo(keywords: list[str], out_path: Path) -> tuple[Path, str] | None:
    """A free, openly licensed photo (Wikimedia, Flickr ...) from Openverse, no key needed. Returns the path and
    the credit line the licence asks for ("ફોટો: name / CC BY 2.0"), or None."""
    for keyword in keywords:
        try:
            resp = requests.get(OPENVERSE, headers={"User-Agent": "ValsadViewReels/1.0"}, timeout=30, params={
                "q": keyword, "license_type": "commercial", "mature": "false", "size": "large", "page_size": 20,
                "category": "photograph", "license": "cc0,by,by-sa"})
            if resp.status_code != 200:
                print(f"Openverse search failed for {keyword!r}: {resp.status_code}")
                continue
            # modern colour photos only: no museum/library archives (old black-and-white scans)
            results = [r for r in resp.json().get("results", [])
                       if (r.get("width") or 0) >= 900 and (r.get("height") or 0) >= 600
                       and not any(k in f"{r.get('source', '')} {r.get('provider', '')} {r.get('creator', '')}".lower()
                                   for k in ("library", "museum", "archive", "getty", "smithsonian", "nasa", "union mission"))]
        except requests.Timeout:
            print("Openverse is not answering, skipping it this time.")
            return None
        except (requests.RequestException, ValueError) as e:
            print(f"Openverse search failed: {e}")
            continue
        # the biggest, sharpest photos first (they look best full screen), a little shuffled
        results.sort(key=lambda r: -(r.get("width") or 0) * (r.get("height") or 0))
        top = results[:6]
        random.shuffle(top)
        for r in top[:4]:
            try:
                with requests.get(r["url"], headers={"User-Agent": "ValsadViewReels/1.0"}, timeout=60) as dl:
                    if dl.status_code != 200 or not dl.headers.get("content-type", "").startswith("image/"):
                        continue
                    out_path.write_bytes(dl.content)
            except requests.RequestException:
                continue
            lic = f"CC {str(r.get('license', '')).upper()} {r.get('license_version') or ''}".strip()
            if str(r.get("license", "")).lower() in ("cc0", "pdm"):
                lic = "Public domain"
            creator = (r.get("creator") or "").strip()[:40]
            print(f"Background: Openverse photo for {keyword!r} ({creator or 'unknown'}, {lic})")
            return out_path, f"ફોટો: {creator} / {lic}" if creator else f"ફોટો: {lic}"
    return None


COMMONS_API = "https://commons.wikimedia.org/w/api.php"
COMMONS_UA = {"User-Agent": "ValsadViewReels/1.0 (https://github.com/ppratik2026/ValsadViewSocial)"}
# free licences only (anyone may reuse, also commercially); CC BY / BY-SA need the author's name, which goes on the poster
FREE_LICENCE = re.compile(r"^(cc0|public domain|pd|cc[- ]by(-sa)?( \d(\.\d)?)?)", re.I)


def _plain(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def fetch_wikimedia_photo(keywords: list[str], out_path: Path) -> tuple[Path, str] | None:
    """A free photo from Wikimedia Commons (the pictures used on Wikipedia), no key needed: only public domain, CC0,
    CC BY and CC BY-SA files; recent colour photos first. Returns the path and the credit line ("ફોટો: name / CC BY-SA
    4.0, Wikimedia Commons"), or None."""
    for keyword in keywords:
        try:
            resp = requests.get(COMMONS_API, headers=COMMONS_UA, timeout=30, params={
                "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": 25,
                "gsrsearch": f"{keyword} filetype:bitmap", "prop": "imageinfo",
                "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1600})
            pages = (resp.json().get("query") or {}).get("pages", {}).values() if resp.status_code == 200 else []
        except requests.Timeout:
            print("Wikimedia Commons is not answering, skipping it this time.")
            return None
        except (requests.RequestException, ValueError) as e:
            print(f"Wikimedia search failed: {e}")
            continue
        found = []
        for page in pages:
            info = (page.get("imageinfo") or [{}])[0]
            meta = info.get("extmetadata") or {}
            lic = _plain((meta.get("LicenseShortName") or {}).get("value", ""))
            if info.get("mime") not in ("image/jpeg", "image/png") or not FREE_LICENCE.match(lic):
                continue
            if (info.get("width") or 0) < 1000 or (info.get("height") or 0) < 650:
                continue
            text = (page.get("title", "") + " " + _plain((meta.get("Categories") or {}).get("value", ""))).lower()
            if re.search(r"black and white|black-and-white|monochrome|sepia|historical|19\d\d|18\d\d|map|logo|diagram|drawing|coat of arms|bird|heron|egret|insect|butterfly|animal|flower|museum", text):
                continue
            # never a real person: no portraits, politicians, leaders, celebrities, rallies or speeches
            if re.search(r"portrait|people of|politician|minister|president|leader|\bmodi\b|gandhi|\bshah\b|\bpatel\b|bjp|"
                         r"congress|\baap\b|\bmla\b|\bmp\b|actor|actress|cricketer|celebrit|selfie|rally|speech|campaign|"
                         r"election|politic|\bsmt\b|\bshri\b|addressing|meeting with|interview", text):
                continue
            year = re.search(r"(20\d\d)", (meta.get("DateTimeOriginal") or {}).get("value", "") or "")
            score = (int(year.group(1)) if year else 2005) * 10 + min(info["width"] // 1000, 6)
            found.append((score, info, lic, _plain((meta.get("Artist") or {}).get("value", ""))[:40]))
        found.sort(key=lambda x: -x[0])
        for _, info, lic, artist in found[:4]:
            try:
                with requests.get(info.get("thumburl") or info["url"], headers=COMMONS_UA, timeout=60) as dl:
                    if dl.status_code != 200 or not dl.headers.get("content-type", "").startswith("image/"):
                        continue
                    out_path.write_bytes(dl.content)
            except requests.RequestException:
                continue
            if re.match(r"(?i)pd|public domain|cc0", lic):
                lic = "Public domain"
            print(f"Background: Wikimedia Commons photo for {keyword!r} ({artist or 'unknown'}, {lic})")
            credit = f"ફોટો: {artist} / {lic}" if artist else f"ફોટો: {lic}"
            return out_path, credit + ", Wikimedia Commons"
    return None


POLLINATIONS_IMAGE = "https://image.pollinations.ai/prompt/"


def _keyed_image(prompt: str, out_path: Path, size: str) -> Path | None:
    """One picture from Pollinations' images API with the free account key (POLLINATIONS_API_KEY), or None."""
    key = os.environ.get("POLLINATIONS_API_KEY", "").strip()
    if not key:
        return None
    model = os.environ.get("POLLINATIONS_IMAGE_MODEL", "gptimage")
    try:
        resp = requests.post(POLLINATIONS_IMAGES_API, headers={"Authorization": f"Bearer {key}"},
                             json={"model": model, "prompt": prompt, "size": size, "n": 1}, timeout=300)
        if resp.status_code != 200:
            print(f"AI image ({model}) failed: HTTP {resp.status_code} {resp.text[:150]!r}")
            return None
        item = resp.json()["data"][0]
        if item.get("b64_json"):
            import base64
            out_path.write_bytes(base64.b64decode(item["b64_json"]))
        else:
            with requests.get(item["url"], timeout=120) as dl:
                dl.raise_for_status()
                out_path.write_bytes(dl.content)
        return out_path
    except (requests.RequestException, ValueError, KeyError, IndexError) as e:
        print(f"AI image ({model}) failed: {e}")
        return None


NO_TEXT = ("IMPORTANT: absolutely no text anywhere in the image - no letters, numbers, words, signs, sign boards, "
           "banners, posters, labels, logos, stamps, price tags or watermarks; any board or screen must be blank")
CARTOON_STYLE = ("flat 2D cartoon illustration, clean vector art with bold outlines, bright cheerful colours, simple "
                 "shapes, Indian setting, generic cartoon characters that do not resemble any real person, "
                 "editorial news illustration style")


def generate_gemini_cartoon(prompt: str, models: list[str], out_path: Path) -> Path | None:
    """A landscape flat 2D cartoon scene from a Gemini image model (needs billing on the key: the free tier has
    no image quota). None if no model gives one."""
    if not os.environ.get("GEMINI_API_KEY") or not prompt:
        return None
    full = f"{prompt}. {CARTOON_STYLE}. {NO_TEXT}"
    client = genai.Client(http_options={"timeout": 150_000})
    for model in models:
        try:
            response = client.models.generate_content(
                model=model, contents=full,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                                   image_config=types.ImageConfig(aspect_ratio="16:9")),
            )
        except Exception as e:   # quota (free tier), busy or unknown model: try the next one
            print(f"   Gemini cartoon with {model} failed: {str(e)[:140]}")
            continue
        for candidate in response.candidates or []:
            for part in (candidate.content.parts if candidate.content else None) or []:
                if part.inline_data and part.inline_data.data:
                    out_path.write_bytes(part.inline_data.data)
                    print(f"Background: Gemini cartoon ({model})")
                    return out_path
    return None


def generate_free_ai_image(prompt: str, out_path: Path, style: str = "3d", keyless: bool = True) -> Path | None:
    """Free AI illustration from Pollinations. style "cartoon": a landscape flat 2D cartoon scene (for the
    brand template); "3d": a tall 3D scene. None if it fails; never stops the run."""
    if style == "cartoon":
        full = f"{prompt}. {CARTOON_STYLE}. {NO_TEXT}"
        size, params = "1536x1024", {"width": 1536, "height": 1100}
    elif style == "photo":
        # realistic news-photo look (the viral design); people only from behind or far away, never a real person
        full = (f"{prompt}, photorealistic news photograph, cinematic dramatic lighting, rich saturated colours, "
                f"Indian setting, sharp focus, people only seen from behind or far away with no recognisable faces, "
                f"no real person. {NO_TEXT}")
        size, params = "1024x1536", {"width": 1080, "height": 2040}
    else:
        # stylised 3D characters keep it clearly illustrative: never a real, recognisable person
        full = (f"{prompt}, Pixar style 3D render, cinematic news thumbnail, vivid colours, dramatic rim lighting, "
                f"shallow depth of field, anonymous characters, no real person. {NO_TEXT}")
        # a bit taller than 9:16: the cards show the top of the image, so the watermark strip at the bottom is cut off
        size, params = "1024x1536", {"width": 1080, "height": 2040}
    if _keyed_image(full, out_path, size):   # with the free account key: a better model than keyless
        print(f"Background: AI {style} illustration (Pollinations key)")
        return out_path
    if not keyless:   # the keyless model's pictures are too weak for this use
        return None
    url = POLLINATIONS_IMAGE + urllib.parse.quote(full)
    params |= {"nologo": "true", "seed": random.randint(1, 10**6)}
    for attempt in range(4):
        try:
            resp = requests.get(url, params=params, timeout=120)
        except requests.RequestException as e:
            print(f"Free AI image failed: {e}")
            return None
        if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("image/"):
            out_path.write_bytes(resp.content)
            print("Background: free AI illustration (Pollinations)")
            return out_path
        print(f"Free AI image failed: HTTP {resp.status_code} {resp.text[:150]!r}")
        if resp.status_code not in (402, 429, 500, 502, 503, 504) or attempt == 3:
            return None
        # busy or rate limited (anonymous use is limited per IP): wait as asked, then retry
        match = re.search(r"[Rr]etry after (\d+)", resp.text)
        time.sleep(min(int(match.group(1)) + 5 if match else 20, 60))
    return None


POLLINATIONS_IMAGES_API = "https://gen.pollinations.ai/v1/images/generations"


def fit_to_reel(path: Path) -> Path:
    """Make a poster exactly 1080x1920 (9:16), filling the frame (an image of another shape is cropped)."""
    from PIL import Image, ImageOps

    img = Image.open(path).convert("RGB")
    if img.size != (1080, 1920):
        ImageOps.fit(img, (1080, 1920), Image.LANCZOS).save(path)
    return path


def generate_free_poster(prompt: str, models: list[str], out_path: Path) -> Path | None:
    """The whole poster (picture + Gujarati text) from the same prompt a person would paste into Gemini.
    Needs a free Pollinations account key (POLLINATIONS_API_KEY): the keyless API only has a model that
    cannot write text. Returns None if there is no key or no model gives an image."""
    key = os.environ.get("POLLINATIONS_API_KEY", "").strip()
    if not key:
        print("   AI poster skipped: no POLLINATIONS_API_KEY (free key from enter.pollinations.ai).")
        return None
    for model in models:
        for attempt in range(2):
            try:
                resp = requests.post(POLLINATIONS_IMAGES_API, headers={"Authorization": f"Bearer {key}"},
                                     json={"model": model, "prompt": prompt, "size": "1024x1536", "n": 1},
                                     timeout=300)
            except requests.RequestException as e:
                print(f"   AI poster ({model}) failed: {e}")
                break
            if resp.status_code == 200:
                try:
                    item = resp.json()["data"][0]
                    if item.get("b64_json"):
                        import base64
                        out_path.write_bytes(base64.b64decode(item["b64_json"]))
                    else:
                        with requests.get(item["url"], timeout=120) as dl:
                            dl.raise_for_status()
                            out_path.write_bytes(dl.content)
                except (ValueError, KeyError, IndexError, requests.RequestException) as e:
                    print(f"   AI poster ({model}) gave no image: {e}")
                    break
                print(f"   AI poster made with model '{model}'")
                return fit_to_reel(out_path)
            print(f"   AI poster ({model}) failed: HTTP {resp.status_code} {resp.text[:200]!r}")
            if resp.status_code not in (429, 500, 502, 503, 504):
                break   # e.g. out of free credits or model unavailable: try the next model
            time.sleep(20)
    return None


def remove_white_background(path: Path, out_path: Path) -> Path | None:
    """Make the plain light background of an object picture transparent (flood fill from the edges, so white
    parts inside the object stay). Returns None if the picture has no plain background to remove."""
    from PIL import Image, ImageChops, ImageDraw, ImageFilter

    img = Image.open(path).convert("RGB")
    img.thumbnail((1200, 1200))
    key = (255, 0, 255)
    filled = img.copy()
    w, h = filled.size
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if sum(filled.getpixel(xy)) > 600:          # only light corners/edges are background
            ImageDraw.floodfill(filled, xy, key, thresh=38)
    diff = ImageChops.difference(filled, Image.new("RGB", filled.size, key)).convert("L")
    mask = diff.point(lambda v: 255 if v > 8 else 0).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    box = mask.getbbox()
    if not box:
        return None
    kept = sum(1 for v in mask.getdata() if v > 128) / (w * h)
    if not 0.05 < kept < 0.92:                      # nothing removed, or the object was eaten: not usable
        print(f"   Cut-out not usable ({kept:.0%} of the picture kept)")
        return None
    out = img.convert("RGBA")
    out.putalpha(mask)
    out.crop(box).save(out_path)
    return out_path


def generate_cutout(object_prompt: str, out_path: Path) -> Path | None:
    """The story's main objects as a transparent 3D sticker (needs POLLINATIONS_API_KEY for a good model)."""
    if not object_prompt or not os.environ.get("POLLINATIONS_API_KEY", "").strip():
        return None
    prompt = (f"{object_prompt}. Glossy 3D render like a premium news infographic sticker, vivid colours, soft studio "
              "lighting, the objects grouped together in the centre, filling most of the frame, isolated on a plain "
              "pure white background, no floor, no shadow on the background, nothing else in the picture. "
              "IMPORTANT: absolutely no text, letters, numbers, labels, logos or currency symbols anywhere, and no people: "
              "no person, face, hand or human figure - objects only.")
    raw = out_path.with_name("cutout_raw.png")
    if not _keyed_image(prompt, raw, "1024x1024"):
        return None
    path = remove_white_background(raw, out_path)
    if path:
        print("Cut-out: 3D object sticker made")
    return path


def get_background(story, cfg: dict, work_dir: Path) -> Path | None:
    if cfg.get("provider") != "gemini" and cfg["free"].get("ai_images", True) and story.image_prompt:
        path = generate_free_ai_image(story.image_prompt, work_dir / "illustration.jpg")
        if path:
            return path
    if cfg.get("provider") == "gemini" and cfg["gemini"].get("ai_background", True):
        path = generate_ai_background(story.image_prompt, cfg["gemini"]["image_model"], work_dir / "background.png")
        if path:
            return path
    try:
        path = fetch_stock_background(story.image_keywords, work_dir / "background.jpg")
    except requests.RequestException as e:  # Pexels is optional, never fail the run for it
        print(f"Pexels failed: {e}")
        path = None
    if not path:
        print("Background: theme colours only.")
    return path
