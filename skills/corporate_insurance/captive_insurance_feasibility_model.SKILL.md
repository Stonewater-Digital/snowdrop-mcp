---
skill: captive_insurance_feasibility_model
category: corporate_insurance
description: Scores captive feasibility based on losses, premium, and surplus needs.
tier: free
inputs: expected_losses, loss_volatility_pct, planned_premium, operating_expenses
---

# Captive Insurance Feasibility Model

## Description
Scores captive feasibility based on losses, premium, and surplus needs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_losses` | `number` | Yes |  |
| `loss_volatility_pct` | `number` | Yes |  |
| `planned_premium` | `number` | Yes |  |
| `target_confidence_pct` | `number` | No |  |
| `operating_expenses` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "captive_insurance_feasibility_model",
  "arguments": {
    "expected_losses": 0,
    "loss_volatility_pct": 0,
    "planned_premium": 0,
    "operating_expenses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "captive_insurance_feasibility_model"`.
