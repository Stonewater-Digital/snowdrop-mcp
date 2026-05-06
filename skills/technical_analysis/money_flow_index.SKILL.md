---
skill: money_flow_index
category: technical_analysis
description: Calculates the volume-weighted RSI known as Money Flow Index (MFI).
tier: free
inputs: highs, lows, closes, volumes, period
---

# Money Flow Index

## Description
Calculates the volume-weighted RSI known as Money Flow Index (MFI).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volume per bar. |
| `period` | `integer` | Yes | Lookback period (default 14). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "money_flow_index",
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
Invoke via `snowdrop_execute` with `tool_name: "money_flow_index"`.
