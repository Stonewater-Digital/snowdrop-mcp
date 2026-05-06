---
skill: contingent_cds_pricer
category: credit_derivatives
description: Values contingent CDS via barrier-adjusted probabilities: barrier probability via down-and-in hitting formula (Broadie-Glasserman) multiplied by conditional default PV.
tier: free
inputs: equity_spot, barrier_level, equity_volatility, drift, horizon_years, default_probability, recovery_rate, notional, discount_rate
---

# Contingent Cds Pricer

## Description
Values contingent CDS via barrier-adjusted probabilities: barrier probability via down-and-in hitting formula (Broadie-Glasserman) multiplied by conditional default PV.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `equity_spot` | `number` | Yes | Current equity price serving as trigger reference. |
| `barrier_level` | `number` | Yes | Equity barrier level for knock-in (spot must breach). |
| `equity_volatility` | `number` | Yes | Equity volatility (decimal). |
| `drift` | `number` | Yes | Equity risk-neutral drift (r-q). |
| `horizon_years` | `number` | Yes | Contract tenor in years. |
| `default_probability` | `number` | Yes | Unconditional default probability over the horizon. |
| `recovery_rate` | `number` | Yes | Recovery assumption on the CDS leg. |
| `notional` | `number` | Yes | Contract notional. |
| `discount_rate` | `number` | Yes | Continuous risk-free rate for PV. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contingent_cds_pricer",
  "arguments": {
    "equity_spot": 0,
    "barrier_level": 0,
    "equity_volatility": 0,
    "drift": 0,
    "horizon_years": 0,
    "default_probability": 0,
    "recovery_rate": 0,
    "notional": 0,
    "discount_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contingent_cds_pricer"`.
