---
skill: credit_spread_analyzer
category: credit_analysis
description: Calculates credit spreads, implied default probabilities, and indicative ratings.
tier: free
inputs: corporate_yield, risk_free_yield, maturity_years
---

# Credit Spread Analyzer

## Description
Calculates credit spreads, implied default probabilities, and indicative ratings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `corporate_yield` | `number` | Yes |  |
| `risk_free_yield` | `number` | Yes |  |
| `recovery_rate` | `number` | No |  |
| `maturity_years` | `integer` | Yes |  |
| `leverage_turns` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_spread_analyzer",
  "arguments": {
    "corporate_yield": 0,
    "risk_free_yield": 0,
    "maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_spread_analyzer"`.
