---
skill: ev_ebitda_comparator
category: market_analytics
description: Computes EV/EBITDA multiples per company, sector median, and growth-adjusted comparisons.
tier: free
inputs: companies
---

# Ev Ebitda Comparator

## Description
Computes EV/EBITDA multiples per company, sector median, and growth-adjusted comparisons.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `companies` | `array` | Yes | List of {name, ev, ebitda, growth_rate} objects. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ev_ebitda_comparator",
  "arguments": {
    "companies": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ev_ebitda_comparator"`.
