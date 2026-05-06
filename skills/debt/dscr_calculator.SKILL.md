---
skill: dscr_calculator
category: debt
description: Computes DSCR, assessment tier, excess cash, and headroom for new debt.
tier: free
inputs: net_operating_income, total_debt_service
---

# Dscr Calculator

## Description
Computes DSCR, assessment tier, excess cash, and headroom for new debt.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_operating_income` | `number` | Yes |  |
| `total_debt_service` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dscr_calculator",
  "arguments": {
    "net_operating_income": 0,
    "total_debt_service": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dscr_calculator"`.
