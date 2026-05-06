---
skill: runway_calculator
category: small_business
description: Calculate how many months of runway remain given current cash and monthly burn rate, plus estimated end date.
tier: free
inputs: current_cash, monthly_burn_rate
---

# Runway Calculator

## Description
Calculate how many months of runway remain given current cash and monthly burn rate, plus estimated end date.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_cash` | `number` | Yes | Current cash on hand. |
| `monthly_burn_rate` | `number` | Yes | Net monthly burn rate (positive = spending). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "runway_calculator",
  "arguments": {
    "current_cash": 0,
    "monthly_burn_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "runway_calculator"`.
