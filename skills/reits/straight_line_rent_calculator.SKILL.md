---
skill: straight_line_rent_calculator
category: reits
description: Computes straight-line rent adjustment over the remaining lease term.
tier: free
inputs: cash_rent, gaap_rent, remaining_term_years
---

# Straight Line Rent Calculator

## Description
Computes straight-line rent adjustment over the remaining lease term.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_rent` | `number` | Yes |  |
| `gaap_rent` | `number` | Yes |  |
| `remaining_term_years` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "straight_line_rent_calculator",
  "arguments": {
    "cash_rent": 0,
    "gaap_rent": 0,
    "remaining_term_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "straight_line_rent_calculator"`.
