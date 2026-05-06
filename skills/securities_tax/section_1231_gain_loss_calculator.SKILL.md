---
skill: section_1231_gain_loss_calculator
category: securities_tax
description: Computes 1231 gains and recapture amounts under 5-year lookback.
tier: free
inputs: current_year_gain, current_year_loss, prior_lookback_losses
---

# Section 1231 Gain Loss Calculator

## Description
Computes 1231 gains and recapture amounts under 5-year lookback.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_year_gain` | `number` | Yes |  |
| `current_year_loss` | `number` | Yes |  |
| `prior_lookback_losses` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "section_1231_gain_loss_calculator",
  "arguments": {
    "current_year_gain": 0,
    "current_year_loss": 0,
    "prior_lookback_losses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "section_1231_gain_loss_calculator"`.
