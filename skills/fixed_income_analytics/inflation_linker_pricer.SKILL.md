---
skill: inflation_linker_pricer
category: fixed_income_analytics
description: Values Treasury Inflation-Protected Securities (TIPS) by discounting real cash flows, and derives breakeven inflation relative to nominal Treasuries with monthly seasonality adjustments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Inflation Linker Pricer

## Description
Values Treasury Inflation-Protected Securities (TIPS) by discounting real cash flows, and derives breakeven inflation relative to nominal Treasuries with monthly seasonality adjustments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "inflation_linker_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inflation_linker_pricer"`.
