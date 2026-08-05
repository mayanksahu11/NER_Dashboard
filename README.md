# NER Report Dashboard

Interactive dashboard for the `*_Report.md` NER benchmark reports in this folder.

## Features
- **Classifier** dropdown (from filename prefix, e.g. `AllFullName`)
- **Date** dropdown, sorted latest-first; the latest report is selected by default
- Parses the markdown tables in the report and renders:
  - Overall metrics table + bar chart
  - Per-language F1 comparison chart
  - Per-language detail tables
- Best/worst values per column are highlighted

## Filename convention
```
<Classifier>_<D><Mon><YYYY>_Report.md
# e.g. AllFullName_4Aug2026_Report.md
```

## Usage
1. Start the server:
   ```
   python serve.py
   ```
2. Open http://localhost:8000/
3. Drop a new `*_Report.md` file into this folder and **refresh the browser** — it appears
   automatically. The manifest is rebuilt on every request; no server restart needed.

## Files
- `index.html` — the dashboard (vanilla JS + Chart.js via CDN)
- `serve.py` — tiny HTTP server that generates `manifest.json` dynamically on each request
- `build_manifest.py` — optional: writes a static `manifest.json` (only needed if you host
  the folder with a plain static server that can't run Python)
