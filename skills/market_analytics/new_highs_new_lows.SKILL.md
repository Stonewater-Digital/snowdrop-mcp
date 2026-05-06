---
skill: new_highs_new_lows
category: market_analytics
description: Computes new-high minus new-low series, ratios, and signals.
tier: free
inputs: new_highs, new_lows
---

# New Highs New Lows

## Description
Computes new-high minus new-low series, ratios, and signals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `new_highs` | `array` | Yes | Counts of new highs. |
| `new_lows` | `array` | Yes | Counts of new lows. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "new_highs_new_lows",
  "arguments": {
    "new_highs": [],
    "new_lows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "new_highs_new_lows"`.
