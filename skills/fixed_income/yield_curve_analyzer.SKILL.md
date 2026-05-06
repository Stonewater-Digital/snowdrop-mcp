---
skill: yield_curve_analyzer
category: fixed_income
description: Classifies curve shape and recession signals from key spreads.
tier: free
inputs: yields
---

# Yield Curve Analyzer

## Description
Classifies curve shape and recession signals from key spreads.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `yields` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "yield_curve_analyzer",
  "arguments": {
    "yields": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "yield_curve_analyzer"`.
