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
- Defined the logical layers: Data Sources → Ingestion → Processing (Validate/Clean/Norm + Transform/Enrich) → Storage (Raw → Cleaned → Curated zones) → Consumption, with Cataloging & Search bidirectionally connected to Processing and Security & Governance spanning every la