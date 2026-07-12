#!/usr/bin/env python3
"""Generuje web/src/data/data.json na podstawie plan/.

Jedno zrodlo prawdy to pliki markdown w plan/ - ten skrypt je parsuje
i sklada w jeden JSON konsumowany przez frontend (web/).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_DIR = ROOT / "plan"
OUTPUT_JSON = ROOT / "web" / "src" / "data" / "data.json"

PLANY = [
    {"id": "wieden", "file": "wieden.md", "label": "Wiedeń"},
]

DAY_ROW_RE = re.compile(
    r"^\|\s*(?P<dzien>\d+)\s*\|\s*(?P<data>[^|]+)\|\s*(?P<miejsce>[^|]+)\|\s*(?P<plan>[^|]+)\|\s*$",
    re.MULTILINE,
)
TABLE_ROW_RE = re.compile(r"^\|(?P<cells>.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_intro(text: str) -> str:
    lines = text.splitlines()
    intro: list[str] = []
    started = False
    for line in lines:
        if line.startswith("# "):
            started = True
            continue
        if not started:
            continue
        if line.startswith("|") or line.startswith("## "):
            break
        intro.append(line)
    return "\n".join(intro).strip()


def extract_days(text: str) -> list[dict]:
    days = []
    for match in DAY_ROW_RE.finditer(text):
        if match.group("dzien") == "" or not match.group("dzien").isdigit():
            continue
        days.append(
            {
                "dzien": int(match.group("dzien")),
                "data": match.group("data").strip(),
                "miejsce": match.group("miejsce").strip(),
                "plan": match.group("plan").strip(),
            }
        )
    return days


def _row_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_koszty(uwagi_text: str) -> dict:
    lines = uwagi_text.splitlines()
    rows: list[list[str]] = []
    header: list[str] = []
    in_table = False
    for line in lines:
        if TABLE_SEP_RE.match(line):
            in_table = True
            continue
        if TABLE_ROW_RE.match(line):
            cells = _row_cells(line)
            if not in_table and not header:
                header = cells
                continue
            if in_table:
                rows.append(cells)
        elif in_table:
            break
    if not rows:
        return {}
    return {"header": header, "rows": rows}


def extract_section(text: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}[^\n]*\n(?P<body>.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group("body").strip() if match else ""


def parse_places(section_text: str) -> list[dict]:
    lines = section_text.splitlines()
    header: list[str] = []
    rows: list[list[str]] = []
    in_table = False
    for line in lines:
        if TABLE_SEP_RE.match(line):
            in_table = True
            continue
        if TABLE_ROW_RE.match(line):
            cells = _row_cells(line)
            if not in_table and not header:
                header = cells
                continue
            if in_table:
                rows.append(cells)
        elif in_table:
            break

    keys = [h.strip().lower() for h in header]
    places: list[dict] = []
    for row in rows:
        record = dict(zip(keys, row, strict=False))
        try:
            lat = float(record.get("lat", ""))
            lng = float(record.get("lng", ""))
        except ValueError:
            continue
        places.append(
            {
                "nazwa": record.get("nazwa", "").strip(),
                "kategoria": (
                    record.get("kategoria") or record.get("typ") or ""
                ).strip(),
                "lat": lat,
                "lng": lng,
                "opis": record.get("opis", "").strip(),
                "link": record.get("link", "").strip(),
            }
        )
    return places


def clean_uwagi(uwagi_text: str) -> list[str]:
    out: list[str] = []
    for raw in uwagi_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if TABLE_ROW_RE.match(line) or TABLE_SEP_RE.match(line):
            continue
        if line.startswith("**Szacunkowy koszt"):
            continue
        out.append(line)
    return out


def build_plan(md_path: Path, plan_id: str, label: str) -> dict:
    text = md_path.read_text(encoding="utf-8")

    days = extract_days(text)
    for day in days:
        day["image"] = f"images/{plan_id}-{day['dzien']:02d}.jpg"

    uwagi_text = extract_section(text, "Uwagi")

    return {
        "id": plan_id,
        "label": label,
        "title": extract_title(text),
        "intro": extract_intro(text),
        "dni": days,
        "koszty": extract_koszty(uwagi_text),
        "uwagi": clean_uwagi(uwagi_text),
        "atrakcje": parse_places(extract_section(text, "Atrakcje")),
        "restauracje": parse_places(extract_section(text, "Restauracje")),
    }


def main() -> None:
    plany = [build_plan(PLAN_DIR / p["file"], p["id"], p["label"]) for p in PLANY]
    data = {"plany": plany}

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Zapisano {len(plany)} planow do {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
