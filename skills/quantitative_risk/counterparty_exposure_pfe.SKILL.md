---
skill: counterparty_exposure_pfe
category: quantitative_risk
description: Computes potential future exposure (PFE) across tenors using collateralized netting set information.
tier: free
inputs: trade_mtm_series, netting_set, collateral, margin_period_of_risk
---

# Counterparty Exposure Pfe

## Description
Computes potential future exposure (PFE) across tenors using collateralized netting set information.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trade_mtm_series` | `array` | Yes | List of MTM scenario sets per tenor with mtm_values array. |
| `netting_set` | `string` | Yes | Identifier of the counterparty netting set. |
| `collateral` | `object` | Yes | Collateral terms including initial/variation margin and thresholds. |
| `margin_period_of_risk` | `integer` | Yes | Margin period of risk in days for regulatory EAD. |
| `confidence_level` | `number` | No | PFE percentile (default 0.975 as in IMM). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "counterparty_exposure_pfe",
  "arguments": {
    "trade_mtm_series": [],
    "netting_set": "<netting_set>",
    "collateral": {},
    "margin_period_of_risk": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "counterparty_exposure_pfe"`.
