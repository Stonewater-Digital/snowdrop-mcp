---
skill: captive_insurance_analyzer
category: insurance_analytics
description: Estimates required surplus and feasibility for forming a captive insurer. Uses Value-at-Risk (VaR) at a user-specified confidence level with a normal loss distribution assumption.
tier: free
inputs: expected_annual_losses, loss_volatility_pct, premium_volume, operating_expenses
---

# Captive Insurance Analyzer

## Description
Estimates required surplus and feasibility for forming a captive insurer. Uses Value-at-Risk (VaR) at a user-specified confidence level with a normal loss distribution assumption. Returns required surplus, VaR capital, break-even loss ratio, and a feasibility score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_annual_losses` | `number` | Yes | Expected mean annual losses to be retained in the captive. Must be > 0. |
| `loss_volatility_pct` | `number` | Yes | Coefficient of variation (CV) of annual losses as a percentage. E.g., 30.0 = losses have a standard deviation of 30% of the mean. Must be > 0. |
| `premium_volume` | `number` | Yes | Annual gross premium charged by the captive. Must be > 0. |
| `operating_expenses` | `number` | Yes | Annual captive operating expenses (management fees, fronting fees, etc.). Must be >= 0. |
| `target_confidence_level_pct` | `number` | No | VaR confidence level for surplus sizing (e.g., 95.0 = 95th percentile loss). Supported values: 90, 95, 97.5, 99, 99.5. |
| `investment_return_pct` | `number` | No | Expected annual return on invested surplus. Must be >= 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "captive_insurance_analyzer",
  "arguments": {
    "expected_annual_losses": 0,
    "loss_volatility_pct": 0,
    "premium_volume": 0,
    "operating_expenses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "captive_insurance_analyzer"`.
