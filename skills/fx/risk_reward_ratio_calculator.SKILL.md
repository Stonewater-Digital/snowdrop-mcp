---
skill: risk_reward_ratio_calculator
category: fx
description: Calculate risk-reward ratio from entry price, stop-loss, and take-profit levels. Also computes breakeven win rate.
tier: free
inputs: entry_price, stop_loss, take_profit
---

# Risk Reward Ratio Calculator

## Description
Calculate risk-reward ratio from entry price, stop-loss, and take-profit levels. Also computes breakeven win rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entry_price` | `number` | Yes | Trade entry price. |
| `stop_loss` | `number` | Yes | Stop-loss price level. |
| `take_profit` | `number` | Yes | Take-profit price level. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "risk_reward_ratio_calculator",
  "arguments": {
    "entry_price": 0,
    "stop_loss": 0,
    "take_profit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_reward_ratio_calculator"`.
