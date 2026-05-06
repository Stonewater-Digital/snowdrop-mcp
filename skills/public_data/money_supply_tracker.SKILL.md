---
skill: money_supply_tracker
category: public_data
description: Track US money supply from FRED. Supports M1 (M1SL) and M2 (M2SL) measures.
tier: free
inputs: none
---

# Money Supply Tracker

## Description
Track US money supply from FRED. Supports M1 (M1SL) and M2 (M2SL) measures. Returns latest value and trend. Requires FRED_API_KEY.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `measure` | `string` | No | Money supply measure: 'M1' or 'M2'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "money_supply_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "money_supply_tracker"`.
