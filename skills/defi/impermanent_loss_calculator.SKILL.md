---
skill: impermanent_loss_calculator
category: defi
description: Evaluates current LP value vs hold value and required fees to break even.
tier: free
inputs: initial_price_ratio, current_price_ratio, initial_deposit_value
---

# Impermanent Loss Calculator

## Description
Evaluates current LP value vs hold value and required fees to break even.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `initial_price_ratio` | `number` | Yes |  |
| `current_price_ratio` | `number` | Yes |  |
| `initial_deposit_value` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "impermanent_loss_calculator",
  "arguments": {
    "initial_price_ratio": 0,
    "current_price_ratio": 0,
    "initial_deposit_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "impermanent_loss_calculator"`.
