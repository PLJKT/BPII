# BPII Financial Dashboard — Development Guide

## Project Overview

Static financial dashboard for **PT Batavia Prosperindo Internasional Tbk (IDX: BPII)**, an Indonesian financial holding group with three operating subsidiaries:
- **BPAM** — Asset management (AUM ~IDR 49tn, 107 mutual funds)
- **BPTR** — Fleet rental (6,928 vehicles, listed as BBLI.JK)
- **MTWI** — General insurance (GWP IDR 1,695.8bn, listed on IDX)

The dashboard covers FY2014–FY2025 plus 1H2026 and 9M2026 interim data, with 10 pages: Overview, Profitability, Debt & Solvency, Valuation, Risk & Direction, Holding Structure, Organization, 9M2026, FY2025, FY2024.

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
| `AN` | 14-element arrays (2014–2025, 1H26, 9M26): revenue, niCons, ebitda, margins, FCF, segment revenue, etc. Interim-specific nulls left where the interim note does not disclose them. |
| `KP` | KPI card data per page (ov, k24, k25, k26, prof, debt, val) |
| `DEBT` | Debt page: liability breakdown, lenders, solvency ratios, trade receivables (WC) |
| `VAL` | Valuation: price, market cap, P/E, P/B, share price history, peers |
| `FY` | Annual page-specific: seg24/seg25 pie data, pl24/pl25 P&L, bs24/bs25/bs26 balance sheet, cf cash bridge, h26rev segment comparison |
| `ORG` | Organization: board/commission/audit members, corporate facts, management |
| `OWN` | Shareholder structure (Malacca Trust 89.86%, Public 10.12%, treasury shares cancelled) |
| `SUBS` / `SUBOPS` | Subsidiary ownership, assets, operating metrics. Four entities: BPAM (am), BPTR (lease), MTWI (ins), BP Pte. Ltd. (other/Singapore, 100%, no IDX ticker); `PILLAR`/`PILLAR_MAP` group them into the four pillars. |
| `EV` | Key events per year (ev24, ev25, ev26) |
| `RK` | Risk factors (inline only, NOT in DATA_KEYS) |
| `CHT` | Chart labels (trilingual: en/id/zh) |
| `GLOS` | Glossary terms for hover tooltips |

### AN Array Convention

All `AN.*` arrays have **14 elements** corresponding to:
`[2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 1H26, 9M26]`

Use `null` for years before a subsidiary was consolidated (e.g., BPTR from 2019H1, MTWI from 2020H2, BPF until 2021). Interim elements are `null` wherever the interim note does not disclose the line (e.g., 9M net segment revenue, EBITDA/D&A, annualized ROE/ROA). Annual-only arrays (`msales`, `landAcq`, `fcfCons`, `fcfConsMargin`) keep their 12 annual elements and do not carry interim points.

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

**Current market snapshot (18 Nov 2026)**:
- Price **IDR 400**, market cap **IDR 3.95tn** (9.884bn shares = 9,884,153,240; treasury 425.8m cancelled)
- **P/B = 2.72x** on **parent equity** (BVPS 147.3 = parent equity IDR 1,456.2bn / 9.884bn shares; NCI IDR 376.6bn excluded)
- **P/E = 29.3x FY25** (EPS 13.64) and **45.7x TTM** (TTM EPS 8.74 = TTM net profit 86.4bn = FY25 134.8 − 9M25 110.9 + 9M26 62.6)
- **Dividend yield 1.6%** (TTM DPS 6.32 IDR; FY25 DPS 11.4)
- 52-week range 396–696 IDR
- 12-month chart window: **Dec-25 → Nov-26** (roll forward monthly; drop oldest, append newest)

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
- **9M2026 gross sales & revenue = IDR 2,218.2bn (+10.8% YoY, PSAK117 gross top line)**; the interim note does **not** break out net insurance service revenue, so the 9M net-revenue and segment split are left `null` rather than estimated. Gross top line must not be mixed with the net service-revenue series.
- **Insurance segment revenue** uses **net underwriting result** (hasil underwriting neto), not gross premium. This makes segment totals reconcile with consolidated P&L revenue.
- **2021–2022 as-reported basis**: includes BPF (consumer finance) which was divested after 2021. 2022 onward is continuing operations.

### Insurance (MTWI / PSAK 117)

- MTWI adopted **PSAK 117** (insurance contracts standard) from 2023.
- **Insurance contract liabilities = IDR 2,109.8bn** at 30 Sep 2026 (31 Dec 2025: 3,109.7bn). These are policyholder obligations under PSAK 117, not debt.
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

**Net debt (30 Sep 2026)**: interest-bearing debt IDR 1,576.8bn (bank loans 1,477.8 + consumer financing 90.2 + leases 8.8) less cash IDR 247.3bn = **net debt IDR 1,329.5bn**; net debt / parent equity **91.3%**. Marketable securities are not netted in the headline. **Net debt/EBITDA is not recomputed for the interim** because 9M26 EBITDA/D&A is not disclosed; the FY2025 anchor remains net debt/EBITDA ≈ 4.1x on cash-only netting (≈1.0x if securities are also netted). Insurance reserves are excluded from interest-bearing debt in every basis.

### Interest Coverage — Two Bases

- **EBITDA / interest = 2.8x** (FY2025: 334.1 / 121.5) — operating cash-flow basis
- **EBIT (PBT) / interest = 1.6x** (FY2025: PBT 192.4 / 121.5) — pre-tax basis

Both are shown; EBIT/interest is the stricter measure.

### Free Cash Flow

`FCF = CFO − Capex` (no land acquisition adjustment — financial holding has no land bank).

**FCF has been negative since 2023 exit, negative in 2024–2025 and both 2026 interims**:
- 2023: +336.6bn (MTWI consolidation boosted CFO)
- 2024: **−639.9bn**
- 2025: **−455.8bn**
- 1H26: **−91.7bn** (official: CFO 33.4 − PP&E capex 125.1; an earlier build wrongly treated operating supplier/employee payments as capex, showing −451.2bn)
- 9M26: **−396.5bn** (CFO −68.9 − PP&E capex 327.6)

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
- **9M26 net segment revenue split, EBITDA/D&A, annualized ROE/ROA**: not disclosed in the interim note; left `null` for the 9M26 element and to be backfilled from the FY2026 annual report.
- **Monthly close for thin-trading months**: some month-end closes are approximated from EODHD/investing.com snapshots rather than exact month-end prints.

---

## Commit Convention

All commits use the prefix `R<nn>:` where `<nn>` is a sequential revision number:

```
R67: fix annual pages - FY2024 crash (seg24b), pl24/bs24 data, 1H26 net revenue
R69: cleanup dead code + DEVELOPMENT.md
R74: apply Xurve insights - parent-equity P/B 3.2x, TTM P/E 52.3x, actual DPS, FCF risk
R75: update share price chart to Oct 2026 (Sep close 460, Oct latest 452)
R78: apply 9M2026 unaudited consolidated data; refresh valuation to 400 IDR / 2.72x / 29.3x FY25 / 45.7x TTM; fix 1H26 capex/FCF to official PP&E basis
```

---

## Trilingual Support

All user-facing text is in **English / Bahasa Indonesia / 中文**, toggled via the language switcher. Data objects use `{en: [...], id: [...], zh: [...]}` structure. Chart labels are in `CHT.en/id/zh`. When adding new text, always provide all three translations.
