---
skill: rule_of_72_calculator
category: personal_finance
description: Uses the rule of 72 alongside logarithmic growth math to estimate doubling, tripling, and quadrupling timelines for an annual return.
tier: free
inputs: annual_rate
---

# Rule Of 72 Calculator

## Description
Uses the rule of 72 alongside logarithmic growth math to estimate doubling, tripling, and quadrupling timelines for an annual return.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_rate` | `number` | Yes | Annual compound growth rate as decimal (e.g., 0.08). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rule_of_72_calculator",
  "arguments": {
    "annual_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rule_of_72_calculator"`.
