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

### Local (auto-refresh on new files)
1. Start the server:
   ```
   python serve.py
   ```
2. Open http://localhost:8000/
3. Drop a new `*_Report.md` file into this folder and **refresh the browser** — it appears
   automatically. The manifest is rebuilt on every request; no server restart needed.

### Hosted on GitHub Pages
A workflow at `.github/workflows/pages.yml` regenerates `manifest.json` and deploys the
folder to GitHub Pages on every push to `main`. One-time setup:

1. Push the repo to GitHub.
2. In the repo → **Settings → Pages**, set **Source** to **GitHub Actions**.
3. Any subsequent `git push` (including new reports) auto-deploys.
   Live URL will be shown in the workflow run, typically:
   `https://<user>.github.io/<repo>/`

## Files
- `index.html` — the dashboard (vanilla JS + Chart.js via CDN)
- `serve.py` — tiny HTTP server that generates `manifest.json` dynamically on each request (local dev)
- `build_manifest.py` — writes a static `manifest.json`; used by the Pages workflow and as a fallback for any plain static host
- `.github/workflows/pages.yml` — GitHub Pages deployment
