---
skill: yield_curve_analyzer
category: quant
description: Builds spot discounts and forward rates to classify curve shape.
tier: free
inputs: par_yields
---

# Yield Curve Analyzer

## Description
Builds spot discounts and forward rates to classify curve shape.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `par_yields` | `array` | Yes |  |

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
    "par_yields": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "yield_curve_analyzer"`.
