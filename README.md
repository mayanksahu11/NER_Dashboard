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
Reports must be named:
```
<Classifier>_<D><Mon><YYYY>_Report.md          ← Open (non-blind) eval
<Classifier>_<D><Mon><YYYY>_Blind_Report.md    ← Blind eval
```
- **`<Classifier>`** — no spaces, e.g. `AllFullName`, `FirstName`, `LastName`. Becomes an entry in the Classifier dropdown.
- **`<D>`** — day of month, 1 or 2 digits (`4`, `15`).
- **`<Mon>`** — 3-letter English month, first letter uppercase: `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec`.
- **`<YYYY>`** — 4-digit year.
- **`_Blind_`** — optional marker before `Report.md`. If present, the report is tagged as a blind evaluation (test data not visible to devs). Otherwise it's treated as open (non-blind).
- Suffix must be `_Report.md`.

Examples:
```
AllFullName_4Aug2026_Report.md            ← open eval
AllFullName_19Aug2026_Blind_Report.md     ← blind eval
FirstName_15Sep2026_Report.md             ← open eval
```
Files that don't match are silently skipped by `build_manifest.py` and won't appear in the dashboard.

### Report body format
Each report is a markdown file whose body the dashboard parses. Structure:
````markdown
# NER - <title>
## Date - DD/MM/YYYY

Settings: <free-form settings line>

## Overall

| Model | COR | PAR | SPU | MIS | S-P | S-R | S-F1 | P-P | P-R | P-F1 | T-P | T-R | T-F1 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| opentext | ... |
| nerkit   | ... |

## Per language

### <langcode> (gold=<N>)

| Model | COR | PAR | SPU | MIS | S-P | S-R | S-F1 | P-P | P-R | P-F1 | T-P | T-R | T-F1 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| opentext | ... |
| nerkit   | ... |
````
Notes:
- The first data row (e.g. `opentext`) is treated as the **baseline** for coloring; subsequent rows (`nerkit`) show green when better, red when worse.
- Only the strict metrics (`COR`, `PAR`, `SPU`, `MIS`, `S-P`, `S-R`, `S-F1`) are rendered; `P-*` and `T-*` columns are dropped from the view.
- Language codes (`en`, `ja`, `zh`, …) are auto-mapped to full names in the UI.

## Usage

### Local (auto-refresh on new files)
1. Start the server:
   ```
   python serve.py
   ```
2. Open http://localhost:8000/
3. Drop a new `*_Report.md` file into this folder and **refresh the browser** — it appears
   automatically. The manifest is rebuilt on every request; no server restart needed.

### Hosted on Azure Static Web Apps (Microsoft-internal only)
The recommended host. Restricts access to the Microsoft Entra tenant.

1. Create a **Static Web App** in Azure Portal, connected to this GitHub repo (`main` branch), app location `/`, no build.
2. Register an Entra app (single-tenant, Microsoft only) and set redirect URI to `https://<swa-host>/.auth/login/aad/callback`.
3. In the SWA → **Configuration**, add app settings `AAD_CLIENT_ID` and `AAD_CLIENT_SECRET`.
4. Push a change — `.github/workflows/azure-swa.yml` (or the SWA-generated workflow) regenerates `manifest.json` and deploys.

### Hosted on GitHub Pages (public)
A workflow at `.github/workflows/pages.yml` regenerates `manifest.json` and deploys the
folder to GitHub Pages on every push to `main`. Only usable if the repo is public.

### Uploading new reports
Once hosted, adding a new report is just a git push:
```powershell
Copy-Item C:\path\to\NewClassifier_15Aug2026_Report.md .
git add .
git commit -m "Add report"
git push
```
The workflow rebuilds `manifest.json` and redeploys automatically (~1 minute). You can also drag-drop the file via the GitHub web UI (**Add file → Upload files**).

## Files
- `index.html` — the dashboard (vanilla JS + Chart.js via CDN)
- `serve.py` — tiny HTTP server that generates `manifest.json` dynamically on each request (local dev)
- `build_manifest.py` — writes a static `manifest.json`; used by the Pages workflow and as a fallback for any plain static host
- `.github/workflows/pages.yml` — GitHub Pages deployment
