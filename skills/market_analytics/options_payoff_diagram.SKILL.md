---
skill: options_payoff_diagram
category: market_analytics
description: Calculates strategy payoff across a price grid and identifies basic spread types.
tier: free
inputs: legs, price_range
---

# Options Payoff Diagram

## Description
Calculates strategy payoff across a price grid and identifies basic spread types.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `legs` | `array` | Yes | List of option legs with type (call/put), strike, premium, quantity, direction (long/short). |
| `price_range` | `array` | Yes | List of underlying prices to evaluate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "options_payoff_diagram",
  "arguments": {
    "legs": [],
    "price_range": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_payoff_diagram"`.
