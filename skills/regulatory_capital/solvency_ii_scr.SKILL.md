---
skill: solvency_ii_scr
category: regulatory_capital
description: Aggregates market, counterparty, life, health, and non-life SCRs with standard correlations.
tier: free
inputs: risk_modules, correlation_matrix
---

# Solvency Ii Scr

## Description
Aggregates market, counterparty, life, health, and non-life SCRs with standard correlations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `risk_modules` | `array` | Yes | SCR per risk module in base currency. |
| `correlation_matrix` | `object` | Yes | Correlation coefficients keyed by risk module name. |
| `own_funds` | `number` | No | Available own funds for solvency ratio. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "solvency_ii_scr",
  "arguments": {
    "risk_modules": [],
    "correlation_matrix": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "solvency_ii_scr"`.
