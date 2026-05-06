---
skill: gordon_growth_model
category: market_analytics
description: Computes intrinsic value using Gordon Growth, plus yield and growth sensitivity.
tier: free
inputs: current_dividend, growth_rate, required_return
---

# Gordon Growth Model

## Description
Computes intrinsic value using Gordon Growth, plus yield and growth sensitivity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_dividend` | `number` | Yes | Most recent annual dividend per share. |
| `growth_rate` | `number` | Yes | Expected perpetual growth (decimal). |
| `required_return` | `number` | Yes | Investor required return (decimal). |
| `current_price` | `number` | No | Optional current market price. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gordon_growth_model",
  "arguments": {
    "current_dividend": 0,
    "growth_rate": 0,
    "required_return": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gordon_growth_model"`.
