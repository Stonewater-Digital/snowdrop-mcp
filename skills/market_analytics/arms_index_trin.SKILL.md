---
skill: arms_index_trin
category: market_analytics
description: Computes TRIN as (Adv/Dec)/(AdvVol/DecVol) and averages it to identify overbought/oversold.
tier: free
inputs: advances, declines, advancing_volume, declining_volume
---

# Arms Index Trin

## Description
Computes TRIN as (Adv/Dec)/(AdvVol/DecVol) and averages it to identify overbought/oversold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `advances` | `array` | Yes | Advancing issues. |
| `declines` | `array` | Yes | Declining issues. |
| `advancing_volume` | `array` | Yes | Volume in advancers. |
| `declining_volume` | `array` | Yes | Volume in decliners. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "arms_index_trin",
  "arguments": {
    "advances": [],
    "declines": [],
    "advancing_volume": [],
    "declining_volume": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "arms_index_trin"`.
