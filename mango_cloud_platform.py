import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import base64

st.set_page_config(
    page_title="Manga · AWS Cloud Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM TOKENS (Framer-based, per DESIGN.md) ─────────────────────
CANVAS    = "#090909"
SURF1     = "#141414"
SURF2     = "#1c1c1c"
HAIR      = "#262626"
HAIR_S    = "#1a1a1a"
INK       = "#ffffff"
INK_M     = "#999999"
INK_F     = "#444444"
ACCENT    = "#0099ff"
# Signature gradient-spotlight hues (Framer DESIGN.md)
G_VIOLET  = "#6a4cf5"
G_MAGENTA = "#d44df0"
G_ORANGE  = "#ff7a3d"

# Architecture node colors per layer
C = {
    "src":  ("#1e3a5f", "#4a7ac8"),
    "ing":  ("#0d2040", "#3a6aaa"),
    "proc": ("#0d2830", "#3a7060"),
    "cat":  ("#1a1a3a", "#5a5ab8"),
    "raw":  ("#1a0d20", "#7a3a9a"),
    "sil":  ("#1a1020", "#9a3a6a"),
    "gld":  ("#0a1a0c", "#2a7a40"),
    "dyn":  ("#0a180a", "#2a7a3a"),
    "con":  ("#0d1a30", "#3a5a8a"),
    "sec":  ("#200a0a", "#7a2828"),
    "gov":  ("#1a1a3a", "#5a5ab8"),
}

# ── GLOBAL CSS (Framer design system — per DESIGN.md) ───────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Mona+Sans:wght@400;500;600;700;800&display=swap');

:root{{
  --font-display:'Mona Sans','Inter',-apple-system,sans-serif;
  --font-body:'Inter',-apple-system,sans-serif;
}}
html,body,[data-testid="stAppViewContainer"]{{
  background:{CANVAS}!important;color:{INK};
  font-family:var(--font-body);
  font-feature-settings:'cv01','cv05','cv09','cv11','ss03';
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
}}

/* ── CENTER MAIN CONTENT — symmetric margins, independent of sidebar ──────── */
section[data-testid="stMain"]{{width:100%!important}}
[data-testid="stMain"] .block-container{{
  max-width:1240px!important;
  padding:72px 48px 96px!important;
  margin-left:auto!important;margin-right:auto!important;
}}

[data-testid="stSidebar"]{{background:#0a0a0a!important;border-right:1px solid {HAIR};min-width:248px!important;width:248px!important}}
[data-testid="stSidebarContent"]{{padding:24px 14px 18px!important}}
[data-testid="stSidebar"] *{{color:{INK_M}!important}}
/* ── SIDEBAR NAV BUTTONS (robust across Streamlit versions) ── */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{{gap:4px!important}}
section[data-testid="stSidebar"] .stButton{{width:100%!important;margin:0!important}}
section[data-testid="stSidebar"] .stButton>button{{
    width:100%!important;display:flex!important;align-items:center!important;
    justify-content:flex-start!important;text-align:left!important;
    min-height:42px!important;padding:10px 14px!important;margin:0!important;
    background:transparent!important;border:1px solid transparent!important;
    border-radius:10px!important;color:{INK_M}!important;
    font-size:14px!important;font-weight:500!important;letter-spacing:-.14px!important;
    font-family:var(--font-body)!important;
    transition:background 160ms ease,border-color 160ms ease,color 160ms ease!important;
}}
section[data-testid="stSidebar"] .stButton>button>div,
section[data-testid="stSidebar"] .stButton>button [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] .stButton>button p{{
    width:100%!important;text-align:left!important;margin:0!important;color:inherit!important;
    justify-content:flex-start!important;
}}
section[data-testid="stSidebar"] .stButton>button:hover{{
    background:{SURF1}!important;border-color:{HAIR}!important;color:{INK}!important;
}}
section[data-testid="stSidebar"] .stButton>button[kind="primary"],
section[data-testid="stSidebar"] .stButton>button[data-testid="baseButton-primary"],
section[data-testid="stSidebar"] .stButton>button[data-testid="stBaseButton-primary"]{{
    background:{SURF2}!important;border-color:{HAIR}!important;
    color:{INK}!important;font-weight:600!important;
}}
section[data-testid="stSidebar"] .stButton>button p{{color:inherit!important}}
/* collapsedControl kept visible so JS can click it */
header[data-testid="stHeader"]{{display:none}}

.card{{background:{SURF1};border:1px solid {HAIR};border-radius:15px;padding:18px 20px;margin-bottom:12px;transition:border-color .18s}}
.card:hover{{border-color:#3a3a3a}}
.metric-card{{background:{SURF1};border:1px solid {HAIR};border-radius:15px;padding:20px;text-align:center}}
.metric-value{{font-family:var(--font-display);font-size:36px;font-weight:600;color:{INK};letter-spacing:-1.8px;line-height:1}}
.metric-label{{font-size:11px;color:{INK_M};text-transform:uppercase;letter-spacing:.1em;margin-top:7px;font-weight:500}}

/* Signature gradient spotlight card */
.spotlight{{
  border-radius:30px;padding:30px 34px;margin:4px 0 8px;color:#fff;
  background:linear-gradient(120deg,{G_VIOLET} 0%,{G_MAGENTA} 52%,{G_ORANGE} 110%);
  box-shadow:0 24px 60px rgba(106,76,245,.22);
}}
.spotlight .sl-eyebrow{{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;opacity:.82}}
.spotlight .sl-pillars{{font-family:var(--font-display);font-size:34px;font-weight:600;letter-spacing:-1.6px;line-height:1.04;margin-top:10px}}
.spotlight .sl-sub{{font-size:14px;line-height:1.5;opacity:.9;margin-top:12px;max-width:760px}}

.figma-chart-frame{{background:#ffffff;border:1px solid #ececec;border-radius:15px;padding:18px;overflow:auto;box-shadow:0 18px 48px rgba(0,0,0,.32);margin:8px 0 18px}}
.figma-chart-frame img{{display:block;width:100%;max-width:1500px;height:auto;margin:0 auto}}
.figma-chart-missing{{background:{SURF1};border:1px solid {HAIR};border-radius:10px;padding:14px 16px;color:{INK_M};font-size:12px;margin-bottom:12px}}
.section-title{{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:{INK_F};margin-bottom:14px;padding-bottom:6px;border-bottom:1px solid {HAIR}}}
.page-title{{font-family:var(--font-display);font-size:46px;font-weight:600;color:{INK};letter-spacing:-2.4px;margin-bottom:8px;line-height:1.0}}
.page-sub{{font-size:18px;color:{INK_M};margin-bottom:28px;font-weight:400;letter-spacing:-.18px;line-height:1.3}}
.badge{{display:inline-block;font-size:10px;font-weight:500;padding:4px 11px;border-radius:100px;margin:2px;letter-spacing:.01em;background:{SURF2};color:{INK_M};border:1px solid {HAIR}}}
.badge-blue{{background:{SURF2};color:#cfcfcf;border:1px solid {HAIR}}}
.badge-green{{background:{SURF2};color:{INK_M};border:1px solid {HAIR}}}
.badge-orange{{background:{SURF2};color:{INK_M};border:1px solid {HAIR}}}
.badge-purple{{background:{SURF2};color:{INK_M};border:1px solid {HAIR}}}
.badge-red{{background:{SURF2};color:{INK_M};border:1px solid {HAIR}}}
.stk-card{{background:{SURF1};border:1px solid {HAIR};border-radius:15px;padding:14px 16px;margin-bottom:10px}}
.stk-name{{font-size:14px;font-weight:600;color:{INK};letter-spacing:-.2px}}
.stk-role{{font-size:10px;color:{INK_F};text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}}
.stk-concern{{font-size:11.5px;color:{INK_M};line-height:1.55}}
.stk-tag{{font-size:9px;font-weight:500;padding:3px 9px 3px 8px;border-radius:100px;display:inline-flex;align-items:center;gap:6px;margin-left:8px;background:{SURF2};color:{INK_M};border:1px solid {HAIR};letter-spacing:.02em;vertical-align:middle}}
.stk-tag::before{{content:"";width:6px;height:6px;border-radius:50%;display:inline-block}}
.stk-skeptic::before{{background:#c8893a}}
.stk-champion::before{{background:{ACCENT}}}
.stk-neutral::before{{background:{INK_M}}}
[data-testid="stTabs"] button{{font-size:12px!important;font-weight:500!important;color:{INK_M}!important;font-family:var(--font-body)!important}}
[data-testid="stTabs"] button[aria-selected="true"]{{color:{INK}!important;border-bottom:2px solid {ACCENT}!important}}
[data-testid="stDataFrame"]{{border:1px solid {HAIR};border-radius:10px}}
hr{{border-color:{HAIR}!important}}
a,a:visited{{color:{ACCENT}!important;text-decoration:none}}
/* Style horizontal Streamlit buttons outside the sidebar */
div[data-testid="stHorizontalBlock"] .stButton>button{{
    background:transparent!important;border:1px solid {HAIR}!important;
    color:{INK_M}!important;border-radius:100px!important;
    padding:4px 0!important;font-size:11px!important;font-weight:500!important;
    font-family:var(--font-body)!important;transition:all .15s!important;
    min-height:0!important;line-height:1.5!important;
}}
div[data-testid="stHorizontalBlock"] .stButton>button:hover{{
    background:{SURF1}!important;border-color:{HAIR}!important;color:{INK}!important;
}}
</style>""", unsafe_allow_html=True)

# ── DATA LOADER ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = Path(__file__).parent
    files = {"Sales":"sales_sample.csv","Customers":"customers_sample.csv",
             "Inventory":"inventory_sample.csv","Customer Reviews":"customer_reviews_sample.csv",
             "External Factors":"external_factors_sample.csv","Shipping":"shipping_sample.csv"}
    out = {}
    for name, fname in files.items():
        p = base / fname
        if p.exists():
            try: out[name] = pd.read_csv(p)
            except: pass
    return out

DATA = load_data()

# ── FIGMA ARCHITECTURE EXPORTS ──────────────────────────────────────────────
APP_DIR = Path(__file__).parent

HLA_IMAGE_CANDIDATES = (
    "assets/manga-cloud-platform-high-level-architecture.jpg",
    "Manga Cloud Platform — High-Level Architecture.jpg",
)

LLA_IMAGE_CANDIDATES = (
    "assets/manga-cloud-platform-low-level-aws-architecture.jpg",
    "Manga Cloud Platform — Low-Level AWS Architecture.jpg",
)

def resolve_architecture_image(*candidates):
    search_roots = (APP_DIR, APP_DIR / "assets", Path.home() / "Downloads")
    for candidate in candidates:
        candidate_path = Path(candidate)
        if candidate_path.is_absolute() and candidate_path.exists():
            return candidate_path
        for root in search_roots:
            image_path = root / candidate_path
            if image_path.exists():
                return image_path
    return None

@st.cache_data(show_spinner=False)
def encode_architecture_image(path_str, modified_at):
    _ = modified_at
    return base64.b64encode(Path(path_str).read_bytes()).decode("ascii")

def render_figma_architecture(candidates, alt_text):
    image_path = resolve_architecture_image(*candidates)
    if image_path is None:
        st.markdown(
            '<div class="figma-chart-missing">Figma architecture export not found. Showing generated fallback diagram.</div>',
            unsafe_allow_html=True,
        )
        return False

    encoded = encode_architecture_image(str(image_path), image_path.stat().st_mtime)
    st.markdown(
        f'<div class="figma-chart-frame"><img src="data:image/jpeg;base64,{encoded}" alt="{alt_text}"></div>',
        unsafe_allow_html=True,
    )
    return True

# ── ARCHITECTURE DIAGRAM BUILDER ────────────────────────────────────────────
def arch_fig(title, nodes, edges, xr, yr, h=600):
    """Build a Plotly architecture diagram with rectangular colored nodes and hover."""
    fig = go.Figure()
    # Edges (drawn below nodes)
    for e in edges:
        x0,y0,x1,y1 = e
        fig.add_shape(type="line",x0=x0,y0=y0,x1=x1,y1=y1,
                      line=dict(color="#2a4a6a",width=1.2),layer="below")
        fig.add_annotation(x=x1,y=y1,ax=x0,ay=y0,xref='x',yref='y',axref='x',ayref='y',
                           arrowhead=2,arrowsize=1,arrowwidth=1.2,arrowcolor="#3a6a9a",
                           showarrow=True,text="")
    # Nodes
    for n in nodes:
        x,y,w,h2 = n['x'],n['y'],n.get('w',1.35),n.get('h',0.62)
        fc,bc = n['c']
        fig.add_shape(type="rect",x0=x-w/2,y0=y-h2/2,x1=x+w/2,y1=y+h2/2,
                      fillcolor=fc,line=dict(color=bc,width=1.5))
        lbl = n['label']
        sub = n.get('sub','')
        yoff = 0.11 if sub else 0
        fig.add_annotation(x=x,y=y+yoff,text=f"<b>{lbl}</b>",showarrow=False,
            font=dict(color="#e0eaff",size=8.5,family="Inter,sans-serif"),
            xanchor='center',yanchor='middle',bgcolor='rgba(0,0,0,0)')
        if sub:
            fig.add_annotation(x=x,y=y-0.13,text=sub,showarrow=False,
                font=dict(color="#7a9ab8",size=7.5,family="Inter,sans-serif"),
                xanchor='center',yanchor='middle',bgcolor='rgba(0,0,0,0)')
        # Hover area — polygon fill trick
        fig.add_trace(go.Scatter(
            x=[x-w/2,x+w/2,x+w/2,x-w/2,x-w/2],
            y=[y-h2/2,y-h2/2,y+h2/2,y+h2/2,y-h2/2],
            fill='toself',fillcolor='rgba(0,0,0,0.01)',
            line=dict(color='rgba(0,0,0,0)',width=0),
            hovertext=n['hover'],hoverinfo='text',
            hoveron='fills',mode='lines',showlegend=False))
    fig.update_layout(
        plot_bgcolor=CANVAS,paper_bgcolor=CANVAS,
        xaxis=dict(visible=False,range=xr),yaxis=dict(visible=False,range=yr),
        height=h,margin=dict(l=8,r=8,t=36,b=8),showlegend=False,
        hoverlabel=dict(bgcolor=SURF1,bordercolor=HAIR,
            font=dict(color=INK,size=11,family="Inter,sans-serif"),align='left'),
        title=dict(text=title,font=dict(color=ACCENT,size=12,family="Inter"),x=0.5),
    )
    return fig

# ── HLA DIAGRAM DATA ────────────────────────────────────────────────────────
HLA_NODES = [
    # ── Data Sources row y=7.3
    dict(x=1.0,y=7.3,w=1.5,h=0.65,c=C["src"],label="Streaming",sub="Real-time events",
         hover="<b>Streaming Sources</b><br><b>What:</b> Continuous high-frequency events — POS transactions, web clicks, reviews, add-to-cart.<br><b>Why:</b> Eliminates Manga's 24-hour lag. Enables sub-second inventory alerts and live sales dashboards impossible with batch.<br><b>RFP: R1, R3</b>"),
    dict(x=2.8,y=7.3,w=1.5,h=0.65,c=C["src"],label="Batch",sub="Scheduled loads",
         hover="<b>Batch Sources</b><br><b>What:</b> Scheduled large-volume data loads — nightly ERP, daily CRM sync, hourly inventory reconciliation.<br><b>Why:</b> Not all data needs real-time. Replaces fragile cron scripts with managed, monitored pipelines with retry and alerting.<br><b>RFP: R3, R6</b>"),
    dict(x=4.6,y=7.3,w=1.5,h=0.65,c=C["src"],label="Structured",sub="Tables · schemas",
         hover="<b>Structured Data</b><br><b>What:</b> Tabular, schema-defined records — sales, inventory, customers, shipping.<br><b>Why:</b> Columnar Parquet format enables fast BI queries. Schema enforcement at ingest prevents quality issues downstream.<br><b>RFP: R1, R5</b>"),
    dict(x=6.4,y=7.3,w=1.5,h=0.65,c=C["src"],label="Unstructured",sub="Text · images · logs",
         hover="<b>Unstructured Data</b><br><b>What:</b> Review text, product images, clickstream logs — no fixed schema.<br><b>Why:</b> Manga's Excel layer ignores this entirely. Capturing review text and images unlocks sentiment analysis, visual search, and brand monitoring.<br><b>RFP: R1, ML use cases</b>"),
    # ── Ingestion y=6.0
    dict(x=3.7,y=6.0,w=4.6,h=0.7,c=C["ing"],label="INGESTION",sub="Unified entry point — streaming and batch — replaces all cron-job ETL scripts",
         hover="<b>Ingestion Layer</b><br><b>What:</b> Single unified entry point for all source types. Handles streaming and batch with consistent retry logic, job bookmarks, failure alerting, and lineage tracking.<br><b>Why:</b> Replaces 6+ siloed cron scripts with one observable, reliable platform. One monitoring dashboard for all pipelines.<br><b>RFP: R1, R3, R4</b>"),
    # ── Cataloging y=4.8 (left)
    dict(x=1.2,y=4.8,w=2.0,h=0.9,c=C["cat"],label="CATALOGING",sub="& SEARCH",
         hover="<b>Cataloging & Search</b><br><b>What:</b> Central metadata registry — schema, owner, lineage, freshness, tags. Bidirectionally connected to Processing — captures schema changes automatically.<br><b>Why:</b> Self-service discovery. Analysts find any dataset without emailing Engineering. Without this, Manga's analysts continue working with undocumented, untrustworthy data.<br><b>RFP: R4, R5, R7</b>"),
    # ── Processing y=4.8
    dict(x=4.1,y=4.8,w=2.0,h=0.9,c=C["proc"],label="VALIDATE / CLEAN",sub="Standardize / Norm",
         hover="<b>Validate / Clean / Standardize / Norm</b><br><b>What:</b> Quality gate — null checks, range validation, deduplication, format standardization. Applied after raw ingestion.<br><b>Why:</b> Prevents bad data from reaching Redshift or SageMaker. All failures trigger alerts before propagating to downstream consumers.<br><b>RFP: R5, R4</b>"),
    dict(x=6.3,y=4.8,w=2.0,h=0.9,c=C["proc"],label="TRANSFORM",sub="& Enrich",
         hover="<b>Transform & Enrich</b><br><b>What:</b> Joins datasets (sales↔customers↔products), calculates KPIs, enriches with external context — weather, campaigns, logistics.<br><b>Why:</b> Raw data alone cannot power forecasting or dynamic pricing. Joining with external_factors is what makes ML predictions accurate. This is where Manga's competitive advantage is built.<br><b>RFP: R1, R3</b>"),
    # ── Storage y=3.2
    dict(x=2.4,y=3.2,w=1.8,h=0.75,c=C["raw"],label="Raw Zone",sub="Bronze · immutable",
         hover="<b>Raw Zone (Bronze)</b><br><b>What:</b> Immutable append-only storage. Data exactly as received — never modified after write.<br><b>Why:</b> Full reprocessing if business logic changes. Satisfies GDPR audit trail. S3 Intelligent-Tiering auto-archives cold data, cutting storage cost 60%+.<br><b>RFP: R1, R4, R6</b>"),
    dict(x=4.5,y=3.2,w=1.8,h=0.75,c=C["sil"],label="Cleaned Zone",sub="Silver · PII-masked",
         hover="<b>Cleaned Zone (Silver)</b><br><b>What:</b> Validated, deduplicated, PII-masked Parquet. Catalog entries created here.<br><b>Why:</b> Single source of truth. Dev/Pre-Prod environments never see real customer PII — directly addresses R2. Open Parquet format prevents vendor lock-in.<br><b>RFP: R2, R4, R5</b>"),
    dict(x=6.6,y=3.2,w=1.8,h=0.75,c=C["gld"],label="Curated Zone",sub="Gold · BI & ML ready",
         hover="<b>Curated / Consumption Zone (Gold)</b><br><b>What:</b> Pre-aggregated, query-optimized datasets for BI and ML feature serving. Updated continuously.<br><b>Why:</b> Replaces daily Excel dumps. Sub-second QuickSight dashboards. ML feature vectors served with low latency to SageMaker.<br><b>RFP: R1, R6, replaces Excel</b>"),
    # ── Consumption y=1.9
    dict(x=3.7,y=1.9,w=4.6,h=0.7,c=C["con"],label="CONSUMPTION",sub="BI Dashboards · ML Platform · Partner APIs · AI Agents",
         hover="<b>Consumption Layer</b><br><b>What:</b> Exposes curated data to all consumers — BI dashboards for business users, ML platform for data scientists, REST APIs for partners and AI agents.<br><b>Why:</b> Decoupled from storage so BI, data science, and external partners don't interfere. Self-service replaces the current 'email Engineering for a report' workflow.<br><b>RFP: R1, R7</b>"),
    # ── Security bar y=0.7
    dict(x=4.0,y=0.7,w=7.8,h=0.65,c=C["sec"],label="SECURITY & GOVERNANCE — applied at every layer",sub="RBAC · KMS encryption at rest · TLS 1.3 in-transit · GDPR · CloudTrail Audit Logs · PII Masking",
         hover="<b>Security & Governance (Cross-cutting)</b><br><b>What:</b> Applied at every layer — RBAC at column/row level, KMS encryption at rest, TLS 1.3 in-transit, PII masking, threat monitoring, immutable GDPR audit logs.<br><b>TLS vs E2EE:</b> We use TLS termination at service boundaries (not E2EE) — this allows the platform to process and analyse data while keeping every service hop encrypted.<br><b>RFP: R4, GDPR, Laura's mandate</b>"),
]

HLA_EDGES = [
    # Sources → Ingestion
    (1.0,6.97,2.5,6.35),(2.8,6.97,2.9,6.35),(4.6,6.97,4.2,6.35),(6.4,6.97,5.2,6.35),
    # Ingestion → Validate
    (4.0,5.65,4.1,5.25),
    # Ingestion → Raw
    (2.8,5.65,2.4,3.58),
    # Catalog ↔ Validate (bidirectional)
    (2.2,4.8,3.1,4.8),(3.1,4.73,2.2,4.73),
    # Validate → Transform
    (5.1,4.8,5.3,4.8),
    # Transform → Curated
    (6.3,4.35,6.6,3.58),
    # Raw → Cleaned → Curated
    (3.3,3.2,3.6,3.2),(5.4,3.2,5.7,3.2),
    # Validate → Cleaned
    (4.1,4.35,4.5,3.58),
    # Curated → Consumption
    (6.6,2.82,5.5,2.25),
    # Cleaned → Consumption
    (4.5,2.82,4.2,2.25),
]

# ── LLA DIAGRAM DATA ────────────────────────────────────────────────────────
LLA_NODES = [
    # ── Security row y=9.5 (small h)
    dict(x=0.8,y=9.5,w=1.3,h=0.55,c=C["sec"],label="Amazon VPC",sub="Network isolation",
         hover="<b>Amazon VPC</b><br><b>What:</b> Network isolation for all AWS services. Private subnets for Redshift, MWAA, SageMaker.<br><b>Why:</b> VPC endpoints for S3 and DynamoDB — traffic never leaves the AWS backbone. Security groups enforce least-privilege network access.<br><b>RFP: R4</b>"),
    dict(x=2.3,y=9.5,w=1.3,h=0.55,c=C["sec"],label="IAM + KMS",sub="Auth · Encryption",
         hover="<b>IAM + AWS KMS</b><br><b>What:</b> IAM enforces least-privilege for all service-to-service and user access. KMS manages encryption keys for S3, Redshift, DynamoDB.<br><b>Why:</b> KMS keys rotate automatically. TLS 1.3 in-transit between all services. We use TLS termination (not E2EE) so the platform can process and analyse data while keeping every hop encrypted.<br><b>RFP: R4</b>"),
    dict(x=3.8,y=9.5,w=1.3,h=0.55,c=C["sec"],label="AWS CloudTrail",sub="GDPR audit logs",
         hover="<b>AWS CloudTrail</b><br><b>What:</b> Immutable audit log of every API call across all AWS accounts — who accessed what data, when, from where.<br><b>Why:</b> Critical for GDPR compliance — Right of Access and Right to Erasure both require audit trails. Enables forensic investigation of security incidents. Directly addresses Laura's mandate.<br><b>RFP: R4, GDPR</b>"),
    dict(x=5.3,y=9.5,w=1.3,h=0.55,c=C["sec"],label="CloudWatch",sub="Monitoring · Alerts",
         hover="<b>Amazon CloudWatch</b><br><b>What:</b> Unified monitoring across all services — pipeline latency, DQ failures, S3 growth, Redshift performance, Lambda errors.<br><b>Why:</b> SNS/PagerDuty alerts for on-call. Custom operational dashboards for the data engineering team. Logs Insights for ad-hoc log analysis.<br><b>RFP: R4, R5</b>"),
    dict(x=6.8,y=9.5,w=1.3,h=0.55,c=C["sec"],label="AWS Organizations",sub="Dev·PreProd·Prod",
         hover="<b>AWS Organizations</b><br><b>What:</b> Three separate AWS accounts (Dev, Pre-Prod, Prod) under one Organisation. Service Control Policies enforce guardrails.<br><b>Why:</b> Prod accounts protected from Dev mistakes. Cost limits enforced per account. Anonymised data samples flow from Prod to Dev via cross-account S3 replication.<br><b>RFP: R2, R3</b>"),
    dict(x=8.3,y=9.5,w=1.3,h=0.55,c=C["sec"],label="Terraform/CDK",sub="IaC · 3 envs",
         hover="<b>Terraform / AWS CDK</b><br><b>What:</b> All infrastructure defined as code, Git version-controlled. One set of templates provisions identical Dev, Pre-Prod, and Prod.<br><b>Why:</b> Peer review for infra changes. Rollbacks. Modular design lets Javier's team own specific modules. Addresses vendor lock-in concern directly.<br><b>RFP: R2, R3</b>"),
    # ── Sources row y=8.1
    dict(x=0.8,y=8.1,w=1.3,h=0.65,c=C["src"],label="POS / ERP",sub="Sales · Inventory",
         hover="<b>POS / ERP Systems</b><br><b>What:</b> Generates sales_sample.csv and inventory_sample.csv. High-frequency structured data.<br><b>Why:</b> Highest-value data source. Real-time POS feeds Kinesis for sub-second processing; inventory syncs hourly via Glue batch jobs with job bookmarks to prevent duplicates.<br><b>RFP: R1</b>"),
    dict(x=2.3,y=8.1,w=1.3,h=0.65,c=C["src"],label="Web / App",sub="Events · Reviews",
         hover="<b>Web & Mobile App</b><br><b>What:</b> customer_reviews_sample.csv plus clickstream events. Semi-structured (text, images). Highest velocity source.<br><b>Why:</b> Streamed via Kinesis for sub-second capture. Review text routed to Comprehend for automated NLP sentiment scoring — zero manual effort.<br><b>RFP: R1</b>"),
    dict(x=3.8,y=8.1,w=1.3,h=0.65,c=C["src"],label="CRM",sub="Customers · PII",
         hover="<b>CRM System</b><br><b>What:</b> customers_sample.csv — names, addresses, loyalty status. Contains PII.<br><b>Why:</b> Synced via AWS DMS with CDC (change data capture) — zero data loss at cutover. Lake Formation applies column-level masking before any Dev/Pre-Prod environment accesses this data.<br><b>RFP: R4, GDPR</b>"),
    dict(x=5.3,y=8.1,w=1.3,h=0.65,c=C["src"],label="External APIs",sub="Weather · Logistics",
         hover="<b>External APIs</b><br><b>What:</b> external_factors_sample.csv (weather, events, campaigns) and shipping_sample.csv. Lambda functions poll on EventBridge schedules.<br><b>Why:</b> New sources added as new Lambda functions — no impact on existing pipelines. Directly supports R7 Extensibility. Cost: near-zero (pay per invocation).<br><b>RFP: R7</b>"),
    dict(x=6.8,y=8.1,w=1.3,h=0.65,c=C["src"],label="3rd-Party Data",sub="Market signals",
         hover="<b>Third-Party Data (AWS Data Exchange)</b><br><b>What:</b> Licensed market, demographic, and competitive datasets from commercial providers via AWS marketplace.<br><b>Why:</b> Subscriptions deliver data directly to S3 with automatic license compliance tracking. Eliminates manual download/upload workflows. Supports R7 extensibility.<br><b>RFP: R7</b>"),
    dict(x=8.3,y=8.1,w=1.3,h=0.65,c=C["src"],label="SaaS / Files",sub="SFTP partners",
         hover="<b>SaaS / File Sources (AWS Transfer Family)</b><br><b>What:</b> Partners and legacy systems delivering data via SFTP/FTPS protocols.<br><b>Why:</b> Not all partners can call APIs. Transfer Family provides a managed SFTP endpoint that lands files directly in S3 — no server to manage. Complements Lambda connectors.<br><b>RFP: R3, R7</b>"),
    # ── Ingestion row y=6.7
    dict(x=0.9,y=6.7,w=1.4,h=0.65,c=C["ing"],label="Kinesis Streams",sub="Sub-second ingest",
         hover="<b>Amazon Kinesis Data Streams</b><br><b>What:</b> Managed real-time streaming. POS sales and web events flow through at sub-second latency.<br><b>Why:</b> Auto-scales to handle Fashion Week spikes without manual capacity planning. Directly replaces the daily cron job for real-time sources.<br><b>Cost:</b> Pay per shard-hour.<br><b>RFP: R1, R3</b>"),
    dict(x=2.5,y=6.7,w=1.4,h=0.65,c=C["ing"],label="Kinesis Firehose",sub="Stream → S3 Parquet",
         hover="<b>Kinesis Data Firehose</b><br><b>What:</b> Reads from Kinesis Streams and delivers micro-batches to S3 Raw Zone. Auto-converts to Parquet on the way.<br><b>Why:</b> Zero-server Parquet conversion reduces downstream query cost by 70%+ vs JSON. Also supports direct delivery to Redshift for hot data.<br><b>Cost:</b> Pay per GB ingested.<br><b>RFP: R1, R6</b>"),
    dict(x=4.1,y=6.7,w=1.4,h=0.65,c=C["ing"],label="AWS Glue ETL",sub="Batch pipelines",
         hover="<b>AWS Glue ETL</b><br><b>What:</b> Managed Spark replacing all cron-job scripts. Built-in job bookmarks prevent reprocessing. Visual Studio for non-Spark engineers.<br><b>Why:</b> Handles batch pipeline, Validate/Clean, and Normalize/Transform stages in one managed service. Cost: pay per DPU-hour (only when running).<br><b>RFP: R3, R5</b>"),
    dict(x=5.7,y=6.7,w=1.4,h=0.65,c=C["ing"],label="AWS Lambda",sub="API connectors",
         hover="<b>AWS Lambda</b><br><b>What:</b> Serverless functions triggered by EventBridge schedules to poll external APIs.<br><b>Why:</b> Each source is an independent function — adding a new data source means adding a new function with zero impact on existing pipelines. R7 extensibility by design.<br><b>Cost:</b> Essentially free at this scale.<br><b>RFP: R3, R7</b>"),
    dict(x=7.1,y=6.7,w=1.3,h=0.65,c=C["ing"],label="AWS DMS",sub="DB migration · CDC",
         hover="<b>AWS Database Migration Service</b><br><b>What:</b> One-time historical migration + ongoing CDC replication from on-premises DBs to S3.<br><b>Why:</b> Zero-downtime cutover. CDC keeps source and target in sync during transition — critical for migrating CRM without disrupting operations.<br><b>RFP: R3</b>"),
    dict(x=8.4,y=6.7,w=1.3,h=0.65,c=C["ing"],label="Data Exchange",sub="3rd-party licensed",
         hover="<b>AWS Data Exchange</b><br><b>What:</b> Managed marketplace for licensed third-party datasets — weather providers, market data, demographic enrichment.<br><b>Why:</b> Subscriptions deliver directly to S3 with automatic license compliance. Eliminates manual workflows. Supports R7 Interoperability.<br><b>RFP: R7</b>"),
    dict(x=9.7,y=6.7,w=1.3,h=0.65,c=C["ing"],label="Transfer Family",sub="SFTP / FTPS",
         hover="<b>AWS Transfer Family</b><br><b>What:</b> Fully managed SFTP/FTPS service providing a secure endpoint for partner file transfers, landing directly in S3.<br><b>Why:</b> Partners and legacy systems that cannot call APIs use this pathway. No file-transfer server to manage. Complements Lambda for non-API sources.<br><b>RFP: R3, R7</b>"),
    # ── Storage column (center)
    dict(x=4.7,y=5.2,w=2.4,h=0.75,c=C["raw"],label="S3 Raw Zone",sub="Bronze · immutable · all formats",
         hover="<b>S3 Raw Zone (Bronze)</b><br><b>What:</b> Immutable landing zone — data stored exactly as received from source. Never modified after write.<br><b>Why:</b> Full reprocessing possible if logic changes. Satisfies GDPR audit trail. Intelligent-Tiering auto-moves cold data to cheaper storage classes, cutting cost 60%+.<br><b>RFP: R1, R4, R6</b>"),
    dict(x=4.7,y=3.9,w=2.4,h=0.75,c=C["sil"],label="S3 Curated Zone",sub="Silver · validated · PII-masked",
         hover="<b>S3 Curated Zone (Silver)</b><br><b>What:</b> Cleaned, deduplicated, schema-validated Parquet. PII masked via Glue PII detection before Dev/Pre-Prod access.<br><b>Why:</b> Open Parquet format means Athena, Redshift Spectrum, and SageMaker all read it natively — no lock-in. PII masking ensures Dev never sees real customer data.<br><b>RFP: R2, R4, R5</b>"),
    dict(x=3.3,y=2.6,w=2.2,h=0.75,c=C["gld"],label="Amazon Redshift",sub="Gold · columnar DWH",
         hover="<b>Amazon Redshift</b><br><b>What:</b> Columnar data warehouse for pre-aggregated serving layer. Replaces daily Excel aggregation entirely.<br><b>Why:</b> Columnar storage makes QuickSight dashboards sub-second on billions of rows. RA3 nodes decouple compute/storage — scale each independently. Spectrum queries S3 directly without loading.<br><b>RFP: R1, R6</b>"),
    dict(x=6.1,y=2.6,w=2.0,h=0.75,c=C["dyn"],label="Amazon DynamoDB",sub="<10ms ML serving",
         hover="<b>Amazon DynamoDB</b><br><b>What:</b> NoSQL store for <10ms lookups needed by ML inference and real-time features.<br><b>Why:</b> Recommendation results and live inventory flags need millisecond response — impossible with Redshift. Pay-per-request keeps cost proportional to actual usage. Serves the future virtual shopping assistant.<br><b>RFP: R1, R7</b>"),
    # ── Governance column (right side)
    dict(x=8.5,y=5.0,w=1.8,h=0.65,c=C["gov"],label="Glue Data Catalog",sub="Metadata · Lineage",
         hover="<b>AWS Glue Data Catalog</b><br><b>What:</b> Central metadata store for all datasets. Integrates natively with Athena, Redshift Spectrum, SageMaker.<br><b>Why:</b> Self-service discovery — Alex's team finds any dataset without emailing Engineering. Schema evolution tracked automatically. This IS the 'Cataloging & Search' layer from the HLA.<br><b>RFP: R4, R5, R7</b>"),
    dict(x=8.5,y=4.2,w=1.8,h=0.65,c=C["proc"],label="MWAA (Airflow)",sub="Orchestration · DAGs",
         hover="<b>Amazon MWAA (Managed Airflow)</b><br><b>What:</b> Fully managed Apache Airflow. Replaces all cron jobs with DAG-based pipelines with dependency management, retry logic, SLA alerts.<br><b>Why:</b> Open-source Airflow core directly addresses Javier's vendor lock-in concern. One dashboard for every pipeline's health. Cost: instance-based, no per-task fees.<br><b>RFP: R3</b>"),
    dict(x=8.5,y=3.4,w=1.8,h=0.65,c=C["gov"],label="Glue Data Quality",sub="Validation · Alerts",
         hover="<b>AWS Glue Data Quality</b><br><b>What:</b> Automated validation rules after each pipeline — null checks, range validation, referential integrity, freshness thresholds.<br><b>Why:</b> Failures trigger CloudWatch alerts before bad data reaches Redshift or SageMaker. Quality scores tracked over time. Addresses R5 directly.<br><b>RFP: R5</b>"),
    dict(x=8.5,y=2.6,w=1.8,h=0.65,c=C["gov"],label="Lake Formation",sub="RBAC · GDPR",
         hover="<b>AWS Lake Formation</b><br><b>What:</b> Fine-grained RBAC at column and row level. Laura (InfoSec) defines centrally who sees what.<br><b>Why:</b> Junior analysts see masked customer data; data scientists get full access. Centralised GDPR compliance, data sharing agreements, and audit trails at query time.<br><b>RFP: R4, GDPR</b>"),
    dict(x=8.5,y=1.8,w=1.8,h=0.65,c=C["gov"],label="Amazon Macie",sub="PII scanning",
         hover="<b>Amazon Macie</b><br><b>What:</b> ML-powered PII scanner continuously monitoring S3 buckets for sensitive data from customers_sample.csv and sales_sample.csv.<br><b>Why:</b> Automated PII detection catches sensitive data that lands in the wrong zone before any human sees it. Findings routed to CloudWatch and Security Hub. GDPR compliance automation.<br><b>RFP: R4, GDPR</b>"),
    # ── Consumption row y=1.0
    dict(x=0.8,y=1.0,w=1.5,h=0.65,c=C["con"],label="Amazon Athena",sub="Serverless SQL",
         hover="<b>Amazon Athena</b><br><b>What:</b> Serverless interactive SQL directly on S3 — no data loading required.<br><b>Why:</b> Analysts run ad-hoc queries on Raw/Curated zones instantly without Engineering. Reads Glue Catalog automatically. Pay per TB scanned (~$5/TB).<br><b>RFP: R7 self-service</b>"),
    dict(x=2.6,y=1.0,w=1.5,h=0.65,c=C["con"],label="Amazon QuickSight",sub="BI dashboards",
         hover="<b>Amazon QuickSight</b><br><b>What:</b> Managed BI connected to Redshift and S3. Real-time interactive dashboards replacing daily Excel reports.<br><b>Why:</b> SPICE in-memory engine for sub-second queries. Pay-per-session vs traditional per-seat licensing cuts BI costs 60%+ at Manga's scale. ML anomaly detection built in.<br><b>RFP: R1, R6</b>"),
    dict(x=4.4,y=1.0,w=1.5,h=0.65,c=C["con"],label="Amazon SageMaker",sub="ML · Forecasting",
         hover="<b>Amazon SageMaker</b><br><b>What:</b> End-to-end ML: feature engineering, training, deployment, monitoring.<br><b>Why:</b> Four priority use cases: (1) product recommendations, (2) demand forecasting (DeepAR), (3) dynamic pricing, (4) return prediction. Feature Store integrates directly with the Curated Zone. ML is architecturally impossible today.<br><b>RFP: R1</b>"),
    dict(x=6.0,y=1.0,w=1.5,h=0.65,c=C["con"],label="Comprehend",sub="NLP sentiment",
         hover="<b>Amazon Comprehend</b><br><b>What:</b> Managed NLP sentiment analysis on customer_reviews_sample.csv text automatically.<br><b>Why:</b> Zero ML expertise required — fully managed API call. Outputs positive/negative/neutral scores per review. Feeds QuickSight dashboards for the merchandising team.<br><b>RFP: R1, ML use cases</b>"),
    dict(x=7.5,y=1.0,w=1.5,h=0.65,c=C["con"],label="API Gateway",sub="Partners · AI agents",
         hover="<b>API Gateway + Lambda</b><br><b>What:</b> Secure REST/GraphQL APIs exposing curated data to logistics partners, marketing platforms, and AI agents.<br><b>Why:</b> Explicitly required in RFP. Rate limiting, versioning, and API keys built in. Supports future data monetisation as a revenue stream. Backwards compatibility guaranteed via versioned contracts.<br><b>RFP: R7</b>"),
    dict(x=8.9,y=1.0,w=1.5,h=0.65,c=C["sec"],label="Carbon Footprint",sub="Sustainability R8",
         hover="<b>AWS Customer Carbon Footprint Tool</b><br><b>What:</b> Native tool tracking carbon emissions per service and region. Year-over-year comparison vs on-premises baseline.<br><b>Why:</b> Manga quantifies sustainability improvement for R8 compliance and ESG board reporting. Selecting EU (Ireland) / EU (Frankfurt) regions maximises renewable energy mix.<br><b>RFP: R8</b>"),
]

LLA_EDGES = [
    # Sources → Ingestion
    (0.8,7.77,0.9,7.03),(2.3,7.77,2.5,7.03),(3.8,7.77,4.1,7.03),
    (5.3,7.77,5.7,7.03),(6.8,7.77,7.1,7.03),(8.3,7.77,8.4,7.03),(9.2,8.1,9.7,7.03),
    # POS/Web → KDS (streaming path)
    (0.8,7.77,0.9,7.03),(2.3,7.77,0.9,7.03),
    # KDS → Firehose → Raw
    (0.9,6.37,2.5,6.37),(2.5,6.37,4.7,5.58),
    # Glue/Lambda/DMS/DEX/TRF → Raw
    (4.1,6.37,4.7,5.58),(5.7,6.37,4.7,5.58),(7.1,6.37,5.2,5.58),
    (8.4,6.37,5.5,5.58),(9.7,6.37,5.8,5.58),
    # Raw → Curated
    (4.7,4.82,4.7,4.28),
    # Curated → Redshift + DynamoDB
    (4.2,3.52,3.3,2.98),(5.2,3.52,6.1,2.98),
    # Governance → Curated
    (7.6,5.0,5.9,4.28),(7.6,3.4,5.9,4.08),(7.6,2.6,5.9,3.78),
    (7.6,4.2,4.1,6.7),  # MWAA → Glue ETL
    (7.6,1.8,5.9,3.62),  # Lake Formation → Curated
    (7.6,1.8,4.7,5.58),  # Macie → Raw (scan)
    # Consumption ← storage
    (3.3,2.22,2.6,1.33),(3.3,2.22,0.8,1.33),  # Redshift → QuickSight, Athena
    (4.7,3.52,4.4,1.33),(4.7,3.52,6.0,1.33),  # Curated → SageMaker, Comprehend
    (6.1,2.22,7.5,1.33),(6.1,2.22,8.9,1.33),  # DynamoDB → API Gateway, Carbon
    (4.4,0.67,7.5,0.67),  # SageMaker → API Gateway (serve results)
]

# ── SESSION STATE ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "overview"

# ── RAIL TOGGLE + FULLSCREEN BUTTONS (injected into parent page) ────────────
st.components.v1.html("""
<style>
  #mn-rail, #mn-fs {
    position:fixed; left:16px; z-index:999999;
    width:32px; height:32px;
    display:inline-flex; align-items:center; justify-content:center;
    padding:0; margin:0;
    background:rgba(20,20,20,0.75); color:rgba(255,255,255,0.85);
    border:1px solid rgba(255,255,255,0.12); border-radius:6px;
    cursor:pointer; opacity:0.65;
    backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px);
    transition:opacity 160ms, background 160ms, border-color 160ms,
               left 220ms cubic-bezier(.3,.7,.4,1), transform 120ms;
    font-family:inherit;
  }
  #mn-rail { top:16px; }
  #mn-fs   { top:54px; }
  #mn-rail:hover, #mn-fs:hover {
    opacity:1; background:rgba(45,45,45,0.92);
    border-color:rgba(255,255,255,0.24);
  }
  #mn-rail:active, #mn-fs:active { transform:scale(0.93); }
  #mn-rail svg, #mn-fs svg { width:18px; height:18px; pointer-events:none; }
  .fs-exit { display:none; }
</style>

<button id="mn-rail" title="Toggle sidebar">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"
       stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="4" width="18" height="16" rx="2"/>
    <line x1="9" y1="4" x2="9" y2="20"/>
  </svg>
</button>

<button id="mn-fs" title="Toggle fullscreen">
  <svg class="fs-enter" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
    <path d="M4 9V4h5"/><path d="M20 9V4h-5"/>
    <path d="M4 15v5h5"/><path d="M20 15v5h-5"/>
  </svg>
  <svg class="fs-exit" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
    <path d="M9 4v5H4"/><path d="M15 4v5h5"/>
    <path d="M9 20v-5H4"/><path d="M15 20v-5h5"/>
  </svg>
</button>

<script>
(function(){
  var doc = window.parent.document;

  // ── Move buttons into the parent page so they render at root level ──
  function mountButtons(){
    ['mn-rail','mn-fs'].forEach(function(id){
      var existing = doc.getElementById(id);
      if(existing) existing.remove();
      var el = document.getElementById(id);
      if(el){
        var clone = el.cloneNode(true);
        doc.body.appendChild(clone);
        // Copy styles too
        var styleEl = document.querySelector('style');
        if(styleEl && !doc.getElementById('mn-style')){
          var s = doc.createElement('style');
          s.id = 'mn-style';
          s.textContent = styleEl.textContent;
          doc.head.appendChild(s);
        }
      }
    });
    bindEvents();
  }

  function getSidebarBtn(){
    // When sidebar is OPEN: collapse button inside the sidebar
    return doc.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
           doc.querySelector('button[aria-label="Close sidebar"]') ||
           doc.querySelector('[data-testid="stSidebar"] button[kind="header"]');
  }
  function getExpandBtn(){
    // When sidebar is CLOSED: the expand arrow on the left edge
    return doc.querySelector('[data-testid="collapsedControl"]') ||
           doc.querySelector('button[aria-label="Open sidebar"]');
  }
  function isSidebarOpen(){
    var sb = doc.querySelector('[data-testid="stSidebar"]');
    if(!sb) return false;
    return sb.getBoundingClientRect().width > 40;
  }

  function syncPosition(){
    // Pin both controls to the far-left top, regardless of sidebar state
    var rail = doc.getElementById('mn-rail');
    var fs   = doc.getElementById('mn-fs');
    if(rail) rail.style.left = '16px';
    if(fs)   fs.style.left   = '16px';
  }

  function syncFs(){
    var fs = doc.getElementById('mn-fs');
    if(!fs) return;
    var on = !!(doc.fullscreenElement || doc.webkitFullscreenElement);
    fs.querySelector('.fs-enter').style.display = on ? 'none' : '';
    fs.querySelector('.fs-exit').style.display  = on ? '' : 'none';
  }

  function bindEvents(){
    var rail = doc.getElementById('mn-rail');
    var fs   = doc.getElementById('mn-fs');
    if(!rail || !fs) return;

    rail.onclick = function(){
      if(isSidebarOpen()){
        var btn = getSidebarBtn();
        if(btn){ btn.click(); return; }
      } else {
        var btn = getExpandBtn();
        if(btn){ btn.click(); return; }
      }
    };

    fs.onclick = function(){
      var el = doc.documentElement;
      if(doc.fullscreenElement || doc.webkitFullscreenElement){
        (doc.exitFullscreen || doc.webkitExitFullscreen).call(doc);
      } else {
        (el.requestFullscreen || el.webkitRequestFullscreen).call(el);
      }
    };
  }

  doc.addEventListener('fullscreenchange', syncFs);
  doc.addEventListener('webkitfullscreenchange', syncFs);

  // Mount on load and re-sync periodically (Streamlit re-renders wipe DOM)
  mountButtons();
  setInterval(function(){
    if(!doc.getElementById('mn-rail')) mountButtons();
    syncPosition();
    syncFs();
  }, 600);
})();
</script>
""", height=1)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
NAV_PAGES = [
    ("Overview",           "overview"),
    ("High-Level Arch",    "hla"),
    ("Low-Level Arch",     "lla"),
    ("Data Sources",       "data"),
    ("Requirements",       "reqs"),
    ("Use Cases",          "usecases"),
]

with st.sidebar:
    st.markdown(f"""
    <div style="padding:48px 0 24px;text-align:left;">
      <div style="font-size:11px;font-weight:800;color:{INK};letter-spacing:.08em;
                  text-transform:uppercase;margin-bottom:2px;">Manga Cloud</div>
      <div style="font-size:10px;color:{INK_F};letter-spacing:.06em;text-transform:uppercase;">
        RFP Response · AWS
      </div>
    </div>""", unsafe_allow_html=True)

    for label, key in NAV_PAGES:
        active = st.session_state.page == key
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True, type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.markdown(f"""
    <div style="position:absolute;bottom:20px;left:0;right:0;padding:0 16px;
                font-size:10px;color:{INK_F};line-height:1.7;">
      IE University · MBD-EN2025<br>
      Cloud Analytics · Group B<br>
      Due: June 19, 2026
    </div>""", unsafe_allow_html=True)

PAGE = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if PAGE == "overview":
    st.markdown('<div class="page-title">Cloud Data Platform for Manga</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">AWS-powered modernisation proposal — replacing legacy cron-ETL with a real-time, scalable data lakehouse</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="spotlight">
      <div class="sl-eyebrow">The proposal in three moves</div>
      <div class="sl-pillars">Unify &nbsp;·&nbsp; Accelerate &nbsp;·&nbsp; Enable</div>
      <div class="sl-sub">One governed AWS lakehouse for every data source · time-to-insight cut from 24 hours to sub-second · ML-powered recommendations, dynamic pricing and demand forecasting that are impossible today.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    for col,(val,lbl) in zip([c1,c2,c3,c4],[("€280M","Annual Revenue"),("+3.5%","Growth vs market"),("100+","Physical Stores"),("2×","Cost vs Competitors")]):
        col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])
    with left:
        st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="card"><p style="font-size:13px;color:{INK_M};line-height:1.8;margin:0">
        Manga's current architecture — independent ETL pipelines triggered by cron jobs, aggregating into daily Excel files — is incompatible with real-time, AI-driven retail.<br><br>
        Our proposal delivers a <strong style="color:{INK}">cloud-native AWS data lakehouse</strong> on three pillars:
        <strong style="color:{ACCENT}">Unify</strong> all data sources into a single governed platform,
        <strong style="color:{INK}">Accelerate</strong> time-to-insight from 24 hours to sub-second, and
        <strong style="color:{INK}">Enable</strong> ML-powered features — recommendations, dynamic pricing, demand forecasting — impossible today.
        </p></div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:16px">Problem: As-Is Architecture</div>', unsafe_allow_html=True)
        for title,desc in [
            ("Daily batch cron jobs","No real-time capability. Managers make decisions on yesterday's data."),
            ("Siloed ETL pipelines","Each pipeline built by a different team. No shared standards or observability."),
            ("Excel as the BI layer","Manual aggregation into Excel files. No self-service, no drill-down."),
            ("2× competitor infrastructure cost","Colocation model costs twice as much for half the analytical output."),
            ("GDPR exposure","Previous InfoSec Manager dismissed after a major security incident. Compliance status unclear."),
        ]:
            st.markdown(f'<div class="card" style="padding:13px 18px;margin-bottom:8px;border-left:2px solid {HAIR}"><strong style="color:{INK};font-size:12.5px;letter-spacing:-.2px">{title}</strong><p style="font-size:11.5px;color:{INK_M};margin:5px 0 0">{desc}</p></div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">Key Stakeholders</div>', unsafe_allow_html=True)
        for name,role,concern,stype,tag in [
            ("Marta Ríos","COO · 25 yrs","Wants end-to-end solution with solid business case. Results over ideology.","champion","Champion"),
            ("Javier Medina","CTO · 15 yrs","Fears vendor lock-in. Champions open-source and modular systems.","skeptic","Skeptic"),
            ("Manuel Ortega","CFO · 25 yrs","Alarmed by 2× cost vs competitors. Open to change if ROI is clear.","neutral","Cost-focused"),
            ("Laura Smith","InfoSec Manager","New hire with GDPR mandate. Security non-negotiable after prior incident.","skeptic","Security-first"),
            ("Alex Lee","Head of Data & AI","Joined from competitor. Knows the current architecture is broken.","champion","Champion"),
        ]:
            st.markdown(f'<div class="stk-card"><div class="stk-name">{name} <span class="stk-tag stk-{stype}">{tag}</span></div><div class="stk-role">{role}</div><div class="stk-concern">{concern}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Core Value Drivers</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i,(title,desc) in enumerate([
        ("Real-Time Everything","Replace all daily-batch pipelines with Kinesis streaming. Sub-second POS, web events, and inventory updates."),
        ("Open & Modular","Apache Airflow (MWAA), open Parquet/Delta formats, Terraform IaC. No proprietary lock-in — directly addresses the CTO's concern."),
        ("Security by Design","Lake Formation RBAC, Macie PII scanning, KMS at rest, TLS 1.3 in-transit, CloudTrail GDPR audit logs — built in from day one."),
        ("ML-Ready Platform","SageMaker Feature Store connected to the Curated Zone. Recommendations, forecasting, and dynamic pricing from day one."),
        ("Measurable Cost Savings","Pay-per-use vs fixed colocation. S3 Intelligent-Tiering, Spot Instances — projected 40–60% infrastructure cost reduction."),
        ("Sustainability Metrics","AWS Carbon Footprint Tool tracks emissions by service/region — quantifiable ESG improvement vs colocation for R8 compliance."),
    ]):
        with cols[i % 3]:
            st.markdown(f'<div class="card" style="min-height:152px"><div style="font-family:var(--font-display);font-size:13px;font-weight:600;color:{INK_F};letter-spacing:.04em;margin-bottom:12px">0{i+1}</div><div style="font-size:14px;font-weight:600;color:{INK};margin-bottom:7px;letter-spacing:-.3px">{title}</div><div style="font-size:11.5px;color:{INK_M};line-height:1.65">{desc}</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HIGH-LEVEL ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "hla":
    st.markdown('<div class="page-title">High-Level Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Technology-agnostic conceptual design — architectural process layers without vendor specifics (RFP Section 2)</div>', unsafe_allow_html=True)

    if not render_figma_architecture(HLA_IMAGE_CANDIDATES, "Manga Cloud Platform High-Level Architecture"):
        st.info("**Hover** over any node to see its role, design rationale, and which RFP requirements it covers.")
        fig_hla = arch_fig(
            "High-Level Architecture — Hover any node for details",
            HLA_NODES, HLA_EDGES,
            xr=[-0.2, 9.0], yr=[0.2, 8.0], h=620
        )
        st.plotly_chart(fig_hla, use_container_width=True)

        # Layer legend
        st.markdown("---")
        cols = st.columns(9)
        for col, (lbl, (fc, bc)) in zip(cols, [
            ("Data Sources", C["src"]), ("Ingestion", C["ing"]),
            ("Cataloging", C["cat"]), ("Processing", C["proc"]),
            ("Raw Zone", C["raw"]), ("Cleaned Zone", C["sil"]),
            ("Curated Zone", C["gld"]), ("Consumption", C["con"]),
            ("Security", C["sec"]),
        ]):
            col.markdown(f'<div style="background:{fc};border:1px solid {bc};border-radius:6px;padding:6px 8px;text-align:center;font-size:9px;font-weight:600;color:#c8d8f0;letter-spacing:.03em">{lbl}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOW-LEVEL ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "lla":
    st.markdown('<div class="page-title">Low-Level AWS Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Specific AWS services mapped to every Manga data source and use case (RFP Section 3)</div>', unsafe_allow_html=True)

    if not render_figma_architecture(LLA_IMAGE_CANDIDATES, "Manga Cloud Platform Low-Level AWS Architecture"):
        st.info("**Hover** over any service node to see rationale, cost model, and which RFP requirement (R1–R8) it addresses.")
        fig_lla = arch_fig(
            "Low-Level AWS Architecture — Hover any node for details",
            LLA_NODES, LLA_EDGES,
            xr=[-0.3, 11.2], yr=[0.3, 10.2], h=700
        )
        st.plotly_chart(fig_lla, use_container_width=True)

        # Layer legend
        st.markdown("---")
        cols = st.columns(9)
        for col, (lbl, (fc, bc)) in zip(cols, [
            ("Sources", C["src"]), ("Ingestion", C["ing"]),
            ("Raw Zone", C["raw"]), ("Curated Zone", C["sil"]),
            ("Gold / DWH", C["gld"]), ("NoSQL", C["dyn"]),
            ("Governance", C["gov"]), ("Consumption", C["con"]),
            ("Security", C["sec"]),
        ]):
            col.markdown(f'<div style="background:{fc};border:1px solid {bc};border-radius:6px;padding:6px 8px;text-align:center;font-size:9px;font-weight:600;color:#c8d8f0;letter-spacing:.03em">{lbl}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DATA SOURCES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "data":
    st.markdown('<div class="page-title">Data Sources</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Manga\'s 6 sample datasets — schema, quality profile, and ingestion strategy (RFP Appendix III)</div>', unsafe_allow_html=True)

    meta = {
        "Sales":{"source":"POS System & E-commerce","ingestion":"Kinesis → Firehose → S3","pattern":"Streaming (real-time)","pii":False,"use_cases":["Revenue tracking","Dynamic pricing","Customer behaviour modelling"],"desc":"Transactional records: datetime, customer/product/store IDs, payment method, purchase price, and applied discount."},
        "Customers":{"source":"CRM & Loyalty Program","ingestion":"AWS DMS → Glue → S3","pattern":"Batch (daily sync)","pii":True,"use_cases":["Segmentation","Personalisation","Lifecycle analysis"],"desc":"Demographic data: full name, age, gender, address, zip, loyalty status. Contains PII — column masking applied in Curated zone."},
        "Inventory":{"source":"ERP / WMS","ingestion":"Glue ETL → S3","pattern":"Batch (hourly)","pii":False,"use_cases":["Supply chain optimisation","Stock alerts","Pricing strategy"],"desc":"Current stock levels per product per store, current price, and product description."},
        "Customer Reviews":{"source":"Website / Mobile App","ingestion":"Kinesis → Firehose → S3 + Comprehend","pattern":"Streaming (event-driven)","pii":True,"use_cases":["Sentiment analysis","Product improvement","Trust metrics"],"desc":"Review text, star rating, image binaries, customer and product IDs, timestamp."},
        "External Factors":{"source":"Weather API + Internal","ingestion":"Lambda → S3","pattern":"Batch (daily pull)","pii":False,"use_cases":["Demand forecasting","Campaign evaluation","Pricing context"],"desc":"Daily context: weather, fuel price, bank holiday, local event, campaign ID, aggregated sales/volume."},
        "Shipping":{"source":"Logistics Partner API","ingestion":"Lambda → Glue → S3","pattern":"Batch (daily)","pii":True,"use_cases":["Delivery performance","Return analysis","Cost efficiency"],"desc":"Order ID, delivery address, estimated/actual delivery time, delivery price, actual cost, return status."},
    }
    for ds_name, ds in meta.items():
        df = DATA.get(ds_name)
        with st.expander(f"**{ds_name}**  —  {ds['desc'][:70]}...", expanded=False):
            c1,c2,c3 = st.columns(3)
            c1.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:14px;padding-top:6px;letter-spacing:-.3px">{ds["source"]}</div><div class="metric-label">Source System</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:14px;padding-top:6px;letter-spacing:-.3px">{ds["pattern"]}</div><div class="metric-label">Ingestion Pattern</div></div>', unsafe_allow_html=True)
            pii_c = "#c8893a" if ds['pii'] else INK_M
            pii_t = "Contains PII" if ds['pii'] else "No PII"
            c3.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:14px;color:{pii_c};padding-top:6px;letter-spacing:-.3px">{pii_t}</div><div class="metric-label">Data Sensitivity</div></div>', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:11px;color:{INK_M};margin:8px 0 4px'><b>AWS Path:</b> <code>{ds['ingestion']}</code></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:11px;color:{INK_M};margin-bottom:10px'>{ds['desc']}</div>", unsafe_allow_html=True)
            st.markdown("".join([f'<span class="badge badge-blue">{uc}</span>' for uc in ds['use_cases']]), unsafe_allow_html=True)
            if df is not None:
                st.dataframe(df.head(10), use_container_width=True, hide_index=True)
                st.markdown(f"<div style='font-size:10px;color:{INK_F};margin-top:4px'>Showing 10 of {len(df)} rows · {len(df.columns)} columns</div>", unsafe_allow_html=True)
            else:
                st.warning(f"Sample CSV not found for {ds_name}. Place the CSV in the same folder as the app.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REQUIREMENTS COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "reqs":
    st.markdown('<div class="page-title">Requirements Coverage</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">How each of the 8 RFP requirements (R1–R8) is addressed by the proposed AWS architecture</div>', unsafe_allow_html=True)

    reqs = [
        ("R1","Unified Multi-modal Data Platform",
         "Streaming (Kinesis) + batch (Glue) pipelines. S3 Lakehouse stores structured (Parquet), semi-structured (JSON), and unstructured (images). Single Glue Catalog provides unified access. Athena enables serverless SQL directly on S3.",
         ["Kinesis Streams","Kinesis Firehose","AWS Glue ETL","S3 Lakehouse","Amazon Redshift","Amazon Athena"]),
        ("R2","Multi-Environment Setup",
         "AWS Organizations provisions Dev / Pre-Prod / Prod from identical Terraform templates. Anonymised production samples (via Glue PII masking + Lake Formation) automatically replicated to non-prod. Dev engineers never see real PII.",
         ["AWS Organizations","Terraform/CDK","Lake Formation (PII masking)","S3 Cross-Account Replication"]),
        ("R3","Automation & IaC",
         "Infrastructure-as-Code via Terraform/CDK. MWAA (Managed Airflow) replaces all cron jobs with DAG-based orchestration. Glue job bookmarks, EventBridge schedules, and S3 lifecycle policies automate the full data lifecycle.",
         ["Terraform / AWS CDK","Amazon MWAA (Airflow)","AWS Glue (job bookmarks)","EventBridge schedules"]),
        ("R4","Security & High Availability",
         "IAM least-privilege + KMS encryption at rest. TLS 1.3 enforced in-transit (TLS termination at service boundaries — allows platform-side analytics while keeping every hop encrypted). Lake Formation column/row RBAC. Macie PII scanning. CloudTrail GDPR audit logs. VPC network isolation. Multi-AZ deployments. Target: 99.9% uptime.",
         ["IAM + AWS KMS (at rest)","TLS 1.3 in-transit","AWS Lake Formation","Amazon Macie","AWS CloudTrail (GDPR audit)","Amazon VPC","Multi-AZ deployments"]),
        ("R5","Data Quality",
         "AWS Glue Data Quality rules after each pipeline: null constraints, range validation, referential integrity (sales ↔ inventory ↔ customers), freshness thresholds. Failures trigger CloudWatch/SNS alerts before bad data reaches downstream consumers.",
         ["AWS Glue Data Quality","CloudWatch Alerts","Glue Data Catalog (schema)","SNS Notifications"]),
        ("R6","Cost Optimisation",
         "Pay-per-use vs fixed colocation. S3 Intelligent-Tiering auto-archives cold data. Spot Instances for non-critical Glue jobs. Redshift Reserved Instances. QuickSight pay-per-session. Athena pay-per-query. Projected 40–60% infrastructure cost reduction.",
         ["S3 Intelligent-Tiering","Spot Instances (Glue)","Redshift Reserved Instances","QuickSight pay-per-session","Athena pay-per-query"]),
        ("R7","Extensibility & Interoperability",
         "Decoupled Lambda connectors add new sources without touching existing pipelines. AWS Data Exchange for licensed 3rd-party data. Transfer Family for SFTP partners. API Gateway exposes curated data to partners and AI agents. Open Parquet format prevents lock-in.",
         ["API Gateway + Lambda","AWS Data Exchange","AWS Transfer Family","Open Parquet / Delta","Glue Catalog (schema registry)"]),
        ("R8","Sustainability",
         "AWS data centres operate with high renewable energy usage. EU (Ireland) / EU (Frankfurt) regions maximise green energy mix. AWS Customer Carbon Footprint Tool provides quantitative emissions dashboard vs on-premises colocation baseline for ESG board reporting.",
         ["AWS Carbon Footprint Tool","Green regions (EU-WEST-1)","Serverless (Lambda, Firehose, Athena)","Auto-scaling (no idle resources)"]),
    ]
    for rid,title,desc,svcs in reqs:
        st.markdown(f"""
        <div class="card" style="margin-bottom:10px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
            <div>
              <span style="font-family:var(--font-display);font-size:14px;font-weight:600;color:{INK_F}">{rid}</span>
              <span style="font-size:14px;font-weight:600;color:{INK};margin-left:10px;letter-spacing:-.3px">{title}</span>
            </div>
            <span style="font-size:10px;font-weight:500;color:{INK_M};background:{SURF2};border:1px solid {HAIR};padding:4px 11px 4px 9px;border-radius:100px;display:inline-flex;align-items:center;gap:7px">
              <span style="width:6px;height:6px;border-radius:50%;background:{ACCENT};display:inline-block"></span>Fully Covered</span>
          </div>
          <p style="font-size:11.5px;color:{INK_M};line-height:1.65;margin-bottom:10px">{desc}</p>
          <div>{"".join([f'<span class="badge">{s}</span>' for s in svcs])}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Coverage Summary</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=[r[0] for r in reqs], y=[100]*8,
        marker_color=SURF2, marker_line_color=ACCENT, marker_line_width=1.5,
        text=["100%"]*8, textposition="inside",
        textfont=dict(color=INK, size=12, family="Inter"),
    ))
    fig.update_layout(
        plot_bgcolor=CANVAS, paper_bgcolor=CANVAS,
        font=dict(color=INK_M, family="Inter"),
        xaxis=dict(gridcolor=HAIR, title="Requirement"),
        yaxis=dict(gridcolor=HAIR, title="Coverage %", range=[0,120]),
        height=260, margin=dict(l=40,r=20,t=20,b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: USE CASES
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "usecases":
    st.markdown('<div class="page-title">ML Use Cases</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Five end-to-end use cases showing the architecture in action with Manga\'s actual data sources (RFP Section 5)</div>', unsafe_allow_html=True)

    ucs = [
        {"id":"UC1","title":"Product Recommendation Engine",
         "datasets":["Sales","Customers","Inventory"],
         "aws":["SageMaker (collaborative filtering)","DynamoDB (serving)","API Gateway","Kinesis (real-time signals)"],
         "desc":"Collaborative filtering model trained on purchase history and customer profiles. Real-time inference via SageMaker endpoint, results cached in DynamoDB for <10ms response. Exposed via API Gateway to the e-commerce front-end and virtual shopping assistant.",
         "impact":"+12–18% avg order value","pipeline":"sales + customers → S3 Curated → SageMaker training → DynamoDB → API Gateway → Website"},
        {"id":"UC2","title":"Demand Forecasting",
         "datasets":["Sales","External Factors","Inventory"],
         "aws":["SageMaker DeepAR","AWS Glue (feature engineering)","QuickSight (dashboard)","MWAA (weekly retrain DAG)"],
         "desc":"Time-series forecasting using SageMaker DeepAR on sales history enriched with external context — weather, bank holidays, local events, fuel prices. Model retrains weekly via MWAA DAG. Forecasts feed inventory replenishment decisions.",
         "impact":"−30% stockouts, −20% overstock write-offs","pipeline":"sales + external_factors → Glue feature engineering → SageMaker DeepAR → QuickSight"},
        {"id":"UC3","title":"Sentiment-Driven Merchandising",
         "datasets":["Customer Reviews"],
         "aws":["Amazon Comprehend (NLP)","AWS Glue (aggregation)","Amazon QuickSight","SNS (alerts on score drops)"],
         "desc":"Comprehend processes review text in near real-time, assigning sentiment scores per review. Glue aggregates scores by product, store, and week. QuickSight surfaces products with declining sentiment, alerting the buying team before damage compounds.",
         "impact":"2–3 weeks earlier product decisions","pipeline":"customer_reviews → Kinesis → Comprehend → S3 Curated → Glue aggregation → QuickSight + SNS"},
        {"id":"UC4","title":"Dynamic Pricing Engine",
         "datasets":["Sales","Inventory","External Factors"],
         "aws":["SageMaker (regression model)","Kinesis (real-time inventory)","Lambda (pricing guardrails)","DynamoDB (price store)"],
         "desc":"ML model trained on price elasticity, current inventory, competitor signals, and contextual factors. Lambda function compares model output against pricing guardrails before writing to DynamoDB, which feeds the POS and e-commerce pricing layer.",
         "impact":"+3–7% gross margin improvement","pipeline":"sales + inventory + external_factors → SageMaker → Lambda (guardrails) → DynamoDB → POS / E-commerce"},
        {"id":"UC5","title":"Return Rate & Logistics Optimisation",
         "datasets":["Shipping","Sales","Customers"],
         "aws":["SageMaker (binary classification)","Glue (join pipeline)","QuickSight (ops dashboard)","SNS (high-return alerts)"],
         "desc":"Binary classifier predicts return likelihood at purchase time using delivery history, customer return-rate profile, and product attributes. High-risk orders trigger proactive interventions. Logistics cost variance tracked in QuickSight.",
         "impact":"−10–15% return processing costs","pipeline":"shipping + sales + customers → Glue join → SageMaker classifier → SNS alerts + QuickSight ops dashboard"},
    ]
    for uc in ucs:
        with st.expander(f"**{uc['id']}**  —  {uc['title']}", expanded=False):
            col1, col2 = st.columns([3,2])
            with col1:
                st.markdown(f"""
                <div style="font-size:12px;color:{INK_M};line-height:1.75;margin-bottom:12px">{uc['desc']}</div>
                <div style="background:{SURF1};border:1px solid {HAIR};border-radius:10px;padding:11px 14px;font-size:10.5px;color:{ACCENT};font-family:monospace;line-height:1.8">
                  <strong style="color:{INK_M};font-family:var(--font-body)">Pipeline</strong><br>{uc['pipeline']}
                </div>
                <div style="margin-top:10px;padding:11px 14px;background:{SURF2};border:1px solid {HAIR};border-radius:10px;font-size:11.5px;color:{INK}">
                  <strong style="color:{INK_M}">Business Impact:</strong> {uc['impact']}
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="section-title">Data Sources</div>', unsafe_allow_html=True)
                for ds in uc['datasets']:
                    st.markdown(f'<span class="badge">{ds}</span>', unsafe_allow_html=True)
                st.markdown('<div class="section-title" style="margin-top:14px">AWS Services</div>', unsafe_allow_html=True)
                for svc in uc['aws']:
                    st.markdown(f'<span class="badge" style="display:block;margin:3px 0;text-align:left">{svc}</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Dataset Usage Matrix</div>', unsafe_allow_html=True)
    matrix = {
        "Use Case":["Recommendations","Demand Forecast","Sentiment","Dynamic Pricing","Return Optimisation"],
        "Sales":[1,1,0,1,1],"Customers":[1,0,0,0,1],"Inventory":[1,1,0,1,0],
        "Customer Reviews":[0,0,1,0,0],"External Factors":[0,1,0,1,0],"Shipping":[0,0,0,0,1],
    }
    hm = pd.DataFrame(matrix).set_index("Use Case")
    fig2 = px.imshow(hm, color_continuous_scale=[[0,SURF1],[1,"#13335a"]], aspect="auto")
    fig2.update_traces(
        text=hm.map(lambda v:"✓" if v else ""),
        texttemplate="%{text}", textfont=dict(size=16,color=ACCENT),
    )
    fig2.update_layout(
        plot_bgcolor=CANVAS, paper_bgcolor=CANVAS,
        font=dict(color=INK_M, family="Inter"),
        coloraxis_showscale=False, height=260,
        margin=dict(l=160,r=20,t=20,b=60), xaxis=dict(side="bottom"),
    )
    st.plotly_chart(fig2, use_container_width=True)
