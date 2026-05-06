---
skill: procyclicality_buffer
category: quantitative_risk
description: Implements Basel CCyB mapping from credit-to-GDP gap and aggregates jurisdictional CCyB exposure-weighted rates.
tier: free
inputs: credit_to_gdp_ratio, long_term_trend, jurisdictions
---

# Procyclicality Buffer

## Description
Implements Basel CCyB mapping from credit-to-GDP gap and aggregates jurisdictional CCyB exposure-weighted rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `credit_to_gdp_ratio` | `number` | Yes | Current credit-to-GDP ratio. |
| `long_term_trend` | `number` | Yes | HP-filter trend of credit-to-GDP. |
| `jurisdictions` | `array` | Yes | Exposure shares per jurisdiction with local CCyB rate. |
| `risk_weighted_assets` | `number` | No | Risk-weighted assets to translate CCyB rate into buffer. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "procyclicality_buffer",
  "arguments": {
    "credit_to_gdp_ratio": 0,
    "long_term_trend": 0,
    "jurisdictions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "procyclicality_buffer"`.
