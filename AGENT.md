# AGENT.md — Project Context & State

> **KEEP THIS FILE UPDATED.**
> Every time you push changes to this repo, update the relevant sections below.
> This file is read automatically by AI assistants (Claude, Cowork) at the start of every session,
> so all team members get full project context regardless of which device they are working from.

---

## Project Identity

| Field | Value |
|---|---|
| **Project name** | Manga Cloud Platform — RFP Response |
| **Course** | Data Analytics in the Cloud — MBD-EN2025 |
| **Institution** | IE University |
| **Deliverable** | RFP response document + interactive web app (Vercel) + video walkthrough |
| **Deadline** | June 19, 2026 |
| **GitHub repo** | https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform |
| **Live website (Vercel)** | https://mangacloud-khaki.vercel.app/ |
| **Figma HLA diagram** | https://www.figma.com/board/UtHLPjygSysLe43cpzNCAp |
| **Figma LLA diagram** | https://www.figma.com/board/mvaVaoJErDBqNXt114FPqU |

---

## Project Summary (for AI context)

This is a **group university project** for IE University's Cloud Analytics course. We are responding to a fictional RFP from **Manga** (a fictional Spanish fashion retailer modelled on Mango) that wants to modernise its legacy on-premises data infrastructure into a cloud-native AWS data platform.

**The scenario:** Manga has 100+ physical stores, €280M annual revenue, and a broken data stack — daily cron-job ETL scripts, siloed pipelines, Excel-based BI, no real-time capability, 2× infrastructure cost vs competitors, and unclear GDPR compliance.

**Our deliverable:** A complete RFP response proposing an AWS-based cloud data lakehouse, presented as an interactive Streamlit app with clickable architecture diagrams, dataset previews, requirements coverage analysis, and ML use case demonstrations.

The project is **not about building the actual cloud infrastructure** — it is about designing and presenting the architecture proposal in a compelling, technically accurate way that satisfies all 8 RFP requirements (R1–R8).

---

## Key Stakeholders (Manga side — from RFP)

| Person | Role | Stance | Key Concern |
|---|---|---|---|
| Marta Ríos | COO | Champion | End-to-end solution with clear business case |
| Javier Medina | CTO | Skeptic | Vendor lock-in; open-source preference |
| Manuel Ortega | CFO | Cost-focused | 2× infra cost vs competitors; needs clear ROI |
| Laura Smith | InfoSec Manager | Security-first | GDPR; prior security incident; non-negotiable |
| Alex Lee | Head of Data & AI | Champion | Wants modern DataOps; knows current arch is broken |

---

## RFP Requirements Status

| ID | Requirement | Status | Key AWS Services |
|---|---|---|---|
| R1 | Unified multi-modal data platform | Covered | Kinesis, Glue, S3, Redshift, Athena |
| R2 | Multi-environment (Dev/Pre-Prod/Prod) | Covered | AWS Organizations, Terraform, Lake Formation |
| R3 | Automation & IaC | Covered | MWAA (Airflow), Terraform/CDK, Glue, EventBridge |
| R4 | Security & high availability | Covered | IAM, KMS, TLS, Lake Formation, Macie, CloudTrail, VPC |
| R5 | Data quality monitoring | Covered | Glue Data Quality, CloudWatch, SNS |
| R6 | Cost optimisation | Covered | S3 Intelligent-Tiering, Spot Instances, QuickSight pay-per-session |
| R7 | Extensibility & interoperability | Covered | API Gateway, Lambda, Data Exchange, Transfer Family |
| R8 | Sustainability & carbon metrics | Covered | AWS Carbon Footprint Tool, EU green regions |

---

## Architecture Overview

### High-Level Architecture (technology-agnostic)

```
DATA SOURCES          CATALOGING & SEARCH (bidirectional ↔ Processing)
(Streaming / Batch /  ─────────────────────────────────────────────────
 Structured /
 Unstructured)
      │
      ▼
 INGESTION
      │
      ▼
 PROCESSING
  ┌─────────────────────┐   ┌─────────────────┐
  │ Validate/Clean/     │──▶│ Transform &     │
  │ Standardize/Norm    │   │ Enrich          │
  └─────────────────────┘   └─────────────────┘
      │
      ▼
 STORAGE
  Raw Zone ──▶ Cleaned Zone ──▶ Curated/Consumption Zone
      │
      ▼
 CONSUMPTION (BI / ML / Partner APIs / AI Agents)
      │
 ─────────────────────────────────────────────────
 SECURITY & GOVERNANCE (spans all layers)
```

### Low-Level Architecture (AWS-specific)

**Ingestion:** Kinesis Data Streams → Kinesis Firehose | AWS Glue ETL | AWS Lambda + EventBridge | AWS DMS | AWS Data Exchange | AWS Transfer Family

**Storage:** S3 Raw Zone (Bronze) → S3 Curated Zone (Silver) → Amazon Redshift (Gold) + Amazon DynamoDB

**Processing & Governance:** Glue Data Catalog | Amazon MWAA (Airflow) | Glue Data Quality | AWS Lake Formation | Amazon Macie

**Consumption:** Amazon Athena | Amazon QuickSight | Amazon SageMaker | Amazon Comprehend | API Gateway

**Security:** Amazon VPC | IAM + KMS | TLS 1.3 in-transit | AWS CloudTrail | Amazon CloudWatch | AWS Organizations | Terraform/CDK | AWS Carbon Footprint Tool

**Encryption note:** We use TLS termination at service boundaries (not E2EE) — this allows the platform to process and analyse data while keeping every service hop encrypted.

---

## Design System

All visual work (Streamlit app, Figma diagrams) must follow **`DESIGN.md`** in the repo root.
It covers:
- Color tokens (canvas, surfaces, accent, semantic colors, gradient accents)
- Typography scale (sizes, weights, letter-spacing per role)
- Spacing system (5px base unit)
- Border radius scale
- Card, badge, navigation component patterns
- Plotly chart styling rules
- Architecture diagram node colors per layer
- HTML interactive diagram CSS
- Do's and Don'ts for consistency

**Never introduce a new color, font size, or spacing value that isn't in `DESIGN.md`.**

**Active tokens (as implemented):**
- Display font: `Mona Sans` → fallback `Inter` — page titles, metric values, spotlight text
- Body font: `Inter` with feature settings `cv01 cv05 cv09 cv11 ss03`
- Gradient spotlight hues: `G_VIOLET=#6a4cf5`, `G_MAGENTA=#d44df0`, `G_ORANGE=#ff7a3d`
- Content max-width: `1240px`, padding: `72px 48px 96px`
- Card border-radius: `15px` (was 10px)
- New component: `.spotlight` — gradient hero card used on Overview page

---

## AI Collaboration Rules

If an AI assistant has any question or uncertainty about how to implement a task, what design direction to use, what visual style to follow, which colors, shapes, fonts, spacing, layout, interaction pattern, or any other project decision to choose, it must ask Luka before implementing.

Do not make unclear design or implementation decisions silently. When in doubt, ask first and wait for the answer.

After every 5 user prompts in an active project session, update this `AGENT.md` file with the latest project information, including completed changes, new decisions, remaining tasks, known issues, and any important implementation notes.

For engineering work, especially data architecture, implementation quality, deployment decisions, testing strategy, review practices, and project delivery workflows, AI assistants should reference the external skills repository when relevant:

- https://github.com/mattpocock/skills

Use this repository as an additional engineering skills source, while keeping this project's `AGENT.md`, `DESIGN.md`, RFP constraints, and Luka's direct instructions as the highest-priority guidance.

---

## Git & Contribution Rules

> **These rules are mandatory for every commit and pull request in this repository.**

1. **All commits and PRs must be authored under the human contributor's name** (the team member doing the work — e.g. `Luka Tcheishvili <cheishvililuka.lc@gmail.com>`). Configure git locally before committing:
   ```bash
   git config user.name  "Your Name"
   git config user.email "your-email@example.com"
   ```
2. **Never add Claude, Cowork, Codex, or any AI tool as a contributor, author, or co-author.**
   - Do **not** add `Co-Authored-By: Claude ...` (or any AI) trailers to commit messages.
   - Do **not** add "Generated with / Co-authored by AI" footers.
   - The git history must show only human team members.
3. AI assistants may *prepare* changes, but the commit/PR is always made **in the name of the user**.
4. Keep commit messages short and descriptive of the change (e.g. `Move sample CSVs into Data/`, `Rename CLAUDE.md to AGENT.md`).
5. **Update the Log every 5 prompts.** After every 5 prompts in an agent/LLM session, append a dated entry to the **Log** section at the bottom of this file summarising what was done, and keep the **What Has To Be Done** section current at the same time.
6. **Never commit secrets.** API keys and tokens go in a local `.env` (gitignored) — never in tracked files or commit history.

---

## Repository Structure

```
Mango_Cloud_Data_Platform/
├── mango_cloud_platform.py        # Main Streamlit app (all 6 pages)
├── requirements.txt               # Python dependencies (streamlit, pandas, plotly)
├── .gitignore                     # Ignores .env, __pycache__, local scratch images, etc.
├── .env.example                   # Template for local secrets (copy to .env — .env is gitignored)
├── README.md                      # Project overview and documentation
├── AGENT.md                      # ← THIS FILE — AI context and project state
├── DESIGN.md                      # Design system — colors, typography, spacing, components
├── Data/                          # All sample datasets live here
│   ├── sales_sample.csv               # POS / e-commerce transactions
│   ├── customers_sample.csv           # CRM / loyalty data (contains PII)
│   ├── inventory_sample.csv           # ERP / WMS stock levels
│   ├── customer_reviews_sample.csv    # Web/app reviews (text + images, contains PII)
│   ├── external_factors_sample.csv    # Weather, events, campaigns
│   └── shipping_sample.csv            # Logistics partner data (contains PII)
├── Group Work B - Retail.pdf      # Original RFP document from professor
├── Manga_DataHub_RFP_Response.pdf # Our written RFP response document
├── assets/                        # Exported architecture images (from Figma)
│   ├── manga-cloud-platform-high-level-architecture.jpg
│   └── manga-cloud-platform-low-level-aws-architecture.jpg
├── deliverables/                  # Final deliverables (deck, RFP doc, speaker script, cost figure)
│   ├── Manga_DataHub_RFP_Response.docx
│   ├── Manga_DataHub_Deck.pptx
│   ├── Speaker_Script.md
│   └── cost_comparison.png
└── manga-vercel/                  # Static (Vercel) build of the proposal — same content, no Streamlit
    ├── index.html                     # Single-file app (HTML + CSS + JS, Plotly via CDN)
    ├── vercel.json                    # Static hosting config
    ├── assets/                        # Architecture diagrams
    └── data/                          # CSV copies for the Data Sources page
```

---

## App Structure (mango_cloud_platform.py)

The app has **6 pages** navigated via sidebar buttons stored in `st.session_state.page`:

| Page key | Title | What it contains |
|---|---|---|
| `overview` | Overview | KPI metrics, executive summary, stakeholder cards, value drivers |
| `hla` | High-Level Architecture | Tech-agnostic clickable HTML diagram + Plotly interactive chart with hover |
| `lla` | Low-Level Architecture | AWS service map HTML diagram + Plotly interactive chart with hover |
| `data` | Data Sources | Expandable panels for each of the 6 CSVs with schema and ingestion info |
| `reqs` | Requirements Coverage | R1–R8 cards with AWS services + coverage bar chart |
| `usecases` | Use Cases | 5 ML use case expanders + dataset usage heatmap |

**Architecture image rendering:**
- `render_figma_architecture()` — loads exported JPG from `assets/` folder and renders it in HLA/LLA pages
- Falls back to Plotly diagram if image file not found
- Images: `assets/manga-cloud-platform-high-level-architecture.jpg` and `assets/manga-cloud-platform-low-level-aws-architecture.jpg`

**Key implementation notes:**
- A one-time branded `show_manga_loader()` / `hide_manga_loader()` overlay appears before the app opens in each Streamlit session, using parent-page component injection, a MANGA wordmark, capsule progress bar, fade-out animation, and fail-safe removal so the loader cannot remain frozen over the app.
- Both HLA and LLA pages use `st.tabs()` with two tabs: Interactive HTML diagram + Plotly chart
- Plotly charts use `go.Scatter` with square markers and rich `hovertext` per node
- HTML diagrams use `st.components.v1.html()` with embedded JS for click interactions
- CSVs loaded with `@st.cache_data` + `try/except` — app works even if CSVs are missing
- All styling done via a single CSS block injected with `st.markdown(unsafe_allow_html=True)`
- Dark theme throughout: background `#0a0e1a`, cards `#111827`, accent `#4a9af0`

---

## Dataset Details

| File | Rows (approx) | Key columns | PII | Ingestion pattern |
|---|---|---|---|---|
| `sales_sample.csv` | ~1000 | datetime, customer_id, product_id, store_id, price, discount, payment_method | No | Kinesis streaming |
| `customers_sample.csv` | ~500 | customer_id, name, age, gender, address, zip, loyalty_status | **Yes** | AWS DMS batch |
| `inventory_sample.csv` | ~300 | product_id, store_id, stock_level, price, description | No | Glue batch hourly |
| `customer_reviews_sample.csv` | ~400 | review_id, customer_id, product_id, rating, review_text, image_url | **Yes** | Kinesis + Comprehend |
| `external_factors_sample.csv` | ~365 | date, weather, fuel_price, bank_holiday, local_event, campaign_id | No | Lambda daily pull |
| `shipping_sample.csv` | ~600 | order_id, delivery_address, estimated_delivery, actual_delivery, delivery_price, actual_cost, return_status | **Yes** | Lambda + Glue batch |

---

## What Has Been Completed

- [x] Initial Streamlit app built with 6 pages and full dark theme
- [x] Overview page: KPI metrics, executive summary, stakeholder cards, value drivers
- [x] HLA page: Restructured to match professor's tech-agnostic reference (Streaming/Batch/Structured/Unstructured sources, Validate/Clean/Norm → Transform/Enrich, Raw→Cleaned→Curated, Cataloging & Search bidirectional, Security spanning bottom)
- [x] LLA page: Updated with all services from professor's reference (added AWS Data Exchange, Transfer Family, Athena, CloudTrail)
- [x] Interactive Plotly charts on both HLA and LLA — hover any node for what it does, why we chose it, cost model, RFP coverage
- [x] Data Sources page: expandable panels for all 6 CSVs
- [x] Requirements Coverage page: R1–R8 cards + bar chart
- [x] Use Cases page: 5 ML use cases + dataset heatmap
- [x] TLS vs E2EE security context added (based on professor's course announcement)
- [x] App portability fixed: try/except on CSV loading, works for all team members
- [x] Figma HLA diagram created: https://www.figma.com/board/UtHLPjygSysLe43cpzNCAp
- [x] Figma LLA diagram created: https://www.figma.com/board/mvaVaoJErDBqNXt114FPqU
- [x] README fully rewritten: executive summary, requirements table, what we did, tech stack, use cases
- [x] AGENT.md created (this file)
- [x] GitHub Actions workflow for AGENT.md update reminders
- [x] Figma architecture images exported and added to assets/ folder
- [x] render_figma_architecture() added to app — displays Figma JPG exports in HLA/LLA pages
- [x] Sidebar rail toggle improved — localStorage persistence, manga-rail-toggle/manga-fs-toggle IDs
- [x] Data Insights page added — 10 charts across all 6 datasets
- [x] Top navigation bar replaced with proper sidebar + fixed rail/fullscreen buttons
- [x] Framer design system fully applied (Inter font, pure black canvas, #0099ff accent)
- [x] Mona Sans added as display font (fallback Inter) with Framer font-feature-settings (cv01,cv05,cv09,cv11,ss03)
- [x] Gradient spotlight card added (.spotlight — violet→magenta→orange, used on Overview page hero)
- [x] Centered layout — max-width 1240px, padding 72px 48px 96px, auto margins
- [x] Typography refined — 46px/600 display titles, 36px metrics, tighter letter-spacing
- [x] Stakeholder tags redesigned as pill badges with colored dot indicators
- [x] Badges unified to monochrome SURF2 background (matches Framer do's/don'ts)
- [x] Sidebar toggle fixed — mn-rail/mn-fs buttons programmatically click Streamlit's native collapse button
- [x] Sidebar nav button CSS hardened — section-scoped selectors, gap:4px on stVerticalBlock, flex layout, works across Streamlit versions (kind=primary, baseButton-primary, stBaseButton-primary all covered)
- [x] Overview page now includes the full project team member list
- [x] README now includes the full project team member list
- [x] Page entrance animations now follow the Risk Fraud HTML deck pattern: scoped fade-up keyframes, deck-style block targeting, staggered delays, reduced-motion/print support, and MutationObserver replay on Streamlit page changes
- [x] One-time branded loading screen added before the app opens, based on the provided `mango_loader_streamlit.py` reference
- [x] Loading screen freeze fixed by moving overlay control to executable Streamlit component JS with stale-overlay cleanup and automatic fail-safe completion
- [x] Vercel static app restored the fixed view controls: sidebar drawer/toggle plus browser fullscreen button
- [x] Vercel view controls stacked vertically with fullscreen above the sidebar toggle
- [x] Removed empty duplicate `AGENTS.md` scaffold; `AGENT.md` is the single canonical agent context file

---

## Remaining Tasks

> Update this section as tasks are completed or new ones are identified.

### High Priority (needed for submission)

- [ ] **Record the video walkthrough** — walk through the live Streamlit app explaining each page; mention RFP requirements being addressed; show the Figma diagrams
- [ ] **Finalise the written RFP response PDF** (`Manga_DataHub_RFP_Response.pdf`) — ensure all 8 requirements are addressed in the written document with the same content as the app
- [ ] **Review and proofread the app** — check all text for typos, consistent terminology (Manga not Mango), correct RFP references

### Medium Priority (improvements)

- [ ] **Add a cost estimation section** — rough monthly AWS cost breakdown for the proposed architecture (could be a new app page or a section on the Requirements page)
- [ ] **Improve the Figma diagrams** — add colour coding, legends, and AWS service icons to both FigJam boards; make them presentation-ready
- [ ] **Add a migration timeline** — phase 1 (foundation), phase 2 (streaming), phase 3 (ML) roadmap; could be a Gantt chart in the app or Figma
- [ ] **Data quality examples** — add actual Glue Data Quality rule examples using the sample CSVs (null checks, range validation) as a concrete demo

### Nice to Have

- [ ] **Add sample SageMaker output** — mock recommendation or forecast output visualised in the app using the sample datasets
- [ ] **Dark/light theme toggle** — the app is currently dark-only; some professors may present on bright projectors
- [ ] **Export to PDF button** — allow downloading the proposal as a PDF directly from the app

---

## How to Run Locally

```bash
git clone https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform.git
cd Mango_Cloud_Data_Platform
pip install -r requirements.txt
streamlit run mango_cloud_platform.py
```

Requirements: `streamlit>=1.32.0`, `pandas>=2.0.0`, `plotly>=5.18.0`

---

## Important Decisions & Rationale

| Decision | Rationale |
|---|---|
| AWS over Azure/GCP | RFP example provided by professor used AWS; strongest retail analytics ecosystem |
| Open Parquet format | Addresses CTO Javier's vendor lock-in concern directly |
| MWAA (Managed Airflow) | Open-source Airflow core = no lock-in; replaces cron jobs with observable DAGs |
| TLS termination (not E2EE) | E2EE would prevent platform-side analytics; TLS between every service hop is sufficient |
| QuickSight pay-per-session | 60%+ cheaper vs traditional per-seat BI licensing at Manga's scale |
| Redshift + S3 (not Snowflake) | Stays within AWS ecosystem; Spectrum allows querying S3 without loading |
| Three-zone lakehouse (Raw/Curated/Gold) | Industry standard; Raw enables full reprocessing; PII masking at Curated boundary |
| CloudTrail for GDPR | Immutable audit logs required for Right of Access / Right to Erasure compliance |

---

## How to Update This File

When you push changes, update the relevant section(s):

- **Fixed a bug or improved a feature** → update "What Has Been Completed" and check off any tasks in "Remaining Tasks"
- **Added a new feature or page** → update "App Structure" and "What Has Been Completed"
- **Made an architectural decision** → add a row to "Important Decisions & Rationale"
- **Identified new work** → add to "Remaining Tasks" under the appropriate priority
- **Changed a file or added a new one** → update "Repository Structure"
- **Reached every 5 user prompts in an active project session** → update this file with the latest project state, decisions, completed work, open issues, and next tasks

A GitHub Action will warn you on every push if you forgot to update this file.

---

*Last updated: 2026-06-17 | Updated by: Luka Tcheishvili*

---

## What Has To Be Done

> Running list of open work. Keep this current — add items as they come up, remove them when done (and record them in the Log below).

- [ ] **Record the video** — the deck (`deliverables/Manga_DataHub_Deck.pptx`) and speaker script (`deliverables/Speaker_Script.md`) are ready; recording is on the team.
- [ ] **Finish the service logos** — add real images for **CloudWatch** (missing) and **Terraform** (came as HTML), and replace the **DynamoDB** source (has a baked-in checkerboard). The other 22 are wired in.
- [ ] **Revoke & rotate the GitHub token** that was shared in chat (do this on GitHub → Settings → Developer settings → Personal access tokens), then put the new token in the local gitignored `.env`.

---

## Log

> Newest entries first. Record what was actually done, by whom, and when.

### 2026-06-17 (deliverables) — Luka Tcheishvili
- Built the **presentation deck** (`deliverables/Manga_DataHub_Deck.pptx`) — 12 dark slides with per-slide speaker notes — and a timed **speaker script** (`deliverables/Speaker_Script.md`) for all 6 presenters.
- Rebuilt the **RFP response as an editable Word doc** (`deliverables/Manga_DataHub_RFP_Response.docx`) with a working clickable Table of Contents, 10 pages (≤15), and the cost figure embedded — fixing the empty-TOC issue.
- Added a **cost-comparison figure** (`deliverables/cost_comparison.png`): colocation vs AWS, ~57% reduction (€1.30M → €0.56M, ~€0.74M/yr saved); illustrative.
- Organized generated files into `deliverables/`; moved build/preview artifacts to a gitignored `_scratch/`.

### 2026-06-17 — Luka Tcheishvili
- Restored the fixed view controls in `manga-vercel/index.html`: a sidebar toggle that becomes a popover drawer on mobile, plus a browser fullscreen toggle with accessible labels and persistent desktop sidebar state.
- Stacked the Vercel view controls vertically and placed the fullscreen button above the sidebar toggle while preserving the sidebar-following position.
- Removed the empty duplicate `AGENTS.md` scaffold so the repository has one canonical agent context file: `AGENT.md`.
- Added **official AWS service logos** to the low-level architecture hover popups: 22 user-supplied logos normalized to uniform 256px white tiles in `manga-vercel/assets/logos/` and referenced locally (no CDN dependency). CloudWatch & Terraform still on fallback; DynamoDB source needs a clean replacement.
- Enlarged the logos to fill the popup tile (tighter whitespace trim, reduced padding).
- Fixed Vercel asset caching so updated images appear without a hard refresh (`must-revalidate`).
- Confirmed the site is live and auto-deploying from `main`: https://mangacloud-khaki.vercel.app/
- Removed the Streamlit live link from the README and AGENT.md — **Vercel is the single live URL** (Streamlit remains only as local source, not linked).

### 2026-06-16 (later) — Luka Tcheishvili
- Re-exported the low-level architecture diagram from Figma with vertically-centered labels; replaced the image (web-optimized) and fixed the "Bronze" label typo.
- Stood up **Vercel** hosting (project `manga_cloud`, root `manga-vercel/`, auto-deploy on push to `main`); live at https://mangacloud-khaki.vercel.app/.
- Fixed asset caching (`must-revalidate` + cache-busted image URLs) so updated diagrams appear without stale caching.
- Switched the README live-app links from Streamlit to the Vercel URL.
- Added `.gitignore` and `.env.example`; created a local gitignored `.env` for the GitHub token (old shared token to be revoked/rotated).
- Added the "update the Log every 5 prompts" and "never commit secrets" rules.

### 2026-06-16 — Luka Tcheishvili
- Renamed `CLAUDE.md` → `AGENT.md` and updated all internal references (incl. `DESIGN.md`).
- Added the **Git & Contribution Rules** section (commits/PRs under the human's name; no AI listed as contributor).
- Moved the 6 sample CSVs into a new `Data/` folder; updated the Streamlit loader to read from `Data/` (with root fallback) so the app still runs.
- Added a static **Vercel build** of the proposal in `manga-vercel/` (single-file `index.html`, same content/design, Plotly via CDN). Streamlit app kept unchanged as the fallback.
- Added this **What Has To Be Done** + **Log** structure to AGENT.md.
