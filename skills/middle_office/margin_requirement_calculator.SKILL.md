---
skill: margin_requirement_calculator
category: middle_office
description: Computes SPAN-style margin based on risk weights and add-ons.
tier: free
inputs: positions
---

# Margin Requirement Calculator

## Description
Computes SPAN-style margin based on risk weights and add-ons.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `house_margin_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "margin_requirement_calculator",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "margin_requirement_calculator"`.
