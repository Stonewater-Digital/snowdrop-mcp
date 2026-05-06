---
skill: retail_sales_tracker
category: public_data
description: Track US advance retail sales from FRED (series RSAFS). Returns latest value and trend.
tier: free
inputs: none
---

# Retail Sales Tracker

## Description
Track US advance retail sales from FRED (series RSAFS). Returns latest value and trend. Requires FRED_API_KEY.

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
  "tool": "retail_sales_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "retail_sales_tracker"`.
