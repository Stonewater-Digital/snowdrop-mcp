---
skill: yield_spread_calculator
category: public_data
description: Calculate the yield spread between a long-term and short-term interest rate. Detects yield curve inversion and provides historical context.
tier: free
inputs: long_rate, short_rate
---

# Yield Spread Calculator

## Description
Calculate the yield spread between a long-term and short-term interest rate. Detects yield curve inversion and provides historical context.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `long_rate` | `number` | Yes | Long-term interest rate (e.g., 10-year Treasury yield as percentage, like 4.25). |
| `short_rate` | `number` | Yes | Short-term interest rate (e.g., 2-year Treasury yield as percentage, like 3.90). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "yield_spread_calculator",
  "arguments": {
    "long_rate": 0,
    "short_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "yield_spread_calculator"`.
