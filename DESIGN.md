# DESIGN.md — Manga Cloud Platform Design System

> **Source:** [Framer Design System (awesome-design-md)](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/framer)
> **ALL team members must follow this file.** Every UI change to the Streamlit app,
> Figma boards, or any other visual output must use the tokens defined here.
> Consistency across devices and contributors depends on it.

---

## Why This Exists

This project is built by multiple people across different devices. Without a shared design
reference, the app will drift — mismatched grays, inconsistent padding, different font sizes
per contributor. This file fixes that. When in doubt about any visual decision, check here first.

---

## Design Philosophy

We use a **dark-canvas system** inspired by Framer's marketing site:

- The page background is **near-black** (`#0a0e1a`) — this IS the whitespace
- All type on canvas is **white or light blue-gray** — never colored text
- A **single accent color** (`#4a9af0` blue) is reserved for interactive elements and highlights only
- Cards are **dark charcoal lifts** above the canvas — hierarchy through surface depth, not color
- Gradient/accent colors are used **sparingly** — one or two highlights per section, never as backgrounds

This is a professional data platform proposal, not a colorful dashboard. The dark, confident
aesthetic signals technical credibility to the Manga stakeholders.

---

## Color Tokens

```
/* Canvas & Surfaces */
--canvas:       #0a0e1a   /* Page background — use everywhere as the base */
--surface-1:    #111827   /* Cards, expanders, sidebar */
--surface-2:    #182235   /* Hover states, active cards */
--surface-3:    #0d1220   /* Sidebar background */

/* Borders */
--hairline:     #1e2d45   /* Default card borders */
--hairline-soft:#1a2840   /* Subtle dividers */
--hairline-active: #3a6ab0 /* Hover/active border */

/* Text */
--ink:          #c8d8f0   /* Primary text — headings, card titles */
--ink-body:     #a0b8c8   /* Body text — descriptions, paragraphs */
--ink-muted:    #6a8aaa   /* Secondary text — labels, meta, captions */
--ink-faint:    #3a5a7a   /* Disabled, placeholder, decorative */

/* Accent (use sparingly — interactive elements only) */
--accent:       #4a9af0   /* Links, active nav, key highlights */
--accent-dark:  #1a3860   /* Accent backgrounds */
--accent-border:#2a5a90   /* Accent borders */

/* Semantic */
--success:      #50c880   /* Covered, positive states */
--success-bg:   #0a1e14   /* Success card backgrounds */
--success-border:#1a4828  /* Success borders */
--warning:      #f0a040   /* Skeptic, cost flags */
--warning-bg:   #2a1800   /* Warning card backgrounds */
--warning-border:#5a3000  /* Warning borders */
--danger:       #f07070   /* Problems, errors */
--danger-bg:    #1e0a0a   /* Danger card backgrounds */
--danger-border:#5a2020   /* Danger borders */

/* Gradient accents (for architecture node highlights — use max 2 per view) */
--gradient-blue:   #4a9af0
--gradient-purple: #b070f0
--gradient-green:  #50c880
--gradient-orange: #f0a040
```

### In Streamlit CSS

Use these as the values in the `st.markdown()` CSS block at the top of `mango_cloud_platform.py`:

```css
/* Already implemented — do not change these values */
background-color: #0a0e1a;   /* --canvas */
background: #111827;          /* --surface-1 (cards) */
background: #0d1220;          /* --surface-3 (sidebar) */
border: 1px solid #1e2d45;   /* --hairline */
color: #c8d8f0;               /* --ink */
color: #6a8aaa;               /* --ink-muted */
color: #4a9af0;               /* --accent */
```

### In Figma / FigJam

When editing the FigJam boards, use these exact hex values. Do not use Figma's default palette.

---

## Typography

We use **Inter** (available via Google Fonts) as our body typeface throughout.
GT Walsheim from the source design system is not available for free — Inter is the approved substitute.

### Type Scale

| Role | Size | Weight | Letter Spacing | Use in app |
|---|---|---|---|---|
| Page Title | 22px | 800 | -0.3px | `.page-title` — top of every page |
| Section Title | 11px | 700 | +1.2px | `.section-title` — uppercase labels |
| Card Title | 13px | 700 | -0.1px | Component headings inside cards |
| Metric Value | 28px | 800 | 0 | KPI numbers on Overview page |
| Body | 13px | 400 | -0.1px | Card descriptions, paragraphs |
| Body Small | 11px | 400 | 0 | Secondary descriptions, meta |
| Caption | 10px | 400 | +0.8px | Uppercase labels, badge text |
| Badge | 10px | 700 | +0.8px | `.badge` pills |
| Code / Path | 11px | 400 | 0 | `monospace` — pipeline paths |

### Applied in Streamlit CSS

```css
/* Page title */
.page-title  { font-size: 22px; font-weight: 800; color: #c8d8f0; }

/* Section label */
.section-title {
  font-size: 11px; font-weight: 700; letter-spacing: .12em;
  text-transform: uppercase; color: #4a6a9a;
}

/* Metric */
.metric-value { font-size: 28px; font-weight: 800; color: #4a9af0; }
.metric-label { font-size: 11px; color: #6a8aaa; letter-spacing: .08em; text-transform: uppercase; }

/* Badge */
.badge { font-size: 10px; font-weight: 700; padding: 3px 9px; border-radius: 20px; }
```

---

## Spacing

Based on a **5px base unit** (matching the Framer source system).

| Token | Value | Use |
|---|---|---|
| `xxs` | 4px | Tight badge padding, icon gaps |
| `xs` | 8px | Between inline elements |
| `sm` | 12px | Card internal gaps |
| `md` | 15px | Default card padding |
| `lg` | 20px | Section gaps, card padding |
| `xl` | 30px | Between major sections |
| `section` | 40–60px | Between page sections |

### In Streamlit

```css
/* Card padding */
.card { padding: 18px 20px; margin-bottom: 12px; }

/* Metric card */
.metric-card { padding: 16px; }

/* Stakeholder card */
.stk-card { padding: 14px 16px; margin-bottom: 10px; }
```

---

## Border Radius

| Token | Value | Use |
|---|---|---|
| `xs` | 4px | Tiny chips |
| `sm` | 6px | Badges, inline tags |
| `md` | 8px | Architecture diagram boxes |
| `lg` | 10px | Cards, panels |
| `pill` | 20px | Rounded button-style elements |
| `full` | 9999px | Circular icons |

```css
/* Cards */
border-radius: 10px;  /* --lg — default for all .card elements */

/* Badges */
border-radius: 20px;  /* --pill — all .badge elements */

/* Architecture diagram boxes */
border-radius: 8px;   /* --md — HTML diagram boxes */
```

---

## Component Patterns

### Cards

Every card in the app follows this pattern — do not deviate:

```css
.card {
  background: #111827;          /* --surface-1 */
  border: 1px solid #1e2d45;   /* --hairline */
  border-radius: 10px;
  padding: 18px 20px;
  margin-bottom: 12px;
  transition: border-color .2s;
}
.card:hover {
  border-color: #3a6ab0;        /* --hairline-active */
}
```

**Accent-top cards** (value drivers, requirement cards) add a colored top border:
```css
border-top: 3px solid {accent-color};
```

Accent colors for top borders: use `--accent` (#4a9af0), `--success` (#50c880),
`--warning` (#f0a040), or `--gradient-purple` (#b070f0) only. Never use raw CSS colors.

### Badges / Pills

```css
/* Blue (default — AWS services, data info) */
.badge-blue   { background:#0a1830; color:#60a8f0; border:1px solid #1a3860; }

/* Green (covered, positive) */
.badge-green  { background:#0a1e14; color:#50c880; border:1px solid #1a4828; }

/* Orange (warnings, costs, skeptic) */
.badge-orange { background:#2a1800; color:#f0a040; border:1px solid #5a3000; }

/* Purple (ML, AI) */
.badge-purple { background:#1a0a28; color:#b070f0; border:1px solid #3a1858; }

/* Red (problems, security risks) */
.badge-red    { background:#1e0a0a; color:#f07070; border:1px solid #5a2020; }
```

**When to use each:**
- Blue → default, AWS service names, dataset names, neutral info
- Green → covered requirements, positive outcomes, open-source
- Orange → RFP requirements, cost flags, skeptic stakeholders, warnings
- Purple → ML/AI use cases, SageMaker, Comprehend
- Red → problems, current pain points, security incidents

### Stakeholder Cards

```css
.stk-champion { background:#0a1e14; color:#50c880; }  /* Marta, Alex */
.stk-skeptic  { background:#2a1800; color:#f0a040; }  /* Javier, Laura */
.stk-neutral  { background:#0a1830; color:#60a8f0; }  /* Manuel */
```

### Navigation (Sidebar)

Active nav item:
```css
background: #1a2840;
color: #4a9af0;
border-radius: 8px;
```

Inactive: no background, `color: #a0b8d8`.

---

## Plotly Chart Styling

All Plotly charts in the app must use these settings:

```python
fig.update_layout(
    plot_bgcolor='#0a0e1a',   # --canvas
    paper_bgcolor='#0a0e1a',  # --canvas
    font=dict(color='#6a8aaa', family='Segoe UI'),  # --ink-muted
)

# Gridlines
xaxis=dict(gridcolor='#1e2d45')   # --hairline
yaxis=dict(gridcolor='#1e2d45')   # --hairline

# Hover label
hoverlabel=dict(
    bgcolor='#0d1525',        # dark surface
    bordercolor='#2a4a6a',
    font=dict(color='#c8d8f0', size=11, family='Segoe UI'),
)
```

### Architecture Diagram Node Colors

Use these per layer — do not invent new node colors:

| Layer | Node Color | Border |
|---|---|---|
| Data Sources | `#1e3a5f` | `#4a7ac8` |
| Ingestion | `#0d2040` | `#3a6aaa` |
| Processing | `#0d2830` | `#3a7060` |
| Cataloging | `#1a1a3a` | `#4a4a8a` |
| Storage (Raw) | `#1a0d20` | `#6a3a7a` |
| Storage (Curated) | `#1a1020` | `#7a3a6a` |
| Storage (Gold) | `#0d1a10` | `#3a6a40` |
| Consumption | `#0d1a30` | `#3a5a8a` |
| Security | `#200a0a` | `#6a2020` |

Edge/connector lines: `color='#2a4a6a'`, `width=1.5`

---

## HTML Architecture Diagrams (Interactive)

The clickable HTML diagrams inside `st.components.v1.html()` use this internal CSS — keep consistent:

```css
/* Box (any clickable component) */
.box {
  background: #111827;
  border: 1px solid #1e2d45;
  border-radius: 8px;
  cursor: pointer;
  transition: all .18s ease;
}
.box:hover, .box.active {
  background: #182235;
  border-color: #4a7ac8;
  box-shadow: 0 4px 16px rgba(74,122,200,.18);
}

/* Info panel (detail text on click) */
.info-panel {
  background: #0d1525;
  border: 1px solid #1e3050;
  border-radius: 8px;
  font-size: 11px;
  color: #7090b0;
  line-height: 1.6;
}
```

---

## Do's and Don'ts

### Do

- Use `--canvas` (`#0a0e1a`) as the only page background — never white, never gray
- Use surface lifts (`--surface-1` → `--surface-2`) to show hierarchy — not color changes
- Use `--accent` (`#4a9af0`) only for: active nav, links, key metric values, hover borders
- Use `--success` green only for: covered requirements, positive outcomes, open-source labels
- Use `--warning` orange only for: RFP requirement badges, cost warnings, skeptic tags
- Keep all card borders at `1px solid #1e2d45` — thicker borders look cheap
- Add top-accent borders (3px) only when a card needs categorical color coding
- Use `--ink` (`#c8d8f0`) for headings, `--ink-muted` (`#6a8aaa`) for secondary text — nothing else
- Keep badge text uppercase and small (10px) — they should read as labels, not sentences

### Don't

- Don't use white (`#ffffff`) backgrounds anywhere in the app
- Don't introduce new colors not listed in this file
- Don't use colored text (red, green, orange) for body paragraphs — only badges and semantic indicators
- Don't add drop shadows to cards — border + background lift is sufficient
- Don't mix border-radius values arbitrarily — use the defined scale
- Don't change the `plot_bgcolor` or `paper_bgcolor` in Plotly charts — they must stay `#0a0e1a`
- Don't use more than 2 accent colors in a single chart or diagram
- Don't add animations or transitions longer than `.2s` — the app should feel fast
- Don't use Streamlit's default color theme settings — all theming is done via CSS injection

---

## Streamlit-Specific Rules

1. **All CSS goes in one block** at the top of `mango_cloud_platform.py` via `st.markdown(..., unsafe_allow_html=True)`. Do not add scattered inline styles.
2. **Custom components via HTML** use `st.components.v1.html()`. They must implement the same color tokens internally.
3. **`st.info()`, `st.warning()`, `st.error()`** can be used for callout boxes — Streamlit's default styling is acceptable for these.
4. **Plotly charts** must always set `plot_bgcolor` and `paper_bgcolor` — never rely on Streamlit defaults.
5. **`st.dataframe()`** uses the default Streamlit dark theme — do not customise it further.
6. **Sidebar buttons** use `st.button(..., use_container_width=True)` — do not use `st.radio()` for navigation.

---

## File Reference

| File | Role |
|---|---|
| `mango_cloud_platform.py` | Apply all CSS tokens in the `st.markdown()` block at line ~17 |
| Figma HLA board | Use color tokens for node fills; use `--hairline` for connector lines |
| Figma LLA board | Same as HLA; layer colors per the node color table above |
| `DESIGN.md` | ← This file — the single source of truth for all visual decisions |
| `AGENT.md` | Project context and task tracking (not design) |

---

## Updating This File

When you add a new component, color, or pattern to the app, add it here **in the same commit**.
The GitHub Actions workflow will remind you if you push without updating context files.

---

*Source design system: [Framer — awesome-design-md](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/framer)*
*Last updated: 2026-06-03 | Updated by: Luka Tcheishvili*
