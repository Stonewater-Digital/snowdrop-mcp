---
skill: first_loss_tranche_pricer
category: credit_derivatives
description: Monte Carlo Vasicek/Li large pool approximation for equity tranches using base-correlation averaging to determine the effective copula correlation.
tier: free
inputs: portfolio_notional, default_probability, recovery_rate, attachment_point, detachment_point, base_correlation_attachment, base_correlation_detachment, num_paths, discount_rate, horizon_years
---

# First Loss Tranche Pricer

## Description
Monte Carlo Vasicek/Li large pool approximation for equity tranches using base-correlation averaging to determine the effective copula correlation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_notional` | `number` | Yes | Total underlying notional. |
| `default_probability` | `number` | Yes | Portfolio default probability over horizon (decimal). |
| `recovery_rate` | `number` | Yes | Recovery assumption (decimal). |
| `attachment_point` | `number` | Yes | Equity tranche attachment in fractional terms. |
| `detachment_point` | `number` | Yes | Equity tranche detachment (fraction). |
| `base_correlation_attachment` | `number` | Yes | Base correlation at the attachment point. |
| `base_correlation_detachment` | `number` | Yes | Base correlation at the detachment point. |
| `num_paths` | `integer` | Yes | Monte Carlo path count (>=3000 recommended). |
| `discount_rate` | `number` | Yes | Risk-free rate for PV. |
| `horizon_years` | `number` | Yes | Maturity in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "first_loss_tranche_pricer",
  "arguments": {
    "portfolio_notional": 0,
    "default_probability": 0,
    "recovery_rate": 0,
    "attachment_point": 0,
    "detachment_point": 0,
    "base_correlation_attachment": 0,
    "base_correlation_detachment": 0,
    "num_paths": 0,
    "discount_rate": 0,
    "horizon_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "first_loss_tranche_pricer"`.
