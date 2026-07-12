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
    "atrakcja-wieden-01": "Stephansdom Vienna south tower full view",
    "atrakcja-wieden-02": "Hofburg Palace Vienna facade",
    "atrakcja-wieden-03": "Schonbrunn Palace Vienna facade",
    "atrakcja-wieden-04": "Naschmarkt Vienna market stalls",
    "atrakcja-wieden-05": "Vienna State Opera building",
    "atrakcja-wieden-06": "Wiener Riesenrad Prater Ferris wheel",
    "atrakcja-wieden-07": "Kunsthistorisches Museum Wien building Maria-Theresien-Platz",
    "atrakcja-wieden-08": "Belvedere Palace Vienna Upper garden",
    "restauracja-wieden-01": "Wiener Schnitzel plate",
    "restauracja-wieden-02": "Tafelspitz",
    "restauracja-wieden-03": "Zwiebelrostbraten",
    "restauracja-wieden-04": "Cafe Central Vienna interior",
    "restauracja-wieden-05": "Demel Vienna confectionery",
    "restauracja-wieden-06": "Sachertorte cake slice",
    "restauracja-wieden-07": "Wiener Melange coffee",
    "restauracja-wieden-08": "Griechenbeisl Vienna",
    "restauracja-wieden-09": "Zum Schwarzen Kameel Vienna",
    "restauracja-wieden-10": "Cafe Hawelka Vienna",
    "restauracja-wieden-11": "Cafe Landtmann Vienna",
    "restauracja-wieden-12": "Burgtheater Vienna interior",
    "restauracja-wieden-13": "Kurrentgasse Vienna street",
    "restauracja-wieden-14": "Bäckerstraße Wien",
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
