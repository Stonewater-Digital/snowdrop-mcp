---
skill: collar_strategy_analyzer
category: derivatives
description: Analyzes protective collar payoff, net cost, and protection ranges.
tier: free
inputs: spot_price, put_strike, call_strike, put_premium, call_premium
---

# Collar Strategy Analyzer

## Description
Analyzes protective collar payoff, net cost, and protection ranges.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes | Current stock price. Must be > 0. |
| `put_strike` | `number` | Yes | Put strike (floor). Must be > 0. |
| `call_strike` | `number` | Yes | Call strike (cap). Must be > put_strike. |
| `put_premium` | `number` | Yes | Put premium paid per share. Must be >= 0. |
| `call_premium` | `number` | Yes | Call premium received per share. Must be >= 0. |
| `shares` | `number` | No | Number of shares (default 100). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "collar_strategy_analyzer",
  "arguments": {
    "spot_price": 0,
    "put_strike": 0,
    "call_strike": 0,
    "put_premium": 0,
    "call_premium": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "collar_strategy_analyzer"`.
