import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import os

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mango Retail · AWS Cloud Data Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Base ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0e1a !important;
    color: #d0ddf0;
}
[data-testid="stSidebar"] {
    background-color: #0d1220 !important;
    border-right: 1px solid #1e2d45;
}
[data-testid="stSidebar"] * { color: #a0b8d8 !important; }

/* ---- Hide default header ---- */
header[data-testid="stHeader"] { display: none; }

/* ---- Cards ---- */
.card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 12px;
    transition: border-color .2s;
}
.card:hover { border-color: #3a6ab0; }

.metric-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.metric-value { font-size: 28px; font-weight: 800; color: #4a9af0; }
.metric-label { font-size: 11px; color: #6a8aaa; text-transform: uppercase;
                letter-spacing: .08em; margin-top: 4px; }

/* ---- Section headers ---- */
.section-title {
    font-size: 11px; font-weight: 700; letter-spacing: .12em;
    text-transform: uppercase; color: #4a6a9a;
    margin-bottom: 14px; padding-bottom: 6px;
    border-bottom: 1px solid #1e2d45;
}
.page-title {
    font-size: 22px; font-weight: 800; color: #c8d8f0;
    margin-bottom: 4px;
}
.page-sub {
    font-size: 13px; color: #6a8aaa; margin-bottom: 20px;
}

/* ---- Badges ---- */
.badge {
    display: inline-block; font-size: 10px; font-weight: 700;
    padding: 3px 9px; border-radius: 20px; margin: 2px;
}
.badge-blue  { background:#0a1830; color:#60a8f0; border:1px solid #1a3860; }
.badge-green { background:#0a1e14; color:#50c880; border:1px solid #1a4828; }
.badge-orange{ background:#2a1800; color:#f0a040; border:1px solid #5a3000; }
.badge-purple{ background:#1a0a28; color:#b070f0; border:1px solid #3a1858; }
.badge-red   { background:#1e0a0a; color:#f07070; border:1px solid #5a2020; }

/* ---- Req pills ---- */
.req-pill {
    display: inline-block; font-size: 10px; font-weight: 700;
    padding: 4px 10px; border-radius: 6px; margin: 3px;
    background: #0d1525; border: 1px solid #2a4060; color: #7090c0;
}
.req-pill.covered { background:#0a1e14; border-color:#2a6040; color:#50d090; }

/* ---- Stakeholder cards ---- */
.stk-card {
    background: #111827; border: 1px solid #1e2d45;
    border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
}
.stk-name { font-size: 13px; font-weight: 700; color: #c0d4f0; }
.stk-role { font-size: 10px; color: #4a6a9a; text-transform: uppercase;
            letter-spacing: .08em; margin-bottom: 8px; }
.stk-concern { font-size: 11px; color: #8090a8; line-height: 1.5; }
.stk-tag { font-size: 9px; font-weight: 700; padding: 2px 7px;
           border-radius: 4px; display: inline-block; margin-top: 6px; }
.stk-skeptic { background:#2a1800; color:#f0a040; }
.stk-champion { background:#0a1e14; color:#50c880; }
.stk-neutral { background:#0a1830; color:#60a8f0; }

/* ---- Tabs ---- */
[data-testid="stTabs"] button {
    font-size: 12px !important; font-weight: 600 !important;
    color: #6a8aaa !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #4a9af0 !important;
    border-bottom: 2px solid #4a9af0 !important;
}

/* ---- Dataframe ---- */
[data-testid="stDataFrame"] { border: 1px solid #1e2d45; border-radius: 8px; }

/* ---- Divider ---- */
hr { border-color: #1e2d45 !important; }

/* ---- Sidebar nav ---- */
.nav-item {
    padding: 9px 12px; border-radius: 8px; margin-bottom: 4px;
    cursor: pointer; font-size: 13px; font-weight: 600;
    transition: background .15s;
}
.nav-item:hover { background: #1a2840; }
.nav-active { background: #1a2840 !important; color: #4a9af0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Data Loader ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = Path(__file__).parent
    datasets = {}
    files = {
        "Sales":            "sales_sample.csv",
        "Customers":        "customers_sample.csv",
        "Inventory":        "inventory_sample.csv",
        "Customer Reviews": "customer_reviews_sample.csv",
        "External Factors": "external_factors_sample.csv",
        "Shipping":         "shipping_sample.csv",
    }
    for name, fname in files.items():
        path = base / fname
        if path.exists():
            datasets[name] = pd.read_csv(path)
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
        "🏠  Overview":                  "overview",
        "📐  High-Level Architecture":   "hla",
        "⚙️  Low-Level Architecture":    "lla",
        "🗄️  Data Sources":              "data",
        "✅  Requirements Coverage":     "reqs",
        "💡  Use Cases":                 "usecases",
    }

    if "page" not in st.session_state:
        st.session_state.page = "overview"

    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    for label, key in pages.items():
        active = "nav-active" if st.session_state.page == key else ""
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

    # ── KPI Row
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        ("€280M", "Annual Revenue"),
        ("+3.5%", "Growth (vs market avg)"),
        ("100+", "Physical Stores"),
        ("2×", "Cost vs Competitors"),
    ]
    for col, (val, lbl) in zip([c1, c2, c3, c4], kpis):
        col.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{val}</div>
          <div class="metric-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        <p style="font-size:13px; color:#a0b8c8; line-height:1.8; margin:0">
        Manga's current architecture — a collection of independent ETL pipelines triggered by cron jobs,
        aggregating into daily Excel files — is fundamentally incompatible with the real-time, AI-driven
        experiences modern retail demands. <br><br>
        Our proposal delivers a <strong style="color:#c8d8f0">cloud-native AWS data lakehouse</strong> on three pillars:
        <strong style="color:#4a9af0">Unify</strong> all data sources into a single governed platform,
        <strong style="color:#50c880">Accelerate</strong> time-to-insight from 24 hours to sub-second,
        and <strong style="color:#f0a040">Enable</strong> ML-powered features — recommendations, dynamic
        pricing, demand forecasting — that are simply impossible today.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:16px">Problem: As-Is Architecture</div>', unsafe_allow_html=True)
        problems = [
            ("⏰", "Daily batch cron jobs", "No real-time capability. Managers wait 24h for yesterday's sales data."),
            ("🗂️", "Siloed ETL pipelines", "Each pipeline built by a different team with its own stack. No shared standards."),
            ("📊", "Excel as the BI layer", "Manual aggregation into Excel files. No self-service. No drill-down."),
            ("💸", "2× competitor cost", "Colocation model costs twice as much while delivering half the analytical output."),
            ("🔒", "Security gaps", "Previous InfoSec Manager dismissed after a major incident. GDPR compliance unclear."),
        ]
        for icon, title, desc in problems:
            st.markdown(f"""
            <div class="card" style="padding:12px 16px; margin-bottom:8px; border-left:3px solid #5a2020">
              <span style="font-size:16px">{icon}</span>
              <strong style="color:#f07070; font-size:12px; margin-left:8px">{title}</strong>
              <p style="font-size:11px; color:#7a8a9a; margin:4px 0 0 28px">{desc}</p>
            </div>""", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">Key Stakeholders</div>', unsafe_allow_html=True)
        stakeholders = [
            ("Marta Ríos", "COO · 25 yrs", "Wants end-to-end solution with solid business case. Results over ideology.", "champion", "✅ Champion"),
            ("Javier Medina", "CTO · 15 yrs", "Fears vendor lock-in. Champions open-source & modular systems. Skeptical of cloud.", "skeptic", "⚠️ Skeptic"),
            ("Manuel Ortega", "CFO · 25 yrs", "Signed the colocation deal. Now alarmed by 2× cost vs competitors. Open to change if ROI is clear.", "neutral", "💰 Cost-focused"),
            ("Laura Smith", "InfoSec Manager", "New hire with GDPR mandate. Security is non-negotiable after the prior incident.", "skeptic", "🔐 Security-first"),
            ("Alex Lee", "Head of Data & AI", "Joined from competitor. Knows the current arch is broken. Wants modern DataOps.", "champion", "🚀 Champion"),
        ]
        for name, role, concern, stype, tag in stakeholders:
            st.markdown(f"""
            <div class="stk-card">
              <div class="stk-name">{name} <span class="stk-tag stk-{stype}">{tag}</span></div>
              <div class="stk-role">{role}</div>
              <div class="stk-concern">{concern}</div>
            </div>""", unsafe_allow_html=True)

    # ── Solution highlights
    st.markdown("---")
    st.markdown('<div class="section-title">Our Solution — Core Value Drivers</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    drivers = [
        ("⚡", "#4a9af0", "Real-Time Everything",
         "Replace all daily-batch pipelines with Kinesis streaming. POS sales, web events, and inventory updates processed in under 1 second."),
        ("🏗️", "#50c880", "Open & Modular",
         "Apache Airflow (MWAA), open Parquet/Delta formats, Terraform IaC. No proprietary lock-in — addressing the CTO's core concern directly."),
        ("🔒", "#f0a040", "Security by Design",
         "Lake Formation RBAC, Macie PII scanning, KMS encryption, full GDPR audit trails — built in from day one, not bolted on."),
        ("🤖", "#b070f0", "ML-Ready Platform",
         "SageMaker connected to a curated feature store. Product recommendations, demand forecasting, and dynamic pricing from day one."),
        ("💸", "#50c880", "Measurable Cost Savings",
         "Pay-per-use vs fixed colocation. S3 Intelligent-Tiering, Spot Instances, reserved capacity — projected 40–60% infra cost reduction."),
        ("🌱", "#4a9af0", "Sustainability Metrics",
         "AWS Carbon Footprint Tool tracks emissions by service/region. Quantifiable improvement vs the colocation model for R8 compliance."),
    ]
    for i, (icon, color, title, desc) in enumerate(drivers):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card" style="border-top:3px solid {color}">
              <div style="font-size:22px; margin-bottom:8px">{icon}</div>
              <div style="font-size:13px; font-weight:700; color:#c0d4f0; margin-bottom:6px">{title}</div>
              <div style="font-size:11px; color:#7090a8; line-height:1.6">{desc}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HIGH-LEVEL ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "hla":
    st.markdown('<div class="page-title">High-Level Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Conceptual, cloud-agnostic design — architectural principles without vendor specifics (RFP Section 2)</div>', unsafe_allow_html=True)

    st.info("💡 **Click any component** in the diagram to see its role, design rationale, and which RFP requirements it addresses.")

    hla_html = """
<!DOCTYPE html><html><head>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0e1a;font-family:'Segoe UI',sans-serif;color:#e0e6f0;padding:16px}
.diagram{display:flex;flex-direction:column;gap:10px}
.row{display:flex;gap:10px;align-items:stretch}
.layer-label{writing-mode:vertical-rl;text-orientation:mixed;transform:rotate(180deg);font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3a5a7a;min-width:22px;display:flex;align-items:center;justify-content:center}
.boxes{display:flex;gap:8px;flex:1}
.box{flex:1;background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:10px 8px;text-align:center;cursor:pointer;transition:all .18s ease}
.box:hover{background:#182235;border-color:#4a7ac8;transform:translateY(-2px);box-shadow:0 4px 16px rgba(74,122,200,.18)}
.box.active{background:#182235;border-color:#4a7ac8;box-shadow:0 0 0 2px rgba(74,122,200,.25)}
.box-icon{font-size:20px;margin-bottom:5px}
.box-title{font-size:10.5px;font-weight:700;color:#c8d8f0;margin-bottom:3px}
.box-sub{font-size:9px;color:#4a6a8a;line-height:1.4}
.arrow-row{display:flex;align-items:center;justify-content:center;height:16px;color:#2a4a6a;font-size:12px}
.sources-row .box{background:#0d1320;border-color:#1a2840}
.info-panel{margin-top:12px;background:#0d1525;border:1px solid #1e3050;border-radius:8px;padding:12px 14px;min-height:70px;font-size:11px;color:#7090b0;line-height:1.6;transition:all .2s}
.info-panel .info-title{font-weight:700;color:#c8d8f0;margin-bottom:5px;font-size:12px}
.badge{display:inline-block;font-size:8.5px;font-weight:700;padding:2px 7px;border-radius:20px;margin:2px}
.b-blue{background:#0a1830;color:#60a8f0;border:1px solid #1a3860}
.b-green{background:#0a1e14;color:#50c880;border:1px solid #1a4828}
.b-orange{background:#2a1800;color:#f0a040;border:1px solid #5a3000}
.cross{display:flex;gap:8px;margin-top:2px}
.cross-pill{flex:1;background:#111020;border:1px dashed #2a2a4a;border-radius:6px;padding:7px 10px;text-align:center;cursor:pointer;transition:all .15s}
.cross-pill:hover{border-color:#4a4a8a}
.cross-pill.active{border-color:#6a6ab0;background:#161030}
.cp-title{font-size:10px;font-weight:700;color:#7a70b0}
.cp-sub{font-size:8.5px;color:#4a4a7a;margin-top:2px}
</style></head><body>
<div class="diagram">
  <div class="row sources-row">
    <div class="layer-label">Sources</div>
    <div class="boxes">
      <div class="box" onclick="show('src-pos')"><div class="box-icon">🏪</div><div class="box-title">POS & ERP</div><div class="box-sub">Sales · Inventory · Ops</div></div>
      <div class="box" onclick="show('src-web')"><div class="box-icon">🌐</div><div class="box-title">Web & App</div><div class="box-sub">Events · Reviews · Sessions</div></div>
      <div class="box" onclick="show('src-crm')"><div class="box-icon">👥</div><div class="box-title">CRM</div><div class="box-sub">Customers · Loyalty</div></div>
      <div class="box" onclick="show('src-ext')"><div class="box-icon">🌤️</div><div class="box-title">External APIs</div><div class="box-sub">Weather · Logistics · Events</div></div>
    </div>
  </div>
  <div class="arrow-row">↓ Batch &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↓ Streaming</div>
  <div class="row">
    <div class="layer-label">Ingestion</div>
    <div class="boxes">
      <div class="box" onclick="show('ing-batch')" style="flex:2"><div class="box-icon">📦</div><div class="box-title">Batch Ingestion</div><div class="box-sub">Replaces cron-job ETL pipelines</div></div>
      <div class="box" onclick="show('ing-stream')" style="flex:2"><div class="box-icon">⚡</div><div class="box-title">Stream Ingestion</div><div class="box-sub">Real-time event & transaction feeds</div></div>
      <div class="box" onclick="show('ing-api')"><div class="box-icon">🔌</div><div class="box-title">API Connectors</div><div class="box-sub">Serverless third-party pulls</div></div>
    </div>
  </div>
  <div class="arrow-row">↓ All paths → Object Storage</div>
  <div class="row">
    <div class="layer-label">Storage</div>
    <div class="boxes">
      <div class="box" onclick="show('sto-raw')"><div class="box-icon">🗄️</div><div class="box-title">Raw Zone</div><div class="box-sub">Immutable landing · multi-format</div></div>
      <div class="box" onclick="show('sto-cur')"><div class="box-icon">✨</div><div class="box-title">Curated Zone</div><div class="box-sub">Validated · PII-masked · catalogued</div></div>
      <div class="box" onclick="show('sto-serv')"><div class="box-icon">🎯</div><div class="box-title">Serving Zone</div><div class="box-sub">Aggregated for BI & ML</div></div>
    </div>
  </div>
  <div class="arrow-row">↓</div>
  <div class="row">
    <div class="layer-label">Processing</div>
    <div class="boxes">
      <div class="box" onclick="show('proc-trans')"><div class="box-icon">⚙️</div><div class="box-title">Transformation</div><div class="box-sub">Cleansing · joins · enrichment</div></div>
      <div class="box" onclick="show('proc-orch')"><div class="box-icon">🗂️</div><div class="box-title">Orchestration</div><div class="box-sub">DAG-based workflow engine</div></div>
      <div class="box" onclick="show('proc-qual')"><div class="box-icon">✅</div><div class="box-title">Data Quality</div><div class="box-sub">Automated checks · alerts</div></div>
      <div class="box" onclick="show('proc-gov')"><div class="box-icon">📚</div><div class="box-title">Governance</div><div class="box-sub">Catalog · lineage · RBAC</div></div>
    </div>
  </div>
  <div class="arrow-row">↓</div>
  <div class="row">
    <div class="layer-label">Consumption</div>
    <div class="boxes">
      <div class="box" onclick="show('con-bi')"><div class="box-icon">📊</div><div class="box-title">BI & Reporting</div><div class="box-sub">Replaces Excel reports</div></div>
      <div class="box" onclick="show('con-ml')"><div class="box-icon">🤖</div><div class="box-title">ML & AI</div><div class="box-sub">Forecasting · recommendations</div></div>
      <div class="box" onclick="show('con-api')"><div class="box-icon">🔗</div><div class="box-title">External APIs</div><div class="box-sub">Partners · AI agents</div></div>
    </div>
  </div>
  <div class="cross">
    <div class="cross-pill" onclick="show('sec')"><div class="cp-title">🔒 Security & Compliance</div><div class="cp-sub">RBAC · Encryption · GDPR</div></div>
    <div class="cross-pill" onclick="show('iac')"><div class="cp-title">🏗️ IaC & Automation</div><div class="cp-sub">Dev · Pre-Prod · Prod</div></div>
    <div class="cross-pill" onclick="show('cost')"><div class="cp-title">💰 Cost & Sustainability</div><div class="cp-sub">Auto-scaling · Carbon metrics</div></div>
  </div>
</div>
<div class="info-panel" id="ip"><div class="info-title">Select a component</div>Click any block to see its architectural role and the RFP requirements it addresses.</div>
<script>
const info={
  'src-pos':{t:'🏪 POS & ERP Systems',b:'High-frequency structured data — sales transactions, inventory levels, store operations. Dual-path ingestion: real-time for sales (streaming) and scheduled batch for inventory reconciliation.',tags:[['Structured','blue'],['R1: Multi-modal','orange']]},
  'src-web':{t:'🌐 Web & Mobile Applications',b:'Continuous event streams — clicks, add-to-cart, purchases, reviews (text + images). Semi-structured and unstructured. Highest velocity source. Critical for personalisation and recommendation use cases.',tags:[['R1: Streaming','orange'],['Unstructured (images)','blue'],['Real-time','orange']]},
  'src-crm':{t:'👥 CRM & Loyalty Programs',b:'Customer demographics, purchase history, loyalty status. Contains PII requiring strict GDPR governance. Synced in batch. Column-level masking applied before any non-production environment accesses this data.',tags:[['PII · GDPR','orange'],['R4: Security','orange'],['Batch sync','blue']]},
  'src-ext':{t:'🌤️ External Data Sources',b:'Weather conditions, fuel prices, bank holidays, local events, logistics partner delivery data. Pulled via serverless API connectors on schedule. Key input for demand forecasting and campaign analytics.',tags:[['Third-party APIs','blue'],['R7: Interoperability','blue']]},
  'ing-batch':{t:'📦 Batch Ingestion Layer',b:'Replaces the fragile cron-job ETL scripts with managed, monitored pipelines. Built-in retry logic, job bookmarks (no duplicate processing), alerting on failure, and full lineage tracking. Handles large historical loads and hourly/daily syncs.',tags:[['Replaces cron ETL','orange'],['R3: Automation','green'],['Managed','green']]},
  'ing-stream':{t:'⚡ Stream Ingestion Layer',b:'Enables sub-second data ingestion for POS transactions and web events. Foundational for use cases that are impossible with daily batches: real-time inventory alerts, live sales dashboards, instant fraud detection.',tags:[['Sub-second latency','orange'],['R1: Streaming','orange'],['Enables real-time','green']]},
  'ing-api':{t:'🔌 API Connector Layer',b:'Decoupled serverless functions handle third-party API polling. New sources can be added as new connectors without touching existing pipelines — directly enabling R7 (Extensibility). Failure of one connector does not affect others.',tags:[['R7: Extensibility','green'],['Serverless','green'],['Decoupled','blue']]},
  'sto-raw':{t:'🗄️ Raw Zone (Bronze Layer)',b:'Immutable, append-only storage of source data exactly as received. The system of record that enables full reprocessing if business logic changes. Stores structured, semi-structured (JSON logs), and unstructured (review images) data side-by-side.',tags:[['Immutable','orange'],['R1: Multi-format','blue'],['Full reprocessing','green']]},
  'sto-cur':{t:'✨ Curated Zone (Silver Layer)',b:'Cleaned, deduplicated, schema-validated data. PII masked here for Dev/Pre-Prod. Data catalog entries created at this stage. Single source of truth consumed by all downstream. Partitioned by date for performance.',tags:[['R2: PII masking','orange'],['R5: Data Quality','green'],['Source of truth','blue']]},
  'sto-serv':{t:'🎯 Serving Zone (Gold Layer)',b:'Pre-aggregated, query-optimised datasets. Updated continuously by transformation pipelines. Optimised for BI queries (columnar format) and ML feature serving (low-latency key-value access). Replaces the daily Excel dumps entirely.',tags:[['BI-ready','green'],['ML feature store','blue'],['Replaces Excel','orange']]},
  'proc-trans':{t:'⚙️ Transformation Engine',b:'Distributed processing framework applying business logic: joining sales with customer profiles, calculating KPIs, enriching records with weather/event context. Handles batch and micro-batch streaming. Scales horizontally for peak loads.',tags:[['Distributed Spark','blue'],['Batch + streaming','blue'],['R1: Scalable','green']]},
  'proc-orch':{t:'🗂️ Workflow Orchestration',b:'DAG-based pipeline engine with dependency management, retry logic, SLA monitoring, and a visual UI. Replaces all cron jobs. Engineers can see every pipeline\'s health in one dashboard. Open-source core addresses vendor lock-in concerns.',tags:[['R3: Orchestration','orange'],['Open-source','green'],['No lock-in','green']]},
  'proc-qual':{t:'✅ Data Quality Framework',b:'Automated validation rules after each pipeline: null checks, range validation, referential integrity, freshness. Failures trigger alerts before bad data reaches downstream. Quality scores tracked over time. Addresses R5 directly.',tags:[['R5: Data Quality','orange'],['Automated','green'],['Real-time alerts','blue']]},
  'proc-gov':{t:'📚 Data Governance Layer',b:'Central metadata catalog with schema registry, data lineage, and ownership tracking. RBAC policies defined centrally. Self-service discovery for analysts — find any dataset without asking engineering. GDPR audit trails.',tags:[['Data lineage','blue'],['Self-service','green'],['GDPR audit','orange']]},
  'con-bi':{t:'📊 BI & Reporting Layer',b:'Interactive dashboards replace manual Excel files. Real-time data access vs 24-hour lag. Self-service — business users explore data without engineering support. Drill-through from summary KPIs to transaction level.',tags:[['Replaces Excel','orange'],['Self-service','green'],['Real-time','blue']]},
  'con-ml':{t:'🤖 ML & AI Platform',b:'Managed ML lifecycle: feature engineering from the curated layer, model training/evaluation, deployment, and monitoring. Use cases: product recommendations, demand forecasting, dynamic pricing, sentiment analysis, return prediction.',tags:[['Forecasting','blue'],['Recommendations','blue'],['Dynamic pricing','blue']]},
  'con-api':{t:'🔗 External API Exposure',b:'Secure, rate-limited APIs expose curated datasets to partners, logistics providers, and AI agents (explicitly listed in the RFP). Enables data monetisation as a future revenue stream. Backwards compatibility guaranteed via versioned API contracts.',tags:[['R7: Interoperability','orange'],['AI agent ready','blue'],['Data monetisation','green']]},
  'sec':{t:'🔒 Security & Compliance (Cross-cutting)',b:'Applied at every layer: encryption at rest and in transit, RBAC at column and row level, PII detection and auto-masking, threat detection, immutable audit logs. GDPR compliance built-in from day one. Directly addresses Laura\'s mandate and R4.',tags:[['R4: Security','orange'],['GDPR','orange'],['Encryption','blue'],['RBAC','blue']]},
  'iac':{t:'🏗️ IaC & Multi-Environment (Cross-cutting)',b:'All infrastructure defined as code, version-controlled in Git. One set of templates provisions identical Dev, Pre-Prod, and Prod environments. Peer review for infra changes. Anonymised production data samples flow automatically to Dev/Pre-Prod. Addresses R2 and R3.',tags:[['R2: Multi-env','orange'],['R3: IaC','orange'],['Git versioned','green']]},
  'cost':{t:'💰 Cost & Sustainability (Cross-cutting)',b:'Auto-scaling matches resource allocation to demand — no idle servers paying for nothing. Data lifecycle policies archive cold data automatically. Carbon emissions tracked by region. Demonstrates quantifiable sustainability improvement vs colocation. R6 and R8.',tags:[['R6: Cost optimisation','orange'],['R8: Sustainability','orange'],['Auto-scaling','green']]},
};
function show(k){
  const d=info[k];if(!d)return;
  document.querySelectorAll('.box,.cross-pill').forEach(b=>b.classList.remove('active'));
  event.currentTarget.classList.add('active');
  const tags=(d.tags||[]).map(([l,t])=>{
    const cls=t==='orange'?'b-orange':t==='green'?'b-green':'b-blue';
    return`<span class="badge ${cls}">${l}</span>`;
  }).join('');
  document.getElementById('ip').innerHTML=`<div class="info-title">${d.t}</div><p>${d.b}</p><div style="margin-top:8px">${tags}</div>`;
}
</script></body></html>
"""
    st.components.v1.html(hla_html, height=760, scrolling=False)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOW-LEVEL ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "lla":
    st.markdown('<div class="page-title">Low-Level AWS Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Specific AWS services mapped to every Manga data source and use case (RFP Section 3)</div>', unsafe_allow_html=True)

    st.info("💡 **Click any AWS service** for rationale, cost notes, and the specific RFP requirement (R1–R8) it addresses.")

    lla_html = """
<!DOCTYPE html><html><head>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0e1a;font-family:'Segoe UI',sans-serif;color:#d0ddf0;padding:14px;font-size:11px}
.title{text-align:center;font-size:11px;font-weight:700;color:#4a6a9a;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}
.canvas{display:flex;flex-direction:column;gap:7px}
.lane{display:flex;align-items:stretch;gap:7px}
.lane-label{width:64px;min-width:64px;background:#111827;border:1px solid #1e2d45;border-radius:6px;display:flex;align-items:center;justify-content:center;padding:4px}
.lane-label span{writing-mode:vertical-rl;transform:rotate(180deg);font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3a5a7a}
.lane-body{flex:1;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.svc{background:#111827;border:1px solid #1e2d45;border-radius:7px;padding:8px 7px;cursor:pointer;transition:all .15s;display:flex;flex-direction:column;align-items:center;min-width:76px;flex:1}
.svc:hover{background:#182235;border-color:#4a80d0;transform:translateY(-2px);box-shadow:0 4px 14px rgba(74,128,208,.18)}
.svc.active{background:#182235;border-color:#4a80d0;box-shadow:0 0 0 2px rgba(74,128,208,.28)}
.svc-icon{font-size:18px;margin-bottom:3px}
.svc-name{font-size:9px;font-weight:700;color:#90b0d8;text-align:center;line-height:1.3}
.svc-tag{font-size:7.5px;color:#3a5a78;margin-top:2px;text-align:center}
.arrow{color:#2a4060;font-size:11px;display:flex;align-items:center;padding:0 1px;flex-shrink:0}
.flow{font-size:8.5px;color:#253550;text-align:center;margin:1px 0}
.info-box{margin-top:10px;background:#0d1525;border:1px solid #1e3050;border-radius:8px;padding:11px 14px;min-height:68px}
.info-box .ititle{font-size:12px;font-weight:700;color:#c0d4f0;margin-bottom:5px}
.info-box .ibody{font-size:10.5px;color:#6080a0;line-height:1.65}
.badge{display:inline-block;font-size:8px;font-weight:700;padding:2px 6px;border-radius:10px;margin:2px}
.b-orange{background:#2a1800;color:#f0a040;border:1px solid #5a3000}
.b-blue{background:#0a1830;color:#60a8f0;border:1px solid #1a3860}
.b-green{background:#0a1e14;color:#50c880;border:1px solid #1a4828}
.b-purple{background:#1a0a28;color:#b070f0;border:1px solid #3a1858}
</style></head><body>
<div class="canvas">
  <div class="lane">
    <div class="lane-label"><span>Sources</span></div>
    <div class="lane-body">
      <div class="svc" onclick="show('src-pos')"><div class="svc-icon">🏪</div><div class="svc-name">POS / ERP</div><div class="svc-tag">Sales · Inventory</div></div>
      <div class="arrow">→</div>
      <div class="svc" onclick="show('src-web')"><div class="svc-icon">🌐</div><div class="svc-name">Web / App</div><div class="svc-tag">Events · Reviews</div></div>
      <div class="arrow">→</div>
      <div class="svc" onclick="show('src-crm')"><div class="svc-icon">👥</div><div class="svc-name">CRM</div><div class="svc-tag">Customers · Loyalty</div></div>
      <div class="arrow">→</div>
      <div class="svc" onclick="show('src-ext')"><div class="svc-icon">🌤️</div><div class="svc-name">External APIs</div><div class="svc-tag">Weather · Logistics</div></div>
    </div>
  </div>
  <div class="flow">↓ Kinesis Streams &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↓ AWS Glue ETL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↓ Lambda scheduler</div>
  <div class="lane">
    <div class="lane-label"><span>Ingestion</span></div>
    <div class="lane-body">
      <div class="svc" onclick="show('kinesis')"><div class="svc-icon">⚡</div><div class="svc-name">Kinesis Data Streams</div><div class="svc-tag">Real-time ingest</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('firehose')"><div class="svc-icon">🔥</div><div class="svc-name">Kinesis Firehose</div><div class="svc-tag">Stream → S3</div></div>
      <div class="arrow">|</div>
      <div class="svc" onclick="show('glue-etl')"><div class="svc-icon">🔄</div><div class="svc-name">AWS Glue ETL</div><div class="svc-tag">Batch pipelines</div></div>
      <div class="arrow">|</div>
      <div class="svc" onclick="show('lambda')"><div class="svc-icon">λ</div><div class="svc-name">AWS Lambda</div><div class="svc-tag">API connectors</div></div>
      <div class="arrow">|</div>
      <div class="svc" onclick="show('dms')"><div class="svc-icon">🔃</div><div class="svc-name">AWS DMS</div><div class="svc-tag">DB migration</div></div>
    </div>
  </div>
  <div class="flow">↓ All paths land in S3 Data Lakehouse</div>
  <div class="lane">
    <div class="lane-label"><span>Storage</span></div>
    <div class="lane-body">
      <div class="svc" onclick="show('s3-raw')"><div class="svc-icon">🪣</div><div class="svc-name">S3 Raw Zone</div><div class="svc-tag">Parquet · JSON · Binary</div></div>
      <div class="arrow">→</div>
      <div class="svc" onclick="show('s3-cur')"><div class="svc-icon">✨</div><div class="svc-name">S3 Curated Zone</div><div class="svc-tag">Validated · PII masked</div></div>
      <div class="arrow">→</div>
      <div class="svc" onclick="show('redshift')"><div class="svc-icon">🔴</div><div class="svc-name">Amazon Redshift</div><div class="svc-tag">DWH · Serving layer</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('dynamodb')"><div class="svc-icon">⚡</div><div class="svc-name">DynamoDB</div><div class="svc-tag">Low-latency lookups</div></div>
    </div>
  </div>
  <div class="flow">↓ Processing & Governance</div>
  <div class="lane">
    <div class="lane-label"><span>Processing</span></div>
    <div class="lane-body">
      <div class="svc" onclick="show('glue-cat')"><div class="svc-icon">📚</div><div class="svc-name">Glue Data Catalog</div><div class="svc-tag">Metadata · Lineage</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('mwaa')"><div class="svc-icon">🗂️</div><div class="svc-name">MWAA (Airflow)</div><div class="svc-tag">Orchestration</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('glue-dq')"><div class="svc-icon">✅</div><div class="svc-name">Glue Data Quality</div><div class="svc-tag">Validation · Alerts</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('lake-form')"><div class="svc-icon">🏛️</div><div class="svc-name">Lake Formation</div><div class="svc-tag">RBAC · GDPR · PII</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('macie')"><div class="svc-icon">🔍</div><div class="svc-name">Amazon Macie</div><div class="svc-tag">PII scanning</div></div>
    </div>
  </div>
  <div class="flow">↓ Consumption Layer</div>
  <div class="lane">
    <div class="lane-label"><span>Consumption</span></div>
    <div class="lane-body">
      <div class="svc" onclick="show('quicksight')"><div class="svc-icon">📊</div><div class="svc-name">Amazon QuickSight</div><div class="svc-tag">BI · Dashboards</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('sagemaker')"><div class="svc-icon">🤖</div><div class="svc-name">Amazon SageMaker</div><div class="svc-tag">ML · Forecasting</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('comprehend')"><div class="svc-icon">💬</div><div class="svc-name">Comprehend</div><div class="svc-tag">Sentiment · NLP</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('apigw')"><div class="svc-icon">🔗</div><div class="svc-name">API Gateway</div><div class="svc-tag">External exposure</div></div>
    </div>
  </div>
  <div class="lane">
    <div class="lane-label"><span style="color:#6a5a9a">Cross-cut</span></div>
    <div class="lane-body">
      <div class="svc" onclick="show('iam')"><div class="svc-icon">🔐</div><div class="svc-name">IAM + KMS</div><div class="svc-tag">Auth · Encryption</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('terraform')"><div class="svc-icon">🏗️</div><div class="svc-name">Terraform / CDK</div><div class="svc-tag">IaC · 3 environments</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('cloudwatch')"><div class="svc-icon">👁️</div><div class="svc-name">CloudWatch</div><div class="svc-tag">Monitoring · Alerts</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('orgs')"><div class="svc-icon">🏢</div><div class="svc-name">AWS Organizations</div><div class="svc-tag">Dev · PreProd · Prod</div></div>
      <div class="arrow">+</div>
      <div class="svc" onclick="show('carbon')"><div class="svc-icon">🌱</div><div class="svc-name">Carbon Footprint</div><div class="svc-tag">Sustainability (R8)</div></div>
    </div>
  </div>
</div>
<div class="info-box" id="ib">
  <div class="ititle">Click any service for details</div>
  <div class="ibody">Each AWS service is selected to address a specific Manga requirement. Click to see the rationale, pricing model, and the RFP requirement it covers.</div>
</div>
<script>
const d={
  'src-pos':{t:'🏪 POS / ERP',b:'Generates sales_sample.csv and inventory_sample.csv. High-frequency structured data. Sales feed Kinesis for real-time processing; inventory syncs hourly via Glue batch jobs.',tags:[['Structured','blue'],['R1','orange']]},
  'src-web':{t:'🌐 Web & Mobile App',b:'customer_reviews_sample.csv plus clickstream events. Semi-structured (text, images). Highest velocity source — streamed via Kinesis Data Streams. Review text routed to Comprehend for automated NLP.',tags:[['Real-time','orange'],['Unstructured','blue'],['R1','orange']]},
  'src-crm':{t:'👥 CRM System',b:'customers_sample.csv — names, addresses, loyalty status. Contains PII. Synced via AWS DMS. Lake Formation applies column masking before Dev/Pre-Prod access.',tags:[['PII · GDPR','orange'],['R4','orange'],['Batch','blue']]},
  'src-ext':{t:'🌤️ External APIs',b:'external_factors_sample.csv (weather, events, campaigns) and shipping_sample.csv from logistics partners. Lambda functions poll APIs on schedule via EventBridge and land data directly in S3 Raw.',tags:[['Lambda pull','blue'],['R7','green']]},
  'kinesis':{t:'⚡ Amazon Kinesis Data Streams',b:'Managed real-time streaming. POS sales and web events flow through Kinesis at sub-second latency. Replaces daily cron jobs entirely for these sources. Auto-scales to handle Fashion Week spikes. Cost: pay per shard-hour.',tags:[['R1: Streaming','orange'],['R3: Automation','green'],['Sub-second','blue']]},
  'firehose':{t:'🔥 Kinesis Data Firehose',b:'Reads from Kinesis Streams and delivers micro-batches to S3 Raw Zone. Auto-converts to Parquet (columnar) on the way. No servers to manage. Also supports direct delivery to Redshift. Cost: pay per GB ingested.',tags:[['Serverless','green'],['Parquet conversion','blue'],['S3 delivery','blue']]},
  'glue-etl':{t:'🔄 AWS Glue ETL',b:'Managed Spark runtime replacing hand-coded ETL scripts. Built-in job bookmarks prevent reprocessing. Visual Studio for non-Spark engineers. Handles inventory batch loads, CRM syncs, historical data. Cost: pay per DPU-hour.',tags:[['Replaces cron ETL','orange'],['R3: Automation','green'],['Managed Spark','blue']]},
  'lambda':{t:'λ AWS Lambda',b:'Serverless API connector functions triggered by EventBridge schedules. Polls weather, holiday, and logistics APIs. New sources added as new functions — no impact on existing pipelines. Directly supports R7 Extensibility. Cost: pay per invocation.',tags:[['R7: Extensibility','green'],['Serverless','green'],['EventBridge','blue']]},
  'dms':{t:'🔃 AWS DMS',b:'Database Migration Service handles the one-time historical data migration from on-premises colocation systems to S3. Supports CDC (change data capture) for ongoing replication during transition, ensuring zero data loss at cutover.',tags:[['Migration','orange'],['CDC replication','blue'],['Zero data loss','green']]},
  's3-raw':{t:'🪣 S3 Raw Zone (Bronze)',b:'Immutable landing zone. Data stored exactly as received — source of truth enabling full reprocessing. Intelligent-Tiering auto-moves cold data to cheaper storage. Stores Parquet, JSON logs, and binary review images. Lifecycle: archive after 90 days.',tags:[['R1: Multi-modal','orange'],['R6: Cost (tiering)','green'],['Immutable','blue']]},
  's3-cur':{t:'✨ S3 Curated Zone (Silver)',b:'Cleaned, deduplicated, schema-validated data. PII from customers_sample.csv masked here via Glue PII detection. Catalog entries created. Partitioned by date for performance. Single source of truth for all downstream. Open Parquet format — no lock-in.',tags:[['R2: PII masking','orange'],['R5: Quality','green'],['Open format','blue']]},
  'redshift':{t:'🔴 Amazon Redshift (Serving / Gold)',b:'Columnar data warehouse. Pre-joined, aggregated datasets for QuickSight and ad-hoc queries. Redshift Spectrum queries S3 directly without loading (cost saver). Replaces daily Excel aggregation entirely. RA3 nodes decouple compute/storage scaling.',tags:[['Replaces Excel','orange'],['R1: Unified','blue'],['Columnar DWH','blue']]},
  'dynamodb':{t:'⚡ Amazon DynamoDB',b:'NoSQL store for <10ms lookups needed by ML inference and the future virtual shopping assistant. Stores real-time product recommendation results and live inventory flags. Pay-per-request pricing keeps costs proportional to usage.',tags:[['<10ms latency','orange'],['R7: API exposure','blue'],['ML serving','green']]},
  'glue-cat':{t:'📚 AWS Glue Data Catalog',b:'Central metadata store for all datasets. Integrates with Athena, Redshift Spectrum, SageMaker. Enables self-service discovery — Alex\'s team finds and queries any dataset without asking engineering. Tracks schema evolution automatically.',tags:[['Data lineage','blue'],['Self-service','green'],['Schema registry','blue']]},
  'mwaa':{t:'🗂️ Amazon MWAA (Managed Airflow)',b:'Fully managed Apache Airflow. Replaces all cron jobs with DAGs. Dependency management, retry logic, SLA alerts, visual monitoring UI. Open-source Airflow core — directly addresses Javier\'s vendor lock-in concern. Cost: instance-based.',tags:[['R3: Orchestration','orange'],['Open-source','green'],['No lock-in','green']]},
  'glue-dq':{t:'✅ AWS Glue Data Quality',b:'Automated rules after each pipeline: null checks on customer_id/product_id, price range validation, referential integrity between sales and inventory, freshness checks on external_factors. Failures trigger CloudWatch alerts before bad data reaches Redshift.',tags:[['R5: Data Quality','orange'],['Automated','green'],['Real-time alerts','blue']]},
  'lake-form':{t:'🏛️ AWS Lake Formation',b:'Fine-grained RBAC at column and row level. Laura (InfoSec) defines who sees what centrally — junior analysts see masked customer data, data scientists get full access. Centralized GDPR compliance, data sharing agreements, and audit trails.',tags:[['R4: Security','orange'],['GDPR','orange'],['Column RBAC','blue']]},
  'macie':{t:'🔍 Amazon Macie',b:'ML-powered PII scanner. Continuously monitors S3 for sensitive data from customers_sample.csv and sales_sample.csv. Findings sent to CloudWatch. Ensures PII never lands in wrong zone or reaches unauthorized principals.',tags:[['R4: PII scanning','orange'],['GDPR','orange'],['Automated','green']]},
  'quicksight':{t:'📊 Amazon QuickSight',b:'Managed BI — connects to Redshift and S3. Replaces daily Excel reports. SPICE in-memory engine for fast queries. Pay-per-session pricing vs traditional BI per-seat licensing. ML-powered anomaly detection and forecasting built in.',tags:[['Replaces Excel','orange'],['Self-service BI','green'],['R6: Cost','blue']]},
  'sagemaker':{t:'🤖 Amazon SageMaker',b:'End-to-end ML platform. Use cases: (1) Product recommendations — collaborative filtering on sales+customers, (2) Demand forecasting — DeepAR on sales+external_factors, (3) Dynamic pricing — regression on inventory+competitive data, (4) Return prediction on shipping data.',tags:[['Forecasting','blue'],['Recommendations','blue'],['Dynamic pricing','blue'],['R1: ML','green']]},
  'comprehend':{t:'💬 Amazon Comprehend',b:'Managed NLP. Runs sentiment analysis on customer_reviews_sample.csv text automatically. Outputs sentiment scores per product. Feeds QuickSight dashboards for merchandising teams. No ML expertise required — fully managed API call.',tags:[['Sentiment NLP','blue'],['Reviews data','blue'],['Managed','green']]},
  'apigw':{t:'🔗 API Gateway + Lambda',b:'Secure REST/GraphQL APIs expose curated data to logistics partners, marketing platforms, and AI agents (explicitly listed in RFP). Rate limiting, API keys, usage plans built in. Supports R7 Interoperability and future data monetisation.',tags:[['R7: Interop','orange'],['AI agents','blue'],['Partners','blue']]},
  'iam':{t:'🔐 IAM + AWS KMS',b:'IAM enforces least-privilege for all service-to-service and user access. KMS manages encryption keys for S3, Redshift, DynamoDB. TLS enforced in transit. Every principal follows least-privilege. Addresses Laura\'s mandate and R4 directly.',tags:[['R4: Security','orange'],['Encryption','blue'],['Least privilege','green']]},
  'terraform':{t:'🏗️ Terraform / AWS CDK',b:'All infra defined as code, Git version-controlled. One command provisions identical Dev, Pre-Prod, and Prod environments. Enables peer review of infra changes and rollbacks. Modular design lets Javier\'s team own specific modules.',tags:[['R2: Multi-env','orange'],['R3: IaC','orange'],['Git versioned','green']]},
  'cloudwatch':{t:'👁️ Amazon CloudWatch',b:'Unified monitoring across all services: pipeline latency, DQ failures, S3 growth, Redshift query performance, Lambda errors. SNS/PagerDuty alerts for on-call. Custom operational dashboards for the data engineering team.',tags:[['R4: High availability','orange'],['Unified monitoring','green'],['Alerting','blue']]},
  'orgs':{t:'🏢 AWS Organizations',b:'Three separate AWS accounts (Dev, Pre-Prod, Prod) under one Organization. Service Control Policies enforce guardrails: Prod accounts protected, cost limits per account. Anonymised data samples flow from Prod to Dev via S3 cross-account replication.',tags:[['R2: Multi-environment','orange'],['Governance','blue'],['Cost guardrails','green']]},
  'carbon':{t:'🌱 AWS Customer Carbon Footprint Tool',b:'Native tool tracking carbon emissions per service and region. Year-over-year comparison. Manga quantifies sustainability improvement vs on-premises colocation — critical for R8 compliance and ESG reporting. Dashboard exportable for board-level reporting.',tags:[['R8: Sustainability','orange'],['Carbon metrics','green'],['ESG reporting','blue']]},
};
function show(k){
  const r=d[k];if(!r)return;
  document.querySelectorAll('.svc').forEach(s=>s.classList.remove('active'));
  event.currentTarget.classList.add('active');
  const tags=(r.tags||[]).map(([l,t])=>`<span class="badge b-${t==='orange'?'orange':t==='green'?'green':'blue'}">${l}</span>`).join('');
  document.getElementById('ib').innerHTML=`<div class="ititle">${r.t}</div><div class="ibody">${r.b}</div><div style="margin-top:7px">${tags}</div>`;
}
</script></body></html>
"""
    st.components.v1.html(lla_html, height=760, scrolling=False)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DATA SOURCES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "data":
    st.markdown('<div class="page-title">Data Sources</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Manga\'s 6 sample datasets — schema, quality profile, and ingestion strategy for each (RFP Appendix III)</div>', unsafe_allow_html=True)

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
            c1.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="font-size:20px">{ds_meta['icon']}</div>
              <div class="metric-label">{ds_meta['source']}</div>
            </div>""", unsafe_allow_html=True)
            c2.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="font-size:14px; padding-top:4px">{ds_meta['pattern']}</div>
              <div class="metric-label">Ingestion Pattern</div>
            </div>""", unsafe_allow_html=True)
            pii_color = "#f07070" if ds_meta['pii'] else "#50c880"
            pii_text = "⚠️ Contains PII" if ds_meta['pii'] else "✅ No PII"
            c3.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="font-size:14px; color:{pii_color}; padding-top:4px">{pii_text}</div>
              <div class="metric-label">Data Sensitivity</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:11px; color:#6a8aaa; margin:8px 0 4px'>**AWS Path:** `{ds_meta['ingestion']}`</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:11px; color:#8090a8; margin-bottom:10px'>{ds_meta['desc']}</div>", unsafe_allow_html=True)
            uc_badges = "".join([f'<span class="badge badge-blue">{uc}</span>' for uc in ds_meta['use_cases']])
            st.markdown(f"<div style='margin-bottom:12px'>{uc_badges}</div>", unsafe_allow_html=True)

            if df is not None:
                st.dataframe(
                    df.head(10),
                    use_container_width=True,
                    hide_index=True,
                )
                st.markdown(f"<div style='font-size:10px; color:#3a5a7a; margin-top:4px'>Showing 10 of {len(df)} sample rows · {len(df.columns)} columns</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REQUIREMENTS COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "reqs":
    st.markdown('<div class="page-title">Requirements Coverage</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">How each of the 8 RFP requirements (R1–R8) is addressed by the proposed AWS architecture</div>', unsafe_allow_html=True)

    requirements = [
        ("R1", "Unified Multi-modal Data Platform",
         "High-throughput streaming (Kinesis) + batch (Glue) pipelines. S3 Data Lakehouse stores structured (Parquet), semi-structured (JSON), and unstructured (images, logs) data. Single Glue Catalog provides unified access across departments.",
         ["Kinesis Streams", "AWS Glue ETL", "S3 Lakehouse", "Glue Catalog", "Amazon Redshift"],
         "✅ Fully Covered", "green"),
        ("R2", "Multi-Environment Setup",
         "AWS Organizations provisions three isolated accounts (Dev / Pre-Prod / Prod) from the same Terraform templates. Anonymised production samples (via Glue PII masking + Lake Formation) automatically replicated to non-prod environments.",
         ["AWS Organizations", "Terraform/CDK", "Lake Formation (PII masking)", "S3 Cross-Account Replication"],
         "✅ Fully Covered", "green"),
        ("R3", "Automation",
         "Infrastructure-as-Code via Terraform/CDK. MWAA (Managed Airflow) replaces all cron jobs with DAG-based orchestration. Glue job bookmarks, auto-scaling, and lifecycle policies automate the entire data lifecycle.",
         ["Terraform / AWS CDK", "Amazon MWAA (Airflow)", "AWS Glue (job bookmarks)", "EventBridge schedules"],
         "✅ Fully Covered", "green"),
        ("R4", "Security & High Availability",
         "IAM least-privilege + KMS encryption at rest/transit. Lake Formation column/row RBAC. Macie PII scanning. Multi-AZ deployments for Redshift, MWAA, DynamoDB. S3 11-nines durability. CloudWatch + SNS alerting. Target: 99.9% uptime.",
         ["IAM + AWS KMS", "AWS Lake Formation", "Amazon Macie", "Multi-AZ deployments", "CloudWatch alarms"],
         "✅ Fully Covered", "green"),
        ("R5", "Data Quality",
         "AWS Glue Data Quality rules run automatically after each pipeline. Checks: null constraints, range validation, referential integrity (sales ↔ inventory ↔ customers), freshness thresholds. Failures trigger CloudWatch alerts before bad data reaches downstream consumers.",
         ["AWS Glue Data Quality", "CloudWatch Alerts", "Glue Data Catalog (schema validation)", "SNS Notifications"],
         "✅ Fully Covered", "green"),
        ("R6", "Cost Optimisation",
         "Pay-per-use model vs fixed colocation. S3 Intelligent-Tiering auto-archives cold data. Spot Instances for non-critical Glue jobs. Redshift Reserved Instances for predictable workloads. QuickSight pay-per-session vs traditional BI per-seat. Projected 40–60% infrastructure cost reduction.",
         ["S3 Intelligent-Tiering", "Spot Instances (Glue)", "Redshift Reserved Instances", "QuickSight pay-per-session"],
         "✅ Fully Covered", "green"),
        ("R7", "Extensibility & Interoperability",
         "Decoupled Lambda connectors add new sources without touching existing pipelines. API Gateway exposes curated data to partners and AI agents. Open formats (Parquet, Delta) prevent lock-in. Versioned APIs ensure backward compatibility.",
         ["API Gateway + Lambda", "Open Parquet / Delta formats", "Glue Catalog (schema registry)", "Versioned REST APIs"],
         "✅ Fully Covered", "green"),
        ("R8", "Sustainability",
         "AWS data centres operate with high renewable energy usage. Selecting EU (Ireland) / EU (Frankfurt) regions maximises green energy mix. AWS Customer Carbon Footprint Tool provides quantitative emissions dashboard vs the on-premises colocation baseline.",
         ["AWS Carbon Footprint Tool", "Green regions (EU-WEST-1)", "Serverless (Lambda, Firehose)", "Auto-scaling (no idle resources)"],
         "✅ Fully Covered", "green"),
    ]

    for req_id, title, desc, services, status, color in requirements:
        color_map = {"green": "#0a2010", "orange": "#2a1a00", "red": "#200a0a"}
        border_map = {"green": "#1a6030", "orange": "#6a4000", "red": "#602020"}
        text_map = {"green": "#50d090", "orange": "#f0a040", "red": "#f07070"}
        with st.container():
            st.markdown(f"""
            <div class="card" style="background:{color_map[color]}; border-left:4px solid {border_map[color]}; border-color:{border_map[color]}; margin-bottom:10px">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px">
                <div>
                  <span style="font-size:13px; font-weight:800; color:{text_map[color]}">{req_id}</span>
                  <span style="font-size:13px; font-weight:700; color:#c0d4f0; margin-left:8px">{title}</span>
                </div>
                <span style="font-size:10px; font-weight:700; color:{text_map[color]}; background:{color_map[color]}; border:1px solid {border_map[color]}; padding:3px 9px; border-radius:20px">{status}</span>
              </div>
              <p style="font-size:11.5px; color:#8090a8; line-height:1.65; margin-bottom:10px">{desc}</p>
              <div>{"".join([f'<span class="badge badge-blue">{s}</span>' for s in services])}</div>
            </div>""", unsafe_allow_html=True)

    # Coverage summary chart
    st.markdown("---")
    st.markdown('<div class="section-title">Coverage Summary</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=[r[0] for r in requirements],
        y=[100] * 8,
        marker_color="#1a6030",
        marker_line_color="#50d090",
        marker_line_width=1.5,
        text=["100%"] * 8,
        textposition="inside",
        textfont=dict(color="#50d090", size=11, family="Segoe UI"),
    ))
    fig.update_layout(
        plot_bgcolor="#0d1525",
        paper_bgcolor="#0a0e1a",
        font=dict(color="#6a8aaa", family="Segoe UI"),
        xaxis=dict(gridcolor="#1e2d45", title="Requirement"),
        yaxis=dict(gridcolor="#1e2d45", title="Coverage %", range=[0, 120]),
        height=260,
        margin=dict(l=40, r=20, t=20, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: USE CASES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "usecases":
    st.markdown('<div class="page-title">Sample Use Cases</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Five end-to-end use cases showing the architecture in action with Manga\'s actual data sources (RFP Section 5)</div>', unsafe_allow_html=True)

    use_cases = [
        {
            "id": "UC1", "icon": "🤖", "title": "Product Recommendation Engine",
            "datasets": ["Sales", "Customers", "Inventory"],
            "aws": ["SageMaker (collaborative filtering)", "DynamoDB (serving)", "API Gateway", "Kinesis (real-time signals)"],
            "desc": "Collaborative filtering model trained on purchase history (sales_sample.csv) and customer profiles (customers_sample.csv). Real-time inference via SageMaker endpoint, results cached in DynamoDB for <10ms response. Exposed via API Gateway to the e-commerce front-end and virtual shopping assistant.",
            "impact": "Projected +12–18% AOV (average order value) based on retail industry benchmarks.",
            "pipeline": "sales_sample.csv + customers_sample.csv → S3 Curated → SageMaker training → DynamoDB → API Gateway → Website",
        },
        {
            "id": "UC2", "icon": "📈", "title": "Demand Forecasting",
            "datasets": ["Sales", "External Factors", "Inventory"],
            "aws": ["SageMaker DeepAR", "AWS Glue (feature engineering)", "QuickSight (dashboard)", "MWAA (weekly retrain DAG)"],
            "desc": "Time-series forecasting using SageMaker's DeepAR algorithm on sales history enriched with external context (weather, bank holidays, local events, fuel prices from external_factors_sample.csv). Model retrains weekly via MWAA DAG. Forecasts feed into inventory replenishment decisions.",
            "impact": "Reduces stockouts by ~30% and overstock write-offs by ~20%.",
            "pipeline": "sales_sample.csv + external_factors_sample.csv → Glue feature engineering → SageMaker DeepAR → QuickSight",
        },
        {
            "id": "UC3", "icon": "💬", "title": "Sentiment-Driven Merchandising",
            "datasets": ["Customer Reviews"],
            "aws": ["Amazon Comprehend (NLP)", "AWS Glue (aggregation)", "Amazon QuickSight", "SNS (alerts on score drops)"],
            "desc": "Amazon Comprehend processes review text from customer_reviews_sample.csv in near real-time, assigning positive/negative/neutral scores per review. Glue aggregates sentiment scores by product, store, and week. QuickSight dashboard surfaces products with declining sentiment scores, alerting the buying team.",
            "impact": "Enables proactive product decisions 2–3 weeks earlier than manual review cycles.",
            "pipeline": "customer_reviews_sample.csv → Kinesis → Comprehend (NLP) → S3 Curated → Glue aggregation → QuickSight + SNS alerts",
        },
        {
            "id": "UC4", "icon": "💰", "title": "Dynamic Pricing Engine",
            "datasets": ["Sales", "Inventory", "External Factors"],
            "aws": ["SageMaker (regression model)", "Kinesis (real-time inventory feed)", "Lambda (pricing API)", "DynamoDB (price store)"],
            "desc": "ML model trained on historical price elasticity data, current inventory levels, competitor pricing signals, and contextual factors (weather, events). Produces recommended prices per SKU in real-time. Lambda function compares model output against pricing guardrails before writing to DynamoDB, which feeds the POS and e-commerce pricing layer.",
            "impact": "Potential 3–7% gross margin improvement from optimised clearance and peak pricing.",
            "pipeline": "sales + inventory + external_factors → SageMaker model → Lambda (guardrails) → DynamoDB → POS / E-commerce",
        },
        {
            "id": "UC5", "icon": "🚚", "title": "Return Rate & Logistics Optimisation",
            "datasets": ["Shipping", "Sales", "Customers"],
            "aws": ["SageMaker (classification)", "Glue (join pipeline)", "QuickSight (operations dashboard)", "SNS (high-return alerts)"],
            "desc": "Binary classification model predicts likelihood of return at purchase time, using features from shipping history (delivery time, cost delta), customer profile (return rate history), and product attributes. High-risk orders trigger proactive interventions (enhanced packaging, delivery instructions). Logistics cost variance (delivery_price vs actual_shipping_cost from shipping_sample.csv) tracked in QuickSight.",
            "impact": "10–15% reduction in return processing costs. Better delivery partner SLA management.",
            "pipeline": "shipping_sample.csv + sales + customers → Glue join → SageMaker classifier → SNS alerts + QuickSight ops dashboard",
        },
    ]

    for uc in use_cases:
        with st.expander(f"**{uc['id']}** {uc['icon']} {uc['title']}", expanded=False):
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"""
                <div style="font-size:12px; color:#90a8c0; line-height:1.7; margin-bottom:12px">{uc['desc']}</div>
                <div style="background:#0d1525; border:1px solid #1e3050; border-radius:7px; padding:10px 12px; font-size:10.5px; color:#4a9af0; font-family:monospace; line-height:1.8">
                  🔀 <strong style="color:#6a8aaa">Pipeline:</strong><br>{uc['pipeline']}
                </div>
                <div style="margin-top:10px; padding:8px 12px; background:#0a1e14; border:1px solid #1a4828; border-radius:6px; font-size:11px; color:#50d090">
                  📊 <strong>Business Impact:</strong> {uc['impact']}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="section-title">Data Sources Used</div>', unsafe_allow_html=True)
                for ds in uc['datasets']:
                    st.markdown(f'<span class="badge badge-blue">📁 {ds}</span>', unsafe_allow_html=True)
                st.markdown('<div class="section-title" style="margin-top:14px">AWS Services</div>', unsafe_allow_html=True)
                for svc in uc['aws']:
                    st.markdown(f'<span class="badge badge-green" style="display:block; margin:3px 0; text-align:left">⚙️ {svc}</span>', unsafe_allow_html=True)

    # ── Use case / dataset heatmap
    st.markdown("---")
    st.markdown('<div class="section-title">Dataset Usage Matrix</div>', unsafe_allow_html=True)
    matrix_data = {
        "Use Case":          ["Recommendations", "Demand Forecast", "Sentiment", "Dynamic Pricing", "Return Optimisation"],
        "Sales":             [1, 1, 0, 1, 1],
        "Customers":         [1, 0, 0, 0, 1],
        "Inventory":         [1, 1, 0, 1, 0],
        "Customer Reviews":  [0, 0, 1, 0, 0],
        "External Factors":  [0, 1, 0, 1, 0],
        "Shipping":          [0, 0, 0, 0, 1],
    }
    hm_df = pd.DataFrame(matrix_data).set_index("Use Case")
    fig2 = px.imshow(
        hm_df,
        color_continuous_scale=[[0, "#0d1525"], [1, "#1a6040"]],
        aspect="auto",
        text_auto=False,
    )
    fig2.update_traces(
        text=hm_df.map(lambda v: "✓" if v else ""),
        texttemplate="%{text}",
        textfont=dict(size=16, color="#50d090"),
    )
    fig2.update_layout(
        plot_bgcolor="#0d1525",
        paper_bgcolor="#0a0e1a",
        font=dict(color="#6a8aaa", family="Segoe UI"),
        coloraxis_showscale=False,
        height=260,
        margin=dict(l=160, r=20, t=20, b=60),
        xaxis=dict(side="bottom"),
    )
    st.plotly_chart(fig2, use_container_width=True)
