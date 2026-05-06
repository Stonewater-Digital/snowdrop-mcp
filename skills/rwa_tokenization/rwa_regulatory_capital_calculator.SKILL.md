---
skill: rwa_regulatory_capital_calculator
category: rwa_tokenization
description: Calculates RWA exposure and capital requirement based on risk weights and target ratios.
tier: free
inputs: asset_balance, risk_weight_pct, capital_ratio_target_pct
---

# Rwa Regulatory Capital Calculator

## Description
Calculates RWA exposure and capital requirement based on risk weights and target ratios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_balance` | `number` | Yes | Balance of tokenized assets |
| `risk_weight_pct` | `number` | Yes | Regulatory risk weight percent |
| `capital_ratio_target_pct` | `number` | Yes | Target capital ratio percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_regulatory_capital_calculator",
  "arguments": {
    "asset_balance": 0,
    "risk_weight_pct": 0,
    "capital_ratio_target_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_regulatory_capital_calculator"`.
