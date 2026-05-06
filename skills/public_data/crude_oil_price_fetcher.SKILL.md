---
skill: crude_oil_price_fetcher
category: public_data
description: Fetch WTI (West Texas Intermediate) crude oil spot price from FRED (series DCOILWTICO). Requires FRED_API_KEY.
tier: free
inputs: none
---

# Crude Oil Price Fetcher

## Description
Fetch WTI (West Texas Intermediate) crude oil spot price from FRED (series DCOILWTICO). Requires FRED_API_KEY.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crude_oil_price_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crude_oil_price_fetcher"`.
