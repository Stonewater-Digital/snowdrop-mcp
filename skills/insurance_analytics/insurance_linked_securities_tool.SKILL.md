---
skill: insurance_linked_securities_tool
category: insurance_analytics
description: Analyzes expected loss, attachment/exhaustion probabilities, multiple-at-risk (MAR), risk-adjusted spread, and relative value score for ILS instruments (cat bonds, industry loss warranties, sidecars).
tier: free
inputs: modeled_annual_expected_loss_pct, attachment_return_period_years, exhaustion_return_period_years, quoted_spread_bps, risk_free_rate_pct, notional
---

# Insurance Linked Securities Tool

## Description
Analyzes expected loss, attachment/exhaustion probabilities, multiple-at-risk (MAR), risk-adjusted spread, and relative value score for ILS instruments (cat bonds, industry loss warranties, sidecars).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `modeled_annual_expected_loss_pct` | `number` | Yes | Modeled annual expected loss as % of notional. Output from a catastrophe model (e.g., RMS, AIR). Must be > 0. |
| `attachment_return_period_years` | `number` | Yes | Return period at attachment in years (e.g., 50 = 1-in-50-year event). Must be >= exhaustion_return_period_years. |
| `exhaustion_return_period_years` | `number` | Yes | Return period at exhaustion in years (e.g., 200 = 1-in-200-year event). Must be >= attachment_return_period_years. |
| `quoted_spread_bps` | `number` | Yes | Quoted annual spread above risk-free in basis points. Must be > 0. |
| `risk_free_rate_pct` | `number` | Yes | Risk-free (SOFR/T-bill) rate as percentage. Must be >= 0. |
| `notional` | `number` | Yes | Notional principal of the ILS instrument. Must be > 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "insurance_linked_securities_tool",
  "arguments": {
    "modeled_annual_expected_loss_pct": 0,
    "attachment_return_period_years": 0,
    "exhaustion_return_period_years": 0,
    "quoted_spread_bps": 0,
    "risk_free_rate_pct": 0,
    "notional": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "insurance_linked_securities_tool"`.
