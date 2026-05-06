---
skill: reit_nav_calculator
category: reits
description: Values properties via NOI/cap rates to derive NAV per share.
tier: free
inputs: properties, other_assets, total_debt, preferred_equity, cash, shares_outstanding
---

# Reit Nav Calculator

## Description
Values properties via NOI/cap rates to derive NAV per share.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `properties` | `array` | Yes |  |
| `other_assets` | `number` | Yes |  |
| `total_debt` | `number` | Yes |  |
| `preferred_equity` | `number` | Yes |  |
| `cash` | `number` | Yes |  |
| `shares_outstanding` | `number` | Yes |  |
| `share_price` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_nav_calculator",
  "arguments": {
    "properties": [],
    "other_assets": 0,
    "total_debt": 0,
    "preferred_equity": 0,
    "cash": 0,
    "shares_outstanding": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_nav_calculator"`.
