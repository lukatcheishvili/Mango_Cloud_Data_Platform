# Manga DataHub Detailed Cost Analysis

Date prepared: 2026-06-17

This document explains how the project cost estimate was built, which AWS public prices were
used, and how the headline claim is calculated:

```text
Current colocation run-rate: EUR 1,300,000 / year
Target AWS run-rate:         EUR   560,000 / year
Estimated saving:            EUR   740,000 / year
Estimated reduction:         740,000 / 1,300,000 = 56.9%, rounded to 57%
```

## 1. Important Positioning

The cost model is a presentation-ready directional TCO estimate, not an audited quote. The RFP
case gives us two hard inputs:

| Input from case | How it is used |
|---|---|
| Manga has EUR 280M annual revenue | Used only to sanity-check scale. The current cost model equals about 0.46% of revenue. |
| Manga has about 2x infrastructure cost vs competitors | Used to derive a current baseline from a competitor-normal operating assumption. |

The case does not provide Manga's actual colocation invoice, exact data volumes, current BI
license spend, or current support contract. Because of that, the absolute EUR values are
explicit assumptions. The percentage logic is still useful because it compares fixed,
peak-sized infrastructure with managed, usage-based cloud services.

If the professor asks "where did the EUR 1.30M come from?", the honest answer is:

```text
The RFP states that Manga pays about 2x competitors for infrastructure.
We assumed a competitor-normal analytics infrastructure cost of about EUR 650k/year.
Therefore Manga current baseline = EUR 650k * 2 = EUR 1.30M/year.
```

This should be replaced with Manga's real invoices during discovery.

## 2. AWS Price Sources Used

All AWS prices below are public AWS pricing references accessed on 2026-06-17. AWS states that
prices vary by Region, so the final client estimate should be rebuilt in AWS Pricing Calculator
for the chosen EU Region, most likely eu-west-1 Ireland or eu-central-1 Frankfurt.

| Service | Public unit price used in this model | Source |
|---|---:|---|
| AWS Glue ETL, Crawlers, Data Quality | USD 0.44 per DPU-hour | https://aws.amazon.com/glue/pricing/ |
| AWS Glue Data Catalog | First 1M metadata objects free; USD 1.00 per 100k objects over 1M per month | https://aws.amazon.com/glue/pricing/ |
| Amazon Kinesis Data Streams, provisioned | USD 0.015 per shard-hour; USD 0.014 per 1M PUT payload units in AWS example | https://aws.amazon.com/kinesis/data-streams/pricing/ |
| Amazon Kinesis Data Streams, on-demand standard example | USD 0.08 per GB data-in; USD 0.040 per GB data-out in AWS example | https://aws.amazon.com/kinesis/data-streams/pricing/ |
| Amazon Data Firehose | USD 0.029 per GB ingested for first 500 TB/month; USD 0.018 per GB for JSON to Parquet/ORC conversion; USD 0.020 per GB dynamic partitioning | https://aws.amazon.com/firehose/pricing/ |
| AWS Lambda | USD 0.20 per 1M requests; USD 0.0000166667 per GB-second; first 1M requests and 400k GB-seconds free per month | https://aws.amazon.com/lambda/pricing/ |
| Amazon S3 Standard | USD 0.023 per GB-month planning rate | https://aws.amazon.com/s3/pricing/ |
| Amazon S3 Standard-IA | USD 0.0125 per GB-month planning rate | https://aws.amazon.com/s3/pricing/ |
| Amazon S3 Glacier Flexible Retrieval | USD 0.0036 per GB-month planning rate | https://aws.amazon.com/s3/pricing/ |
| S3 lifecycle transition | USD 0.01 per 1,000 transition requests from S3 Standard to Standard-IA, per AWS example | https://aws.amazon.com/s3/pricing/ |
| Amazon Athena SQL | USD 5 per TB scanned; AWS example shows 3 TB = USD 15 and Parquet/column pruning reducing scan cost | https://aws.amazon.com/athena/pricing/ |
| Amazon Athena capacity reservation | USD 0.30 per DPU-hour in AWS example | https://aws.amazon.com/athena/pricing/ |
| Amazon Redshift provisioned/serverless | Provisioned starts at USD 0.543/hour; Serverless begins at USD 1.50/hour | https://aws.amazon.com/redshift/pricing/ |
| Amazon Redshift managed storage | USD 0.024 per GB-month in AWS example | https://aws.amazon.com/redshift/pricing/ |
| Amazon QuickSight Author | USD 24 per user/month | https://aws.amazon.com/quicksight/pricing/ |
| Amazon QuickSight Reader | USD 3 per user/month | https://aws.amazon.com/quicksight/pricing/ |
| Amazon QuickSight SPICE | USD 0.38 per GB/month; 10 GB included with each Author | https://aws.amazon.com/quicksight/pricing/ |
| Amazon MWAA | AWS examples show about USD 449/month for a small environment and about USD 1,047/month for a large environment | https://aws.amazon.com/managed-workflows-for-apache-airflow/pricing/ |
| AWS DMS | Serverless/on-demand migration capacity is pay-per-hour; AWS Pricing Calculator recommended for final migration sizing | https://aws.amazon.com/dms/pricing/ |

Planning FX assumption for presentation tables:

```text
1 USD = 0.92 EUR
```

This FX rate is a planning convention only. Replace it with the current EUR/USD rate before
submission if the team wants exact currency conversion.

## 3. Current Colocation Baseline

The baseline is not from an invoice. It is derived from the RFP fact that Manga pays about
2x competitors for infrastructure.

### 3.1 Baseline Formula

```text
Annual revenue = EUR 280,000,000
Assumed competitor-normal analytics infrastructure intensity = 0.23% of revenue

Competitor-normal annual infrastructure cost
= 280,000,000 * 0.0023
= EUR 644,000
Rounded planning baseline = EUR 650,000

Manga current infrastructure cost
= competitor-normal baseline * 2
= 650,000 * 2
= EUR 1,300,000 per year
```

### 3.2 Baseline Cost Breakdown

| Current cost area | Annual cost | Why this is plausible for current state |
|---|---:|---|
| Compute and ETL servers | EUR 420,000 | Always-on partner/colocation servers sized for peak nightly batch jobs, cron scripts, and manual reprocessing. |
| Storage and backup | EUR 280,000 | SAN/NAS, backup retention, duplicate extracts, and historical data kept in expensive tiers. |
| BI and reporting | EUR 240,000 | Excel distribution, manual report generation, licensing/support overhead, and engineering time for every new report. |
| Operations, facilities, support | EUR 360,000 | Fixed partner support, incident handling, monitoring, facilities, and manual operations. |
| Total | EUR 1,300,000 | Equals the assumed 2x competitor-normal baseline. |

## 4. AWS Target Run-Rate

The AWS target is a fully loaded annual run-rate. It is not only the raw AWS service bill.

```text
Direct AWS metered services, planning estimate:       EUR 217,000
Platform operations, FinOps, support, run team:       EUR 175,000
Security, governance, observability, DR reserve:      EUR  65,000
Contingency and usage growth buffer:                  EUR 103,000
Target fully loaded AWS annual run-rate:              EUR 560,000
```

The reason for this structure is that public AWS prices only price metered services. The project
also needs production support, incident management, data governance, access reviews, cost control,
 DR drills, backups, tagging, audit evidence, and room for data volume variance.

### 4.1 Fully Loaded Target by Cost Area

| AWS target cost area | Annual target | What is included |
|---|---:|---|
| Compute and ETL | EUR 150,000 | Glue, Data Quality, Kinesis, Firehose, Lambda, MWAA, batch/stream orchestration, and run support allocated to pipelines. |
| Storage and backup | EUR 95,000 | S3 Raw/Curated/Serving zones, lifecycle transitions, backups, replication reserve, object monitoring, and restore testing. |
| BI and serving | EUR 135,000 | Redshift, Athena, QuickSight, SPICE, dashboard serving, warehouse tuning, and performance support. |
| Operations, security, governance | EUR 180,000 | CloudWatch, CloudTrail, KMS, Macie, Lake Formation administration, Terraform/CDK, support, FinOps, DR, and compliance work. |
| Total | EUR 560,000 | Fully loaded run-rate used in the RFP response. |

## 5. Direct AWS Metered Service Calculations

These calculations show the underlying service math. They are intentionally transparent so the
team can defend the estimate and adjust volumes quickly.

### 5.1 Streaming Ingestion: Kinesis Data Streams

We use provisioned Kinesis for predictable POS/review streams because the store count is known and
the workload can be capacity-planned. AWS example pricing shows a 4-shard stream costing USD 52.14
per month for shard hours plus PUT payload units.

Planning assumption:

```text
3 production streams or equivalent stream capacity
Monthly cost per 4-shard stream = USD 52.14
Annual Kinesis cost = 52.14 * 3 * 12 = USD 1,877
EUR equivalent = 1,877 * 0.92 = EUR 1,727
Rounded with monitoring/retention buffer = EUR 2,500 / year
```

### 5.2 Stream Delivery: Amazon Data Firehose

Firehose lands streaming events into S3 and converts JSON to Parquet to reduce downstream Athena
and Redshift Spectrum scan cost.

Planning assumption:

```text
Monthly streaming data landed = 2 TB = 2,048 GB
Direct PUT / Kinesis-source ingestion = USD 0.029 per GB
Format conversion to Parquet = USD 0.018 per GB
Dynamic partitioning = USD 0.020 per GB

Monthly cost
= 2,048 * (0.029 + 0.018 + 0.020)
= 2,048 * 0.067
= USD 137.22

Annual cost
= 137.22 * 12
= USD 1,646.64

EUR equivalent
= 1,646.64 * 0.92
= EUR 1,515

Rounded with object/request buffer = EUR 2,000 / year
```

### 5.3 Batch ETL and Transformations: AWS Glue

Glue replaces the current cron-job ETL scripts. The model uses DPU-hours, not always-on servers.

Planning assumption:

```text
Daily batch estate:
20 daily jobs * 4 DPUs * 1.5 hours/job * 30 days = 3,600 DPU-hours/month
Rounded planning usage = 3,500 DPU-hours/month

Glue ETL monthly cost
= 3,500 * USD 0.44
= USD 1,540

Glue ETL annual cost
= 1,540 * 12
= USD 18,480
```

Glue Data Quality:

```text
DQ usage = 600 DPU-hours/month
DQ monthly cost = 600 * 0.44 = USD 264
DQ annual cost = 264 * 12 = USD 3,168
```

Crawlers/catalog/statistics/optimization:

```text
Crawler and optimization reserve = 300 DPU-hours/month
Monthly cost = 300 * 0.44 = USD 132
Annual cost = 132 * 12 = USD 1,584

Data Catalog metadata:
Assume under first 1M objects/accesses during MVP = USD 0
Reserve for growth and partition churn = USD 100/month = USD 1,200/year
```

Total Glue planning cost:

```text
Glue total USD = 18,480 + 3,168 + 1,584 + 1,200 = USD 24,432
Glue total EUR = 24,432 * 0.92 = EUR 22,477
Rounded = EUR 23,000 / year
```

### 5.4 Orchestration: Amazon MWAA

MWAA replaces cron with Airflow DAGs, dependency handling, retries, and operational visibility.
AWS examples show a small environment around USD 449/month and a larger environment around
USD 1,047/month.

Planning assumption:

```text
Production environment plus non-production/test capacity = USD 1,500/month
Annual cost = 1,500 * 12 = USD 18,000
EUR equivalent = 18,000 * 0.92 = EUR 16,560
Rounded with log/storage buffer = EUR 18,000 / year
```

### 5.5 API Connectors and Event Tasks: AWS Lambda

Lambda handles scheduled pulls from external APIs, small enrichment tasks, and glue code around
events. This is deliberately modeled with a high request count to show that Lambda remains small
relative to the full platform.

Planning assumption:

```text
Requests/month = 20,000,000
Memory = 512 MB = 0.5 GB
Average duration = 300 ms = 0.3 seconds
Free tier = 1,000,000 requests and 400,000 GB-seconds/month

Request charges:
Billable requests = 20,000,000 - 1,000,000 = 19,000,000
Monthly request cost = 19 * USD 0.20 = USD 3.80

Compute charges:
Monthly GB-seconds = 20,000,000 * 0.5 * 0.3 = 3,000,000 GB-seconds
Billable GB-seconds = 3,000,000 - 400,000 = 2,600,000
Monthly compute cost = 2,600,000 * 0.0000166667 = USD 43.33

Monthly Lambda cost = 3.80 + 43.33 = USD 47.13
Annual Lambda cost = 47.13 * 12 = USD 565.56
EUR equivalent = 565.56 * 0.92 = EUR 520
Rounded with API/logging buffer = EUR 1,000 / year
```

### 5.6 Storage and Lakehouse Retention: Amazon S3

The architecture keeps immutable raw data, curated Parquet, serving aggregates, and archives.
Lifecycle policy moves cold data to cheaper classes.

Planning footprint:

| Tier | Average footprint | Unit rate | Monthly cost |
|---|---:|---:|---:|
| Raw hot data, S3 Standard | 20 TB = 20,480 GB | USD 0.023 / GB-month | USD 471.04 |
| Curated/Serving hot data, S3 Standard | 30 TB = 30,720 GB | USD 0.023 / GB-month | USD 706.56 |
| Warm history, S3 Standard-IA | 60 TB = 61,440 GB | USD 0.0125 / GB-month | USD 768.00 |
| Cold archive, S3 Glacier Flexible Retrieval | 120 TB = 122,880 GB | USD 0.0036 / GB-month | USD 442.37 |
| Storage subtotal | 230 TB average | Mixed | USD 2,387.97 / month |

Annual storage subtotal:

```text
2,387.97 * 12 = USD 28,655.64
EUR equivalent = 28,655.64 * 0.92 = EUR 26,363
```

Lifecycle, request, replication, inventory, and backup testing reserve:

```text
Reserve = 45% of storage subtotal
= 26,363 * 0.45
= EUR 11,863

Direct S3/lakehouse annual estimate
= 26,363 + 11,863
= EUR 38,226
Rounded = EUR 40,000 / year
```

The fully loaded storage/backup target is higher at EUR 95,000/year because it includes
cross-region replication reserve, restore testing, object-lock/legal hold administration,
privacy deletion workflows, and operational support.

### 5.7 Ad Hoc SQL on the Lakehouse: Amazon Athena

Athena is billed by TB scanned. Parquet, compression, and partition pruning are a major cost lever.
AWS's own example shows a 3 TB text-file query costing USD 15, and the same analytical question
dropping to USD 1.25 with compression plus Parquet column pruning.

Planning assumption:

```text
Unoptimized scan volume = 60 TB/month
Reduction from Parquet + partition pruning = 70%
Optimized billed scan volume = 60 * (1 - 0.70) = 18 TB/month

Monthly Athena cost = 18 * USD 5 = USD 90
Annual Athena cost = 90 * 12 = USD 1,080
EUR equivalent = 1,080 * 0.92 = EUR 994
Ad hoc growth buffer = 3x
Rounded = EUR 3,000 / year
```

### 5.8 BI Warehouse: Amazon Redshift

Redshift serves curated BI workloads that need predictable concurrency and performance. The model
uses a planning envelope rather than a single hard cluster shape because Redshift may be serverless
or provisioned during implementation.

Planning assumption:

```text
AWS public anchor:
Redshift Serverless begins at USD 1.50/hour.
Provisioned Redshift begins at USD 0.543/hour.
Managed storage example is USD 0.024/GB-month.

Base serverless/provisioned BI compute envelope = USD 3,500/month
Annual Redshift compute/storage estimate = 3,500 * 12 = USD 42,000
EUR equivalent = 42,000 * 0.92 = EUR 38,640
Rounded with snapshots/performance reserve = EUR 45,000 / year
```

This budget can be reduced with Serverless Reservations or Reserved Instances once actual usage
patterns are known. AWS states Redshift Serverless Reservations can reduce compute costs by up to
45% for eligible workloads.

### 5.9 BI Dashboards: Amazon QuickSight

QuickSight replaces Excel distribution and manual reporting. The base model uses per-user pricing
because Manga has a known internal audience.

Planning assumption:

```text
Authors = 25
Readers = 400
SPICE total = 500 GB
Included SPICE = 25 authors * 10 GB = 250 GB
Billable SPICE = 500 - 250 = 250 GB

Author monthly cost = 25 * USD 24 = USD 600
Reader monthly cost = 400 * USD 3 = USD 1,200
SPICE monthly cost = 250 * USD 0.38 = USD 95

Monthly QuickSight cost = 600 + 1,200 + 95 = USD 1,895
Annual QuickSight cost = 1,895 * 12 = USD 22,740
EUR equivalent = 22,740 * 0.92 = EUR 20,921
Rounded = EUR 23,000 / year
```

### 5.10 Migration: AWS DMS

DMS is treated as a one-time migration/cutover cost, not a steady annual run-rate. The public AWS
DMS page states that serverless/on-demand migration capacity is paid by the hour and scales with
the data transaction volume. Because the case does not provide database size, exact DCUs, or
cutover duration, we reserve a one-time implementation budget:

```text
One-time DMS migration and CDC testing reserve = EUR 12,000
Included in implementation planning, not the recurring EUR 560,000 AWS run-rate
```

## 6. Direct AWS Subtotal

| Service group | Annual direct estimate |
|---|---:|
| Kinesis Data Streams | EUR 2,500 |
| Data Firehose | EUR 2,000 |
| AWS Glue ETL, Crawlers, Data Quality, Catalog | EUR 23,000 |
| Amazon MWAA | EUR 18,000 |
| AWS Lambda | EUR 1,000 |
| Amazon S3 lakehouse direct storage/requests reserve | EUR 40,000 |
| Amazon Athena | EUR 3,000 |
| Amazon Redshift | EUR 45,000 |
| Amazon QuickSight | EUR 23,000 |
| CloudWatch, CloudTrail, KMS, Macie, Lake Formation, backup/monitoring reserve | EUR 60,000 |
| Direct AWS metered-service subtotal | EUR 217,500 |

Rounded direct AWS service usage:

```text
EUR 217,500 -> EUR 217,000
```

## 7. Why the Target Is EUR 560k, Not EUR 217k

The raw AWS services are only one part of the cost. A production enterprise data platform also
requires people, support, compliance, change control, and contingency.

```text
Direct AWS metered service estimate = EUR 217,000
Platform operations and FinOps = EUR 175,000
Security/governance/DR reserve = EUR 65,000
Subtotal before contingency = EUR 457,000

Contingency and usage growth buffer
= 457,000 * 22.5%
= EUR 102,825
Rounded = EUR 103,000

Fully loaded target
= 217,000 + 175,000 + 65,000 + 103,000
= EUR 560,000/year
```

This is the correct number to compare against current colocation because current colocation cost
also includes support/operations overhead, not only hardware.

## 8. Savings Calculation

```text
Current annual cost = EUR 1,300,000
AWS target annual cost = EUR 560,000

Annual savings
= 1,300,000 - 560,000
= EUR 740,000

Savings percentage
= 740,000 / 1,300,000
= 0.5692
= 56.9%
Rounded = 57%
```

## 9. Sensitivity Analysis

| Scenario | Current baseline | AWS annual run-rate | Annual saving | Saving % | Interpretation |
|---|---:|---:|---:|---:|---|
| Optimistic | EUR 1,300,000 | EUR 460,000 | EUR 840,000 | 64.6% | Higher automation, lower data growth, strong Redshift/QuickSight optimization. |
| Base case | EUR 1,300,000 | EUR 560,000 | EUR 740,000 | 56.9% | Used in the proposal and cost figure. |
| Conservative | EUR 1,300,000 | EUR 720,000 | EUR 580,000 | 44.6% | Higher support needs, more data retention, more BI concurrency. |

The base and conservative cases both sit inside the RFP's requested 40-60% reduction range.

## 10. Presentation Talking Points

Use this concise version on Slide 8:

```text
Our cost model is not a raw AWS bill; it is a fully loaded annual run-rate.
The RFP says Manga spends about 2x competitors, so we model the current state at EUR 1.30M/year.
The AWS target is EUR 560k/year, built from public AWS unit prices plus operations, governance,
DR, support, and contingency. That creates EUR 740k annual savings, or about 57%.
```

If asked for the details:

```text
Glue is priced per DPU-hour, not per server.
Firehose and Kinesis are priced per GB/shard usage.
Athena is priced per TB scanned, which is why Parquet and partitioning are critical.
QuickSight is priced per Author/Reader plus SPICE.
Redshift is bounded with serverless/provisioned public price anchors.
S3 lifecycle policies reduce storage cost by moving cold history into IA and Glacier.
```

If asked what could change the estimate:

```text
The largest variables are actual current invoices, real data volume, BI user count, required
retention periods, support model, and final AWS Region. The formulas stay the same; we would
replace assumptions with discovery numbers.
```

## 11. Data Needed to Finalize the Estimate

Before submitting a client-grade quote, collect:

| Missing input | Why it matters |
|---|---|
| Current annual colocation and support invoices | Replaces the assumed EUR 1.30M baseline. |
| Exact AWS Region | AWS public prices vary by Region. |
| Monthly source data volume and growth rate | Drives S3, Firehose, Glue, Athena, Redshift, backup, and replication costs. |
| Number of BI Authors, Readers, and embedded sessions | Drives QuickSight pricing model choice. |
| Required RTO/RPO and cross-region replication scope | Drives DR and backup reserve. |
| PII retention/legal-hold rules | Drives S3 lifecycle and deletion workflow cost. |
| Internal vs managed-service operations model | Drives the fully loaded run-rate above raw AWS service pricing. |
