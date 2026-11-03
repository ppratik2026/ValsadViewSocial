"""Command line wrapper: python tools/poster_to_reel.py poster.jpg reel.mp4 [--style ...] [--music ...]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.poster_reel import main  # noqa: E402

main()
