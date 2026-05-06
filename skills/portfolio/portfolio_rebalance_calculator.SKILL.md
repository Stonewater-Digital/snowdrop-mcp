---
skill: portfolio_rebalance_calculator
category: portfolio
description: Calculates the trades needed to rebalance a portfolio from current values to target weights, showing buy/sell amounts per asset.
tier: free
inputs: current_values, target_weights
---

# Portfolio Rebalance Calculator

## Description
Calculates the trades needed to rebalance a portfolio from current values to target weights, showing buy/sell amounts per asset.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_values` | `array` | Yes | List of current dollar values per asset. |
| `target_weights` | `array` | Yes | List of target weights (should sum to 1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_rebalance_calculator",
  "arguments": {
    "current_values": [],
    "target_weights": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_rebalance_calculator"`.
