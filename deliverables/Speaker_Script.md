# Manga DataHub - Speaker Script

**Target length:** ~13 minutes  
**Format:** 11-slide HTML deck, 6 presenters  
**Source deck:** `deliverables/powerpoint presentation - Cloud Analytics.html`

Use this script as the presenter source of truth for the current HTML deck. It follows the slide order shown in the interactive presentation, not the older 13-slide draft.

| # | HTML slide | Speaker | Time |
|---|---|---|---|
| 1 | MBD-EN2025 - RFP Response | Andrea | 0:35 |
| 2 | The Problem | Andrea | 1:20 |
| 3 | The Solution | Andrea -> Mateus | 1:05 |
| 4 | Stakeholders | Mateus | 1:00 |
| 5 | High-Level Architecture | Mateus | 1:25 |
| 6 | Low-Level Architecture - AWS | Ricardo | 1:45 |
| 7 | Requirements Coverage | Ricardo | 1:20 |
| 8 | Cost & ROI | Tina | 1:35 |
| 9 | Machine Learning Use Cases | Luka | 1:25 |
| 10 | Delivery Roadmap & Risk | Luka | 1:15 |
| 11 | CloudCore Solutions | Nicklas | 0:50 |

---

## Slide 1 - MBD-EN2025 - RFP Response

**Speaker: Andrea | Time: 0:35**

Good morning. We are CloudCore Solutions, and today we are presenting our response to Manga's RFP: the Manga DataHub.

Our proposal is built around three outcomes: unify Manga's fragmented data, accelerate the business from daily reporting to near real-time insight, and enable advanced analytics and machine learning on top of a governed cloud platform.

Over the next 13 minutes, the six of us will show the business problem, the architecture, the cost case, the roadmap, and what this platform unlocks for Manga.

---

## Slide 2 - The Problem

**Speaker: Andrea | Time: 1:20**

Manga is a strong retailer, but its data architecture has fallen behind the business.

The company has EUR 280 million in annual revenue and more than 100 stores, but growth is only 3.5%, online growth is just 1.2%, and infrastructure spend is roughly twice the competitor level while producing only about half the output.

The technical root cause is visible on the right side of the slide. Manga relies on cron-job ETL, disconnected operational systems, Excel-heavy BI, unclear GDPR controls, and no scalable machine learning layer.

That creates a 24-hour data lag. Store, web, CRM, POS, ERP, and external data exist, but they do not arrive in one trusted platform quickly enough to support pricing, inventory, marketing, or omnichannel decisions.

So the issue is not only a reporting issue. It is an operating model issue. Manga needs a cloud data platform that is faster, cheaper, more governed, and ready for analytics.

---

## Slide 3 - The Solution

**Speaker: Andrea -> Mateus | Time: 1:05**

Our solution is the Manga DataHub, built on three pillars.

First, unify: all source systems land in one governed lakehouse so the business no longer works from conflicting extracts.

Second, accelerate: ingestion, processing, and serving are automated so dashboards and data products move from daily delay to near real-time or sub-second access where needed.

Third, enable: once the foundation is trusted, Manga can build ML use cases such as demand forecasting, recommendations, sentiment analysis, dynamic pricing, and return-rate optimisation.

One important design choice is the open-source core: Airflow-style orchestration, Spark-style processing, and Parquet-based storage. That gives Manga cloud benefits without locking the data model into a single proprietary stack.

Mateus will now explain how that solution maps to the people making the decision.

---

## Slide 4 - Stakeholders

**Speaker: Mateus | Time: 1:00**

This slide shows that the architecture is not only technical. It is mapped to each stakeholder's concern.

Marta, the COO, needs operational visibility across stores and ecommerce. Manuel, the CFO, needs a lower and more transparent cost base. Javier, the CTO, is skeptical of vendor lock-in, so we use open formats and modular services. Laura, the InfoSec Manager, needs encryption, access control, auditability, and GDPR readiness. Alex, the Head of Data and AI, needs governed data products that can support ML.

Our proposal works because it does not optimize for one stakeholder at the expense of the others. The same platform supports cost control, security, analytics, and future scalability.

---

## Slide 5 - High-Level Architecture

**Speaker: Mateus | Time: 1:25**

At the high level, the architecture has five layers.

On the left, Manga's data sources include CRM, POS, ERP, ecommerce, web events, external APIs, and file-based partner data.

The ingestion layer separates batch, streaming, CDC, API, and file transfer patterns, because not every dataset should move in the same way.

The processing layer validates, transforms, and standardizes data before it enters the lakehouse.

The lakehouse itself is divided into raw, cleaned, and curated zones. Raw keeps the original record for traceability, cleaned applies quality and schema controls, and curated prepares business-ready datasets for dashboards, APIs, and ML.

Finally, the consumption layer supports BI, operational APIs, data science, and partner access.

Security and governance span every layer. That is why the diagram shows them above the flow: identity, encryption, monitoring, lineage, and data quality are platform controls, not afterthoughts.

Ricardo will now translate this logical design into the AWS implementation.

---

## Slide 6 - Low-Level Architecture - AWS

**Speaker: Ricardo | Time: 1:45**

This slide shows how the high-level design becomes a concrete AWS platform.

At the top, security and monitoring span all layers. We use CloudTrail for audit logs, VPC networking for isolation, Terraform or CDK for infrastructure as code, IAM and KMS for access control and encryption, CloudWatch for monitoring and alerts, and AWS Organizations for dev, pre-prod, and production separation.

On the left, the source systems use the ingestion pattern that fits each case. External weather and logistics APIs are pulled on schedule. CRM changes are captured through DMS. Market signals arrive through event subscription. Ecommerce events stream through Kinesis. ERP and POS exports can use Transfer Family, and SaaS or file sources can land through Glue connectors or batch pipelines.

In the middle, S3 is the lakehouse backbone. Data lands first in the raw zone, then moves through validation and transformation into curated datasets. Glue Data Quality, Glue DataBrew, Macie, and Lake Formation provide cataloging, quality checks, privacy scanning, and governed access.

On the right, different consumers use different serving technologies. Redshift supports analytics queries, DynamoDB supports low-latency operational access, SageMaker supports ML, Athena supports ad hoc SQL, Comprehend supports text and sentiment analysis, QuickSight supports dashboards, and API Gateway exposes partner or application APIs.

The key point is that each service has a role. This is not a random AWS list; it is a mapped implementation of Manga's source patterns, governance needs, and consumption use cases.

---

## Slide 7 - Requirements Coverage

**Speaker: Ricardo | Time: 1:20**

This slide is our RFP traceability view. All eight requirements are covered, and each one is linked to concrete platform evidence.

R1 is the unified data platform, delivered through the S3 lakehouse, Glue catalog, and governed data zones.

R2 is environment and access separation through AWS Organizations, IAM, KMS, VPC, and infrastructure as code.

R3 is modernization of the current cron-job ETL into managed orchestration, repeatable deployments, and observable pipelines.

R4 covers security, high availability, disaster recovery, encryption, auditability, and backup patterns.

R5 covers data quality through profiling, validation rules, DQ checks, and curated business datasets.

R6 covers cost efficiency through the move from fixed colocation and license-heavy spending to metered cloud services.

R7 covers integration and APIs through API Gateway, event patterns, and governed access for business and partner systems.

R8 covers sustainability through carbon reporting, regional choices, right-sizing, lifecycle policies, and storage tiering.

So this slide is the bridge between the architecture and the lecturer's marking criteria: the design is traceable, not just visually complete.

---

## Slide 8 - Cost & ROI

**Speaker: Tina | Time: 1:35**

The financial case is one of the strongest parts of the proposal.

Today, Manga's estimated fully loaded annual platform cost is EUR 1.30 million. That includes compute and servers, ETL, operations and DBA work, storage and backup, and BI or ETL licenses.

The proposed AWS-based run-rate is EUR 0.56 million per year. That creates an estimated annual saving of EUR 0.74 million, or 57%.

The budget bridge at the bottom shows how we get to that EUR 0.56 million. Direct AWS metered services account for about EUR 217 thousand. Platform operations and FinOps account for about EUR 175 thousand. Security, governance, and disaster recovery account for about EUR 65 thousand. We also include EUR 103 thousand of contingency, which is important because the first-year cloud bill should not be presented as artificially perfect.

The comparison is not just "AWS is cheaper." The real difference is fixed cost versus variable cost. Colocation requires capacity to be bought ahead of demand, while AWS allows Manga to scale compute, storage, ingestion, and analytics around actual usage.

After migration, the model should be validated monthly using AWS Cost Explorer, the Cost and Usage Report, tagging, budgets, and FinOps reviews. That keeps the 57% target measurable rather than theoretical.

---

## Slide 9 - Machine Learning Use Cases

**Speaker: Luka | Time: 1:25**

The ML slide shows why the data platform matters beyond dashboards.

The first use case is demand forecasting. By combining POS, inventory, ecommerce, promotions, and external signals, Manga can reduce stockouts and improve replenishment decisions.

The second is personalized recommendations. With a unified customer and product view, Manga can increase online conversion and average order value, which directly attacks the current 1.2% online growth problem.

The third is sentiment merchandising. Customer reviews, support tickets, and social feedback can be processed with NLP so merchandising teams see trend signals earlier instead of waiting for manual analysis.

The slide also includes dynamic pricing and return-rate optimisation. These are natural next steps once the platform has reliable historical, behavioral, and operational data.

The important point is that these ML use cases are not standalone experiments. They depend on the previous slides: governed ingestion, clean lakehouse zones, quality rules, security controls, and scalable serving.

---

## Slide 10 - Delivery Roadmap & Risk

**Speaker: Luka | Time: 1:15**

The roadmap is phased to reduce migration risk.

In months 1 and 2, Manga builds the foundation: AWS landing zone, networking, IAM, KMS, infrastructure as code, and the first governed data lake structure.

In months 3 to 5, the team migrates priority pipelines and builds the lakehouse, starting with the datasets that create the highest business value.

Month 7 is the production cutover, where the platform becomes the operational source for dashboards and data products.

By month 9, the focus shifts to handover, FinOps, operating model maturity, and the first production ML use cases.

The main risks are migration disruption, vendor lock-in, and data privacy. We mitigate them with parallel DMS replication and reconciliation, open formats like Parquet and Spark-compatible processing, and a DPIA plus access controls before personal data is broadly activated.

Nicklas will close with the live platform and Q&A.

---

## Slide 11 - CloudCore Solutions

**Speaker: Nicklas | Time: 0:50**

To close, the proposal gives Manga three outcomes.

First, it covers all eight RFP requirements with clear traceability.

Second, it reduces the estimated annual platform cost by 57%, from EUR 1.30 million to EUR 0.56 million.

Third, it moves Manga from a 24-hour reporting lag toward near real-time and sub-second analytical access where the business needs it.

Everything you have seen is also available as the live interactive platform at **mangacloud.web**.

Thank you. We are ready for your questions.

---

## Q&A Routing

Use this only after the formal presentation.

| Topic | Lead speaker |
|---|---|
| Business problem, RFP framing | Andrea |
| Stakeholders, lock-in, open architecture | Mateus |
| AWS architecture, security, HA/DR, RTO/RPO | Ricardo |
| Cost model, savings, assumptions, FinOps | Tina |
| ML use cases, analytics value | Luka |
| Sustainability, roadmap, close | Nicklas |

---

## Presenter Notes

- Do not add extra spoken slides for cost detail or future improvements; those are supporting Q&A topics in the current HTML deck.
- Keep the final slide focused on `mangacloud.web`, since the visible slide uses the alias rather than showing the full Vercel URL.
- When asked about the cost numbers, explain that the EUR 0.56 million target combines direct AWS meters, platform operations, security/governance/DR, and contingency.
- When asked about sustainability, point back to R8: carbon reporting, right-sized compute, green-region preference, and S3 lifecycle tiering.
