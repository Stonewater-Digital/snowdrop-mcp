---
skill: ratio_interpretation_guide
category: education
description: Returns definition, formula, healthy range, and interpretation for 15+ financial ratios.
tier: free
inputs: ratio_name
---

# Ratio Interpretation Guide

## Description
Returns definition, formula, healthy range, and interpretation for 15+ financial ratios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ratio_name` | `string` | Yes | The name of the financial ratio to look up. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ratio_interpretation_guide",
  "arguments": {
    "ratio_name": "<ratio_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ratio_interpretation_guide"`.
