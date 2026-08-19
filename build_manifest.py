"""Scans the current directory for *_Report.md files and writes manifest.json.

Filename convention: <Classifier>_<D><Mon><YYYY>_Report.md
Example: AllFullName_4Aug2026_Report.md
"""
import json
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
PATTERN = re.compile(
    r"^(?P<classifier>.+?)_(?P<day>\d{1,2})(?P<mon>[A-Za-z]{3})(?P<year>\d{4})_(?:(?P<blind>Blind)_)?Report\.md$"
)
MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def main() -> None:
    entries = []
    for p in sorted(HERE.glob("*_Report.md")):
        m = PATTERN.match(p.name)
        if not m:
            print(f"skip (bad name): {p.name}")
            continue
        mon = m.group("mon").capitalize()
        if mon not in MONTHS:
            print(f"skip (bad month): {p.name}")
            continue
        d = datetime(int(m.group("year")), MONTHS[mon], int(m.group("day")))
        blind = m.group("blind") is not None
        entries.append({
            "file": p.name,
            "classifier": m.group("classifier"),
            "date": d.strftime("%Y-%m-%d"),
            "date_label": f"{int(m.group('day'))} {mon} {m.group('year')}",
            "blind": blind,
        })
    entries.sort(key=lambda e: (e["classifier"], e["date"]))
    out = HERE / "manifest.json"
    out.write_text(json.dumps({"reports": entries}, indent=2), encoding="utf-8")
    print(f"wrote {out} ({len(entries)} entries)")


if __name__ == "__main__":
    main()
