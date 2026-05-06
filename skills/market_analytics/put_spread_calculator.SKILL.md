---
skill: put_spread_calculator
category: market_analytics
description: Calculates payoff metrics for bull or bear put spreads.
tier: free
inputs: short_strike, short_premium, long_strike, long_premium, contracts, option_type
---

# Put Spread Calculator

## Description
Calculates payoff metrics for bull or bear put spreads.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `short_strike` | `number` | Yes | Strike sold. |
| `short_premium` | `number` | Yes | Premium received for short put. |
| `long_strike` | `number` | Yes | Strike bought. |
| `long_premium` | `number` | Yes | Premium paid for long put. |
| `contracts` | `integer` | Yes | Number of spreads. |
| `option_type` | `string` | Yes | bull or bear. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "put_spread_calculator",
  "arguments": {
    "short_strike": 0,
    "short_premium": 0,
    "long_strike": 0,
    "long_premium": 0,
    "contracts": 0,
    "option_type": "<option_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "put_spread_calculator"`.
