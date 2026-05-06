---
skill: cdo_squared_correlation
category: structured_products
description: Aggregates inner CDO tranche correlations to infer compound/base metrics and reports spread sensitivity across the outer tranche. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cdo Squared Correlation

## Description
Aggregates inner CDO tranche correlations to infer compound/base metrics and reports spread sensitivity across the outer tranche. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cdo_squared_correlation",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cdo_squared_correlation"`.
