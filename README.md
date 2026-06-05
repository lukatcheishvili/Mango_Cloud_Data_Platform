# 🛍️ Manga Cloud Platform — RFP Response

> **IE University · MBD-EN2025 · Cloud Analytics · Group Work B**
> Interactive proposal for migrating a retail data architecture to AWS — built with Streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://manga-cloud-platform.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Live App

**[https://manga-cloud-platform.streamlit.app/](https://manga-cloud-platform.streamlit.app/)**

---

## 👥 Project Team

- ANDREA ALARCÓN VALLES
- MATEUS CARNEIRO
- TINA JANNASCH
- RICARDO LIÉVANO PEDROZA
- LUKA TCHEISHVILI
- NICKLAS URBAN

### 📐 Architecture Diagrams (Figma)

| Diagram | Link |
|---|---|
| 🗺️ High-Level Architecture | **[View in FigJam](https://www.figma.com/board/UtHLPjygSysLe43cpzNCAp)** |
| ⚙️ Low-Level AWS Architecture | **[View in FigJam](https://www.figma.com/board/mvaVaoJErDBqNXt114FPqU)** |

---

## 📋 Executive Summary

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

## 🎯 What Was Required (RFP)

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

## ✅ What We Did

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

---

## 🛠️ What We Used

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
- **Amazon Kinesis Data Streams** — sub-second real-time ingestion for POS and web events
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

## 📊 Dataset Overview

Six synthetic datasets representing Manga's existing systems:

| Dataset | Source | Ingestion Pattern | PII |
|---|---|---|---|
| `sales_sample.csv` | POS / E-commerce | Kinesis (streaming) | No |
| `customers_sample.csv` | CRM / Loyalty | Glue batch (daily) | ✅ Yes |
| `inventory_sample.csv` | ERP / WMS | Glue batch (hourly) | No |
| `customer_reviews_sample.csv` | Web / App | Kinesis + Comprehend | ✅ Yes |
| `external_factors_sample.csv` | Weather API / Internal | Lambda (daily pull) | No |
| `shipping_sample.csv` | Logistics Partner API | Lambda + Glue | ✅ Yes |

---

## 💡 ML Use Cases

| Use Case | Datasets Used | AWS Services | Business Impact |
|---|---|---|---|
| Product Recommendations | Sales, Customers, Inventory | SageMaker, DynamoDB, API Gateway | +12–18% avg order value |
| Demand Forecasting | Sales, External Factors, Inventory | SageMaker DeepAR, MWAA, QuickSight | −30% stockouts, −20% overstock |
| Sentiment-Driven Merchandising | Customer Reviews | Comprehend, Glue, QuickSight, SNS | 2–3 weeks earlier product decisions |
| Dynamic Pricing Engine | Sales, Inventory, External Factors | SageMaker, Lambda, DynamoDB | +3–7% gross margin |
| Return Rate Optimisation | Shipping, Sales, Customers | SageMaker, Glue, QuickSight, SNS | −10–15% return processing costs |

---

## ▶️ Run Locally

```bash
git clone https://github.com/lukatcheishvili/Mango_Cloud_Data_Platform.git
cd Mango_Cloud_Data_Platform
pip install -r requirements.txt
streamlit run mango_cloud_platform.py
```

All 6 sample CSV files are included in the repo. The app handles missing files gracefully with a warning.

---

## ☁️ Deploy to Streamlit Cloud

1. Fork or push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select repo · branch `main` · file `mango_cloud_platform.py`
4. Click **Deploy** — live in ~2 minutes, no config needed

---

## 📁 Project Context

| | |
|---|---|
| **Course** | Data Analytics in the Cloud — MBD-EN2025 |
| **Institution** | IE University |
| **Deadline** | June 19, 2026 |
| **Deliverable** | RFP response document + interactive presentation + video |
| **Scenario** | Manga operates 100+ physical stores globally with €280M annual revenue, growing at +3.5% vs a higher market average, spending 2× competitors on infrastructure for half the analytical output |
