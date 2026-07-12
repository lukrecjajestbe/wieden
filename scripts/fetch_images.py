#!/usr/bin/env python3
"""Pobiera reprezentatywne zdjecie dla kazdego dnia planu z Wikimedia Commons.

Zapisuje do web/public/images/<plan_id>-<NN>.jpg. Pomija pobieranie jesli
plik juz istnieje - usun go recznie zeby wymusic ponowne pobranie.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import httpx
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "web" / "public" / "images"

HEADERS = {"User-Agent": "WiedenTripPlanner/1.0 (jakub@lite.tech)"}
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
MAX_WIDTH = 1600
JPEG_QUALITY = 78

SEARCH_QUERIES: dict[str, str] = {
    "wieden-01": "Schonbrunn Palace Vienna garden",
    "wieden-02": "Vienna State Opera building",
    "wieden-03": "Kunsthistorisches Museum Vienna exterior",
}


def find_image_url(query: str) -> str | None:
    response = httpx.get(
        COMMONS_API,
        params={
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "piprop": "original",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 8,
        },
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
    ordered = sorted(pages.values(), key=lambda p: p.get("index", 999))
    for page in ordered:
        original = page.get("original")
        if original and re.search(
            r"\.(jpe?g|png)$", original["source"], re.IGNORECASE
        ):
            return original["source"]
    return None


def download_and_resize(url: str, dest: Path) -> None:
    with httpx.stream(
        "GET", url, headers=HEADERS, timeout=30, follow_redirects=True
    ) as response:
        response.raise_for_status()
        raw = b"".join(response.iter_bytes())

    image = Image.open(io.BytesIO(raw)).convert("RGB")
    if image.width > MAX_WIDTH:
        new_height = round(image.height * MAX_WIDTH / image.width)
        image = image.resize((MAX_WIDTH, new_height), Image.LANCZOS)
    image.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for image_id, query in SEARCH_QUERIES.items():
        dest = IMAGES_DIR / f"{image_id}.jpg"
        if dest.exists():
            print(f"pomijam (juz istnieje): {image_id}")
            continue

        try:
            image_url = find_image_url(query)
            if not image_url:
                print(f"BRAK wyniku dla: {image_id} ({query})")
                continue
            download_and_resize(image_url, dest)
            print(f"OK {image_id} <- {image_url}")
        except httpx.HTTPError as exc:
            print(f"BLAD {image_id}: {exc}")


if __name__ == "__main__":
    main()
