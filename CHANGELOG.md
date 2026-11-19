# Changelog

> Internal only. Not shown on the public page.

## R1 — 2026-09-21
- Initial build: adapted from KIJA dashboard template.
- Replaced industrial-park segments (Real Estate / Infrastructure) with financial-holding segments (Asset Management / Car Rental / Insurance).
- Removed Land Bank page; added Segments & Assets page showing subsidiary operating metrics (BPAM AUM/funds/agents, BPTR fleet, MTWI gross premium/underwriting profit).
- Three-language UI (EN / ID / ZH).
- 10-year annual series FY2015–FY2025 + 1H2026 interim.
- GitHub Action auto-updates BPII.JK weekday close price.

## R78 — 2026-11-19
- Applied 9M2026 unaudited consolidated results (period ended 30 Sep 2026, ref. 038/BPI/CR/X/2026): gross revenue IDR 2,218.2bn (+10.8% YoY, PSAK117 gross); consolidated NP 75.0bn; attributable NP 62.6bn (−43.6% YoY); CFO −68.9bn; PP&E capex 327.6bn; FCF −396.5bn; total assets 5,930.2bn; equity 1,832.8bn; cash 247.3bn.
- Refreshed valuation to 18 Nov 2026 close IDR 400: market cap 3.95tn; P/B 2.72x (BVPS 147.3, parent equity 1,456.2bn, NCI 376.6bn excluded); P/E FY25 29.3x (EPS 13.64); P/E TTM 45.7x (TTM NP 86.4bn, EPS 8.74); yield 1.6% (TTM DPS 6.32); 52w 396–696.
- Corrected 1H26 capex/FCF to the official PP&E purchase basis: capex 484.6 → 125.1bn; FCF −451.2 → −91.7bn (the earlier build wrongly treated operating supplier/employee payments as capex).
- Debt snapshot to 30 Sep 2026: interest-bearing debt 1,576.8bn (bank loans 1,477.8 + consumer financing 90.2 + leases 8.8); net debt 1,329.5bn; net debt/parent equity 91.3%; insurance reserves 2,109.8bn excluded from debt. Net debt/EBITDA not recomputed (interim EBITDA/D&A not disclosed).
- Subsidiary total assets updated to 30 Sep 2026: BPTR 2,177.5bn (67.4%), MTWI 2,735.2bn (85.9%), BP Pte. Ltd. 420.2bn (100%), BPAM 198.6bn (82.08%). BPD mapped to the Other pillar and rendered in the holding structure; Singapore entity carries no IDX ticker.
- Debt details table reconciled to 30 Sep 2026: total interest-bearing 1,576.8bn; risk indicators L/E 2.24x, cash/debt 0.16x (9M26), EBITDA/interest 2.8x and net debt/EBITDA 4.1x kept as FY25 anchors (interim EBITDA n/a). DEC snapshot, NXT legend and nav label updated to 9M2026.
- Trilingual EN/ID/ZH kept in sync. Left null pending FY2026 annual report: 9M net segment revenue split, EBITDA/D&A, segment pie, annualized ROE/ROA, current ratio.

## R79 — 2026-11-19
- Full calibration of all renderable blocks to the 9M2026 snapshot (30 Sep 2026, unaudited); inline `DATA_KEYS` fallbacks re-synced to the current BPII values so an offline / failed-XHR load cannot show retired figures.
- Removed unwired inline dead copies that held a stale foreign-model valuation (price 180, shares 20.59bn, BVPS 304.1, EPS 20.55, EBITDA 1,735.5, debt 4,863 / cash 3,200, net debt 1,663, 52w 105–364, DPS 2.03): `VALI` (DCF/P/E/P/B/SOTP illustration), `KEYP` (Bloomberg-style parameter table), `VLL` (valuation labels), and the old `SUBOPS` shareholding array. The `KEYP` highlights block in `data.json` (BPII FY25) is retained; no render function consumes either schema.
- TOP3 priorities restated to 9M26 in EN/ID/ZH: attributable NP −43.6% YoY (62.6 vs 110.9bn) despite gross revenue +10.8%; D/E improved to 2.24x from FY25 2.75x; BPAM AUM kept on an explicit FY2025 basis (9M AUM not disclosed).
- Risk (`RK`, inline-only) leverage row completed to 9M26: D/E 2.24x, interest-bearing debt 1,576.8bn, net debt 1,329.5bn, net debt/parent equity 91.3%; net debt/EBITDA 4.1x and interest coverage 2.8x retained as FY25 anchors (interim EBITDA/D&A n/a). FCF row expanded to the four-period sequence −639.9 (2024), −455.8 (2025), −91.7 (1H26), −396.5 (9M26). Subsidiary-specific rows (BPTR fleet 6,928 / revenue 619.5, MTWI GWP 1,695.8 / UW +130.9, BPAM AUM 49tn / 107 funds) tagged FY2025; 9M subsidiary splits not estimated.
- `AN` 1H26 undisclosed lines set to `null`: gross margin, ROE, ROA, EBITDA, EBITDA margin (interim D&A/annualized ratios not disclosed); net margin and FCF margin kept where computable from disclosed net revenue. Corrected a stale ID event bullet in `EV.ev25` that still cited the old Q4 close 510 / 5.3tn market cap.
- Rate-sensitivity estimate updated to ~15.8bn interest per 100bp on 1,576.8bn interest-bearing debt. WC / trade-receivables table and DSO keep the 1H26 column as the latest disclosed AR split; 9M consolidated and segment AR are not broken out in the interim note (not estimated).
- Trilingual EN/ID/ZH kept in sync; local regression across all 10 pages (plus ID/ZH key pages) reported zero console/page errors and no stale foreign or superseded values in the live DOM. Remaining nulls pending FY2026 annual report: 9M net segment revenue split, EBITDA/D&A, 9M segment pie, annualized ROE/ROA, current ratio, 9M segment AR split/aging.

## R80 — 2026-11-19
- Overview charts recalibrated to the 9M2026 disclosure basis. Bar charts (o1 revenue, o4 segment revenue, o7 segment net profit) now plot **full-year periods only (FY2014–2025)**; the 1H26 half-period bars are removed so a half-year column cannot be read as a full-year result. Line charts (o2 net profit, o3 margins/leverage) keep the 1H26 and 9M26 interim points as trend markers.
- 9M26 nulls retained wherever the interim note does not disclose a comparable basis: consolidated net service revenue (the PSAK117 gross top line 2,218.2bn is not mixed into the net series), EBITDA/D&A, 9M net/gross margin and annualized ROE/ROA, and the 9M segment revenue / net-profit split. No interim EBITDA is reconstructed from net income + tax (D&A unavailable).
- o2 net profit line already carries the 9M26 points: consolidated 75.0bn, attributable 62.6bn; o3 D/E 2.24x. The 1H26 net margin 8.1% was verified on the same net-revenue basis as the annual series (53.0 / 653.7) and retained.
- Trilingual EN/ID/ZH labels corrected: misleading "+ 1H2026 / + 1H26" titles removed from the revenue, EBITDA and segment charts; the o7 hard-coded English title converted to a bound trilingual label; the profit-page margin title aligned to the FY2014–2025 basis with an interim-point note.
- Inline `AN`/`FY` fallbacks re-verified identical to `data.json` (null positions included). Local three-language regression: zero console/page errors, no undefined/NaN, no retired foreign-model values; bar charts render FY2014–2025 only.
- Left null pending FY2026 annual report: 9M net segment revenue split, EBITDA/D&A, 9M segment pie/stack, annualized ROE/ROA, current ratio, 9M segment AR split/aging.

## R81 — 2026-11-19
- Sourced 9M2026 (unaudited, 30 Sep 2026) interim filings for the two listed subsidiaries and reconciled them to the consolidated basis. Segment series (`FY.segStack`, `AN.segLease/segIns`) record subsidiaries on a **100% full-entity basis** (not BPII's ownership share), matching the historical 1H26/FY25 points:
  - BPTR (IDX: **BPTR**): Sales and revenue **524.9bn**; parent net profit **35.5bn** (`FinancialStatement-2026-III-BPTR.pdf`, IDX mirror `www.idx.id`).
  - MTWI: Net Insurance Service Result **51.7bn**; parent net profit **8.5bn** (`mtwi-lkt-september-2026.pdf`). MTWI gross service revenue 1,362.4bn is a PSAK117 gross figure and is not entered into the net series.
  - BPAM (unlisted, no interim disclosure) and the consumer-finance segment remain `null` for 9M26.
- Ownership reconciliation: BPTR 67.4% / MTWI 85.9%; external NCI subtotal 12.782bn vs reported consolidated NCI 12.387bn (diff −0.395 from BPAM's external stake, subsidiary-level NCI and eliminations, not disclosed line-by-line). BPTR+MTWI BPII share 31.270bn of reported attributable NP 62.572bn; residual belongs to BPAM + BPD + holding/eliminations. Consolidated NI 74.960 = parent 62.572 + NCI 12.387.
- Overview six-chart 9M26 outcomes: **o2** net profit line carries consolidated 75.0 / parent 62.6bn (9M26); **o3** D/E 2.24x, gpm/npm/roe/roa null (net revenue and annualized ratios not disclosed); **o4** segment revenue and **o7** segment NP bars keep FY2014–2025 only (full-year bars; partial-period points stay in the arrays for trend/half-vs-half use); **o1** consolidated revenue null (PSAK117 gross 2,218.2bn not mixed into the net series); **o6** EBITDA null (interim D&A not disclosed, not reconstructed from NI + tax).
- Corrected the BPTR IDX ticker from the stale `BBLI` copy to **BPTR** in `SUBS` and the development guide.
- Line-chart x-axis: the `baseX` helper now keeps the last two interim categories (`1H26`, `9M26`) visible on the AN.years line/mixed charts (o2, o3, p-1…p-4); echarts auto-thinning had dropped the `9M26` label even though the 9M26 point was plotted. Bar charts still render full-year periods only.
- Inline `AN`/`FY`/`SUBS` fallbacks re-verified identical to `data.json` (null positions included). Left null pending FY2026 annual report: 9M consolidated net service revenue and net segment split, EBITDA/D&A, BPAM 9M revenue/profit, annualized ROE/ROA, current ratio, 9M segment AR split/aging.

## R82 — 2026-11-19
- Removed the **1H26 checkpoint from every current-period series**; the only interim point retained is **9M26** (unaudited, 30 Sep 2026). Undisclosed 9M lines are left `null` rather than back-filled with the 1H26 value.
- `AN` parallel arrays reduced from 14 to **13 elements** (`…2024, 2025, 9M26`). 9M26 values recorded: niCons 75.0, niParent 62.6, assets 5,930.2, liab 4,097.4, equity 1,832.8, D/E 2.24, CFO −68.9, capex 327.6, FCF −396.5, segLease 524.9, segIns 51.7. 9M26 nulls (no 1H26 carry-back): revenue, npm, fcfMargin, segAM, gpm, roe, roa, ebitda, ebitdaMargin. `FY.segStack` nine arrays likewise reduced to 13 elements.
- `DEBT.cashDebt` reduced to four slots (`FY2023, FY2024, FY2025, 9M26`); cash [361.4, 221.1, 247.5, 247.3], debt [503.8, 1,071.3, 1,380.5, 1,576.8].
- **Retired the 1H26-vs-1H25 half comparison**: charts `f26-1`/`f26-2` and the `FY.h26rev` data block were removed; the fy2026 page now shows only the net-debt position (`f26-3`) plus a trilingual "9M segment split incomplete" panel. `fy26.segPie` shows the FY2025 complete mix (BPAM 400.2 / BPTR 616.3 / MTWI 130.5 / Other 92.5) with an explicit note that the 9M segment split is incomplete; the 1H26 pie values were not reused.
- **Working capital**: the 1H26 AR/DSO column was removed; the WC series and table end at FY2025. The `rev*2` annualization special case for the 1H26 DSO point was deleted. `VAL.events` and `VTXT.en/id/zh.events` dropped the 1H26 bullet (FY25 and 9M26 retained). Inline `RK` FCF row dropped the −91.7bn (1H26) checkpoint; the dividend row no longer binds to the "1H26 one-off 460bn" figure.
- Trilingual EN/ID/ZH labels updated: `c_o2_s`, `c_wc1_t`, `wc_note`, `dec_h` and the f26 titles no longer cite 1H26/1H25; the unused `wch_26` header key is emptied; new panel keys `c_f26_seg_t/s` added in all three languages. No undefined/NaN/key-name fallbacks.
- Inline `AN`/`DEBT`/`WC`/`VAL`/`VTXT`/`FY` fallbacks re-synced to `data.json`; `node --check` passes, JSON parses with BOM preserved, anchor ratios recomputed: D/E 4,097.369/1,832.807 = 2.236, FCF −68.937 − 327.567 = −396.504, parent NP 62.572, NCI 12.388.
- **Retained as historical trace** (not current-period data): the `FINAL BPI KONSOL JUNI 2026.pdf` entry in `SOURCES`, prior CHANGELOG/R-development-guide entries, `EV.ev24/ev25`, the monthly share-price labels (Jan-26…Nov-26), and RK FY2025 subsidiary anchors (fleet 6,928, GWP 1,695.8, UW +130.9, AUM 49tn).
- Left null pending FY2026 annual report: 9M consolidated net service revenue and net segment split, EBITDA/D&A, BPAM 9M revenue/profit, annualized ROE/ROA, current ratio, 9M segment AR split/aging, 9M segment pie/stack (BPAM missing).
