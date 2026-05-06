---
skill: solvency_ratio_calculator
category: insurance_analytics
description: Computes the Solvency II SCR coverage ratio from component risk modules. Applies the standard formula diversification benefit before adding operational risk.
tier: free
inputs: available_own_funds, scr_market_risk, scr_underwriting_risk, scr_credit_risk, scr_operational_risk
---

# Solvency Ratio Calculator

## Description
Computes the Solvency II SCR coverage ratio from component risk modules. Applies the standard formula diversification benefit before adding operational risk. Returns coverage ratio, action level classification, and capital buffers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `available_own_funds` | `number` | Yes | Eligible own funds (Tier 1 + Tier 2 + Tier 3) available to cover SCR. Must be >= 0. |
| `scr_market_risk` | `number` | Yes | Market risk module SCR (interest rate, equity, spread, currency, concentration). Must be >= 0. |
| `scr_underwriting_risk` | `number` | Yes | Underwriting risk module SCR (life, non-life, or health). Must be >= 0. |
| `scr_credit_risk` | `number` | Yes | Counterparty default risk module SCR. Must be >= 0. |
| `scr_operational_risk` | `number` | Yes | Operational risk add-on. Per Solvency II standard formula, operational risk is added AFTER diversification (not subject to diversification benefit). Must be >= 0. |
| `diversification_benefit_pct` | `number` | No | Diversification benefit as % of basic SCR (sum of market + underwriting + credit). Reflects off-diagonal correlation in the BSCR aggregation matrix. Typical range 10–30%. Must be 0–50%. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "solvency_ratio_calculator",
  "arguments": {
    "available_own_funds": 0,
    "scr_market_risk": 0,
    "scr_underwriting_risk": 0,
    "scr_credit_risk": 0,
    "scr_operational_risk": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "solvency_ratio_calculator"`.
