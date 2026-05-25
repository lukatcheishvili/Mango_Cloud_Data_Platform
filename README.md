# 🛍️ Manga Cloud Platform — RFP Response

> **IE University · MBD-EN2025 · Cloud Analytics · Group Work B**  
> Interactive proposal for migrating a retail data architecture to AWS — built with Streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

This app is an interactive RFP response for **Manga**, a fictional Spanish fashion retailer (inspired by Mango), seeking to modernise its legacy on-premises data architecture into a cloud-native AWS data platform.

The current architecture relies on independent ETL pipelines triggered by daily cron jobs, aggregating outputs into Excel files shared with BI users. The goal is a full modernisation — real-time streaming, ML-ready, GDPR-compliant, and **40–60% cheaper** than the existing colocation model.

---

## App Pages

| Page | Description |
|---|---|
| 🏠 **Overview** | Executive summary, KPI metrics, stakeholder cards, key value drivers |
| 📐 **High-Level Architecture** | Interactive conceptual diagram — click any layer for design rationale |
| ⚙️ **Low-Level Architecture** | AWS service map — click any service for rationale, cost notes, and R1–R8 coverage |
| 🗄️ **Data Sources** | Live preview of all 6 sample datasets with schema, PII flags, and ingestion strategy |
| ✅ **Requirements Coverage** | R1–R8 requirement breakdown with AWS service mapping and coverage chart |
| 💡 **Use Cases** | 5 end-to-end ML use cases: recommendations, forecasting, sentiment, dynamic pricing, returns |

---

## Tech Stack

**App:** Python · Streamlit · Plotly · Pandas

**Proposed AWS Architecture:**
- **Ingestion:** Kinesis Data Streams · Kinesis Firehose · AWS Glue ETL · Lambda · DMS
- **Storage:** S3 Data Lakehouse (Raw / Curated / Serving) · Amazon Redshift · DynamoDB
- **Processing:** AWS Glue Data Quality · Amazon MWAA (Airflow) · Glue Data Catalog · Lake Formation · Macie
- **Consumption:** Amazon QuickSight · Amazon SageMaker · Amazon Comprehend · API Gateway
- **Cross-cutting:** IAM + KMS · Terraform/CDK · CloudWatch · AWS Organizations · Carbon Footprint Tool

---

## Dataset Overview

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

## Run Locally

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install -r requirements.txt
streamlit run app.py
```

---

## Deploy to Streamlit Cloud

1. Fork or push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select repo · branch `main` · file `app.py`
4. Click **Deploy** — live in ~2 minutes, no config needed

---

## RFP Requirements Coverage

The proposed architecture addresses all **8 RFP requirements**:

| ID | Requirement | Status |
|---|---|---|
| R1 | Unified multi-modal data platform | ✅ Covered |
| R2 | Multi-environment setup (Dev / Pre-Prod / Prod) | ✅ Covered |
| R3 | Automation & IaC | ✅ Covered |
| R4 | Security & high availability (**99.9% uptime SLA**) | ✅ Covered |
| R5 | Data quality monitoring | ✅ Covered |
| R6 | Cost optimisation (**projected 40–60% reduction**) | ✅ Covered |
| R7 | Extensibility & interoperability | ✅ Covered |
| R8 | Sustainability & carbon metrics | ✅ Covered |

---

## Project Context

- **Course:** Data Analytics in the Cloud — MBD-EN2025  
- **Institution:** IE University  
- **Deadline:** February 27, 2026  
- **Deliverable:** RFP response document + interactive presentation + video  
- **Scenario:** Manga operates **100+ physical stores** globally with **€280M annual revenue**, growing at only **+3.5%** vs a higher market average, spending **2× competitors** on infrastructure for half the analytical output.
