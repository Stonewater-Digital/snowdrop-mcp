---
skill: dividend_accrual_calculator
category: middle_office
description: Accrues dividends between ex-date and pay-date across positions.
tier: free
inputs: positions, as_of_date
---

# Dividend Accrual Calculator

## Description
Accrues dividends between ex-date and pay-date across positions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `as_of_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dividend_accrual_calculator",
  "arguments": {
    "positions": [],
    "as_of_date": "<as_of_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dividend_accrual_calculator"`.
