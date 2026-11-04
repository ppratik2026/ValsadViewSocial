"""Showcase reels without the AI keys, in two steps (GitHub Actions: "Showcase reels" workflow):

  collect  gather today's real local news (headline, source, link, article text) into showcase/news.json
  render   make a reel for every story in showcase/stories.json (card text written from those articles,
           one layout per story), with a free stock photo found on the runner; nothing is posted

stories.json: a list of objects with the NewsStory fields (headline, highlight, kicker, subheadline, summary,
points, facts, category, mood, comment, source_name, source_url, image_keywords) plus "template".
"""
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "showcase"


def collect(cfg: dict) -> None:
    from src.free_news import _article_text, gather_items
    items = gather_items(cfg, [], list(cfg["content"]["categories"]), limit=30)
    news = []
    for item in items:
        news.append({"title": item.title, "source": item.source, "link": item.link,
                     "published": item.published.isoformat(), "category": item.category,
                     "text": _article_text(item)})
    OUT.mkdir(exist_ok=True)
    (OUT / "news.json").write_text(json.dumps(news, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(news)} stories saved to showcase/news.json")


def render(cfg: dict, stories_file: Path) -> None:
    from src.backgrounds import fetch_openverse_photo, fetch_stock_background, generate_free_ai_image
    from src.card import render_card
    from src.designs import mood_of
    from src.music import pick_track
    from src.news import NewsStory
    from src.scenes import BY_CATEGORY, draw_scene
    from src.video_builder import build_video, reel_seconds
    from src.viral import stock_keywords

    stories = json.loads(stories_file.read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    fields = set(NewsStory.__dataclass_fields__)
    for n, data in enumerate(stories, 1):
        template = data.pop("template")
        base = {"title_en": data.get("headline", ""), "note": "", "layout": "", "rows": [], "cta": "", "caption": "",
                "hashtags": [], "image_prompt": "", "image_keywords": [], "facts": [], "points": [], "subheadline": "",
                "kicker": "", "source_name": "", "source_url": ""}
        story = NewsStory(**{**base, **{k: v for k, v in data.items() if k in fields}})
        work = OUT / f"{n:02d}-{template}"
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        print(f"\n=== {n}. {template}: {story.headline}")
        if os.environ.get("SHOWCASE_GEMINI") and os.environ.get("GEMINI_API_KEY"):
            # first choice: the whole poster from Gemini (like the reference posters), as an animated reel
            from src.poster import make_poster
            from src.poster_reel import render as poster_reel
            story.cta = story.cta or "તમારો અભિપ્રાય કોમેન્ટમાં જણાવો 👇"
            poster = make_poster(story, cfg, work / "card.png")
            if poster:
                mood = mood_of(story)
                poster_reel(poster, work / "reel.mp4", "auto", pick_track(mood), 12, True, cfg["card"]["handle"])
                print(f"   Gemini poster reel saved {work.relative_to(ROOT)}/reel.mp4")
                continue
            print("   No Gemini poster (see the errors above); making the story-pattern poster instead")
        keywords = stock_keywords(story)
        background = None
        if os.environ.get("SHOWCASE_PICTURE") == "ai" and data.get("image_prompt"):
            if n > 1:   # the keyless free AI allows one picture every ~45 seconds
                import time
                time.sleep(46)
            # a rich AI picture of the story (free Pollinations), like the reference posters' pictures, no text
            background = generate_free_ai_image(
                data["image_prompt"] + ", dramatic cinematic 3D news poster illustration, hyper detailed, vivid colours, "
                "volumetric light", work / "ai.jpg", "photo")
        try:
            if background:
                raise StopIteration
            background = fetch_stock_background(keywords, work / "photo.jpg")
        except StopIteration:
            pass
        except Exception as e:
            print(f"   Pexels failed: {e}")
        if not background and os.environ.get("SHOWCASE_PICTURE") != "ai":
            found = fetch_openverse_photo(keywords, work / "openverse.jpg")
            if found:
                background, story.photo_credit = found
        if not background and data.get("image_prompt"):
            background = generate_free_ai_image(data["image_prompt"], work / "ai.jpg", "photo")
        if not background:
            background = draw_scene(BY_CATEGORY.get(story.category, "city"), [], work / "scene.png")
        os.environ["VIRAL_TEMPLATE"] = template
        card = render_card(story, cfg, work / "card.png", background, work / "intro", "viral")
        mood = mood_of(story)
        build_video(card, cfg["video"], work / "reel.mp4", pick_track(mood), work / "intro",
                    reel_seconds(mood, len(story.points)))
        shutil.rmtree(work / "intro", ignore_errors=True)
        print(f"   saved {work.relative_to(ROOT)}/reel.mp4")


if __name__ == "__main__":
    config = load_config()
    if sys.argv[1] == "collect":
        collect(config)
    else:
        render(config, Path(sys.argv[2]))
