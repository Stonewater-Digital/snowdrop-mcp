---
skill: strategy_backtester
category: simulation
description: Runs deterministic backtests for rule-based trading strategies.
tier: free
inputs: strategy, price_history, initial_capital
---

# Strategy Backtester

## Description
Runs deterministic backtests for rule-based trading strategies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `strategy` | `object` | Yes |  |
| `price_history` | `array` | Yes |  |
| `initial_capital` | `number` | Yes | Starting cash for the simulation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "strategy_backtester",
  "arguments": {
    "strategy": {},
    "price_history": [],
    "initial_capital": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "strategy_backtester"`.
