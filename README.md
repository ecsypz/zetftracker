# Zcash ETF Flow

Self-updating dashboard for daily net flows into ZCSH (Grayscale Zcash ETF).
Data comes straight from Grayscale's official daily product-performance file;
flows are derived as (change in shares outstanding) x (NAV per share).

## One-time setup (~5 minutes)

1. Create a **public** GitHub repository (e.g. `zec-etf-flow`) and upload
   everything in this folder, keeping the structure:
   - `index.html`
   - `data/zcsh.json`
   - `scripts/update.py`
   - `.github/workflows/update.yml`
2. **Settings → Actions → General → Workflow permissions** → select
   **Read and write permissions** → Save. (Lets the bot commit fresh data.)
3. **Settings → Pages** → Source: *Deploy from a branch* → Branch: `main`,
   folder `/ (root)` → Save.
4. Done. The dashboard is live at `https://<your-username>.github.io/zec-etf-flow/`.

## How it stays current

- A GitHub Action runs every weekday evening (two attempts, ~7:45pm and
  ~11:45pm ET) after Grayscale posts the daily NAV. It fetches the file,
  recomputes the whole series from 2021, and commits `data/zcsh.json`
  only when something changed.
- **Manual update any time:** repo → *Actions* tab → *Update ZCSH data* →
  *Run workflow*. That's the one-click.
- The page's *Refresh* button re-reads the latest committed data.

## Notes

- GitHub's cron can drift by up to ~30 minutes under load; fine for daily data.
- If the S3 filename ever changes (Grayscale reworking their pipeline), the
  Action will fail visibly in the Actions tab. Grab the new link from the
  download icon on thezcashetf.com and update `URL` in `scripts/update.py`.
- When Bitwise's Zcash ETF lists, add a second fetch in `scripts/update.py`
  and a second column in `index.html` — the layout already totals across funds.
