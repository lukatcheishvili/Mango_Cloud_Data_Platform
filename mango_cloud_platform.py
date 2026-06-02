import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import os

st.set_page_config(
    page_title="Mango Retail · AWS Cloud Data Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0e1a !important; color: #d0ddf0;
}
[data-testid="stSidebar"] {
    background-color: #0d1220 !important; border-right: 1px solid #1e2d45;
}
[data-testid="stSidebar"] * { color: #a0b8d8 !important; }
header[data-testid="stHeader"] { display: none; }
.card {
    background: #111827; border: 1px solid #1e2d45;
    border-radius: 10px; padding: 18px 20px; margin-bottom: 12px; transition: border-color .2s;
}
.card:hover { border-color: #3a6ab0; }
.metric-card {
    background: #111827; border: 1px solid #1e2d45;
    border-radius: 10px; padding: 16px; text-align: center;
}
.metric-value { font-size: 28px; font-weight: 800; color: #4a9af0; }
.metric-label { font-size: 11px; color: #6a8aaa; text-transform: uppercase; letter-spacing: .08em; margin-top: 4px; }
.section-title {
    font-size: 11px; font-weight: 700; letter-spacing: .12em;
    text-transform: uppercase; color: #4a6a9a;
    margin-bottom: 14px; padding-bottom: 6px; border-bottom: 1px solid #1e2d45;
}
.page-title { font-size: 22px; font-weight: 800; color: #c8d8f0; margin-bottom: 4px; }
.page-sub { font-size: 13px; color: #6a8aaa; margin-bottom: 20px; }
.badge {
    display: inline-block; font-size: 10px; font-weight: 700;
    padding: 3px 9px; border-radius: 20px; margin: 2px;
}
.badge-blue  { background:#0a1830; color:#60a8f0; border:1px solid #1a3860; }
.badge-green { background:#0a1e14; color:#50c880; border:1px solid #1a4828; }
.badge-orange{ background:#2a1800; color:#f0a040; border:1px solid #5a3000; }
.badge-purple{ background:#1a0a28; color:#b070f0; border:1px solid #3a1858; }
.badge-red   { background:#1e0a0a; color:#f07070; border:1px solid #5a2020; }
.stk-card {
    background: #111827; border: 1px solid #1e2d45;
    border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
}
.stk-name { font-size: 13px; font-weight: 700; color: #c0d4f0; }
.stk-role { font-size: 10px; color: #4a6a9a; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 8px; }
.stk-concern { font-size: 11px; color: #8090a8; line-height: 1.5; }
.stk-tag { font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 4px; display: inline-block; margin-top: 6px; }
.stk-skeptic { background:#2a1800; color:#f0a040; }
.stk-champion { background:#0a1e14; color:#50c880; }
.stk-neutral { background:#0a1830; color:#60a8f0; }
[data-testid="stTabs"] button { font-size: 12px !important; font-weight: 600 !important; color: #6a8aaa !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #4a9af0 !important; border-bottom: 2px solid #4a9af0 !important; }
[data-testid="stDataFrame"] { border: 1px solid #1e2d45; border-radius: 8px; }
hr { border-color: #1e2d45 !important; }
</style>
""", unsafe_allow_html=True)


# ── Data Loader ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = Path(__file__).parent
    files = {
        "Sales":            "sales_sample.csv",
        "Customers":        "customers_sample.csv",
        "Inventory":        "inventory_sample.csv",
        "Customer Reviews": "customer_reviews_sample.csv",
        "External Factors": "external_factors_sample.csv",
        "Shipping":         "shipping_sample.csv",
    }
    datasets = {}
    for name, fname in files.items():
        path = base / fname
        if path.exists():
            try:
                datasets[name] = pd.read_csv(path)
            except Exception:
                pass
    return datasets

DATA = load_data()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 18px'>
      <div style='font-size:28px'>🛍️</div>
      <div style='font-size:14px; font-weight:800; color:#c8d8f0;'>Manga Cloud Platform</div>
      <div style='font-size:10px; color:#3a5a7a; letter-spacing:.1em; text-transform:uppercase; margin-top:2px'>RFP Response · AWS Proposal</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Overview":                 "overview",
        "📐  High-Level Architecture":  "hla",
        "⚙️  Low-Level Architecture":   "lla",
        "🗄️  Data Sources":             "data",
        "✅  Requirements Coverage":    "reqs",
        "💡  Use Cases":                "usecases",
    }

    if "page" not in st.session_state:
        st.session_state.page = "overview"

    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    for label, key in pages.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key

    st.markdown("---")
    st.markdown("""
    <div style='font-size:10px; color:#2a4060; text-align:center; line-height:1.7'>
      IE University · MBD-EN2025<br>
      Cloud Analytics · Group Work B<br>
      Due: June 19, 2026
    </div>
    """, unsafe_allow_html=True)

PAGE = st.session_state.page


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if PAGE == "overview":
    st.markdown('<div class="page-title">Cloud Data Platform for Manga</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">AWS-powered modernisation proposal — replacing legacy cron-ETL with a real-time, scalable data lakehouse</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    kpis = [("€280M","Annual Revenue"),("+3.5%","Growth (vs market avg)"),("100+","Physical Stores"),("2×","Cost vs Competitors")]
    for col, (val, lbl) in zip([c1,c2,c3,c4], kpis):
        col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        <p style="font-size:13px; color:#a0b8c8; line-height:1.8; margin:0">
        Manga's current architecture — independent ETL pipelines triggered by cron jobs, aggregating into daily Excel files —
        is incompatible with the real-time, AI-driven experiences modern retail demands.<br><br>
        Our proposal delivers a <strong style="color:#c8d8f0">cloud-native AWS data lakehouse</strong> on three pillars:
        <strong style="color:#4a9af0">Unify</strong> all data sources into a single governed platform,
        <strong style="color:#50c880">Accelerate</strong> time-to-insight from 24 hours to sub-second, and
        <strong style="color:#f0a040">Enable</strong> ML-powered features — recommendations, dynamic pricing,
        demand forecasting — impossible today.
        </p></div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:16px">Problem: As-Is Architecture</div>', unsafe_allow_html=True)
        for icon, title, desc in [
            ("⏰","Daily batch cron jobs","No real-time capability. Managers wait 24 h for yesterday's data."),
            ("🗂️","Siloed ETL pipelines","Each pipeline built by a different team. No shared standards."),
            ("📊","Excel as the BI layer","Manual aggregation. No self-service. No drill-down."),
            ("💸","2× competitor cost","Colocation model costs twice as much for half the analytical output."),
            ("🔒","Security gaps","Previous InfoSec Manager dismissed after a major incident. GDPR compliance unclear."),
        ]:
            st.markdown(f'<div class="card" style="padding:12px 16px;margin-bottom:8px;border-left:3px solid #5a2020"><span style="font-size:16px">{icon}</span><strong style="color:#f07070;font-size:12px;margin-left:8px">{title}</strong><p style="font-size:11px;color:#7a8a9a;margin:4px 0 0 28px">{desc}</p></div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">Key Stakeholders</div>', unsafe_allow_html=True)
        for name, role, concern, stype, tag in [
            ("Marta Ríos","COO · 25 yrs","Wants end-to-end solution with solid business case. Results over ideology.","champion","✅ Champion"),
            ("Javier Medina","CTO · 15 yrs","Fears vendor lock-in. Champions open-source & modular systems.","skeptic","⚠️ Skeptic"),
            ("Manuel Ortega","CFO · 25 yrs","Alarmed by 2× cost vs competitors. Open to change if ROI is clear.","neutral","💰 Cost-focused"),
            ("Laura Smith","InfoSec Manager","New hire with GDPR mandate. Security is non-negotiable.","skeptic","🔐 Security-first"),
            ("Alex Lee","Head of Data & AI","Joined from competitor. Knows the current arch is broken.","champion","🚀 Champion"),
        ]:
            st.markdown(f'<div class="stk-card"><div class="stk-name">{name} <span class="stk-tag stk-{stype}">{tag}</span></div><div class="stk-role">{role}</div><div class="stk-concern">{concern}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Our Solution — Core Value Drivers</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (icon, color, title, desc) in enumerate([
        ("⚡","#4a9af0","Real-Time Everything","Replace all daily-batch pipelines with Kinesis streaming. Sub-second POS sales, web events, and inventory updates."),
        ("🏗️","#50c880","Open & Modular","Apache Airflow (MWAA), open Parquet/Delta formats, Terraform IaC. No proprietary lock-in — addressing the CTO's core concern."),
        ("🔒","#f0a040","Security by Design","Lake Formation RBAC, Macie PII scanning, KMS encryption, TLS in-transit, full GDPR audit trails — built in from day one."),
        ("🤖","#b070f0","ML-Ready Platform","SageMaker connected to a curated feature store. Product recommendations, demand forecasting, and dynamic pricing from day one."),
        ("💸","#50c880","Measurable Cost Savings","Pay-per-use vs fixed colocation. S3 Intelligent-Tiering, Spot Instances — projected 40–60% infra cost reduction."),
        ("🌱","#4a9af0","Sustainability Metrics","AWS Carbon Footprint Tool tracks emissions by service/region — quantifiable improvement vs colocation for R8 compliance."),
    ]):
        with cols[i % 3]:
            st.markdown(f'<div class="card" style="border-top:3px solid {color}"><div style="font-size:22px;margin-bottom:8px">{icon}</div><div style="font-size:13px;font-weight:700;color:#c0d4f0;margin-bottom:6px">{title}</div><div style="font-size:11px;color:#7090a8;line-height:1.6">{desc}</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HIGH-LEVEL ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "hla":
    st.markdown('<div class="page-title">High-Level Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Technology-agnostic conceptual design — architectural process layers without vendor specifics (RFP Section 2)</div>', unsafe_allow_html=True)

    tab_diagram, tab_chart = st.tabs(["🗺️ Interactive Diagram", "📊 Plotly Architecture Chart"])

    with tab_diagram:
        st.info("💡 **Click any component** to see its role, design rationale, and which RFP requirements it addresses.")
        hla_html = """<!DOCTYPE html><html><head>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0e1a;font-family:'Segoe UI',sans-serif;color:#e0e6f0;padding:14px}
.outer{display:grid;grid-template-columns:140px 1fr 140px;grid-template-rows:auto auto auto auto auto auto;gap:8px}
.sources{grid-column:1;grid-row:2/6;background:#0d1320;border:2px dashed #2a4060;border-radius:8px;padding:10px;display:flex;flex-direction:column;gap:7px}
.src-title{font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3a5a7a;margin-bottom:4px;text-align:center}
.main-col{grid-column:2;display:contents}
.catalog-row{grid-column:2;grid-row:1;background:#111830;border:1px solid #2a3a5a;border-radius:8px;padding:10px;text-align:center;cursor:pointer;transition:all .18s}
.catalog-row:hover,.catalog-row.active{background:#182048;border-color:#4a6ad0;box-shadow:0 0 0 2px rgba(74,106,208,.25)}
.ingestion-row{grid-column:2;grid-row:2;background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:10px;text-align:center;cursor:pointer;transition:all .18s}
.ingestion-row:hover,.ingestion-row.active{background:#182235;border-color:#4a7ac8;box-shadow:0 0 0 2px rgba(74,122,200,.25)}
.proc-row{grid-column:2;grid-row:3;display:flex;gap:8px}
.storage-row{grid-column:2;grid-row:4;display:flex;gap:8px}
.sec-row{grid-column:1/4;grid-row:6;background:#1a0808;border:1px solid #3a1515;border-radius:8px;padding:10px;text-align:center;cursor:pointer;transition:all .18s}
.sec-row:hover,.sec-row.active{background:#2a0d0d;border-color:#6a2020}
.consumption-col{grid-column:3;grid-row:2/5;background:#0d1a10;border:1px solid #1a3520;border-radius:8px;padding:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:all .18s}
.consumption-col:hover,.consumption-col.active{background:#132518;border-color:#2a6040;box-shadow:0 0 0 2px rgba(42,96,64,.25)}
.box{flex:1;background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:10px 8px;text-align:center;cursor:pointer;transition:all .18s}
.box:hover,.box.active{background:#182235;border-color:#4a7ac8;box-shadow:0 0 0 2px rgba(74,122,200,.2)}
.src-box{background:#0d1320;border:1px solid #1a2840;border-radius:6px;padding:8px 6px;text-align:center;cursor:pointer;transition:all .15s}
.src-box:hover,.src-box.active{border-color:#4a7ac8;background:#101c30}
.icon{font-size:18px;margin-bottom:4px}
.title{font-size:10px;font-weight:700;color:#c0d4f0;margin-bottom:2px}
.sub{font-size:8.5px;color:#4a6a8a;line-height:1.3}
.arrow-v{text-align:center;color:#2a4a6a;font-size:11px;line-height:1;grid-column:2;padding:1px 0}
.arrow-lr{display:flex;align-items:center;justify-content:center;color:#2a4a6a;font-size:10px;padding:0 4px}
.info{margin-top:10px;background:#0d1525;border:1px solid #1e3050;border-radius:8px;padding:12px 14px;min-height:72px;font-size:11px;color:#7090b0;line-height:1.65;grid-column:1/4}
.info .ititle{font-weight:700;color:#c8d8f0;margin-bottom:5px;font-size:12px}
.badge{display:inline-block;font-size:8.5px;font-weight:700;padding:2px 7px;border-radius:20px;margin:2px}
.bo{background:#0a1830;color:#60a8f0;border:1px solid #1a3860}
.bg{background:#0a1e14;color:#50c880;border:1px solid #1a4828}
.br{background:#2a1800;color:#f0a040;border:1px solid #5a3000}
</style></head><body>
<div class="outer">
  <!-- CATALOGING & SEARCH top -->
  <div class="catalog-row" onclick="show('catalog')" style="grid-row:1">
    <div class="icon">📚</div>
    <div class="title">CATALOGING &amp; SEARCH</div>
    <div class="sub">Metadata · Lineage · Self-service discovery · Schema registry</div>
  </div>

  <!-- DATA SOURCES left -->
  <div class="sources">
    <div class="src-title">DATA SOURCES</div>
    <div class="src-box" onclick="show('streaming')"><div class="icon">🔴</div><div class="title">Streaming</div><div class="sub">Real-time events</div></div>
    <div class="src-box" onclick="show('batch')"><div class="icon">📦</div><div class="title">Batch</div><div class="sub">Scheduled loads</div></div>
    <div class="src-box" onclick="show('structured')"><div class="icon">📋</div><div class="title">Structured</div><div class="sub">Tables · schemas</div></div>
    <div class="src-box" onclick="show('unstructured')"><div class="icon">🖼️</div><div class="title">Unstructured</div><div class="sub">Text · images · logs</div></div>
  </div>

  <!-- INGESTION -->
  <div class="ingestion-row" onclick="show('ingestion')" style="grid-row:2">
    <div class="icon">⚡</div>
    <div class="title">INGESTION</div>
    <div class="sub">Unified entry point — streaming &amp; batch — replaces fragile cron-job scripts</div>
  </div>

  <!-- CONSUMPTION right -->
  <div class="consumption-col" onclick="show('consumption')">
    <div class="icon">📊</div>
    <div class="title" style="font-size:11px">CONSUMPTION</div>
    <div class="sub" style="margin-top:6px">BI · Dashboards</div>
    <div class="sub" style="margin-top:4px">ML · AI</div>
    <div class="sub" style="margin-top:4px">Partner APIs</div>
    <div class="sub" style="margin-top:4px">AI Agents</div>
  </div>

  <!-- PROCESSING row -->
  <div class="proc-row" style="grid-row:3">
    <div class="box" onclick="show('validate')">
      <div class="icon">✅</div>
      <div class="title">VALIDATE · CLEAN<br>STANDARDIZE · NORM</div>
      <div class="sub">Quality gate — nulls, ranges, dedup, schema</div>
    </div>
    <div class="arrow-lr">→</div>
    <div class="box" onclick="show('transform')">
      <div class="icon">⚙️</div>
      <div class="title">TRANSFORM<br>&amp; ENRICH</div>
      <div class="sub">Joins, KPI calc, context enrichment</div>
    </div>
  </div>

  <!-- STORAGE row -->
  <div class="storage-row" style="grid-row:4">
    <div class="box" onclick="show('raw')">
      <div class="icon">🗄️</div>
      <div class="title">Raw Zone</div>
      <div class="sub">Immutable landing · as-received</div>
    </div>
    <div class="arrow-lr">→</div>
    <div class="box" onclick="show('cleaned')">
      <div class="icon">✨</div>
      <div class="title">Cleaned Zone</div>
      <div class="sub">Validated · PII-masked</div>
    </div>
    <div class="arrow-lr">→</div>
    <div class="box" onclick="show('curated')">
      <div class="icon">🎯</div>
      <div class="title">Curated /<br>Consumption Zone</div>
      <div class="sub">Aggregated · BI &amp; ML ready</div>
    </div>
  </div>

  <!-- empty row for arrow -->
  <div style="grid-column:2;grid-row:5;text-align:center;color:#2a4a6a;font-size:11px;padding:2px 0">↑ feeds ↑</div>

  <!-- SECURITY & GOVERNANCE bottom -->
  <div class="sec-row" onclick="show('security')">
    <div class="icon">🔒</div>
    <div class="title" style="font-size:12px">SECURITY &amp; GOVERNANCE</div>
    <div class="sub">RBAC · Encryption (KMS + TLS in-transit) · GDPR · Audit Logs · PII masking · Threat detection — applied at every layer</div>
  </div>

  <!-- INFO PANEL -->
  <div class="info" id="ip">
    <div class="ititle">Select a component</div>
    Click any block above to see its architectural role, design rationale, and the RFP requirements it addresses.
  </div>
</div>
<script>
const D={
  'streaming':{t:'🔴 Streaming Sources',b:'High-frequency, continuous event data — POS transactions, web/mobile clicks, add-to-cart, customer reviews. These are the sources that demand sub-second processing. Manga\'s fundamental pain point is 24-hour lag; streaming sources feed real-time pipelines that eliminate that entirely.',tags:[['Real-time','r'],['R1: Multi-modal','r'],['POS · Web · App','b']]},
  'batch':{t:'📦 Batch Sources',b:'Scheduled, high-volume data loads — nightly inventory reconciliation, daily CRM sync, hourly ERP updates, logistics partner files. Not all data needs real-time; batch is simpler, cheaper, and more reliable for large historical datasets. Replacing fragile cron scripts with managed batch pipelines eliminates Manga\'s single point of failure.',tags:[['Scheduled loads','b'],['R3: Replaces cron ETL','r'],['R6: Cost efficient','g']]},
  'structured':{t:'📋 Structured Data',b:'Tabular, schema-defined records — sales transactions, inventory counts, customer profiles, shipping records. Stored as columnar Parquet for maximum query performance. Schema enforcement at ingest prevents data quality issues downstream. Maps directly to all six sample datasets.',tags:[['Parquet / columnar','b'],['R1: Multi-modal','r'],['R5: Schema enforcement','g']]},
  'unstructured':{t:'🖼️ Unstructured Data',b:'Free-text reviews, product images, clickstream logs — data with no fixed schema. Manga\'s current Excel layer completely ignores this data type. Including unstructured data unlocks sentiment analysis, visual search, and brand monitoring — use cases competitors already have. Maps to customer_reviews_sample.csv (text + images).',tags:[['Text · Images · Logs','b'],['R1: Multi-modal','r'],['Enables ML use cases','g']]},
  'ingestion':{t:'⚡ Ingestion Layer',b:'Single, unified entry point that receives data from all source types and routes it to the appropriate storage zone. Handles both streaming (sub-second) and batch (scheduled) patterns. Provides consistent retry logic, job bookmarks (no duplicate processing), failure alerting, and lineage tracking from one monitoring dashboard. Replaces Manga\'s 6+ siloed ETL scripts.',tags:[['R1: Unified platform','r'],['R3: Automation','g'],['R4: Reliability','b']]},
  'catalog':{t:'📚 Cataloging & Search',b:'Central metadata registry for every dataset: schema, owner, lineage, freshness, and tags. Bidirectionally connected to Processing — captures schema changes automatically and enforces governance in real time. Enables self-service discovery so analysts find and query any dataset without asking Engineering. Without this, Manga\'s analysts continue working with undocumented, untrustworthy data.',tags:[['R4: Governance','r'],['R5: Data Quality','g'],['R7: Self-service','b']]},
  'validate':{t:'✅ Validate / Clean / Standardize / Norm',b:'First processing stage — removes duplicates, enforces null constraints, validates value ranges, standardizes date/currency formats, normalizes units. Applied after raw ingestion, before any joins or aggregations. Acts as the quality gate. All failures trigger alerts before bad data propagates to downstream consumers or ML models.',tags:[['R5: Data Quality','r'],['R4: Data Integrity','b'],['Automated rules','g']]},
  'transform':{t:'⚙️ Transform & Enrich',b:'Second processing stage — joins datasets (sales ↔ customers ↔ products), calculates KPIs (revenue, margin, return rate), enriches records with external context (weather, campaigns, logistics). Raw sales data alone cannot power demand forecasting or dynamic pricing. Joining with external_factors_sample.csv is what makes predictions accurate. This is where Manga\'s competitive advantage is built.',tags:[['R1: Unified processing','r'],['R3: Automation','g'],['Joins · KPIs · Context','b']]},
  'raw':{t:'🗄️ Raw Zone (Bronze)',b:'Immutable, append-only storage of data exactly as received from source — original format, no modifications. Never changed after write. Enables full reprocessing if business logic changes or a bug is discovered. The ultimate system of record. Immutability also satisfies GDPR audit requirements. Stores structured (CSV/Parquet), semi-structured (JSON logs), and unstructured (images).',tags:[['Immutable','r'],['R1: Multi-format','b'],['Full reprocessing','g']]},
  'cleaned':{t:'✨ Cleaned Zone (Silver)',b:'Validated, deduplicated, schema-conformant data. PII from customers_sample.csv masked here before any non-production environment accesses it. Catalog entries created at this stage. Single source of truth — downstream teams can trust this data without running their own validation. Directly supports R2 (Dev/Pre-Prod never see real PII) and R4 (GDPR compliance).',tags:[['R2: PII masking','r'],['R4: GDPR','r'],['R5: Data Quality','g']]},
  'curated':{t:'🎯 Curated / Consumption Zone (Gold)',b:'Pre-aggregated, query-optimized datasets for BI and ML. Updated continuously by transformation pipelines. Columnar format for fast BI queries; ML feature vectors stored here for low-latency SageMaker serving. Replaces the daily Excel aggregation dumps entirely — business users get real-time dashboards instead of waiting 24 hours for a file.',tags:[['BI-ready','g'],['ML feature store','b'],['Replaces Excel','r']]},
  'consumption':{t:'📊 Consumption Layer',b:'Exposes curated data to all consumers: BI dashboards for business users, ML platform for data scientists, REST/GraphQL APIs for logistics partners and AI agents (explicitly required in RFP). Decoupled from storage — consumers do not interfere with each other. Self-service replaces the current "email Engineering for a report" workflow.',tags:[['R1: Unified access','r'],['R7: Interoperability','g'],['Replaces Excel reports','r']]},
  'security':{t:'🔒 Security & Governance (Cross-cutting)',b:'Applied at every layer — not bolted on at the end. Role-based access control (RBAC) at column and row level. Encryption at rest (KMS) and in transit (TLS 1.3). Note: we use TLS termination at service boundaries rather than E2EE, which allows the platform to process and analyze data while maintaining encryption between every service hop. PII detection and auto-masking, threat monitoring, immutable audit logs. Full GDPR compliance built in from day one. Addresses Laura\'s mandate and R4.',tags:[['R4: Security','r'],['GDPR','r'],['TLS in-transit','b'],['KMS at rest','b'],['RBAC','g']]},
};
function show(k){
  const d=D[k];if(!d)return;
  document.querySelectorAll('.box,.src-box,.ingestion-row,.catalog-row,.consumption-col,.sec-row').forEach(b=>b.classList.remove('active'));
  event.currentTarget.classList.add('active');
  const tags=(d.tags||[]).map(([l,t])=>`<span class="badge ${t==='r'?'br':t==='g'?'bg':'bo'}">${l}</span>`).join('');
  document.getElementById('ip').innerHTML=`<div class="ititle">${d.t}</div><p>${d.b}</p><div style="margin-top:8px">${tags}</div>`;
}
</script></body></html>"""
        st.components.v1.html(hla_html, height=720, scrolling=False)

    with tab_chart:
        st.markdown('<div class="page-sub">Hover over any node to see what it does and why we chose it.</div>', unsafe_allow_html=True)

        # Node definitions: (id, label, x, y, color, hover_html)
        hla_nodes = [
            ("streaming",   "🔴 Streaming\nSources",           0.0, 5.5, "#1e3a5f",
             "<b>Streaming Sources</b><br>Continuous high-frequency events — POS, web clicks, reviews.<br><b>Why:</b> Eliminates Manga's 24-hour lag. Enables real-time inventory alerts and live sales dashboards.<br><b>RFP:</b> R1, R3"),
            ("batch",       "📦 Batch\nSources",               0.0, 3.8, "#1e3a5f",
             "<b>Batch Sources</b><br>Scheduled loads — nightly ERP, daily CRM, hourly inventory.<br><b>Why:</b> Cheaper and simpler for large historical data. Replaces fragile cron scripts with managed, monitored pipelines.<br><b>RFP:</b> R3, R6"),
            ("structured",  "📋 Structured\nData",             0.0, 2.1, "#1e3a5f",
             "<b>Structured Data</b><br>Tabular, schema-defined records: sales, inventory, customers, shipping.<br><b>Why:</b> Enables columnar Parquet storage for fast BI queries. Schema enforcement prevents quality issues downstream.<br><b>RFP:</b> R1, R5"),
            ("unstructured","🖼️ Unstructured\nData",           0.0, 0.4, "#1e3a5f",
             "<b>Unstructured Data</b><br>Review text, product images, clickstream logs.<br><b>Why:</b> Manga's Excel layer ignores this entirely. Captures sentiment, visual search, brand monitoring — competitive use cases.<br><b>RFP:</b> R1, ML use cases"),
            ("ingestion",   "⚡ INGESTION",                    2.5, 3.0, "#0d2040",
             "<b>Ingestion Layer</b><br>Unified entry point for all source types. Streaming + batch, consistent retry logic, job bookmarks, failure alerting.<br><b>Why:</b> Replaces 6+ siloed cron scripts with one observable, reliable platform.<br><b>RFP:</b> R1, R3, R4"),
            ("catalog",     "📚 CATALOGING\n& SEARCH",         5.0, 6.5, "#1a1a3a",
             "<b>Cataloging & Search</b><br>Central metadata registry: schema, owner, lineage, freshness, tags. Bidirectional link to Processing.<br><b>Why:</b> Enables self-service discovery. Analysts find any dataset without emailing Engineering. Tracks schema changes automatically.<br><b>RFP:</b> R4, R5, R7"),
            ("validate",    "✅ VALIDATE\nCLEAN / NORM",        5.0, 4.5, "#0d2830",
             "<b>Validate / Clean / Standardize / Norm</b><br>Quality gate: null checks, range validation, deduplication, format standardization.<br><b>Why:</b> Prevents bad data from reaching Redshift or SageMaker. All failures alert before propagating downstream.<br><b>RFP:</b> R5, R4"),
            ("transform",   "⚙️ TRANSFORM\n& ENRICH",          5.0, 2.5, "#0d2830",
             "<b>Transform & Enrich</b><br>Joins datasets, calculates KPIs, enriches with external context (weather, campaigns, logistics).<br><b>Why:</b> Raw data alone can't power forecasting or dynamic pricing. Enrichment with external_factors is what makes ML predictions accurate.<br><b>RFP:</b> R1, R3"),
            ("raw",         "🗄️ Raw\nZone",                    3.5, 0.5, "#1a0d20",
             "<b>Raw Zone (Bronze)</b><br>Immutable append-only storage. Data exactly as received, never modified.<br><b>Why:</b> Full reprocessing if business logic changes. Satisfies GDPR audit trail. Stores Parquet, JSON, and binary images.<br><b>RFP:</b> R1, R4, R6"),
            ("cleaned",     "✨ Cleaned\nZone",                 5.0, 0.5, "#1a1020",
             "<b>Cleaned Zone (Silver)</b><br>Validated, deduplicated, PII-masked data. Catalog entries created here.<br><b>Why:</b> Single source of truth for downstream. Dev/Pre-Prod environments never see real PII — directly addresses R2 and GDPR.<br><b>RFP:</b> R2, R4, R5"),
            ("curated",     "🎯 Curated /\nConsumption Zone",  6.5, 0.5, "#0d1a10",
             "<b>Curated / Consumption Zone (Gold)</b><br>Pre-aggregated, query-optimised for BI and ML feature serving.<br><b>Why:</b> Replaces daily Excel dumps. Makes QuickSight dashboards sub-second. ML feature vectors serve SageMaker with low latency.<br><b>RFP:</b> R1, R6, replaces Excel"),
            ("consumption", "📊 CONSUMPTION",                  8.5, 3.0, "#0d2040",
             "<b>Consumption Layer</b><br>BI dashboards, ML platform, partner APIs, AI agents.<br><b>Why:</b> Decoupled from storage so BI, data science, and external partners don't interfere. Self-service replaces 'email Engineering for a report'.<br><b>RFP:</b> R1, R7"),
            ("security",    "🔒 SECURITY &\nGOVERNANCE",       4.0, -1.5, "#200a0a",
             "<b>Security & Governance (Cross-cutting)</b><br>RBAC, KMS encryption at rest, TLS 1.3 in-transit, PII masking, threat monitoring, GDPR audit logs.<br><b>Why TLS not E2EE:</b> TLS termination at service boundaries lets the platform process and analyse data while keeping all hops encrypted. E2EE would prevent any platform-side analytics.<br><b>RFP:</b> R4, GDPR, addresses Laura's mandate"),
        ]

        node_pos = {n[0]: (n[2], n[3]) for n in hla_nodes}

        hla_edges = [
            ("streaming","ingestion"), ("batch","ingestion"),
            ("structured","ingestion"), ("unstructured","ingestion"),
            ("ingestion","validate"), ("ingestion","raw"),
            ("validate","cleaned"), ("validate","transform"),
            ("transform","curated"), ("cleaned","curated"),
            ("raw","cleaned"), ("curated","consumption"),
            ("catalog","validate"), ("catalog","transform"),
        ]

        fig_hla = go.Figure()

        for src, dst in hla_edges:
            x0, y0 = node_pos[src]
            x1, y1 = node_pos[dst]
            fig_hla.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1], mode='lines',
                line=dict(color='#2a4a6a', width=1.5),
                hoverinfo='none', showlegend=False
            ))
            fig_hla.add_annotation(
                x=x1, y=y1, ax=x0, ay=y0,
                xref='x', yref='y', axref='x', ayref='y',
                arrowhead=3, arrowsize=1.2, arrowwidth=1.5,
                arrowcolor='#3a6a9a', showarrow=True, text=""
            )

        for nid, label, x, y, color, hover in hla_nodes:
            fig_hla.add_trace(go.Scatter(
                x=[x], y=[y], mode='markers+text',
                marker=dict(size=52, color=color, symbol='square',
                            line=dict(color='#4a7ac8', width=1.5)),
                text=[label], textposition='middle center',
                textfont=dict(color='#c8d8f0', size=8.5, family='Segoe UI'),
                hovertext=hover, hoverinfo='text',
                showlegend=False, name=label,
            ))

        fig_hla.update_layout(
            plot_bgcolor='#0a0e1a', paper_bgcolor='#0a0e1a',
            font=dict(color='#6a8aaa', family='Segoe UI'),
            xaxis=dict(visible=False, range=[-1, 10]),
            yaxis=dict(visible=False, range=[-3, 8]),
            height=560,
            margin=dict(l=10, r=10, t=30, b=10),
            hoverlabel=dict(
                bgcolor='#0d1525', bordercolor='#2a4a6a',
                font=dict(color='#c8d8f0', size=11, family='Segoe UI'),
                align='left',
            ),
            title=dict(text="High-Level Architecture — Hover any node for details",
                       font=dict(color='#4a7ac8', size=12), x=0.5),
        )
        st.plotly_chart(fig_hla, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOW-LEVEL ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "lla":
    st.markdown('<div class="page-title">Low-Level AWS Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Specific AWS services mapped to every Manga data source and use case (RFP Section 3)</div>', unsafe_allow_html=True)

    tab_diagram, tab_chart = st.tabs(["🗺️ Interactive Diagram", "📊 Plotly Architecture Chart"])

    with tab_diagram:
        st.info("💡 **Click any AWS service** for rationale, cost notes, and the specific RFP requirement (R1–R8) it addresses.")
        lla_html = """<!DOCTYPE html><html><head>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0e1a;font-family:'Segoe UI',sans-serif;color:#d0ddf0;padding:14px;font-size:11px}
.canvas{display:flex;flex-direction:column;gap:7px}
.lane{display:flex;align-items:stretch;gap:7px}
.ll{width:70px;min-width:70px;background:#111827;border:1px solid #1e2d45;border-radius:6px;display:flex;align-items:center;justify-content:center;padding:4px}
.ll span{writing-mode:vertical-rl;transform:rotate(180deg);font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3a5a7a}
.lb{flex:1;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.svc{background:#111827;border:1px solid #1e2d45;border-radius:7px;padding:8px 7px;cursor:pointer;transition:all .15s;display:flex;flex-direction:column;align-items:center;min-width:72px;flex:1}
.svc:hover,.svc.active{background:#182235;border-color:#4a80d0;transform:translateY(-2px);box-shadow:0 4px 14px rgba(74,128,208,.18)}
.si{font-size:17px;margin-bottom:3px}
.sn{font-size:8.5px;font-weight:700;color:#90b0d8;text-align:center;line-height:1.3}
.st{font-size:7px;color:#3a5a78;margin-top:2px;text-align:center}
.arr{color:#2a4060;font-size:11px;display:flex;align-items:center;padding:0 1px;flex-shrink:0}
.flow{font-size:8px;color:#253550;text-align:center;margin:1px 0}
.ib{margin-top:10px;background:#0d1525;border:1px solid #1e3050;border-radius:8px;padding:11px 14px;min-height:68px}
.ib .it{font-size:12px;font-weight:700;color:#c0d4f0;margin-bottom:5px}
.ib .id{font-size:10.5px;color:#6080a0;line-height:1.65}
.badge{display:inline-block;font-size:8px;font-weight:700;padding:2px 6px;border-radius:10px;margin:2px}
.bo{background:#0a1830;color:#60a8f0;border:1px solid #1a3860}
.bg{background:#0a1e14;color:#50c880;border:1px solid #1a4828}
.br{background:#2a1800;color:#f0a040;border:1px solid #5a3000}
</style></head><body>
<div class="canvas">
  <div class="lane">
    <div class="ll"><span>Sources</span></div>
    <div class="lb">
      <div class="svc" onclick="s('src-pos')"><div class="si">🏪</div><div class="sn">POS / ERP</div><div class="st">Sales · Inventory</div></div>
      <div class="arr">→</div>
      <div class="svc" onclick="s('src-web')"><div class="si">🌐</div><div class="sn">Web / App</div><div class="st">Events · Reviews</div></div>
      <div class="arr">→</div>
      <div class="svc" onclick="s('src-crm')"><div class="si">👥</div><div class="sn">CRM</div><div class="st">Customers · Loyalty</div></div>
      <div class="arr">→</div>
      <div class="svc" onclick="s('src-ext')"><div class="si">🌤️</div><div class="sn">External APIs</div><div class="st">Weather · Logistics</div></div>
      <div class="arr">→</div>
      <div class="svc" onclick="s('src-3p')"><div class="si">🏢</div><div class="sn">3rd-Party Data</div><div class="st">Market · Partner</div></div>
      <div class="arr">→</div>
      <div class="svc" onclick="s('src-files')"><div class="si">📁</div><div class="sn">SaaS / Files</div><div class="st">Uploads · SFTP</div></div>
    </div>
  </div>
  <div class="flow">↓ Kinesis Streams/Firehose &nbsp; ↓ Glue ETL &nbsp; ↓ Lambda &nbsp; ↓ DMS &nbsp; ↓ Data Exchange &nbsp; ↓ Transfer Family</div>
  <div class="lane">
    <div class="ll"><span>Ingestion</span></div>
    <div class="lb">
      <div class="svc" onclick="s('kinesis')"><div class="si">⚡</div><div class="sn">Kinesis Data Streams</div><div class="st">Real-time ingest</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('firehose')"><div class="si">🔥</div><div class="sn">Kinesis Firehose</div><div class="st">Stream → S3</div></div>
      <div class="arr">|</div>
      <div class="svc" onclick="s('glue-etl')"><div class="si">🔄</div><div class="sn">AWS Glue ETL</div><div class="st">Batch pipelines</div></div>
      <div class="arr">|</div>
      <div class="svc" onclick="s('lambda')"><div class="si">λ</div><div class="sn">AWS Lambda</div><div class="st">API connectors</div></div>
      <div class="arr">|</div>
      <div class="svc" onclick="s('dms')"><div class="si">🔃</div><div class="sn">AWS DMS</div><div class="st">DB migration</div></div>
      <div class="arr">|</div>
      <div class="svc" onclick="s('dataexchange')"><div class="si">📡</div><div class="sn">AWS Data Exchange</div><div class="st">3rd-party datasets</div></div>
      <div class="arr">|</div>
      <div class="svc" onclick="s('transfer')"><div class="si">📂</div><div class="sn">Transfer Family</div><div class="st">SFTP / FTPS</div></div>
    </div>
  </div>
  <div class="flow">↓ All paths → S3 Data Lakehouse → Validate/Clean (Glue) → Normalize/Transform (Glue) → Load</div>
  <div class="lane">
    <div class="ll"><span>Storage</span></div>
    <div class="lb">
      <div class="svc" onclick="s('s3-raw')"><div class="si">🪣</div><div class="sn">S3 Raw Zone</div><div class="st">Parquet · JSON · Binary</div></div>
      <div class="arr">→</div>
      <div class="svc" onclick="s('s3-cur')"><div class="si">✨</div><div class="sn">S3 Curated Zone</div><div class="st">Validated · PII masked</div></div>
      <div class="arr">→</div>
      <div class="svc" onclick="s('redshift')"><div class="si">🔴</div><div class="sn">Amazon Redshift</div><div class="st">DWH · Serving layer</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('dynamodb')"><div class="si">⚡</div><div class="sn">DynamoDB</div><div class="st">Low-latency lookups</div></div>
    </div>
  </div>
  <div class="flow">↓ Processing, Orchestration & Governance</div>
  <div class="lane">
    <div class="ll"><span>Processing</span></div>
    <div class="lb">
      <div class="svc" onclick="s('glue-cat')"><div class="si">📚</div><div class="sn">Glue Data Catalog</div><div class="st">Metadata · Lineage</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('mwaa')"><div class="si">🗂️</div><div class="sn">MWAA (Airflow)</div><div class="st">Orchestration</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('glue-dq')"><div class="si">✅</div><div class="sn">Glue Data Quality</div><div class="st">Validation · Alerts</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('lake-form')"><div class="si">🏛️</div><div class="sn">Lake Formation</div><div class="st">RBAC · GDPR · PII</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('macie')"><div class="si">🔍</div><div class="sn">Amazon Macie</div><div class="st">PII scanning</div></div>
    </div>
  </div>
  <div class="flow">↓ Consumption Layer</div>
  <div class="lane">
    <div class="ll"><span>Consumption</span></div>
    <div class="lb">
      <div class="svc" onclick="s('athena')"><div class="si">🔎</div><div class="sn">Amazon Athena</div><div class="st">Ad-hoc SQL on S3</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('quicksight')"><div class="si">📊</div><div class="sn">Amazon QuickSight</div><div class="st">BI · Dashboards</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('sagemaker')"><div class="si">🤖</div><div class="sn">Amazon SageMaker</div><div class="st">ML · Forecasting</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('comprehend')"><div class="si">💬</div><div class="sn">Comprehend</div><div class="st">Sentiment · NLP</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('apigw')"><div class="si">🔗</div><div class="sn">API Gateway</div><div class="st">External exposure</div></div>
    </div>
  </div>
  <div class="lane">
    <div class="ll"><span style="color:#6a5a9a">Security</span></div>
    <div class="lb">
      <div class="svc" onclick="s('vpc')"><div class="si">🌐</div><div class="sn">Amazon VPC</div><div class="st">Network isolation</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('iam')"><div class="si">🔐</div><div class="sn">IAM + KMS</div><div class="st">Auth · Encryption</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('terraform')"><div class="si">🏗️</div><div class="sn">Terraform / CDK</div><div class="st">IaC · 3 environments</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('cloudtrail')"><div class="si">📜</div><div class="sn">AWS CloudTrail</div><div class="st">Audit logs · GDPR</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('cloudwatch')"><div class="si">👁️</div><div class="sn">CloudWatch</div><div class="st">Monitoring · Alerts</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('orgs')"><div class="si">🏢</div><div class="sn">AWS Organizations</div><div class="st">Dev · PreProd · Prod</div></div>
      <div class="arr">+</div>
      <div class="svc" onclick="s('carbon')"><div class="si">🌱</div><div class="sn">Carbon Footprint</div><div class="st">Sustainability (R8)</div></div>
    </div>
  </div>
</div>
<div class="ib" id="ib">
  <div class="it">Click any service for details</div>
  <div class="id">Each AWS service addresses a specific Manga requirement. Click to see rationale, pricing model, and RFP coverage.</div>
</div>
<script>
const D={
  'src-pos':{t:'🏪 POS / ERP',b:'Generates sales_sample.csv and inventory_sample.csv. High-frequency structured data. Sales feed Kinesis for real-time processing; inventory syncs hourly via Glue batch jobs with job bookmarks to prevent duplicate records.',tags:[['Structured','b'],['R1','r']]},
  'src-web':{t:'🌐 Web & Mobile App',b:'customer_reviews_sample.csv plus clickstream events. Semi-structured (text, images). Highest velocity source — streamed via Kinesis Data Streams. Review text routed to Amazon Comprehend for automated NLP sentiment scoring.',tags:[['Real-time','r'],['Unstructured','b'],['R1','r']]},
  'src-crm':{t:'👥 CRM System',b:'customers_sample.csv — names, addresses, loyalty status. Contains PII. Synced via AWS DMS with CDC (change data capture). Lake Formation applies column-level masking before any Dev/Pre-Prod environment accesses this data.',tags:[['PII · GDPR','r'],['R4','r'],['Batch','b']]},
  'src-ext':{t:'🌤️ External APIs',b:'external_factors_sample.csv (weather, events, campaigns) and shipping_sample.csv from logistics partners. Lambda functions poll APIs on EventBridge schedules and land data directly in S3 Raw. New sources added as new functions — no impact on existing pipelines.',tags:[['Lambda pull','b'],['R7','g']]},
  'src-3p':{t:'🏢 Third-Party Data',b:'Market data, competitor signals, demographic enrichment datasets from commercial providers. AWS Data Exchange provides a managed marketplace for subscribing to and ingesting licensed third-party datasets directly into S3, with automatic license compliance tracking.',tags:[['AWS Data Exchange','b'],['R7: Extensibility','g']]},
  'src-files':{t:'📁 SaaS / File-based Sources',b:'Partners and legacy systems that deliver data via SFTP, FTPS, or FTP protocols. AWS Transfer Family provides a fully managed SFTP/FTPS endpoint that lands files directly into S3 without running any file-transfer infrastructure. Replaces legacy file-drop scripts.',tags:[['AWS Transfer Family','b'],['R3: Automation','g'],['R7','b']]},
  'kinesis':{t:'⚡ Amazon Kinesis Data Streams',b:'Managed real-time streaming. POS sales and web events flow through Kinesis at sub-second latency. Replaces daily cron jobs for these sources. Auto-scales to handle Fashion Week traffic spikes. Cost: pay per shard-hour + data retention.',tags:[['R1: Streaming','r'],['R3: Automation','g'],['Sub-second','b']]},
  'firehose':{t:'🔥 Kinesis Data Firehose',b:'Reads from Kinesis Streams and delivers micro-batches to S3 Raw Zone. Auto-converts to Parquet on the way — no servers to manage. Supports direct delivery to Redshift for hot data. Cost: pay per GB ingested.',tags:[['Serverless','g'],['Parquet conversion','b'],['S3 delivery','b']]},
  'glue-etl':{t:'🔄 AWS Glue ETL',b:'Managed Spark runtime replacing hand-coded ETL scripts. Built-in job bookmarks prevent reprocessing. Visual Studio for non-Spark engineers. Handles inventory batch loads, CRM syncs, historical data loads. Cost: pay per DPU-hour. Also runs the Validate/Clean and Normalize/Transform pipeline stages.',tags:[['Replaces cron ETL','r'],['R3: Automation','g'],['Managed Spark','b']]},
  'lambda':{t:'λ AWS Lambda',b:'Serverless API connector functions triggered by EventBridge schedules. Polls weather, holiday, and logistics APIs. New sources added as new Lambda functions — no impact on existing pipelines. Directly supports R7 Extensibility. Cost: pay per invocation (essentially free at this scale).',tags:[['R7: Extensibility','g'],['Serverless','g'],['EventBridge','b']]},
  'dms':{t:'🔃 AWS DMS',b:'Database Migration Service handles the one-time historical data migration from on-premises systems to S3. CDC (change data capture) replication during transition ensures zero data loss at cutover. Also keeps CRM in sync with ongoing replication.',tags:[['Migration','r'],['CDC replication','b'],['Zero data loss','g']]},
  'dataexchange':{t:'📡 AWS Data Exchange',b:'Managed marketplace for licensed third-party datasets — weather providers, market data vendors, demographic enrichment. Subscriptions deliver data directly to S3 with automatic license compliance. Eliminates manual download/upload workflows. Addresses R7 Interoperability for external data sources.',tags:[['R7: Extensibility','g'],['Licensed data','b'],['Managed','g']]},
  'transfer':{t:'📂 AWS Transfer Family',b:'Fully managed SFTP/FTPS/FTP service that provides a secure endpoint for partner file transfers, landing directly into S3. Logistics partners and legacy systems that cannot call APIs use this pathway. No file-transfer server infrastructure to manage. Complements Lambda connectors for non-API sources.',tags:[['SFTP/FTPS','b'],['R3: Automation','g'],['R7: Partners','b']]},
  's3-raw':{t:'🪣 S3 Raw Zone (Bronze)',b:'Immutable landing zone. Data stored exactly as received — source of truth enabling full reprocessing. Intelligent-Tiering auto-moves cold data to cheaper storage classes. Stores Parquet, JSON logs, and binary review images. Lifecycle policy: transition to Glacier after 90 days.',tags:[['R1: Multi-modal','r'],['R6: Cost tiering','g'],['Immutable','b']]},
  's3-cur':{t:'✨ S3 Curated Zone (Silver)',b:'Cleaned, deduplicated, schema-validated data. PII masked via Glue PII detection before Dev/Pre-Prod access. Catalog entries created here. Partitioned by date for query performance. Open Parquet format prevents lock-in — Athena, Redshift Spectrum, and SageMaker all read it natively.',tags:[['R2: PII masking','r'],['R5: Quality','g'],['Open format (no lock-in)','b']]},
  'redshift':{t:'🔴 Amazon Redshift (Gold / Serving)',b:'Columnar data warehouse. Pre-joined, aggregated datasets for QuickSight dashboards and ad-hoc queries. Redshift Spectrum queries S3 directly without loading — saves cost. RA3 nodes decouple compute/storage scaling. Replaces daily Excel aggregation entirely.',tags:[['Replaces Excel','r'],['R1: Unified DWH','b'],['Columnar','b']]},
  'dynamodb':{t:'⚡ Amazon DynamoDB',b:'NoSQL store for <10 ms lookups needed by ML inference endpoints and the future virtual shopping assistant. Stores real-time recommendation results and live inventory flags. Pay-per-request keeps costs proportional to actual usage.',tags:[['<10ms latency','r'],['R7: API exposure','b'],['ML serving','g']]},
  'glue-cat':{t:'📚 AWS Glue Data Catalog',b:'Central metadata store for all datasets. Integrates with Athena, Redshift Spectrum, and SageMaker natively. Enables self-service discovery — Alex\'s team finds any dataset without asking Engineering. Tracks schema evolution automatically. Acts as the "Cataloging & Search" layer from the HLA.',tags:[['Data lineage','b'],['Self-service','g'],['Schema registry','b']]},
  'mwaa':{t:'🗂️ Amazon MWAA (Managed Airflow)',b:'Fully managed Apache Airflow. Replaces all cron jobs with DAG-based pipelines with dependency management, retry logic, SLA alerts, and visual monitoring. Open-source Airflow core directly addresses Javier\'s vendor lock-in concern. Cost: instance-based, no per-task fees.',tags:[['R3: Orchestration','r'],['Open-source','g'],['No lock-in','g']]},
  'glue-dq':{t:'✅ AWS Glue Data Quality',b:'Automated rules after each pipeline: null checks on customer_id/product_id, price range validation, referential integrity (sales ↔ inventory ↔ customers), freshness thresholds. Failures trigger CloudWatch alerts before bad data reaches Redshift or SageMaker.',tags:[['R5: Data Quality','r'],['Automated','g'],['Real-time alerts','b']]},
  'lake-form':{t:'🏛️ AWS Lake Formation',b:'Fine-grained RBAC at column and row level. Laura (InfoSec) defines centrally who sees what. Junior analysts see masked customer data; data scientists get full access. Centralised GDPR compliance, data sharing agreements, and audit trails. Integrates with Glue Catalog for policy enforcement at query time.',tags:[['R4: Security','r'],['GDPR','r'],['Column RBAC','b']]},
  'macie':{t:'🔍 Amazon Macie',b:'ML-powered PII scanner. Continuously monitors S3 buckets for sensitive data from customers_sample.csv and sales_sample.csv. Findings sent to CloudWatch and Security Hub. Ensures PII never lands in the wrong zone or reaches unauthorised principals.',tags:[['R4: PII scanning','r'],['GDPR','r'],['Automated','g']]},
  'athena':{t:'🔎 Amazon Athena',b:'Serverless interactive SQL directly on S3. Analysts run ad-hoc queries on Raw or Curated zones without loading into Redshift — pay per query (TB scanned). Critical for data exploration, debugging pipelines, and one-off business questions. Reads from Glue Data Catalog automatically.',tags:[['Serverless SQL','g'],['Pay per query','g'],['R7: Self-service','b']]},
  'quicksight':{t:'📊 Amazon QuickSight',b:'Managed BI connected to Redshift and S3 via Athena. Replaces daily Excel reports with real-time interactive dashboards. SPICE in-memory engine for fast queries. Pay-per-session vs traditional BI per-seat licensing. ML-powered anomaly detection and forecasting built in.',tags:[['Replaces Excel','r'],['Self-service BI','g'],['R6: Cost','b']]},
  'sagemaker':{t:'🤖 Amazon SageMaker',b:'End-to-end ML platform. Use cases: (1) Product recommendations — collaborative filtering on sales+customers, (2) Demand forecasting — DeepAR on sales+external_factors, (3) Dynamic pricing — regression on inventory+competitive data, (4) Return prediction on shipping data. Feature Store integrates with the Curated Zone.',tags:[['Forecasting','b'],['Recommendations','b'],['Dynamic pricing','b']]},
  'comprehend':{t:'💬 Amazon Comprehend',b:'Managed NLP. Runs sentiment analysis on customer_reviews_sample.csv text automatically. Outputs positive/negative/neutral scores per review. Feeds QuickSight dashboards for the merchandising team. No ML expertise required — fully managed API.',tags:[['Sentiment NLP','b'],['Reviews data','b'],['Managed','g']]},
  'apigw':{t:'🔗 API Gateway + Lambda',b:'Secure REST/GraphQL APIs expose curated data to logistics partners, marketing platforms, and AI agents (explicitly required in RFP). Rate limiting, API keys, usage plans built in. Versioned endpoints ensure backward compatibility. Supports future data monetisation.',tags:[['R7: Interop','r'],['AI agents','b'],['Partners','b']]},
  'vpc':{t:'🌐 Amazon VPC',b:'Network isolation for all AWS services. Private subnets for Redshift, MWAA, SageMaker. VPC endpoints for S3 and DynamoDB — traffic never leaves the AWS backbone. Security groups enforce least-privilege network access. VPC Flow Logs feed CloudWatch for network-level threat detection.',tags:[['R4: Network isolation','r'],['Private subnets','b'],['VPC endpoints','g']]},
  'iam':{t:'🔐 IAM + AWS KMS',b:'IAM enforces least-privilege for all service-to-service and user access. KMS manages encryption keys for S3, Redshift, DynamoDB — encryption at rest. TLS 1.3 enforced in transit between all services. We use TLS termination (not E2EE) so the platform can process and analyse data while keeping all service hops encrypted.',tags:[['R4: Security','r'],['KMS at rest','b'],['TLS in-transit','b'],['Least privilege','g']]},
  'terraform':{t:'🏗️ Terraform / AWS CDK',b:'All infrastructure defined as code, Git version-controlled. One set of templates provisions identical Dev, Pre-Prod, and Prod environments. Peer review for infrastructure changes. Anonymised production data samples flow automatically to Dev/Pre-Prod via S3 cross-account replication.',tags:[['R2: Multi-env','r'],['R3: IaC','r'],['Git versioned','g']]},
  'cloudtrail':{t:'📜 AWS CloudTrail',b:'Immutable audit log of every API call across all AWS accounts — who accessed what data, when, and from where. Critical for GDPR compliance (Right of Access / Right to Erasure audit trails) and for forensic investigation of security incidents. Logs shipped to S3 and analysed by Athena. Directly addresses Laura\'s mandate.',tags:[['R4: Audit trail','r'],['GDPR','r'],['Immutable logs','b']]},
  'cloudwatch':{t:'👁️ Amazon CloudWatch',b:'Unified monitoring: pipeline latency, DQ failures, S3 growth, Redshift query performance, Lambda errors. SNS/PagerDuty alerts for on-call. Custom operational dashboards for the data engineering team. CloudWatch Logs Insights for ad-hoc log analysis.',tags:[['R4: High availability','r'],['Unified monitoring','g'],['Alerting','b']]},
  'orgs':{t:'🏢 AWS Organizations',b:'Three separate AWS accounts (Dev, Pre-Prod, Prod) under one Organisation. Service Control Policies enforce guardrails: Prod accounts are protected, cost limits enforced per account. Anonymised data samples flow from Prod to Dev via S3 cross-account replication with Lake Formation PII masking applied first.',tags:[['R2: Multi-environment','r'],['Governance','b'],['Cost guardrails','g']]},
  'carbon':{t:'🌱 AWS Customer Carbon Footprint Tool',b:'Native tool tracking carbon emissions per service and region. Year-over-year comparison vs on-premises colocation baseline. Manga quantifies sustainability improvement for R8 compliance and ESG board reporting. Selecting EU (Ireland) / EU (Frankfurt) regions maximises renewable energy mix.',tags:[['R8: Sustainability','r'],['Carbon metrics','g'],['ESG reporting','b']]},
};
function s(k){
  const r=D[k];if(!r)return;
  document.querySelectorAll('.svc').forEach(x=>x.classList.remove('active'));
  event.currentTarget.classList.add('active');
  const tags=(r.tags||[]).map(([l,t])=>`<span class="badge ${t==='r'?'br':t==='g'?'bg':'bo'}">${l}</span>`).join('');
  document.getElementById('ib').innerHTML=`<div class="it">${r.t}</div><div class="id">${r.b}</div><div style="margin-top:7px">${tags}</div>`;
}
</script></body></html>"""
        st.components.v1.html(lla_html, height=780, scrolling=False)

    with tab_chart:
        st.markdown('<div class="page-sub">Hover over any node to see what it does and why we chose it.</div>', unsafe_allow_html=True)

        lla_nodes = [
            # Sources row (y=6)
            ("pos",     "🏪 POS/ERP",          0.0, 6.0, "#1e3a5f", "<b>POS / ERP</b><br>Sales transactions & inventory from store systems.<br><b>Why:</b> Highest-value data source. Real-time POS feeds Kinesis; inventory batch syncs hourly via Glue.<br><b>Maps to:</b> sales_sample.csv, inventory_sample.csv"),
            ("web",     "🌐 Web/App",           1.5, 6.0, "#1e3a5f", "<b>Web & Mobile App</b><br>Clickstream events, reviews, sessions.<br><b>Why:</b> Enables personalisation and sentiment analysis. Streamed via Kinesis for sub-second capture.<br><b>Maps to:</b> customer_reviews_sample.csv"),
            ("crm",     "👥 CRM",              3.0, 6.0, "#1e3a5f", "<b>CRM System</b><br>Customer profiles, loyalty data (PII).<br><b>Why:</b> Feeds segmentation and recommendations. DMS CDC ensures continuous sync with zero data loss.<br><b>Maps to:</b> customers_sample.csv"),
            ("ext",     "🌤️ External\nAPIs",   4.5, 6.0, "#1e3a5f", "<b>External APIs</b><br>Weather, logistics, events — polled by Lambda on EventBridge schedules.<br><b>Why:</b> Demand forecasting accuracy requires external context. Lambda connectors are independent — one failure doesn't affect others.<br><b>Maps to:</b> external_factors_sample.csv, shipping_sample.csv"),
            ("3p",      "🏢 3rd Party\nData",  6.0, 6.0, "#1e3a5f", "<b>Third-Party Data (AWS Data Exchange)</b><br>Licensed market, demographic, and competitive datasets subscribed via AWS marketplace.<br><b>Why:</b> Eliminates manual download workflows. License compliance managed automatically. Supports R7 extensibility."),
            ("files",   "📁 SaaS/Files\n(SFTP)",7.5,6.0, "#1e3a5f", "<b>SaaS / File Sources (AWS Transfer Family)</b><br>Partners and legacy systems delivering data via SFTP/FTPS.<br><b>Why:</b> Not all partners can call APIs. Transfer Family provides a managed SFTP endpoint that lands files directly in S3 — no server to manage."),

            # Ingestion row (y=4.5)
            ("kinesis", "⚡ Kinesis\nStreams",  0.5, 4.5, "#0d2040", "<b>Amazon Kinesis Data Streams</b><br>Sub-second real-time ingestion for POS and web events.<br><b>Why:</b> Only streaming service that auto-scales to Fashion Week spikes and integrates natively with Firehose → S3.<br><b>Cost:</b> Pay per shard-hour.<br><b>RFP:</b> R1, R3"),
            ("firehose","🔥 Kinesis\nFirehose", 2.0, 4.5, "#0d2040", "<b>Kinesis Data Firehose</b><br>Micro-batches stream data to S3, auto-converting to Parquet.<br><b>Why:</b> Zero-server Parquet conversion reduces downstream query cost by 70%+ vs JSON. Also delivers directly to Redshift for hot data.<br><b>Cost:</b> Pay per GB.<br><b>RFP:</b> R1, R6"),
            ("glue_etl","🔄 AWS Glue\nETL",    3.5, 4.5, "#0d2040", "<b>AWS Glue ETL</b><br>Managed Spark replacing all cron-job scripts. Job bookmarks prevent duplicates.<br><b>Why:</b> Handles batch pipeline, Validate/Clean, and Normalize/Transform stages in one managed service. Visual Studio for non-Spark engineers.<br><b>Cost:</b> Pay per DPU-hour.<br><b>RFP:</b> R3, R5"),
            ("lam",     "λ Lambda\nConnectors", 5.0, 4.5, "#0d2040", "<b>AWS Lambda</b><br>Serverless functions polling external APIs on EventBridge schedules.<br><b>Why:</b> Each source is an independent function — adding a new data source means adding a new function with zero impact on existing pipelines. R7 extensibility by design.<br><b>RFP:</b> R3, R7"),
            ("dms",     "🔃 AWS DMS",           6.5, 4.5, "#0d2040", "<b>AWS Database Migration Service</b><br>One-time historical migration + ongoing CDC replication from on-premises DBs.<br><b>Why:</b> Zero-downtime cutover. CDC keeps source and target in sync during transition. Critical for migrating CRM without disrupting operations.<br><b>RFP:</b> R3"),

            # Storage row (y=3)
            ("s3raw",   "🪣 S3 Raw\nZone",      1.0, 3.0, "#1a0d20", "<b>S3 Raw Zone (Bronze)</b><br>Immutable landing zone — data exactly as received.<br><b>Why:</b> Full reprocessing possible if logic changes. Satisfies GDPR audit. S3 Intelligent-Tiering archives cold data automatically, cutting storage cost by 60%+.<br><b>RFP:</b> R1, R4, R6"),
            ("s3cur",   "✨ S3 Curated\nZone",  3.0, 3.0, "#1a1020", "<b>S3 Curated Zone (Silver)</b><br>Validated, PII-masked, partitioned Parquet. Single source of truth.<br><b>Why:</b> Open Parquet format means Athena, Redshift Spectrum, and SageMaker all read it natively — no lock-in. PII masking here ensures Dev/Pre-Prod never see real customer data.<br><b>RFP:</b> R2, R4, R5"),
            ("redshift","🔴 Redshift\nDWH",     5.0, 3.0, "#1a0010", "<b>Amazon Redshift</b><br>Columnar DWH for pre-aggregated serving layer. Replaces Excel dumps.<br><b>Why:</b> Columnar storage makes QuickSight dashboards sub-second on billions of rows. RA3 nodes decouple compute/storage — scale each independently. Spectrum queries S3 directly without loading.<br><b>RFP:</b> R1, R6"),
            ("dynamo",  "⚡ DynamoDB",          7.0, 3.0, "#0d1a0d", "<b>Amazon DynamoDB</b><br><10ms lookups for ML inference and real-time features.<br><b>Why:</b> Recommendation results and live inventory flags need millisecond response — impossible with Redshift. Pay-per-request keeps cost proportional to usage.<br><b>RFP:</b> R1, R7"),

            # Processing row (y=1.5)
            ("glue_cat","📚 Glue Data\nCatalog", 0.5, 1.5, "#1a1a3a", "<b>AWS Glue Data Catalog</b><br>Central metadata store — schema, lineage, ownership. Integrates with Athena, Redshift, SageMaker.<br><b>Why:</b> Self-service discovery — Alex's team finds any dataset without emailing Engineering. Schema evolution tracked automatically. This IS the 'Cataloging & Search' from the HLA.<br><b>RFP:</b> R4, R5, R7"),
            ("mwaa",    "🗂️ MWAA\nAirflow",     2.0, 1.5, "#1a1a3a", "<b>Amazon MWAA (Managed Airflow)</b><br>DAG-based orchestration replacing all cron jobs.<br><b>Why:</b> Open-source Airflow core directly addresses Javier's vendor lock-in concern. Dependency management, SLA monitoring, and visual pipeline health dashboard in one place.<br><b>Cost:</b> Instance-based.<br><b>RFP:</b> R3"),
            ("lakeform","🏛️ Lake\nFormation",   3.5, 1.5, "#1a1a3a", "<b>AWS Lake Formation</b><br>Fine-grained RBAC at column and row level. GDPR compliance hub.<br><b>Why:</b> Laura (InfoSec) defines all access policies centrally. Junior analysts see masked data; data scientists get full access. Audit trails for every data access — critical for GDPR Right of Access requests.<br><b>RFP:</b> R4, GDPR"),
            ("macie",   "🔍 Amazon\nMacie",     5.0, 1.5, "#1a1a3a", "<b>Amazon Macie</b><br>ML-powered PII scanner continuously monitoring S3.<br><b>Why:</b> Automated PII detection catches sensitive data that lands in the wrong zone before any human sees it. Findings route to CloudWatch and Security Hub. GDPR compliance automation.<br><b>RFP:</b> R4, GDPR"),

            # Consumption row (y=0)
            ("athena",  "🔎 Amazon\nAthena",    0.5, 0.0, "#0d1a30", "<b>Amazon Athena</b><br>Serverless SQL directly on S3 — no loading required.<br><b>Why:</b> Analysts run ad-hoc queries on Raw/Curated zones instantly. Pay per TB scanned — perfect for irregular exploration queries. Reads Glue Catalog automatically.<br><b>Cost:</b> ~$5/TB scanned.<br><b>RFP:</b> R7 self-service"),
            ("qs",      "📊 QuickSight\nBI",    2.0, 0.0, "#0d1a30", "<b>Amazon QuickSight</b><br>Managed BI replacing Excel reports.<br><b>Why:</b> Real-time dashboards connected to Redshift/S3. SPICE in-memory for sub-second queries. Pay-per-session vs per-seat licensing cuts BI costs 60%+ vs traditional tools. ML anomaly detection built in.<br><b>RFP:</b> R1, R6"),
            ("sage",    "🤖 SageMaker\nML",     3.5, 0.0, "#0d1a30", "<b>Amazon SageMaker</b><br>End-to-end ML lifecycle: feature engineering, training, deployment, monitoring.<br><b>Why:</b> Four priority use cases: (1) recommendations, (2) demand forecasting (DeepAR), (3) dynamic pricing, (4) return prediction. Feature Store integrates directly with the Curated Zone.<br><b>RFP:</b> R1, enables competitive ML"),
            ("comp",    "💬 Comprehend\nNLP",   5.0, 0.0, "#0d1a30", "<b>Amazon Comprehend</b><br>Managed NLP sentiment analysis on review text.<br><b>Why:</b> Zero ML expertise required — fully managed API call. Auto-scores every review in customer_reviews_sample.csv. Feeds merchandising dashboards in QuickSight.<br><b>RFP:</b> R1, ML use cases"),
            ("api",     "🔗 API\nGateway",      6.5, 0.0, "#0d1a30", "<b>API Gateway + Lambda</b><br>Secure REST/GraphQL APIs exposing curated data to partners and AI agents.<br><b>Why:</b> Explicitly required in RFP. Rate limiting, versioning, and API keys built in. Supports future data monetisation as a revenue stream.<br><b>RFP:</b> R7"),

            # Security bar (y=-1.5)
            ("iam_kms", "🔐 IAM+KMS\n+VPC",    1.5, -1.5, "#200a0a", "<b>IAM + KMS + VPC</b><br>Least-privilege access, KMS encryption at rest, VPC network isolation.<br><b>Why:</b> IAM roles for every service-to-service call. KMS keys rotated automatically. VPC keeps all services off the public internet. TLS 1.3 in-transit between all hops — TLS termination (not E2EE) so the platform can process and analyse data while keeping every hop encrypted.<br><b>RFP:</b> R4"),
            ("ctrail",  "📜 CloudTrail\n+CloudWatch", 4.0, -1.5, "#200a0a", "<b>AWS CloudTrail + CloudWatch</b><br>Immutable audit logs + unified operational monitoring.<br><b>Why:</b> CloudTrail records every API call for GDPR audit trail (Right of Access, Right to Erasure). CloudWatch monitors pipeline latency, DQ failures, and cost — SNS alerts for on-call. Critical for Laura's security mandate.<br><b>RFP:</b> R4, GDPR"),
            ("tf_orgs", "🏗️ Terraform\n+Organizations", 6.5, -1.5, "#200a0a", "<b>Terraform / CDK + AWS Organizations</b><br>IaC for three isolated environments (Dev/Pre-Prod/Prod).<br><b>Why:</b> One Terraform template provisions all three accounts identically. Addresses Javier's concern — infrastructure is code, peer-reviewed, version-controlled. Service Control Policies prevent accidental Prod changes from Dev accounts.<br><b>RFP:</b> R2, R3"),
        ]

        node_pos_lla = {n[0]: (n[2], n[3]) for n in lla_nodes}

        lla_edges = [
            ("pos","kinesis"),("pos","glue_etl"),
            ("web","kinesis"),("crm","dms"),
            ("ext","lam"),("3p","lam"),("files","lam"),
            ("kinesis","firehose"),("firehose","s3raw"),
            ("glue_etl","s3raw"),("lam","s3raw"),("dms","s3raw"),
            ("s3raw","s3cur"),("s3cur","redshift"),("s3cur","dynamo"),
            ("s3cur","sage"),("redshift","qs"),("redshift","athena"),
            ("dynamo","api"),("s3cur","comp"),("comp","qs"),
            ("glue_cat","s3cur"),("mwaa","glue_etl"),
            ("lakeform","s3cur"),("macie","s3raw"),
            ("sage","api"),("qs","api"),
        ]

        fig_lla = go.Figure()

        for src, dst in lla_edges:
            if src in node_pos_lla and dst in node_pos_lla:
                x0, y0 = node_pos_lla[src]
                x1, y1 = node_pos_lla[dst]
                fig_lla.add_trace(go.Scatter(
                    x=[x0, x1], y=[y0, y1], mode='lines',
                    line=dict(color='#1e3a5a', width=1.2),
                    hoverinfo='none', showlegend=False
                ))

        for nid, label, x, y, color, hover in lla_nodes:
            fig_lla.add_trace(go.Scatter(
                x=[x], y=[y], mode='markers+text',
                marker=dict(size=48, color=color, symbol='square',
                            line=dict(color='#3a6aaa', width=1.2)),
                text=[label], textposition='middle center',
                textfont=dict(color='#c8d8f0', size=7.5, family='Segoe UI'),
                hovertext=hover, hoverinfo='text',
                showlegend=False, name=label,
            ))

        fig_lla.update_layout(
            plot_bgcolor='#0a0e1a', paper_bgcolor='#0a0e1a',
            font=dict(color='#6a8aaa', family='Segoe UI'),
            xaxis=dict(visible=False, range=[-0.8, 9]),
            yaxis=dict(visible=False, range=[-3, 7.5]),
            height=600,
            margin=dict(l=10, r=10, t=30, b=10),
            hoverlabel=dict(
                bgcolor='#0d1525', bordercolor='#2a4a6a',
                font=dict(color='#c8d8f0', size=11, family='Segoe UI'),
                align='left',
            ),
            title=dict(text="Low-Level AWS Architecture — Hover any node for details",
                       font=dict(color='#4a7ac8', size=12), x=0.5),
        )
        st.plotly_chart(fig_lla, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DATA SOURCES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "data":
    st.markdown('<div class="page-title">Data Sources</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Manga\'s 6 sample datasets — schema, quality profile, and ingestion strategy (RFP Appendix III)</div>', unsafe_allow_html=True)

    meta = {
        "Sales": {
            "icon": "💳", "source": "POS System & E-commerce",
            "ingestion": "Kinesis → Firehose → S3", "pattern": "Streaming (real-time)",
            "pii": False, "use_cases": ["Revenue tracking", "Dynamic pricing", "Customer behaviour modelling"],
            "desc": "Transactional records: datetime, customer/product/store IDs, payment method, purchase price, and applied discount.",
        },
        "Customers": {
            "icon": "👥", "source": "CRM & Loyalty Program",
            "ingestion": "AWS DMS → Glue → S3", "pattern": "Batch (daily sync)",
            "pii": True, "use_cases": ["Segmentation", "Personalisation", "Lifecycle analysis"],
            "desc": "Demographic data: full name, age, gender, address, zip, loyalty status. Contains PII — column masking applied in Curated zone.",
        },
        "Inventory": {
            "icon": "📦", "source": "ERP / WMS",
            "ingestion": "Glue ETL → S3", "pattern": "Batch (hourly)",
            "pii": False, "use_cases": ["Supply chain optimisation", "Stock alerts", "Pricing strategy"],
            "desc": "Current stock levels per product per store, current price, and product description.",
        },
        "Customer Reviews": {
            "icon": "⭐", "source": "Website / Mobile App",
            "ingestion": "Kinesis → Firehose → S3 + Comprehend", "pattern": "Streaming (event-driven)",
            "pii": True, "use_cases": ["Sentiment analysis", "Product improvement", "Trust metrics"],
            "desc": "Review text, star rating, image binaries, customer and product IDs, timestamp.",
        },
        "External Factors": {
            "icon": "🌤️", "source": "Weather API + Internal",
            "ingestion": "Lambda → S3", "pattern": "Batch (daily pull)",
            "pii": False, "use_cases": ["Demand forecasting", "Campaign evaluation", "Pricing context"],
            "desc": "Daily context: weather, fuel price, bank holiday, local event, campaign ID, aggregated sales/volume.",
        },
        "Shipping": {
            "icon": "🚚", "source": "Logistics Partner API",
            "ingestion": "Lambda → Glue → S3", "pattern": "Batch (daily)",
            "pii": True, "use_cases": ["Delivery performance", "Return analysis", "Cost efficiency"],
            "desc": "Order ID, delivery address, estimated/actual delivery time, delivery price, actual cost, return status.",
        },
    }

    for ds_name, ds_meta in meta.items():
        df = DATA.get(ds_name)
        with st.expander(f"{ds_meta['icon']}  **{ds_name}**  —  {ds_meta['desc'][:70]}...", expanded=False):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:20px">{ds_meta["icon"]}</div><div class="metric-label">{ds_meta["source"]}</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:14px;padding-top:4px">{ds_meta["pattern"]}</div><div class="metric-label">Ingestion Pattern</div></div>', unsafe_allow_html=True)
            pii_color = "#f07070" if ds_meta['pii'] else "#50c880"
            pii_text = "⚠️ Contains PII" if ds_meta['pii'] else "✅ No PII"
            c3.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:14px;color:{pii_color};padding-top:4px">{pii_text}</div><div class="metric-label">Data Sensitivity</div></div>', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:11px;color:#6a8aaa;margin:8px 0 4px'><b>AWS Path:</b> <code>{ds_meta['ingestion']}</code></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:11px;color:#8090a8;margin-bottom:10px'>{ds_meta['desc']}</div>", unsafe_allow_html=True)
            uc_badges = "".join([f'<span class="badge badge-blue">{uc}</span>' for uc in ds_meta['use_cases']])
            st.markdown(f"<div style='margin-bottom:12px'>{uc_badges}</div>", unsafe_allow_html=True)
            if df is not None:
                st.dataframe(df.head(10), use_container_width=True, hide_index=True)
                st.markdown(f"<div style='font-size:10px;color:#3a5a7a;margin-top:4px'>Showing 10 of {len(df)} rows · {len(df.columns)} columns</div>", unsafe_allow_html=True)
            else:
                st.warning(f"Sample CSV not found for {ds_name}. Place `{meta[ds_name]['ingestion'].split('→')[0].strip().lower().replace(' ','_')}_sample.csv` in the same folder as the app.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REQUIREMENTS COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "reqs":
    st.markdown('<div class="page-title">Requirements Coverage</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">How each of the 8 RFP requirements (R1–R8) is addressed by the proposed AWS architecture</div>', unsafe_allow_html=True)

    requirements = [
        ("R1","Unified Multi-modal Data Platform",
         "High-throughput streaming (Kinesis) + batch (Glue) pipelines. S3 Data Lakehouse stores structured (Parquet), semi-structured (JSON), and unstructured (images) data. Single Glue Catalog provides unified access. Athena enables serverless SQL directly on S3.",
         ["Kinesis Streams","Kinesis Firehose","AWS Glue ETL","S3 Lakehouse","Amazon Redshift","Amazon Athena"],"✅ Fully Covered","green"),
        ("R2","Multi-Environment Setup",
         "AWS Organizations provisions Dev / Pre-Prod / Prod from identical Terraform templates. Anonymised production samples (via Glue PII masking + Lake Formation RBAC) automatically replicated to non-prod. Dev engineers never see real PII.",
         ["AWS Organizations","Terraform/CDK","Lake Formation (PII masking)","S3 Cross-Account Replication"],"✅ Fully Covered","green"),
        ("R3","Automation",
         "IaC via Terraform/CDK. MWAA (Managed Airflow) replaces all cron jobs with DAG-based orchestration. Glue job bookmarks, auto-scaling, EventBridge schedules, and S3 lifecycle policies automate the full data lifecycle.",
         ["Terraform / AWS CDK","Amazon MWAA (Airflow)","AWS Glue (job bookmarks)","EventBridge schedules"],"✅ Fully Covered","green"),
        ("R4","Security & High Availability",
         "IAM least-privilege + KMS encryption at rest. TLS 1.3 enforced in transit between all services (TLS termination at service boundaries — allows platform-side analytics while keeping every hop encrypted, unlike E2EE). Lake Formation column/row RBAC. Macie PII scanning. CloudTrail immutable audit logs for GDPR. VPC network isolation. Multi-AZ deployments. Target: 99.9% uptime.",
         ["IAM + AWS KMS (at rest)","TLS 1.3 in-transit","AWS Lake Formation","Amazon Macie","AWS CloudTrail (GDPR audit)","Amazon VPC","Multi-AZ deployments"],"✅ Fully Covered","green"),
        ("R5","Data Quality",
         "AWS Glue Data Quality rules run after each pipeline: null constraints, range validation, referential integrity (sales ↔ inventory ↔ customers), freshness thresholds. Failures trigger CloudWatch/SNS alerts before bad data reaches downstream consumers.",
         ["AWS Glue Data Quality","CloudWatch Alerts","Glue Data Catalog (schema)","SNS Notifications"],"✅ Fully Covered","green"),
        ("R6","Cost Optimisation",
         "Pay-per-use vs fixed colocation. S3 Intelligent-Tiering auto-archives cold data. Spot Instances for non-critical Glue jobs. Redshift Reserved Instances. QuickSight pay-per-session. Athena pay-per-query. Projected 40–60% infrastructure cost reduction.",
         ["S3 Intelligent-Tiering","Spot Instances (Glue)","Redshift Reserved Instances","QuickSight pay-per-session","Athena pay-per-query"],"✅ Fully Covered","green"),
        ("R7","Extensibility & Interoperability",
         "Decoupled Lambda connectors add new sources without touching existing pipelines. AWS Data Exchange for licensed third-party data. Transfer Family for SFTP partners. API Gateway exposes curated data to partners and AI agents. Open Parquet format prevents lock-in.",
         ["API Gateway + Lambda","AWS Data Exchange","AWS Transfer Family","Open Parquet / Delta","Glue Catalog (schema registry)"],"✅ Fully Covered","green"),
        ("R8","Sustainability",
         "AWS data centres operate with high renewable energy. EU (Ireland) / EU (Frankfurt) regions maximise green energy mix. AWS Customer Carbon Footprint Tool provides quantitative emissions dashboard vs on-premises colocation baseline for ESG board reporting.",
         ["AWS Carbon Footprint Tool","Green regions (EU-WEST-1)","Serverless (Lambda, Firehose, Athena)","Auto-scaling (no idle resources)"],"✅ Fully Covered","green"),
    ]

    for req_id, title, desc, services, status, color in requirements:
        bg = {"green":"#0a2010","orange":"#2a1a00","red":"#200a0a"}[color]
        bd = {"green":"#1a6030","orange":"#6a4000","red":"#602020"}[color]
        tx = {"green":"#50d090","orange":"#f0a040","red":"#f07070"}[color]
        st.markdown(f"""
        <div class="card" style="background:{bg};border-left:4px solid {bd};border-color:{bd};margin-bottom:10px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
            <div>
              <span style="font-size:13px;font-weight:800;color:{tx}">{req_id}</span>
              <span style="font-size:13px;font-weight:700;color:#c0d4f0;margin-left:8px">{title}</span>
            </div>
            <span style="font-size:10px;font-weight:700;color:{tx};background:{bg};border:1px solid {bd};padding:3px 9px;border-radius:20px">{status}</span>
          </div>
          <p style="font-size:11.5px;color:#8090a8;line-height:1.65;margin-bottom:10px">{desc}</p>
          <div>{"".join([f'<span class="badge badge-blue">{s}</span>' for s in services])}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Coverage Summary</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=[r[0] for r in requirements], y=[100]*8,
        marker_color="#1a6030", marker_line_color="#50d090", marker_line_width=1.5,
        text=["100%"]*8, textposition="inside",
        textfont=dict(color="#50d090", size=11, family="Segoe UI"),
    ))
    fig.update_layout(
        plot_bgcolor="#0d1525", paper_bgcolor="#0a0e1a",
        font=dict(color="#6a8aaa", family="Segoe UI"),
        xaxis=dict(gridcolor="#1e2d45", title="Requirement"),
        yaxis=dict(gridcolor="#1e2d45", title="Coverage %", range=[0,120]),
        height=260, margin=dict(l=40,r=20,t=20,b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: USE CASES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "usecases":
    st.markdown('<div class="page-title">Sample Use Cases</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Five end-to-end use cases showing the architecture in action with Manga\'s actual data sources (RFP Section 5)</div>', unsafe_allow_html=True)

    use_cases = [
        {"id":"UC1","icon":"🤖","title":"Product Recommendation Engine",
         "datasets":["Sales","Customers","Inventory"],
         "aws":["SageMaker (collaborative filtering)","DynamoDB (serving)","API Gateway","Kinesis (real-time signals)"],
         "desc":"Collaborative filtering model trained on purchase history and customer profiles. Real-time inference via SageMaker endpoint, results cached in DynamoDB for <10ms response. Exposed via API Gateway to the e-commerce front-end and virtual shopping assistant.",
         "impact":"Projected +12–18% AOV based on retail industry benchmarks.",
         "pipeline":"sales_sample.csv + customers_sample.csv → S3 Curated → SageMaker training → DynamoDB → API Gateway → Website"},
        {"id":"UC2","icon":"📈","title":"Demand Forecasting",
         "datasets":["Sales","External Factors","Inventory"],
         "aws":["SageMaker DeepAR","AWS Glue (feature engineering)","QuickSight (dashboard)","MWAA (weekly retrain DAG)"],
         "desc":"Time-series forecasting using SageMaker DeepAR on sales history enriched with external context — weather, bank holidays, local events, fuel prices. Model retrains weekly via MWAA DAG. Forecasts feed inventory replenishment decisions.",
         "impact":"Reduces stockouts ~30% and overstock write-offs ~20%.",
         "pipeline":"sales_sample.csv + external_factors_sample.csv → Glue feature engineering → SageMaker DeepAR → QuickSight"},
        {"id":"UC3","icon":"💬","title":"Sentiment-Driven Merchandising",
         "datasets":["Customer Reviews"],
         "aws":["Amazon Comprehend (NLP)","AWS Glue (aggregation)","Amazon QuickSight","SNS (alerts on score drops)"],
         "desc":"Amazon Comprehend processes review text in near real-time, assigning sentiment scores per review. Glue aggregates scores by product, store, and week. QuickSight surfaces products with declining sentiment, alerting the buying team before damage compounds.",
         "impact":"Enables proactive product decisions 2–3 weeks earlier than manual review cycles.",
         "pipeline":"customer_reviews_sample.csv → Kinesis → Comprehend → S3 Curated → Glue aggregation → QuickSight + SNS alerts"},
        {"id":"UC4","icon":"💰","title":"Dynamic Pricing Engine",
         "datasets":["Sales","Inventory","External Factors"],
         "aws":["SageMaker (regression model)","Kinesis (real-time inventory)","Lambda (pricing API)","DynamoDB (price store)"],
         "desc":"ML model trained on price elasticity, current inventory levels, competitor signals, and contextual factors. Lambda function compares model output against pricing guardrails before writing to DynamoDB, which feeds POS and e-commerce pricing layer.",
         "impact":"Potential 3–7% gross margin improvement from optimised clearance and peak pricing.",
         "pipeline":"sales + inventory + external_factors → SageMaker → Lambda (guardrails) → DynamoDB → POS / E-commerce"},
        {"id":"UC5","icon":"🚚","title":"Return Rate & Logistics Optimisation",
         "datasets":["Shipping","Sales","Customers"],
         "aws":["SageMaker (classification)","Glue (join pipeline)","QuickSight (ops dashboard)","SNS (high-return alerts)"],
         "desc":"Binary classification predicts return likelihood at purchase time using delivery history, customer return-rate profile, and product attributes. High-risk orders trigger proactive interventions. Logistics cost variance tracked in QuickSight.",
         "impact":"10–15% reduction in return processing costs. Better delivery partner SLA management.",
         "pipeline":"shipping_sample.csv + sales + customers → Glue join → SageMaker classifier → SNS alerts + QuickSight ops dashboard"},
    ]

    for uc in use_cases:
        with st.expander(f"**{uc['id']}** {uc['icon']} {uc['title']}", expanded=False):
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"""
                <div style="font-size:12px;color:#90a8c0;line-height:1.7;margin-bottom:12px">{uc['desc']}</div>
                <div style="background:#0d1525;border:1px solid #1e3050;border-radius:7px;padding:10px 12px;font-size:10.5px;color:#4a9af0;font-family:monospace;line-height:1.8">
                  🔀 <strong style="color:#6a8aaa">Pipeline:</strong><br>{uc['pipeline']}
                </div>
                <div style="margin-top:10px;padding:8px 12px;background:#0a1e14;border:1px solid #1a4828;border-radius:6px;font-size:11px;color:#50d090">
                  📊 <strong>Business Impact:</strong> {uc['impact']}
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="section-title">Data Sources Used</div>', unsafe_allow_html=True)
                for ds in uc['datasets']:
                    st.markdown(f'<span class="badge badge-blue">📁 {ds}</span>', unsafe_allow_html=True)
                st.markdown('<div class="section-title" style="margin-top:14px">AWS Services</div>', unsafe_allow_html=True)
                for svc in uc['aws']:
                    st.markdown(f'<span class="badge badge-green" style="display:block;margin:3px 0;text-align:left">⚙️ {svc}</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Dataset Usage Matrix</div>', unsafe_allow_html=True)
    matrix_data = {
        "Use Case":         ["Recommendations","Demand Forecast","Sentiment","Dynamic Pricing","Return Optimisation"],
        "Sales":            [1,1,0,1,1],
        "Customers":        [1,0,0,0,1],
        "Inventory":        [1,1,0,1,0],
        "Customer Reviews": [0,0,1,0,0],
        "External Factors": [0,1,0,1,0],
        "Shipping":         [0,0,0,0,1],
    }
    hm_df = pd.DataFrame(matrix_data).set_index("Use Case")
    fig2 = px.imshow(hm_df, color_continuous_scale=[[0,"#0d1525"],[1,"#1a6040"]], aspect="auto")
    fig2.update_traces(
        text=hm_df.map(lambda v: "✓" if v else ""),
        texttemplate="%{text}", textfont=dict(size=16, color="#50d090"),
    )
    fig2.update_layout(
        plot_bgcolor="#0d1525", paper_bgcolor="#0a0e1a",
        font=dict(color="#6a8aaa", family="Segoe UI"),
        coloraxis_showscale=False, height=260,
        margin=dict(l=160,r=20,t=20,b=60), xaxis=dict(side="bottom"),
    )
    st.plotly_chart(fig2, use_container_width=True)
