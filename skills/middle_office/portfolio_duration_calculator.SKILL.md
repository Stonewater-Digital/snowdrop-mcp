---
skill: portfolio_duration_calculator
category: middle_office
description: Calculates aggregate dollar duration and DV01 for fixed income books.
tier: free
inputs: positions
---

# Portfolio Duration Calculator

## Description
Calculates aggregate dollar duration and DV01 for fixed income books.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_duration_calculator",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_duration_calculator"`.
