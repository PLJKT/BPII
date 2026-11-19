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
