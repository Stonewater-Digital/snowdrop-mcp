---
skill: same_store_noi_growth
category: reits
description: Calculates YoY same-store NOI growth and contribution analysis.
tier: free
inputs: prior_noi, current_noi
---

# Same Store Noi Growth

## Description
Calculates YoY same-store NOI growth and contribution analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prior_noi` | `number` | Yes |  |
| `current_noi` | `number` | Yes |  |
| `expansion_noi` | `number` | No |  |
| `disposition_noi` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "same_store_noi_growth",
  "arguments": {
    "prior_noi": 0,
    "current_noi": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "same_store_noi_growth"`.
