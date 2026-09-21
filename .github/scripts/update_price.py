#!/usr/bin/env python3
"""Fetch latest BPII.JK closing price from Yahoo Finance and update data.json."""
import json
import sys
import urllib.request
from datetime import datetime, timezone

DATA_FILE = "data.json"
TICKER = "BPII.JK"
SHARES_BN = 10.31  # total shares outstanding (bn), post 2021 3:1 split
EPS = 14.0         # FY2025 consolidated EPS (IDR) — 144bn NI / 10.31bn shares
BVPS = 176.5       # parent book value per share (IDR) — 1,820bn equity / 10.31bn
DPS = 0.0          # dividend per share (IDR) — update once FY25 dividend declared

def fetch_price():
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    result = data["chart"]["result"][0]
    closes = result["indicators"]["quote"][0]["close"]
    timestamps = result["timestamp"]
    valid = [(t, c) for t, c in zip(timestamps, closes) if c is not None]
    if not valid:
        raise ValueError("No valid closes found")
    last_ts, last_close = valid[-1]
    prev_close = valid[-2][1] if len(valid) >= 2 else last_close
    return round(last_close), round(prev_close), last_ts

def main():
    price, prev_price, ts = fetch_price()
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        dj = json.load(f)

    if "FY" in dj:
        dj["FY"]["refPrice"] = price
    else:
        dj["refPrice"] = price

    if "VAL" in dj:
        val = dj["VAL"]
        if "kpi" in val and len(val["kpi"]) >= 6:
            val["kpi"][0]["v"] = price
            val["kpi"][0]["l"] = f"Price ({date_str})"
            chg = price - prev_price
            chg_pct = (chg / prev_price * 100) if prev_price else 0
            val["kpi"][0]["d"] = f"{chg:+.0f} ({chg_pct:+.1f}%) on day"
            val["kpi"][0]["c"] = "up" if chg >= 0 else "dn"
            mcap = price * SHARES_BN / 1000
            val["kpi"][2]["v"] = round(mcap, 1)
            val["kpi"][2]["d"] = f"{mcap:.2f}T at {price}"
            pb = price / BVPS
            val["kpi"][3]["v"] = round(pb, 1)
            val["kpi"][3]["d"] = f"{pb:.2f}x parent BVPS {BVPS}"
            pe = price / EPS
            val["kpi"][4]["v"] = round(pe, 1)
            val["kpi"][4]["d"] = f"{pe:.1f}x on FY25 EPS {EPS}"
            if DPS > 0:
                dy = DPS / price * 100
                val["kpi"][5]["v"] = round(dy, 1)
                val["kpi"][5]["d"] = f"{DPS} DPS / {price}"

        if "close" in val and len(val["close"]) > 0:
            val["close"][-1] = price

        if "stats" in val:
            for row in val["stats"]:
                if row[0] == "Price / date":
                    row[1] = f"{price}.0 IDR · {date_str} (Yahoo Finance)"
                    break

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dj, f, ensure_ascii=False, indent=2)

    print(f"Updated price: {price} (prev: {prev_price}, date: {date_str})")

if __name__ == "__main__":
    main()
