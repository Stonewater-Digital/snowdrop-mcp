---
skill: catastrophe_bond_analyzer
category: insurance_analytics
description: Evaluates expected loss, risk-adjusted spread, multiple-at-risk (MAR), and approximate Sharpe ratio for catastrophe bonds. Uses trapezoidal integration over the loss distribution to estimate expected loss.
tier: free
inputs: attachment_probability, exhaustion_probability, coupon_spread_bps, notional, risk_free_rate_pct, maturity_years
---

# Catastrophe Bond Analyzer

## Description
Evaluates expected loss, risk-adjusted spread, multiple-at-risk (MAR), and approximate Sharpe ratio for catastrophe bonds. Uses trapezoidal integration over the loss distribution to estimate expected loss.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `attachment_probability` | `number` | Yes | Annual probability that losses exceed the attachment point (0–1). E.g., 0.02 = 2% annual attachment probability (1-in-50-year event). |
| `exhaustion_probability` | `number` | Yes | Annual probability that losses exceed the exhaustion point (0–1). Must be <= attachment_probability. |
| `coupon_spread_bps` | `number` | Yes | Annual coupon spread above LIBOR/SOFR in basis points (e.g., 500 = 5%). |
| `notional` | `number` | Yes | Notional principal of the cat bond. Must be > 0. |
| `risk_free_rate_pct` | `number` | Yes | Risk-free rate (SOFR/T-bill) as a percentage (e.g., 5.0 = 5%). Must be >= 0. |
| `maturity_years` | `number` | Yes | Tenor of the cat bond in years. Must be > 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "catastrophe_bond_analyzer",
  "arguments": {
    "attachment_probability": 0,
    "exhaustion_probability": 0,
    "coupon_spread_bps": 0,
    "notional": 0,
    "risk_free_rate_pct": 0,
    "maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "catastrophe_bond_analyzer"`.
