# Manga Cloud Platform — RFP Response

> **IE University · MBD-EN2025 · Cloud Analytics · Group Work B**
> Interactive proposal for migrating a retail data architecture to AWS — live on Vercel.

[![Live on Vercel](https://img.shields.io/badge/Live-Vercel-000000?logo=vercel&logoColor=white)](https://mangacloud-khaki.vercel.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Live App

**[https://mangacloud-khaki.vercel.app/](https://mangacloud-khaki.vercel.app/)**

---

## Deliverable

- **[Manga_DataHub_RFP_Response.pdf](https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform/blob/main/Manga_DataHub_RFP_Response.pdf)** — Final RFP response document
- **[PowerPoint Presentation — Cloud Analytics.pptx](https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform/blob/main/powerpoint%20presentation%20-%20Cloud%20Analytics.pptx)** — Presentation deck
- **[Live App — mangacloud-khaki.vercel.app](https://mangacloud-khaki.vercel.app/)** — Interactive deployed proposal

---

## Project Team

- ANDREA ALARCÓN VALLES
- MATEUS CARNEIRO
- TINA JANNASCH
- RICARDO LIÉVANO PEDROZA
- LUKA TCHEISHVILI
- NICKLAS URBAN

### Architecture Diagrams (Figma)

| Diagram | Link |
|---|---|
| High-Level Architecture | **[View in FigJam](https://www.figma.com/board/UtHLPjygSysLe43cpzNCAp)** |
| Low-Level AWS Architecture | **[View in FigJam](https://www.figma.com/board/mvaVaoJErDBqNXt114FPqU)** |

---

## Executive Summary

**Manga** is a fictional Spanish fashion retailer (inspired by Mango) operating **100+ physical stores** globally with **€280M annual revenue**. Despite steady growth, Manga spends **2× more on infrastructure than its competitors** while producing far less analytical output. The root cause: a fragile, outdated data architecture that cannot support the speed or scale modern retail demands.

### The Problem

Manga's current setup consists of **independent ETL pipelines triggered by daily cron jobs**, each built by a different team with its own stack and no shared standards. Outputs are aggregated manually into **Excel files** distributed to business users. The consequences:

- **24-hour data lag** — managers make decisions on yesterday's data
- **No real-time capability** — inventory alerts, live sales tracking, and instant fraud detection are impossible
- **No self-service BI** — every report requires an Engineering ticket
- **GDPR exposure** — the previous InfoSec Manager was dismissed after a major security incident; compliance status is unclear
- **2× infrastructure cost** vs competitors for a colocation model that delivers half the analytical output
- **Zero ML capability** — personalisation, demand forecasting, and dynamic pricing are entirely absent

### Our Solution

We proposed a **cloud-native AWS data lakehouse** that replaces every part of this stack. The architecture is built around three pillars:

1. **Unify** — a single, governed platform ingesting all data sources (structured, semi-structured, and unstructured) through both real-time streaming and managed batch pipelines
2. **Accelerate** — time-to-insight reduced from 24 hours to sub-second, replacing Excel reports with live self-service dashboards
3. **Enable** — ML-powered features (product recommendations, demand forecasting, dynamic pricing, sentiment analysis, return prediction) that are architecturally impossible today

---

## What Was Required (RFP)

The RFP issued by Manga specified **8 mandatory requirements**:

| ID | Requirement | Description |
|---|---|---|
| **R1** | Unified multi-modal platform | Ingest and process structured, semi-structured, and unstructured data at scale, with both streaming and batch support |
| **R2** | Multi-environment setup | Separate Dev / Pre-Prod / Prod environments with anonymised data flowing to non-production |
| **R3** | Automation & IaC | All infrastructure as code; no manual deployments; replace cron jobs with managed orchestration |
| **R4** | Security & high availability | RBAC, encryption at rest and in transit, GDPR compliance, PII masking, 99.9% uptime SLA |
| **R5** | Data quality monitoring | Automated validation rules, alerting on failures, schema enforcement across all pipelines |
| **R6** | Cost optimisation | Measurable reduction vs current colocation spend; pay-per-use model |
| **R7** | Extensibility & interoperability | New data sources and consumers added without disrupting existing pipelines; open formats; partner API exposure |
| **R8** | Sustainability | Quantifiable carbon emissions reduction vs on-premises baseline; ESG reporting capability |

All **8 requirements are fully covered** by our proposed architecture.

---

## Evaluation-Ready Operating Evidence

To make the proposal auditable rather than just conceptual, we added explicit assumptions,
targets, and control matrices for the five areas most likely to be challenged by the
lecturer or client panel.

### R6 Cost Model Assumptions

The 40-60% savings claim is an annual run-rate estimate to be validated during discovery.
The base case compares a fixed colocation operating model of approximately **EUR 1.30M/year**
with a managed AWS target of approximately **EUR 0.56M/year**, producing an illustrative
**~57% infrastructure reduction**.

The detailed formula, AWS public unit prices, assumptions, sensitivity range, and presentation
talking points are included as an appendix inside [`deliverables/Manga_DataHub_RFP_Response.pdf`](./deliverables/Manga_DataHub_RFP_Response.pdf).

| Cost area | Current colocation assumption | AWS target assumption | Saving lever |
|---|---|---|---|
| Compute and ETL | Always-on partner servers sized for peak nightly jobs | Glue jobs billed per DPU-hour; non-critical jobs use Spot; MWAA runs small schedulers | Pay only when pipelines run |
| Storage and backup | SAN/NAS plus backup contract sized for seven-year growth | S3 Raw / Curated / Serving zones with Intelligent-Tiering and Glacier lifecycle | Hot data stays fast; cold data becomes cheap |
| BI and serving | Excel distribution plus manual engineering support | QuickSight pay-per-session, Athena pay-per-query, Redshift RA3 reserved for steady BI | Usage-based analytics |
| Operations | Partner-operated colocation and fixed support contract | Managed AWS services, CloudWatch/SNS automation, IaC repeatability | Fewer manual runbooks and escalations |
| Model result | About EUR 1.30M/year baseline | About EUR 0.56M/year target | Validated monthly with Cost Explorer, CUR, and FinOps tags |

### R8 Sustainability Metrics

Until the current data-center provider supplies actual emissions data, the baseline is
normalised as a **carbon index of 100**. The AWS target is a **carbon index of 45-60** after
migration, equivalent to an expected **40-55% reduction in operational carbon intensity**.

| Metric | Baseline method | Target / control | Review cadence |
|---|---|---|---|
| Operational carbon index | Current colocation normalised to 100 using invoices, server count, and provider energy/PUE data | 45-60 after migration, measured with AWS Customer Carbon Footprint Tool | Monthly |
| Idle compute ratio | Always-on servers sized for peak batch windows | Less than 20% idle compute through serverless, autoscaling, and scheduled jobs | Monthly |
| Storage efficiency | All historical data held in high-cost tiers | 90-day transition to S3 IA and 180/365-day transition to Glacier tiers | Monthly |
| Region policy | Provider-dependent energy mix | Prefer EU Ireland / EU Frankfurt; enforce region choices through IaC variables and SCP guardrails | Every release |
| Reporting | Limited provider transparency | Dashboard by service, environment, kgCO2e, TB-month, DPU-hour, and EUR spent | Monthly ESG pack |

### R4 High Availability and Disaster Recovery

| Workload | HA / DR pattern | Target RPO | Target RTO |
|---|---|---:|---:|
| S3 lakehouse | Versioning, Object Lock on Raw, lifecycle policies, optional cross-region replication for Raw and Curated zones | 15 min for replicated zones | 4 h regional recovery |
| Kinesis / Firehose | Managed Multi-AZ stream, retries, failed-record S3 prefix, replay from Raw zone | <5 min | <1 h |
| Glue and MWAA | DAGs and jobs in Git, Terraform redeploy, Glue bookmarks, retries, backfills | Last successful checkpoint | 4 h |
| Redshift / Athena / QuickSight | Automated Redshift snapshots, Spectrum over S3, dashboards can repoint to standby warehouse | 15 min-24 h by data mart criticality | 4-8 h |
| DynamoDB and APIs | Point-in-time recovery, autoscaling, optional global tables for customer-facing APIs | <5 min | <1 h |

### R5 Data Quality Rule Examples

| Dataset | Example Glue Data Quality / DQDL-style controls |
|---|---|
| `sales_sample.csv` | `purchase_price > 0`; `customer_id` completeness > 99%; referential integrity from `product_id` to inventory |
| `customers_sample.csv` | `customer_id` complete and unique; age between 13 and 100; PII detection before non-prod replication |
| `inventory_sample.csv` | `stock >= 0`; `price > 0`; product description completeness > 95% |
| `customer_reviews_sample.csv` | review text length between 5 and 2,000 characters; rating between 1 and 5; product/customer IDs complete |
| `external_factors_sample.csv` | date complete and unique; fuel price positive; campaign IDs conform to agreed pattern when present |
| `shipping_sample.csv` | order ID complete; actual shipping cost non-negative; returned flag limited to true/false values |

Failures block promotion from Curated to Serving and trigger CloudWatch/SNS alerts with the
dataset, rule, failed row count, and owning data product.

### Data Lifecycle and Retention Matrix

| Dataset | Sensitivity | Raw zone retention | Curated / Serving retention | Archive and deletion policy |
|---|---|---|---|---|
| Sales | Tokenised customer IDs; financial records | 7 years | 5 years curated, 3 years serving aggregates | IA after 90 days, Glacier after 365 days; preserve finance aggregates |
| Customers | Direct PII | Active relationship + 24 months | Masked/tokenised in curated; non-prod receives anonymised samples only | Right-to-erasure workflow tokenises or deletes PII within 30 days, subject to legal hold |
| Inventory | No PII | 5 years | 3 years curated and serving | IA after 180 days; expire obsolete product snapshots after retention |
| Customer reviews | PII risk in text/images | 3 years | 3 years curated sentiment/features | PII scan on landing; remove or anonymise review content on customer request |
| External factors | No PII | 5 years | 5 years curated | IA after 180 days; retain for forecast reproducibility |
| Shipping | Address PII and cost records | 6 years | 3 years curated with addresses masked | IA after 90 days, Glacier after 365 days; delete/mask addresses under privacy workflow |

---

## What We Did

### Architecture Design

We designed a **two-tier architecture** aligned with the professor's reference:

**High-Level Architecture (technology-agnostic)**
- Defined the logical layers: Data Sources → Ingestion → Processing (Validate/Clean/Norm + Transform/Enrich) → Storage (Raw → Cleaned → Curated zones) → Consumption, with Cataloging & Search bidirectionally connected to Processing and Security & Governance spanning every layer
- Kept entirely vendor-neutral so the design can be mapped to any cloud provider

**Low-Level Architecture (AWS-specific)**
- Mapped every logical component to a specific AWS service with cost model, operational rationale, and RFP coverage
- Added all services from the professor's reference diagram: AWS Data Exchange, AWS Transfer Family/SFTP, Amazon Athena, AWS CloudTrail
- Documented encryption strategy: TLS 1.3 in transit (TLS termination at service boundaries — allows platform-side analytics while keeping every hop encrypted), KMS at rest

### Interactive Streamlit App

Built a fully interactive RFP response as a Streamlit app with **6 pages**:

- **Branded loading screen** — one-time MANGA launch overlay with Framer-style wordmark, capsule progress bar, smooth fade-out, and fail-safe removal before the app opens
- **Overview** — executive summary, KPI metrics, stakeholder analysis (champions vs. skeptics), core value drivers
- **High-Level Architecture** — technology-agnostic clickable diagram + Plotly interactive chart (hover any node for design rationale and RFP coverage)
- **Low-Level Architecture** — AWS service map + Plotly interactive chart (hover any node for service rationale, cost model, and RFP requirement)
- **Data Sources** — live preview of all 6 sample datasets with schema, PII flags, and ingestion strategy
- **Requirements Coverage** — R1–R8 breakdown with AWS service mapping and coverage chart
- **Use Cases** — 5 end-to-end ML use cases with pipeline diagrams and business impact estimates

### Data Analysis

Worked with **6 synthetic datasets** representing Manga's existing systems, analysing schema, data quality, PII exposure, and optimal ingestion patterns for each.

### Figma Architecture Diagrams

Created professional architecture diagrams in Figma FigJam:
- [High-Level Architecture](https://www.figma.com/board/UtHLPjygSysLe43cpzNCAp) — technology-agnostic process flow
- [Low-Level AWS Architecture](https://www.figma.com/board/mvaVaoJErDBqNXt114FPqU) — full AWS service map

### Live Web App (Vercel)

The proposal is deployed as a static web build (`manga-vercel/`) on **Vercel**, auto-deploying on every push to `main`:

- **Live:** https://mangacloud-khaki.vercel.app/
- **Interactive architecture diagrams** — hover any box in the high- and low-level views for its role, rationale, cost model, and RFP coverage
- **Official AWS service logos** — each low-level service box shows its real logo (Lambda, Glue, S3, Redshift, SageMaker, Kinesis, and more) in the hover popup

---

## What We Used

### App Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **Streamlit** | Interactive web app framework |
| **Plotly** | Interactive architecture charts with hover tooltips |
| **Pandas** | Dataset loading and analysis |
| **Figma / FigJam** | Architecture diagram creation |

### Proposed AWS Architecture

**Ingestion**
- **Amazon Kinesis Data Streams** — sub-second real-time ingestion for POS, review, and order events
- **Amazon Kinesis Firehose** — stream-to-S3 delivery with automatic Parquet conversion
- **AWS Glue ETL** — managed Spark replacing all cron-job scripts; job bookmarks prevent duplicate processing
- **AWS Lambda + EventBridge** — serverless API connectors for external data sources
- **AWS DMS** — database migration and CDC replication from on-premises systems
- **AWS Data Exchange** — licensed third-party datasets (market data, demographics)
- **AWS Transfer Family** — managed SFTP/FTPS endpoint for partner file delivery

**Storage**
- **Amazon S3 (Raw / Curated zones)** — immutable data lakehouse; open Parquet format; Intelligent-Tiering for cost
- **Amazon Redshift** — columnar data warehouse for BI serving; Spectrum for S3 queries without loading
- **Amazon DynamoDB** — <10ms NoSQL lookups for ML inference and real-time features

**Processing & Governance**
- **AWS Glue Data Catalog** — central metadata store; schema registry; self-service discovery
- **Amazon MWAA (Airflow)** — DAG-based orchestration replacing all cron jobs; open-source core (no lock-in)
- **AWS Glue Data Quality** — automated validation rules with CloudWatch alerting
- **AWS Lake Formation** — fine-grained RBAC at column and row level; GDPR compliance hub
- **Amazon Macie** — ML-powered PII scanner continuously monitoring S3

**Consumption**
- **Amazon Athena** — serverless SQL directly on S3; pay per query
- **Amazon QuickSight** — managed BI replacing Excel; pay-per-session pricing
- **Amazon SageMaker** — end-to-end ML: recommendations, demand forecasting (DeepAR), dynamic pricing, return prediction
- **Amazon Comprehend** — managed NLP sentiment analysis on customer reviews
- **Amazon API Gateway** — secure REST APIs exposing curated data to partners and AI agents

**Security & Cross-cutting**
- **AWS IAM + KMS** — least-privilege access; KMS encryption at rest; TLS 1.3 in transit
- **Amazon VPC** — network isolation; private subnets; VPC endpoints
- **AWS CloudTrail** — immutable API audit logs for GDPR Right of Access/Erasure
- **Amazon CloudWatch** — unified monitoring and alerting across all services
- **AWS Organizations** — three isolated accounts (Dev / Pre-Prod / Prod) with Service Control Policies
- **Terraform / AWS CDK** — infrastructure as code; peer-reviewed; Git version-controlled
- **AWS Carbon Footprint Tool** — emissions tracking vs on-premises baseline (R8)

---

## Dataset Overview

Six synthetic datasets representing Manga's existing systems:

| Dataset | Source | Ingestion Pattern | PII |
|---|---|---|---|
| `sales_sample.csv` | POS / E-commerce | Kinesis (streaming) | No |
| `customers_sample.csv` | CRM / Loyalty | Glue batch (daily) | Yes |
| `inventory_sample.csv` | ERP / WMS | Glue batch (hourly) | No |
| `customer_reviews_sample.csv` | Web / App | Kinesis + Comprehend | Yes |
| `external_factors_sample.csv` | Weather API / Internal | Lambda (daily pull) | No |
| `shipping_sample.csv` | Logistics Partner API | Lambda + Glue | Yes |

---

## ML Use Cases

| Use Case | Datasets Used | AWS Services | Business Impact |
|---|---|---|---|
| Product Recommendations | Sales, Customers, Inventory | SageMaker, DynamoDB, API Gateway | +12–18% avg order value |
| Demand Forecasting | Sales, External Factors, Inventory | SageMaker DeepAR, MWAA, QuickSight | −30% stockouts, −20% overstock |
| Sentiment-Driven Merchandising | Customer Reviews | Comprehend, Glue, QuickSight, SNS | 2–3 weeks earlier product decisions |
| Dynamic Pricing Engine | Sales, Inventory, External Factors | SageMaker, Lambda, DynamoDB | +3–7% gross margin |
| Return Rate Optimisation | Shipping, Sales, Customers | SageMaker, Glue, QuickSight, SNS | −10–15% return processing costs |

---

## Run Locally

```bash
git clone https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform.git
cd Mango_Cloud_Data_Platform
pip install -r requirements.txt
streamlit run mango_cloud_platform.py
```

All 6 sample CSV files are included in the repo. The app handles missing files gracefully with a warning.

---

## Deployment (Vercel)

The live site is the static build in [`manga-vercel/`](./manga-vercel), hosted on **Vercel** and auto-deployed on every push to `main`:

1. On [vercel.com](https://vercel.com) → **Add New → Project** → import this repo
2. Set **Root Directory** to `manga-vercel` · Framework preset **Other** · leave build/output empty
3. **Deploy** — live in ~1 minute

> Live URL: https://mangacloud-khaki.vercel.app/
>
> The Streamlit app (`mango_cloud_platform.py`) remains as a local/fallback version — see **Run Locally** above.

---

## Deliverables

Final deliverables live in [`deliverables/`](./deliverables):

| File | What it is |
|---|---|
| `Manga_DataHub_RFP_Response.pdf` | Final PDF response with the detailed cost-analysis appendix embedded |
| `Manga_DataHub_RFP_Response.docx` | Editable RFP proposal with operating-evidence appendix, cost assumptions, HA/DR targets, DQ rules, lifecycle controls, and cost figure |
| `Manga_DataHub_Deck.pptx` | 13-slide presentation with per-slide speaker notes |
| `Speaker_Script.md` | Timed ~13-minute run-of-show across all 6 presenters |
| `cost_comparison.png` | Colocation vs. AWS cost figure (~57% reduction; illustrative) |

---

## Project Context

| | |
|---|---|
| **Course** | Data Analytics in the Cloud — MBD-EN2025 |
| **Institution** | IE University |
| **Deliverable** | RFP response document + interactive presentation + video |
| **Scenario** | Manga operates 100+ physical stores globally with €280M annual revenue, growing at +3.5% vs a higher market average, spending 2× competitors on infrastructure for half the analytical output |
