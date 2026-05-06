---
skill: term_premium_calculator
category: quant
description: Compares observed term yield to expected average of policy rates.
tier: free
inputs: term_yield_pct, expected_short_path_pct
---

# Term Premium Calculator

## Description
Compares observed term yield to expected average of policy rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `term_yield_pct` | `number` | Yes |  |
| `expected_short_path_pct` | `array` | Yes |  |
| `convexity_adjustment_bps` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "term_premium_calculator",
  "arguments": {
    "term_yield_pct": 0,
    "expected_short_path_pct": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "term_premium_calculator"`.
