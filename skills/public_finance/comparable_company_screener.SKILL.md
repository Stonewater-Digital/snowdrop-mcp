---
skill: comparable_company_screener
category: public_finance
description: Calculates EV/Revenue, EV/EBITDA, P/E, and implied values for a target.
tier: free
inputs: target, comps
---

# Comparable Company Screener

## Description
Calculates EV/Revenue, EV/EBITDA, P/E, and implied values for a target.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target` | `object` | Yes |  |
| `comps` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "comparable_company_screener",
  "arguments": {
    "target": {},
    "comps": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "comparable_company_screener"`.
