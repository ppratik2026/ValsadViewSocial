"""Publish the same reel on the Facebook Page (Facebook Reels API), next to Instagram.

Needs FB_PAGE_ID and a token that may post on the Page: FB_PAGE_TOKEN, or else the Facebook system-user token in
IG_ACCESS_TOKEN ("EAA...", with the Page assigned to the system user and pages_manage_posts granted), from which
the Page's own token is fetched. Without FB_PAGE_ID nothing is done; a failure never stops the Instagram post.
"""
import os
import time
from pathlib import Path

import requests

GRAPH = "https://graph.facebook.com"
RUPLOAD = "https://rupload.facebook.com/video-upload"


class FacebookError(RuntimeError):
    pass


def _check(resp: requests.Response) -> dict:
    try:
        data = resp.json()
    except ValueError:
        raise FacebookError(f"HTTP {resp.status_code}: {resp.text[:300]}")
    if resp.status_code >= 400 or "error" in data:
        err = data.get("error", data)
        raise FacebookError(f"HTTP {resp.status_code}: {err.get('message', err)}")
    return data


def page_token(page_id: str, token: str, version: str) -> str:
    """The Page's own access token (a system-user or user token can ask for it); else the token itself."""
    try:
        data = _check(requests.get(f"{GRAPH}/{version}/{page_id}", params={"fields": "access_token",
                                                                            "access_token": token}, timeout=30))
        return data.get("access_token") or token
    except (FacebookError, requests.RequestException):
        return token


def configured() -> bool:
    return bool(os.environ.get("FB_PAGE_ID", "").strip()) and bool(
        os.environ.get("FB_PAGE_TOKEN", "").strip() or os.environ.get("IG_ACCESS_TOKEN", "").strip().startswith("EAA"))


def publish_reel(video: Path, caption: str, version: str = "v21.0", timeout_s: int = 600) -> dict:
    """Upload the reel to the Page and publish it. Returns {"video_id", "permalink"}."""
    page_id = os.environ["FB_PAGE_ID"].strip()
    token = page_token(page_id, os.environ.get("FB_PAGE_TOKEN", "").strip() or os.environ["IG_ACCESS_TOKEN"].strip(),
                       version)
    base = f"{GRAPH}/{version}/{page_id}/video_reels"
    start = _check(requests.post(base, data={"upload_phase": "start", "access_token": token}, timeout=60))
    video_id = start["video_id"]
    size = video.stat().st_size
    with open(video, "rb") as f:
        _check(requests.post(f"{RUPLOAD}/{version}/{video_id}", data=f, timeout=600,
                             headers={"Authorization": f"OAuth {token}", "offset": "0", "file_size": str(size)}))
    _check(requests.post(base, timeout=60, data={"upload_phase": "finish", "video_id": video_id,
                                                 "video_state": "PUBLISHED", "description": caption,
                                                 "access_token": token}))
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        status = _check(requests.get(f"{GRAPH}/{version}/{video_id}", timeout=30,
                                     params={"fields": "status,permalink_url", "access_token": token}))
        state = (status.get("status") or {}).get("video_status", "")
        if state in ("ready", "published") or (status.get("status") or {}).get("publishing_phase", {}).get("status") == "complete":
            link = status.get("permalink_url", "")
            return {"video_id": video_id, "permalink": f"https://www.facebook.com{link}" if link.startswith("/") else link}
        if state == "error":
            raise FacebookError(f"Facebook could not process the reel: {status.get('status')}")
        time.sleep(10)
    return {"video_id": video_id, "permalink": ""}   # still processing: Facebook publishes it when done
