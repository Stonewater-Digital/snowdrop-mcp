---
skill: donchian_channels
category: technical_analysis
description: Applies Richard Donchian's channel breakout system using highest highs and lowest lows.
tier: free
inputs: highs, lows, period
---

# Donchian Channels

## Description
Applies Richard Donchian's channel breakout system using highest highs and lowest lows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High price series. |
| `lows` | `array` | Yes | Low price series. |
| `period` | `integer` | Yes | Lookback period (default 20). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "donchian_channels",
  "arguments": {
    "highs": [],
    "lows": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "donchian_channels"`.
