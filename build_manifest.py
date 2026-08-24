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
    mc_dir = HERE / "model_comparison"
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
        entry = {
            "file": p.name,
            "classifier": m.group("classifier"),
            "date": d.strftime("%Y-%m-%d"),
            "date_label": f"{int(m.group('day'))} {mon} {m.group('year')}",
            "blind": blind,
        }
        # L2 layer: matching model comparison HTML, if any.
        # Convention: model_comparison/<Classifier>_<D><Mon><YYYY>[_Blind]_ModelComparison.html
        blind_tag = "_Blind" if blind else ""
        mc_name = f"{m.group('classifier')}_{int(m.group('day'))}{mon}{m.group('year')}{blind_tag}_ModelComparison.html"
        if (mc_dir / mc_name).exists():
            entry["model_comparison"] = f"model_comparison/{mc_name}"
        entries.append(entry)
    entries.sort(key=lambda e: (e["classifier"], e["date"]))
    out = HERE / "manifest.json"
    out.write_text(json.dumps({"reports": entries}, indent=2), encoding="utf-8")
    print(f"wrote {out} ({len(entries)} entries)")


if __name__ == "__main__":
    main()
