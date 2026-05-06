---
skill: swap_curve_builder
category: fixed_income_analytics
description: Bootstraps an overnight-indexed swap (OIS) discount curve and overlays vanilla IRS par rates with turn-of-year adjustments per ISDA methodology. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Swap Curve Builder

## Description
Bootstraps an overnight-indexed swap (OIS) discount curve and overlays vanilla IRS par rates with turn-of-year adjustments per ISDA methodology. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "swap_curve_builder",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "swap_curve_builder"`.
