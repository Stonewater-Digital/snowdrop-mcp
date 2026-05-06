---
skill: multi_period_rebalancer
category: portfolio_construction
description: Dynamic programming rebalancer choosing whether to rebalance or drift each period based on expected return trade-off versus transaction costs, following Bodie, Kane, Marcus multi-period optimization.
tier: free
inputs: target_weights, initial_weights, expected_returns, transaction_cost_bps
---

# Multi Period Rebalancer

## Description
Dynamic programming rebalancer choosing whether to rebalance or drift each period based on expected return trade-off versus transaction costs, following Bodie, Kane, Marcus multi-period optimization.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_weights` | `object` | Yes | Strategic asset allocation weights that trades reset to. |
| `initial_weights` | `object` | Yes | Starting allocation weights, typically equal to target. |
| `expected_returns` | `array` | Yes | List of per-period expected returns keyed by asset. |
| `transaction_cost_bps` | `number` | Yes | Round-trip transaction cost per unit weight traded (in basis points). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "multi_period_rebalancer",
  "arguments": {
    "target_weights": {},
    "initial_weights": {},
    "expected_returns": [],
    "transaction_cost_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_period_rebalancer"`.
