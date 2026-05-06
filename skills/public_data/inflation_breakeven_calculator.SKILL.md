---
skill: inflation_breakeven_calculator
category: public_data
description: Calculate the inflation breakeven rate from nominal Treasury yield and TIPS yield. The breakeven rate represents market-implied inflation expectations.
tier: free
inputs: nominal_yield, tips_yield
---

# Inflation Breakeven Calculator

## Description
Calculate the inflation breakeven rate from nominal Treasury yield and TIPS yield. The breakeven rate represents market-implied inflation expectations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `nominal_yield` | `number` | Yes | Nominal Treasury yield as percentage (e.g., 4.25 for 4.25%). |
| `tips_yield` | `number` | Yes | TIPS (Treasury Inflation-Protected Securities) yield as percentage (e.g., 1.95 for 1.95%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "inflation_breakeven_calculator",
  "arguments": {
    "nominal_yield": 0,
    "tips_yield": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inflation_breakeven_calculator"`.
