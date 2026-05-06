---
skill: sp500_pe_ratio_tracker
category: public_data
description: Get S&P 500 price-to-earnings ratio with historical comparison. Uses hardcoded recent data and historical averages.
tier: free
inputs: none
---

# Sp500 Pe Ratio Tracker

## Description
Get S&P 500 price-to-earnings ratio with historical comparison. Uses hardcoded recent data and historical averages.

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
  "tool": "sp500_pe_ratio_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sp500_pe_ratio_tracker"`.
