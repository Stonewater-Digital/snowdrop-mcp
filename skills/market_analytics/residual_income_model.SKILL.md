---
skill: residual_income_model
category: market_analytics
description: Discounts residual incomes plus current book value to estimate intrinsic value.
tier: free
inputs: book_value, roe, cost_of_equity, years, terminal_roe
---

# Residual Income Model

## Description
Discounts residual incomes plus current book value to estimate intrinsic value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `book_value` | `number` | Yes | Current book value per share. |
| `roe` | `number` | Yes | Return on equity in stage 1 (decimal). |
| `cost_of_equity` | `number` | Yes | Required return (decimal). |
| `years` | `integer` | Yes | Explicit forecast years. |
| `terminal_roe` | `number` | Yes | ROE applied to terminal period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "residual_income_model",
  "arguments": {
    "book_value": 0,
    "roe": 0,
    "cost_of_equity": 0,
    "years": 0,
    "terminal_roe": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "residual_income_model"`.
