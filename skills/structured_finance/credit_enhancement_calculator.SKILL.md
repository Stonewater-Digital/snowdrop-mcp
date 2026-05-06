---
skill: credit_enhancement_calculator
category: structured_finance
description: Determines required subordination and overcollateralization to hit target ratings.
tier: free
inputs: pool_balance, target_rating, base_loss_pct, stress_multipliers
---

# Credit Enhancement Calculator

## Description
Determines required subordination and overcollateralization to hit target ratings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pool_balance` | `number` | Yes |  |
| `target_rating` | `string` | Yes |  |
| `base_loss_pct` | `number` | Yes |  |
| `stress_multipliers` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_enhancement_calculator",
  "arguments": {
    "pool_balance": 0,
    "target_rating": "<target_rating>",
    "base_loss_pct": 0,
    "stress_multipliers": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_enhancement_calculator"`.
