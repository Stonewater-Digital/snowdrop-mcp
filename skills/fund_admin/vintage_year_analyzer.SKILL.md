---
skill: vintage_year_analyzer
category: fund_admin
description: Benchmarks fund IRR/MOIC/DPI against vintage-year peer quartile data. Returns quartile placement (top/2nd/3rd/bottom) for each metric.
tier: premium
inputs: none
---

# Vintage Year Analyzer

## Description
Benchmarks fund IRR/MOIC/DPI against vintage-year peer quartile data. Returns quartile placement (top/2nd/3rd/bottom) for each metric. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "vintage_year_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vintage_year_analyzer"`.
