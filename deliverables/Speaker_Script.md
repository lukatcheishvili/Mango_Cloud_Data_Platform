# Manga DataHub — Presentation Speaker Script

**Target length:** ~12 minutes · **Format:** 12 slides, 6 presenters
Use this script as the latest presenter source of truth; the `.pptx` also includes presenter notes.
All six members speak — keep each turn tight and hand off clearly.

| # | Slide | Speaker | Time |
|---|-------|---------|------|
| 1 | Title | Andrea (opens for team) | 0:20 |
| 2 | The Problem | Andrea | 1:15 |
| 3 | The Solution — 3 pillars | Andrea → Mateus | 1:00 |
| 4 | Stakeholders | Mateus | 0:50 |
| 5 | High-Level Architecture | Mateus | 1:20 |
| 6 | Low-Level Architecture (AWS) | Tina | 1:30 |
| 7 | Requirements R1–R8 | Ricardo | 1:00 |
| 8 | Cost & ROI | Tina | 1:00 |
| 9 | Roadmap & risks | Ricardo | 1:00 |
| 10 | ML Use Cases | Luka | 1:15 |
| 11 | Future Improvements | Nicklas | 1:00 |
| 12 | Live platform & close / Q&A | Nicklas (all on stage) | 0:40 |

---

## 1 · Title — Andrea
"Good morning. We're **CloudCore Solutions**, responding to Manga's RFP. Over the next twelve minutes the six of us will walk you through the **Manga DataHub** — why Manga needs it, the architecture, what it costs, and what it unlocks." *(Hand to the problem.)*

## 2 · The Problem — Andrea
Anchor the pain in numbers: **€280M revenue but only 3.5% growth and 1.2% online**, while spending **~2× competitors for half the output**. The root cause is architectural — daily cron-job ETL, siloed pipelines, Excel as the BI layer, and an unclear GDPR posture. "This is exactly what the Manga DataHub fixes."

## 3 · The Solution — Andrea → Mateus
Three pillars: **Unify** (one governed platform), **Accelerate** (24h → sub-second), **Enable** (ML that's impossible today). Stress the **open-source core (Airflow, Spark, Parquet)** — this directly answers CTO Javier's lock-in fear. Hand to Mateus: "Let me show how the architecture delivers this."

## 4 · Stakeholders — Mateus
We mapped the proposal to the five named decision-makers. Don't read all five — highlight two: **CFO Manuel** gets 40–60% lower cost and clear ROI; **CTO Javier** gets no lock-in. InfoSec, COO, and Head of Data each have their concern addressed.

## 5 · High-Level Architecture — Mateus
The conceptual design, no vendor names yet: five layers — **Sources → Ingestion → three-zone Lakehouse → Processing → Consumption** — with **Security & Governance spanning everything** and a clean split between streaming and batch. Call out the four principles: separation of concerns, modularity, elasticity, open standards. Hand to Tina.

## 6 · Low-Level Architecture — Tina
Same architecture, now on AWS. **Kinesis + Firehose** for streaming, **Glue** for batch, **S3 three-zone lakehouse** (Bronze/Silver/Gold), **Redshift + DynamoDB** for serving, governance via **Lake Formation + Macie**. Every box maps to an R1–R8 requirement — which Ricardo will show.

## 7 · Requirements R1–R8 — Ricardo
We don't just claim coverage — the written proposal has a full **traceability table** plus an **Operating Evidence Appendix**. Hit highlights: **R3** automation (MWAA replaces cron), **R4** security and recovery targets (Lake Formation, Macie, KMS, RPO/RTO), **R5** concrete Glue Data Quality rules, **R6** cost assumptions, and **R8** carbon metrics. Segue to the numbers.

## 8 · Cost & ROI — Tina (CFO-facing)
Replacing fixed colocation with AWS pay-per-use cuts annual infra cost **~57% — €1.30M to €0.56M, about €0.74M saved a year**. We now show the assumptions behind that claim: fixed infrastructure, storage/backup, analytics serving, and operational overhead, validated monthly with Cost Explorer, CUR, and FinOps tags. **Pause on the −57%.**

If challenged on the number: "The final PDF includes a detailed cost-analysis appendix. It separates raw AWS metered prices from the fully loaded TCO, cites each AWS pricing source, and shows the exact formula: EUR 1.30M baseline minus EUR 0.56M target equals EUR 0.74M annual saving, or 56.9%."

## 9 · Roadmap & risks — Ricardo
Phased, controlled-risk delivery — Marta's priority. **Production cutover in month 7, handover by month 9.** Risks explicitly mitigated: DMS runs in parallel before cutover, open-source addresses lock-in, a DPIA precedes any personal data. Hand to Luka.

## 10 · ML Use Cases — Luka
Three end-to-end use cases on Manga's actual data: **demand forecasting (−30% stockouts), recommendations (+12–18% AOV), sentiment merchandising (2–3 weeks earlier)**. Two more extend the same platform. These directly attack the 1.2% online-growth problem. Hand to Nicklas.

## 11 · Future Improvements — Nicklas
The architecture is extensible by design. Short-term reuses existing infra for real-time personalisation and smart labels; medium-term adds a **Bedrock shopping assistant** and data monetisation; long-term, an **AI-agent ecosystem** and carbon-neutrality. Note the RFP explicitly asked for AI-agent data exposure — we have a path.

## 12 · Live platform & close — Nicklas (all on stage)
"Everything you've seen is **live and interactive at mangacloud-khaki.vercel.app** — open it on your device while we take questions." Thank the panel.

**Anticipated Q&A:** cost assumptions → Tina · security/GDPR and lifecycle controls → Ricardo/Mateus · RTO/RPO and HA/DR → Ricardo · sustainability metrics → Nicklas · vendor lock-in → Mateus · timeline feasibility → Ricardo. Keep answers ~30 seconds.
