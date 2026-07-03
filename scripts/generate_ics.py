#!/usr/bin/env python3
"""Generate one all-day iCalendar file per confirmed dated conference."""

from __future__ import annotations

import datetime as dt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFERENCE_FILE = ROOT / "_data" / "conferences.yml"
CALENDAR_DIR = ROOT / "calendar"


def parse_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def load_conferences() -> list[dict[str, str]]:
    conferences: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in CONFERENCE_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            if current:
                conferences.append(current)
            current = {}
            stripped = stripped[2:]
        if ":" in stripped and current is not None:
            key, value = stripped.split(":", 1)
            current[key.strip()] = parse_scalar(value)

    if current:
        conferences.append(current)
    return conferences


def escape_ics(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\r", "")
        .replace("\n", r"\n")
    )


def fold_line(line: str) -> str:
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line

    chunks: list[str] = []
    current = ""
    for char in line:
        candidate = current + char
        if len(candidate.encode("utf-8")) > 75:
            chunks.append(current)
            current = " " + char
        else:
            current = candidate
    chunks.append(current)
    return "\r\n".join(chunks)


def date_value(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def calendar_text(event: dict[str, str]) -> str:
    start = date_value(event["start_date"])
    end = date_value(event.get("end_date") or event["start_date"]) + dt.timedelta(days=1)
    location = ", ".join(part for part in (event.get("city", ""), event.get("country", "")) if part)
    description_parts = [
        event.get("summary", ""),
        f"Organizer: {event.get('organizer', '')}",
        f"Source: {event.get('source', '')}",
    ]
    if event.get("website"):
        description_parts.append(f"Website: {event['website']}")
    description = "\n\n".join(part for part in description_parts if part)
    dtstamp = "20260703T000000Z"

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//DH Conference Radar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{escape_ics(event['id'])}@dh-conference-radar",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;VALUE=DATE:{start:%Y%m%d}",
        f"DTEND;VALUE=DATE:{end:%Y%m%d}",
        f"SUMMARY:{escape_ics(event['name'])}",
        f"LOCATION:{escape_ics(location)}",
        f"DESCRIPTION:{escape_ics(description)}",
    ]
    if event.get("website"):
        lines.append(f"URL:{escape_ics(event['website'])}")
    lines.extend(["END:VEVENT", "END:VCALENDAR"])
    return "\r\n".join(fold_line(line) for line in lines) + "\r\n"


def main() -> int:
    CALENDAR_DIR.mkdir(exist_ok=True)
    generated = 0

    for old_file in CALENDAR_DIR.glob("*.ics"):
        old_file.unlink()

    for event in load_conferences():
        if event.get("status") != "confirmed" or not event.get("start_date"):
            continue
        output = CALENDAR_DIR / f"{event['id']}.ics"
        output.write_text(calendar_text(event), encoding="utf-8", newline="")
        generated += 1

    print(f"Generated {generated} calendar file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
