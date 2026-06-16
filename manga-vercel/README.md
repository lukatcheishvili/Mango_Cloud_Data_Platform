# Manga Cloud Platform — Vercel build

Static, zero-build port of the Streamlit RFP response. Same content, same dark Framer
design system, same interactive hover-hotspot architecture diagrams and Plotly charts.
The original Streamlit app (`mango_cloud_platform.py`) is left **unchanged** as a backup.

## What's here

```
manga-vercel/
├── index.html        # entire app (HTML + CSS + JS, single file)
├── vercel.json       # static hosting config + caching
├── assets/           # high-level + low-level architecture diagrams (JPG)
└── data/             # 6 sample CSVs (loaded client-side for the Data Sources page)
```

No build step, no framework, no dependencies. Plotly and fonts load from CDN.

## Deploy to Vercel

**Option A — Git (recommended)**
1. Commit this `manga-vercel/` folder to your GitHub repo.
2. On [vercel.com](https://vercel.com) → **Add New → Project** → import the repo.
3. Set **Root Directory** to `manga-vercel`. Framework preset: **Other**. Build command: *(leave empty)*. Output dir: *(leave empty)*.
4. **Deploy** — live in ~1 minute.

**Option B — Vercel CLI**
```bash
npm i -g vercel
cd manga-vercel
vercel        # preview
vercel --prod # production
```

**Option C — drag & drop**
Zip the contents of `manga-vercel/` and drop it on [vercel.com/new](https://vercel.com/new).

## Run locally
Because the Data Sources page fetches the CSVs, open it through a tiny server (not file://):
```bash
cd manga-vercel
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Notes
- Live at https://mangacloud-khaki.vercel.app/ (auto-deploys on every push to `main`; root directory `manga-vercel`).
- The Streamlit version remains the fallback; both render identical content.
