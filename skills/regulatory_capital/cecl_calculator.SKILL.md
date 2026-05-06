---
skill: cecl_calculator
category: regulatory_capital
description: Calculates CECL reserves by segment using life-of-loan loss rates plus qualitative adjustments.
tier: free
inputs: loan_segments
---

# Cecl Calculator

## Description
Calculates CECL reserves by segment using life-of-loan loss rates plus qualitative adjustments.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `loan_segments` | `array` | Yes | Segments with balances and historical loss experience. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cecl_calculator",
  "arguments": {
    "loan_segments": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cecl_calculator"`.
