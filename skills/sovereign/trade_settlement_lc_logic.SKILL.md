---
skill: trade_settlement_lc_logic
category: sovereign
description: Validates Letters of Credit against UCP 600 international rules, checks document completeness, and generates settlement recommendations.
tier: free
inputs: lc_data
---

# Trade Settlement Lc Logic

## Description
Validates Letters of Credit against UCP 600 international rules, checks document completeness, and generates settlement recommendations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lc_data` | `object` | Yes | Letter of Credit terms |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trade_settlement_lc_logic",
  "arguments": {
    "lc_data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trade_settlement_lc_logic"`.
