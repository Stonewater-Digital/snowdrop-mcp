---
skill: interest_rate_risk_banking_book
category: quantitative_risk
description: Computes IRRBB delta EVE and NII across the six Basel shock scenarios.
tier: free
inputs: cashflows, yield_curve, shock_scenarios
---

# Interest Rate Risk Banking Book

## Description
Computes IRRBB delta EVE and NII across the six Basel shock scenarios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cashflows` | `array` | Yes | Repricing buckets with cashflow amount and duration in years. |
| `yield_curve` | `object` | Yes | Mapping of bucket names to base annual yields (decimal). |
| `shock_scenarios` | `object` | Yes | Scenario name to parallel shock in basis points (per BCBS368). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "interest_rate_risk_banking_book",
  "arguments": {
    "cashflows": [],
    "yield_curve": {},
    "shock_scenarios": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "interest_rate_risk_banking_book"`.
