---
skill: max_drawdown_calculator
category: portfolio
description: Calculates the maximum drawdown from a series of prices, measuring the largest peak-to-trough decline as a percentage.
tier: free
inputs: prices
---

# Max Drawdown Calculator

## Description
Calculates the maximum drawdown from a series of prices, measuring the largest peak-to-trough decline as a percentage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | List of asset prices in chronological order. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "max_drawdown_calculator",
  "arguments": {
    "prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "max_drawdown_calculator"`.
