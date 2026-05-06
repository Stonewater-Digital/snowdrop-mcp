---
skill: vintage_year_analyzer
category: fund_accounting
description: Compares funds across vintages and computes quartiles/PME proxies. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Vintage Year Analyzer

## Description
Compares funds across vintages and computes quartiles/PME proxies. (Premium — subscribe at https://snowdrop.ai)

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
