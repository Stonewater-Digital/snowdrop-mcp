---
skill: leverage_ratio_calculator
category: quantitative_risk
description: Computes Basel leverage ratio including SA-CCR derivative add-ons and securities financing exposures.
tier: free
inputs: tier1_capital, on_balance_exposures, derivative_exposures, sft_exposures, off_balance_items
---

# Leverage Ratio Calculator

## Description
Computes Basel leverage ratio including SA-CCR derivative add-ons and securities financing exposures.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tier1_capital` | `number` | Yes | Tier 1 capital in base currency. |
| `on_balance_exposures` | `number` | Yes | Total assets net of regulatory adjustments. |
| `derivative_exposures` | `number` | Yes | Replacement cost plus PFE from SA-CCR. |
| `sft_exposures` | `number` | Yes | Exposure measure for securities financing transactions. |
| `off_balance_items` | `number` | Yes | Credit conversion amount for off-balance sheet items. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "leverage_ratio_calculator",
  "arguments": {
    "tier1_capital": 0,
    "on_balance_exposures": 0,
    "derivative_exposures": 0,
    "sft_exposures": 0,
    "off_balance_items": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "leverage_ratio_calculator"`.
