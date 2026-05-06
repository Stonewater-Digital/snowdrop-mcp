---
skill: chaikin_money_flow
category: technical_analysis
description: Calculates Chaikin Money Flow (CMF) over a specified period to quantify accumulation or distribution.
tier: free
inputs: highs, lows, closes, volumes, period
---

# Chaikin Money Flow

## Description
Calculates Chaikin Money Flow (CMF) over a specified period to quantify accumulation or distribution.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volume per bar. |
| `period` | `integer` | Yes | Lookback for CMF (default 20). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "chaikin_money_flow",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "volumes": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chaikin_money_flow"`.
