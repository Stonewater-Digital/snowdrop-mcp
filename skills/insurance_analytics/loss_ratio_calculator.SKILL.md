---
skill: loss_ratio_calculator
category: insurance_analytics
description: Calculates incurred loss ratio, ALAE-inclusive ratio, and development-adjusted ultimate loss ratio from earned premium and loss components.
tier: free
inputs: incurred_losses, earned_premium
---

# Loss Ratio Calculator

## Description
Calculates incurred loss ratio, ALAE-inclusive ratio, and development-adjusted ultimate loss ratio from earned premium and loss components.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `incurred_losses` | `number` | Yes | Incurred losses (paid + case reserves, excluding ALAE). Must be >= 0. |
| `earned_premium` | `number` | Yes | Net earned premium for the period. Must be > 0. |
| `alae` | `number` | No | Allocated loss adjustment expenses (defense costs, etc.). Must be >= 0. |
| `development_factor` | `number` | No | Cumulative loss development factor (LDF) to ultimate. 1.0 = fully developed; >1.0 = immature losses still developing. Must be >= 1.0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loss_ratio_calculator",
  "arguments": {
    "incurred_losses": 0,
    "earned_premium": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loss_ratio_calculator"`.
