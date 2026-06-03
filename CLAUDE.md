# CLAUDE.md — Project Context & State

> **⚠️ KEEP THIS FILE UPDATED.**
> Every time you push changes to this repo, update the relevant sections below.
> This file is read automatically by AI assistants (Claude, Cowork) at the start of every session,
> so all team members get full project context regardless of which device they are working from.

---

## 🗂️ Project Identity

| Field | Value |
|---|---|
| **Project name** | Manga Cloud Platform — RFP Response |
| **Course** | Data Analytics in the Cloud — MBD-EN2025 |
| **Institution** | IE University |
| **Deliverable** | RFP response document + interactive Streamlit presentation + video walkthrough |
| **Deadline** | June 19, 2026 |
| **GitHub repo** | https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform |
| **Live Streamlit app** | https://manga-cloud-platform.streamlit.app/ |
| **Figma HLA diagram** | https://www.figma.com/board/UtHLPjygSysLe43cpzNCAp |
| **Figma LLA diagram** | https://www.figma.com/board/mvaVaoJErDBqNXt114FPqU |

---

## 🧠 Project Summary (for AI context)

This is a **group university project** for IE University's Cloud Analytics course. We are responding to a fictional RFP from **Manga** (a fictional Spanish fashion retailer modelled on Mango) that wants to modernise its legacy on-premises data infrastructure into a cloud-native AWS data platform.

**The scenario:** Manga has 100+ physical stores, €280M annual revenue, and a broken data stack — daily cron-job ETL scripts, siloed pipelines, Excel-based BI, no real-time capability, 2× infrastructure cost vs competitors, and unclear GDPR compliance.

**Our deliverable:** A complete RFP response proposing an AWS-based cloud data lakehouse, presented as an interactive Streamlit app with clickable architecture diagrams, dataset previews, requirements coverage analysis, and ML use case demonstrations.

The project is **not about building the actual cloud infrastructure** — it is about designing and presenting the architecture proposal in a compelling, technically accurate way that satisfies all 8 RFP requirements (R1–R8).

---

## 👥 Key Stakeholders (Manga side — from RFP)

| Person | Role | Stance | Key Concern |
|---|---|---|---|
| Marta Ríos | COO | ✅ Champion | End-to-end solution with clear business case |
| Javier Medina | CTO | ⚠️ Skeptic | Vendor lock-in; open-source preference |
| Manuel Ortega | CFO | 💰 Cost-focused | 2× infra cost vs competitors; needs clear ROI |
| Laura Smith | InfoSec Manager | 🔐 Security-first | GDPR; prior security incident; non-negotiable |
| Alex Lee | Head of Data & AI | 🚀 Champion | Wants modern DataOps; knows current arch is broken |

---

## 📋 RFP Requirements Status

| ID | Requirement | Status | Key AWS Services |
|---|---|---|---|
| R1 | Unified multi-modal data platform | ✅ Covered | Kinesis, Glue, S3, Redshift, Athena |
| R2 | Multi-environment (Dev/Pre-Prod/Prod) | ✅ Covered | AWS Organizations, Terraform, Lake Formation |
| R3 | Automation & IaC | ✅ Covered | MWAA (Airflow), Terraform/CDK, Glue, EventBridge |
| R4 | Security & high availability | ✅ Covered | IAM, KMS, TLS, Lake Formation, Macie, CloudTrail, VPC |
| R5 | Data quality monitoring | ✅ Covered | Glue Data Quality, CloudWatch, SNS |
| R6 | Cost optimisation | ✅ Covered | S3 Intelligent-Tiering, Spot Instances, QuickSight pay-per-session |
| R7 | Extensibility & interoperability | ✅ Covered | API Gateway, Lambda, Data Exchange, Transfer Family |
| R8 | Sustainability & carbon metrics | ✅ Covered | AWS Carbon Footprint Tool, EU green regions |

---

## 🏗️ Architecture Overview

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

## 📁 Repository Structure

```
Mango_Cloud_Data_Platform/
├── mango_cloud_platform.py        # Main Streamlit app (all 6 pages)
├── requirements.txt               # Python dependencies (streamlit, pandas, plotly)
├── README.md                      # Project overview and documentation
├── CLAUDE.md                      # ← THIS FILE — AI context and project state
├── sales_sample.csv               # POS / e-commerce transactions
├── customers_sample.csv           # CRM / loyalty data (contains PII)
├── inventory_sample.csv           # ERP / WMS stock levels
├── customer_reviews_sample.csv    # Web/app reviews (text + images, contains PII)
├── external_factors_sample.csv    # Weather, events, campaigns
├── shipping_sample.csv            # Logistics partner data (contains PII)
├── Group Work B - Retail.pdf      # Original RFP document from professor
├── Manga_DataHub_RFP_Response.pdf # Our written RFP response document
└── .github/
    └── workflows/
        └── update-context-reminder.yml  # Reminds team to update CLAUDE.md on every push
```

---

## 🖥️ App Structure (mango_cloud_platform.py)

The app has **6 pages** navigated via sidebar buttons stored in `st.session_state.page`:

| Page key | Title | What it contains |
|---|---|---|
| `overview` | Overview | KPI metrics, executive summary, stakeholder cards, value drivers |
| `hla` | High-Level Architecture | Tech-agnostic clickable HTML diagram + Plotly interactive chart with hover |
| `lla` | Low-Level Architecture | AWS service map HTML diagram + Plotly interactive chart with hover |
| `data` | Data Sources | Expandable panels for each of the 6 CSVs with schema and ingestion info |
| `reqs` | Requirements Coverage | R1–R8 cards with AWS services + coverage bar chart |
| `usecases` | Use Cases | 5 ML use case expanders + dataset usage heatmap |

**Key implementation notes:**
- Both HLA and LLA pages use `st.tabs()` with two tabs: Interactive HTML diagram + Plotly chart
- Plotly charts use `go.Scatter` with square markers and rich `hovertext` per node
- HTML diagrams use `st.components.v1.html()` with embedded JS for click interactions
- CSVs loaded with `@st.cache_data` + `try/except` — app works even if CSVs are missing
- All styling done via a single CSS block injected with `st.markdown(unsafe_allow_html=True)`
- Dark theme throughout: background `#0a0e1a`, cards `#111827`, accent `#4a9af0`

---

## 📊 Dataset Details

| File | Rows (approx) | Key columns | PII | Ingestion pattern |
|---|---|---|---|---|
| `sales_sample.csv` | ~1000 | datetime, customer_id, product_id, store_id, price, discount, payment_method | No | Kinesis streaming |
| `customers_sample.csv` | ~500 | customer_id, name, age, gender, address, zip, loyalty_status | **Yes** | AWS DMS batch |
| `inventory_sample.csv` | ~300 | product_id, store_id, stock_level, price, description | No | Glue batch hourly |
| `customer_reviews_sample.csv` | ~400 | review_id, customer_id, product_id, rating, review_text, image_url | **Yes** | Kinesis + Comprehend |
| `external_factors_sample.csv` | ~365 | date, weather, fuel_price, bank_holiday, local_event, campaign_id | No | Lambda daily pull |
| `shipping_sample.csv` | ~600 | order_id, delivery_address, estimated_delivery, actual_delivery, delivery_price, actual_cost, return_status | **Yes** | Lambda + Glue batch |

---

## ✅ What Has Been Completed

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
- [x] CLAUDE.md created (this file)
- [x] GitHub Actions workflow for CLAUDE.md update reminders

---

## 🔲 Remaining Tasks

> Update this section as tasks are completed or new ones are identified.

### High Priority (needed for submission)

- [ ] **Record the video walkthrough** — walk through the live Streamlit app explaining each page; mention RFP requirements being addressed; show the Figma diagrams
- [ ] **Finalise the written RFP response PDF** (`Manga_DataHub_RFP_Response.pdf`) — ensure all 8 requirements are addressed in the written document with the same content as the app
- [ ] **Review and proofread the app** — check all text for typos, consistent terminology (Manga not Mango), correct RFP references
- [ ] **Add team member names** to the Overview page and README (currently missing)

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

## 🛠️ How to Run Locally

```bash
git clone https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform.git
cd Mango_Cloud_Data_Platform
pip install -r requirements.txt
streamlit run mango_cloud_platform.py
```

Requirements: `streamlit>=1.32.0`, `pandas>=2.0.0`, `plotly>=5.18.0`

---

## 📌 Important Decisions & Rationale

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

## 🔄 How to Update This File

When you push changes, update the relevant section(s):

- **Fixed a bug or improved a feature** → update "What Has Been Completed" and check off any tasks in "Remaining Tasks"
- **Added a new feature or page** → update "App Structure" and "What Has Been Completed"
- **Made an architectural decision** → add a row to "Important Decisions & Rationale"
- **Identified new work** → add to "Remaining Tasks" under the appropriate priority
- **Changed a file or added a new one** → update "Repository Structure"

A GitHub Action will warn you on every push if you forgot to update this file.

---

*Last updated: 2026-06-03 | Updated by: Luka Tcheishvili*
