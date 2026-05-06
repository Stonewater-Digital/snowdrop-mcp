---
skill: peg_ratio_calculator
category: market_analytics
description: Evaluates PEG ratio relative to growth and adjusts for dividend yield when provided.
tier: free
inputs: pe_ratio, earnings_growth_rate
---

# Peg Ratio Calculator

## Description
Evaluates PEG ratio relative to growth and adjusts for dividend yield when provided.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pe_ratio` | `number` | Yes | Price-to-earnings ratio. |
| `earnings_growth_rate` | `number` | Yes | Expected EPS growth (decimal). |
| `dividend_yield` | `number` | No | Optional dividend yield (decimal). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "peg_ratio_calculator",
  "arguments": {
    "pe_ratio": 0,
    "earnings_growth_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "peg_ratio_calculator"`.
