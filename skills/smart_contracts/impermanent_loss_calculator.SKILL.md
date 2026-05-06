---
skill: impermanent_loss_calculator
category: smart_contracts
description: Computes impermanent loss percentage for constant product pools given price ratio shifts.
tier: free
inputs: initial_price_ratio, ending_price_ratio
---

# Impermanent Loss Calculator

## Description
Computes impermanent loss percentage for constant product pools given price ratio shifts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `initial_price_ratio` | `number` | Yes | Token A price / Token B price at deposit |
| `ending_price_ratio` | `number` | Yes | Token A price / Token B price at evaluation |

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
    "ending_price_ratio": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "impermanent_loss_calculator"`.
