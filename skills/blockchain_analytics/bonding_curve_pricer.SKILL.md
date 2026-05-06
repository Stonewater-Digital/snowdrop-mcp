---
skill: bonding_curve_pricer
category: blockchain_analytics
description: Evaluates different bonding curve formulations (linear, exponential, Bancor) for price projection.
tier: free
inputs: curve_type, supply, reserve_balance, reserve_ratio, trade_amount
---

# Bonding Curve Pricer

## Description
Evaluates different bonding curve formulations (linear, exponential, Bancor) for price projection.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `curve_type` | `string` | Yes | linear/polynomial/sigmoid/exponential |
| `supply` | `number` | Yes | Current token supply |
| `reserve_balance` | `number` | Yes | Reserve collateral balance |
| `reserve_ratio` | `number` | Yes | Bancor-style reserve ratio (0-1) |
| `trade_amount` | `number` | Yes | Tokens to buy or sell for evaluating slippage |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bonding_curve_pricer",
  "arguments": {
    "curve_type": "<curve_type>",
    "supply": 0,
    "reserve_balance": 0,
    "reserve_ratio": 0,
    "trade_amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bonding_curve_pricer"`.
