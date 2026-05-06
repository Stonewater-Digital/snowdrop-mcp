---
skill: risk_parity_calculator
category: quant
description: Allocates inverse-volatility weights and scales to a target portfolio volatility.
tier: free
inputs: asset_vols_pct
---

# Risk Parity Calculator

## Description
Allocates inverse-volatility weights and scales to a target portfolio volatility.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_vols_pct` | `object` | Yes |  |
| `target_portfolio_vol_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "risk_parity_calculator",
  "arguments": {
    "asset_vols_pct": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_parity_calculator"`.
