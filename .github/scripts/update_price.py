#!/usr/bin/env python3
"""Fetch latest BPII.JK closing price from Yahoo Finance and update data.json.

Scope (R86) — only the live daily price series and the markLine are touched:
  - VAL.close[-1]  = latest close
  - VAL.months[-1] = latest close month (%b-%y)
  - FY.refPrice    = latest close

Market cap, P/B, P/E, dividend yield and the VAL.kpi / VAL.stats blocks are
manual snapshot anchors and are NOT recomputed here. data.json is read and
written as UTF-8 with BOM (utf-8-sig), 1-space indent, ensure_ascii=False,
LF line endings, no trailing newline.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone

DATA_FILE = "data.json"
TICKER = "BPII.JK"


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
        raise ValueError(f"No valid closes returned for {TICKER}")
    last_ts, last_close = valid[-1]
    return round(last_close), last_ts


def main():
    price, ts = fetch_price()
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    month_label = dt.strftime("%b-%y")

    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        dj = json.load(f)

    val = dj.get("VAL")
    if not val or "close" not in val or "months" not in val:
        raise ValueError("VAL.close / VAL.months missing in data.json")
    if not val["close"] or not val["months"]:
        raise ValueError("VAL.close / VAL.months are empty")
    val["close"][-1] = price
    val["months"][-1] = month_label

    if "FY" not in dj or "refPrice" not in dj["FY"]:
        raise ValueError("FY.refPrice missing in data.json")
    dj["FY"]["refPrice"] = price

    with open(DATA_FILE, "w", encoding="utf-8-sig", newline="") as f:
        json.dump(dj, f, ensure_ascii=False, indent=1)

    print(f"Updated price: {price} ({month_label})")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
