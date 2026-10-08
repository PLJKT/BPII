# BPII Financial Dashboard — Development Guide

## Project Overview

Static financial dashboard for **PT Batavia Prosperindo Internasional Tbk (IDX: BPII)**, an Indonesian financial holding group with three operating subsidiaries:
- **BPAM** — Asset management (AUM ~IDR 49tn, 107 mutual funds)
- **BPTR** — Fleet rental (6,928 vehicles, listed as BBLI.JK)
- **MTWI** — General insurance (GWP IDR 1,695.8bn, listed on IDX)

The dashboard covers FY2014–FY2025 plus 1H2026 interim data, with 10 pages: Overview, Profitability, Debt & Solvency, Valuation, Risk & Direction, Holding Structure, Organization, 1H2026, FY2025, FY2024.

**Live site**: https://pljkt.github.io/BPII/

---

## Tech Stack

| Layer | Technology |
|---|---|
| Markup | Single-page `index.html` (~172KB) with hash-based routing |
| Styling | Inline CSS (no framework), green/earth palette (#1F5E40 primary) |
| Charts | [ECharts 5](https://echarts.apache.org/) via CDN |
| Data | `data.json` loaded at runtime with cache-busting (`?v=` timestamp) |
| Deployment | GitHub Pages from `main` branch |
| Build | None — pure static, no bundler |

---

## File Structure

```
BPII/
├── index.html          # Main SPA — all pages, CSS, JS inline
├── data.json           # All financial data (overrides inline fallbacks at runtime)
├── README.md           # Project readme
├── CHANGELOG.md        # Commit history / change log
├── DEVELOPMENT.md      # This file
└── _shots/             # QA screenshots (not deployed)
```

---

## Data Architecture

### Runtime Data Override Pattern

`index.html` contains inline fallback variables (all zeros or placeholders). On page load, `data.json` is fetched and the `DATA_KEYS` array determines which top-level keys override the inline values:

```javascript
var DATA_KEYS = ["KP","EV","DIR","TL","OWN","SUBS","BIZ","VIA","PILLAR",
  "PILLAR_MAP","ORG","DEBT","VAL","DTXT","LTXT","VTXT","NXT","KEYP","AN",
  "CHT","FY","GLOS","TOP3","OPP","DEC","SEG","SUBOPS"];
```

**Important**: When updating data, you MUST update `data.json` (the inline fallbacks are never shown in production). If a key's structure in `data.json` is incomplete, remove it from `DATA_KEYS` to use the inline value instead (as done with `RK` — risk data uses inline only).

### Key data.json Fields

| Field | Purpose |
|---|---|
| `AN` | 13-year annual arrays (2014–2025+1H26): revenue, niCons, ebitda, margins, FCF, segment revenue, etc. |
| `KP` | KPI card data per page (ov, k24, k25, k26, prof, debt, val) |
| `DEBT` | Debt page: liability breakdown, lenders, solvency ratios, trade receivables (WC) |
| `VAL` | Valuation: price, market cap, P/E, P/B, share price history, peers |
| `FY` | Annual page-specific: seg24/seg25 pie data, pl24/pl25 P&L, bs24/bs25/bs26 balance sheet, cf cash bridge, h26rev segment comparison |
| `ORG` | Organization: board/commission/audit members, corporate facts, management |
| `OWN` | Shareholder structure (Malacca Trust 86.15%, Public 9.72%, Treasury 4.13%) |
| `SUBS` / `SUBOPS` | Subsidiary ownership, assets, operating metrics |
| `EV` | Key events per year (ev24, ev25, ev26) |
| `RK` | Risk factors (inline only, NOT in DATA_KEYS) |
| `CHT` | Chart labels (trilingual: en/id/zh) |
| `GLOS` | Glossary terms for hover tooltips |

### AN Array Convention

All `AN.*` arrays have **13 elements** corresponding to:
`[2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 1H26]`

Use `null` for years before a subsidiary was consolidated (e.g., BPTR from 2019H1, MTWI from 2020H2, BPF until 2021).

---

## How to Run Locally

```bash
# From the BPII directory:
python -m http.server 8766

# Then open:
# http://127.0.0.1:8766/index.html
```

**Screenshot / QA tool**:
```bash
python <skill_path>/shot.py http://127.0.0.1:8766/index.html#overview --only desktop
```
This produces a full-page screenshot and reports console errors in JSON.

---

## How to Update Data

### Financial Data (from PDFs)

1. Open the relevant annual report PDF in `../BPII AR/`
2. Extract the number
3. Update `data.json` — find the relevant field (`AN`, `KP`, `DEBT`, `FY`, etc.)
4. If the field is trilingual, update all three (`en`, `id`, `zh`)
5. Verify locally: `python -m http.server 8766` + screenshot
6. Commit: `git add data.json && git commit -m "R<nn>: <description>" && git push`

### Market Data (stock price, valuation)

**Field mapping (critical — do not get this wrong)**: the Valuation page renders from THREE separate data blocks, not just `VAL`:

| What renders | Source field |
|---|---|
| KPI cards (top row: Price / Market cap / P/B / P/E / Dividend) | `KP.val.en/id/zh` (array of `{l,v,u,d,c}`) |
| Snapshot table ("Valuation & trading snapshot") | `VTXT.en/id/zh.stats` (array of `[label, value]`) |
| Peer comparison table | `VTXT.en/id/zh.peers` (array of `[name, pb, pe, dy]`) |
| 12-month price line + volume bars | `VAL.months / close / vol / range` |
| Red dashed markLine (latest price) | `FY.refPrice` |
| P/B vs P/S peer bar chart | `FY.bpiiPBPS = [pb, ps]`, `FY.peerPBPS = [pb, ps]` |

> ⚠️ `VAL.kpi` and `VAL.stats` in data.json are **dead fields** — the render function reads `KP.val` and `VTXT.stats` instead. Editing `VAL.kpi` has no visible effect. This has caused multiple "why didn't it update" rounds.

**Current market snapshot (7 Oct 2026)**:
- Price **IDR 452**, market cap **IDR 4.66tn** (10.31bn shares)
- **P/B = 3.2x** on **parent equity** (BVPS 140.1 = parent equity IDR 1,444.2bn / 10.31bn shares; NCI IDR 376.0bn excluded)
- **P/E = 34.6x FY25** (EPS 13.08) and **52.3x TTM** (TTM EPS 8.64 = TTM net profit 89.1bn = FY25 144.1 − 1H25 108.0 + 1H26 53.0)
- **Dividend yield 1.4%** (TTM DPS 6.32 IDR; FY25 DPS 11.4)
- 52-week range 396–696 IDR
- 12-month chart window: **Nov-25 → Oct-26** (roll forward monthly; drop oldest, append newest)

Sources: IDX, Xurve, stockanalysis.com, Yahoo Finance (BPII.JK).

### Auto Stock Price Update

A GitHub Actions workflow can automatically update `VAL.close` (latest price) on a schedule. The user has indicated they will activate this workflow separately. The workflow should:
1. Fetch latest BPII.JK close price from an API
2. Update `data.json` → `VAL.months[last]` and `VAL.close[last]`
3. Commit and push to `main`

---

## Deployment

GitHub Pages serves the site directly from the `main` branch root. No build step needed.

```bash
git add -A
git commit -m "R<nn>: <description>"
git push origin main
```

The site updates within ~1 minute of push. **Cache note**: `data.json` is loaded with `?v=' + Date.now()` to bypass browser cache. HTML documents may still be cached — users can hard-refresh (Ctrl+Shift+R).

---

## Deleted Pages

Two pages were removed at user request (R51–R52):

| Page | Reason |
|---|---|
| **Segments & Assets** | Consolidated into Overview (segment charts) and Holding Structure (subsidiary data) |
| **Valuation Illustration** | Redundant with Valuation page; contained placeholder DCF/SOTP data |

Dead code for these pages (render functions, chart configs, translation strings, `LAND`/`VALI` data keys) was cleaned up in R69.

---

## Data Conventions & Caveats

### Revenue Basis

- **1H2026 revenue = IDR 653.7bn (net basis)**, NOT gross (1,556.3bn). The net basis deducts insurance claims and reinsurance.
- **Insurance segment revenue** uses **net underwriting result** (hasil underwriting neto), not gross premium. This makes segment totals reconcile with consolidated P&L revenue.
- **2021–2022 as-reported basis**: includes BPF (consumer finance) which was divested after 2021. 2022 onward is continuing operations.

### Insurance (MTWI / PSAK 117)

- MTWI adopted **PSAK 117** (insurance contracts standard) from 2023.
- **Insurance contract liabilities = IDR 3,109.6bn** (62% of total liabilities): RC (remaining coverage) 2,000.8 + ICL (incurred claims) 1,108.8.
- These are NOT debt — they correspond to insurance investment assets on the asset side.
- **Gross premium (1,695.8bn)** ≠ consolidated revenue. Only net insurance service revenue (130.5bn) enters the P&L revenue line.

### EBITDA Calculation

`EBITDA = Net income (consolidated) + Income tax + Depreciation & amortization`

Interest expense is **not** added back (BPII's "Keuangan" is treated as operating cost for a financial holding). This is consistent with the historical anchor values.

### Free Cash Flow

`FCF = CFO − Capex` (no land acquisition adjustment — financial holding has no land bank).

### Net Debt

`Net debt = Total interest-bearing debt − Cash`

Interest-bearing debt = bank loans + consumer finance payables + lease liabilities. **Insurance contract liabilities are excluded** (they are not debt).

**Reported net debt/EBITDA = 4.1x** (FY2025: (1,618.3 − 247.5) / 334.1). This deducts **cash only**. If marketable securities (IDR 647.7bn third-party + 150.1bn related-party = 1,045.3bn total cash + securities) are also netted, net debt falls to ~335bn and net debt/EBITDA ≈ **1.0x**. The 4.1x figure is the conservative headline; the ~1.0x figure is disclosed in the footnotes.

### Interest Coverage — Two Bases

- **EBITDA / interest = 2.8x** (FY2025: 334.1 / 121.5) — operating cash-flow basis
- **EBIT (PBT) / interest = 1.6x** (FY2025: PBT 192.4 / 121.5) — pre-tax basis

Both are shown; EBIT/interest is the stricter measure.

### Free Cash Flow

`FCF = CFO − Capex` (no land acquisition adjustment — financial holding has no land bank).

**FCF has been negative since 2023 exit, negative in 2024–2025**:
- 2023: +336.6bn (MTWI consolidation boosted CFO)
- 2024: **−639.9bn**
- 2025: **−455.8bn**
- 1H26: **−451.2bn**

Driven by BPTR fleet capex and MTWI investment-asset outflows exceeding operating cash flow; financed by debt. Flagged as a High-severity risk on the Risk page.

### Balance Sheet Format

BPII (insurer-format) balance sheet does **not** split current / non-current lines — so a standard current ratio cannot be computed. This is stated rather than estimated.

### Consolidation Timeline

| Subsidiary | Consolidated from |
|---|---|
| BPAM | From 2014 (82.08%) |
| BPF (consumer finance) | 2018–2021 (divested after 2021) |
| BPTR | 2019-06-17 (67.40%) |
| MTWI | 2020-07 (85.90%) |

### Known Data Gaps

- **MTWI combined ratio / claim ratio**: not disclosed in BPII consolidated reports; would require MTWI standalone annual report.
- **MTWI FY2025 RBC (solvency)**: not extracted from standalone report.
- **2016/2017 D&A**: estimated values (PDF fixed-asset roll-forward tables had different format).
- **BPTR customer concentration / capex detail**: in BPTR standalone MD&A, not in BPII consolidated notes.
- **Current ratio**: not computable — insurer balance sheet format has no current/non-current split.
- **Monthly close for thin-trading months**: some month-end closes are approximated from EODHD/investing.com snapshots rather than exact month-end prints.

---

## Commit Convention

All commits use the prefix `R<nn>:` where `<nn>` is a sequential revision number:

```
R67: fix annual pages - FY2024 crash (seg24b), pl24/bs24 data, 1H26 net revenue
R69: cleanup dead code + DEVELOPMENT.md
R74: apply Xurve insights - parent-equity P/B 3.2x, TTM P/E 52.3x, actual DPS, FCF risk
R75: update share price chart to Oct 2026 (Sep close 460, Oct latest 452)
```

---

## Trilingual Support

All user-facing text is in **English / Bahasa Indonesia / 中文**, toggled via the language switcher. Data objects use `{en: [...], id: [...], zh: [...]}` structure. Chart labels are in `CHT.en/id/zh`. When adding new text, always provide all three translations.
