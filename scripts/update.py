#!/usr/bin/env python3
"""Fetch Grayscale's official ZCSH daily file, derive flows, write data/zcsh.json."""
import io, json, datetime, urllib.request
import openpyxl

URL = ("https://reporting-prod-20231113144948145500000003.s3.amazonaws.com/"
       "product-performance/c131f37d-6f8f-4af9-8645-346503081d6a.xlsx")
ETF_START = "2026-08-25"

req = urllib.request.Request(URL, headers={"User-Agent": "zec-flow-tracker"})
raw = urllib.request.urlopen(req, timeout=90).read()
wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True)
ws = wb["Daily Performance"]

rows = {}
for r in list(ws.iter_rows(values_only=True))[1:]:
    if not r or r[3] is None:
        continue
    date = str(r[3])[:10]
    rows[date] = {"date": date, "shares": r[4], "nav": r[5], "mkt": r[7]}

series = sorted(rows.values(), key=lambda x: x["date"])
out, prev, cum = [], None, 0.0
for d in series:
    flow = None
    if prev and d["shares"] is not None and prev["shares"] is not None and d["nav"] is not None:
        flow = (d["shares"] - prev["shares"]) * d["nav"]
    aum = d["shares"] * d["nav"] if d["shares"] and d["nav"] else None
    etf = d["date"] >= ETF_START
    if etf and flow is not None:
        cum += flow
    out.append({**d, "flow": flow, "aum": aum, "cum": round(cum, 2) if etf else None})
    prev = d

payload = {
    "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "source": URL,
    "fund": {"ticker": "ZCSH", "name": "Grayscale Zcash ETF", "fee": "2.50%"},
    "etf_start": ETF_START,
    "rows": out,
}
with open("data/zcsh.json", "w") as f:
    json.dump(payload, f, separators=(",", ":"))
print(f"wrote {len(out)} rows; latest {out[-1]['date']}, cum ETF flow ${cum/1e6:.2f}m")
