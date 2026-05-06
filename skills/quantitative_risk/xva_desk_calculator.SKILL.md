---
skill: xva_desk_calculator
category: quantitative_risk
description: Computes the suite of valuation adjustments using exposure profiles and hazard rate approximations.
tier: free
inputs: exposure_profile, counterparty_pd, own_pd, funding_curve, capital_cost_pct, margin_profile
---

# Xva Desk Calculator

## Description
Computes the suite of valuation adjustments using exposure profiles and hazard rate approximations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposure_profile` | `array` | Yes | Expected exposure schedule by tenor in years. |
| `counterparty_pd` | `number` | Yes | Annual counterparty PD (decimal). |
| `own_pd` | `number` | Yes | Institution PD used for DVA (decimal). |
| `funding_curve` | `array` | Yes | Discount factors represented by tenor and funding rate (decimal). |
| `capital_cost_pct` | `number` | Yes | Cost of capital used for KVA. |
| `margin_profile` | `object` | Yes | Margin terms (initial/variation). |
| `lgd_pct` | `number` | No | Loss-given-default percentage for CVA/DVA. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "xva_desk_calculator",
  "arguments": {
    "exposure_profile": [],
    "counterparty_pd": 0,
    "own_pd": 0,
    "funding_curve": [],
    "capital_cost_pct": 0,
    "margin_profile": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "xva_desk_calculator"`.
