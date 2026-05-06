---
skill: kelly_criterion_calculator
category: quant
description: Computes Kelly fraction, position size, and expected growth rates.
tier: free
inputs: win_probability, win_amount, loss_amount, current_bankroll
---

# Kelly Criterion Calculator

## Description
Computes Kelly fraction, position size, and expected growth rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `win_probability` | `number` | Yes |  |
| `win_amount` | `number` | Yes |  |
| `loss_amount` | `number` | Yes |  |
| `current_bankroll` | `number` | Yes |  |
| `kelly_fraction` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "kelly_criterion_calculator",
  "arguments": {
    "win_probability": 0,
    "win_amount": 0,
    "loss_amount": 0,
    "current_bankroll": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "kelly_criterion_calculator"`.
