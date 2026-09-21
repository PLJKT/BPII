# BPII — PT Batavia Prosperindo Internasional Tbk

Static financial dashboard for **PT Batavia Prosperindo Internasional Tbk** (IDX: **BPII**), a Jakarta-based financial holding group operating through three listed and unlisted subsidiaries:

- **BPAM** — PT Batavia Prosperindo Aset Manajemen (asset management / mutual funds)
- **BPTR** — PT Batavia Prosperindo Trans Tbk (car rental / fleet management)
- **MTWI** — PT Malacca Trust Wuwungan Insurance Tbk (general insurance)

## Site

**<https://pljkt.github.io/BPII/>**

Three languages: English (default) / Bahasa Indonesia / 中文.

## Structure

```
index.html          # single-file SPA (HTML + CSS + JS + inline data fallback)
data.json           # single source of truth (loaded at runtime, overrides inline)
.github/workflows/update-price.yml   # weekday auto-fetch of BPII.JK close
.github/scripts/update_price.py      # Yahoo Finance → data.json patcher
```

## Data

All figures in IDR billion (bn). Historical range: FY2015 – FY2025, plus 1H2026 interim.

Sources: audited annual reports (2015–2025), 1H2026 interim consolidated financial statements, IDX, Yahoo Finance. See footer on the live site for the full source list.

## Disclaimer

This dashboard is an independent analytical tool. It does not constitute investment advice. Data is sourced from public filings; verify with official disclosures before making decisions.
