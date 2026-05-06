---
skill: distribution_waterfall_calculator
category: fund_admin
description: Runs a full 4-tier distribution waterfall: (1) return of capital, (2) preferred return, (3) GP catch-up, (4) residual profit split. Supports both European (whole-fund) and American (deal-by-deal) modes.
tier: premium
inputs: none
---

# Distribution Waterfall Calculator

## Description
Runs a full 4-tier distribution waterfall: (1) return of capital, (2) preferred return, (3) GP catch-up, (4) residual profit split. Supports both European (whole-fund) and American (deal-by-deal) modes. Uses correct catch-up formula: GP gets 100% until carry% of total profits is met. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "distribution_waterfall_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "distribution_waterfall_calculator"`.
