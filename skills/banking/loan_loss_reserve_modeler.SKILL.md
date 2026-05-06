---
skill: loan_loss_reserve_modeler
category: banking
description: Calculates expected credit losses by segment with macro overlays.
tier: free
inputs: loan_portfolio
---

# Loan Loss Reserve Modeler

## Description
Calculates expected credit losses by segment with macro overlays.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loan_portfolio` | `array` | Yes |  |
| `macro_adjustment` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_loss_reserve_modeler",
  "arguments": {
    "loan_portfolio": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_loss_reserve_modeler"`.
