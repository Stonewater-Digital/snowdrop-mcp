---
skill: keltner_channels
category: technical_analysis
description: Calculates Keltner Channels: EMA midline with ATR-based upper and lower envelopes.
tier: free
inputs: highs, lows, closes, ema_period, atr_period, multiplier
---

# Keltner Channels

## Description
Calculates Keltner Channels: EMA midline with ATR-based upper and lower envelopes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `ema_period` | `integer` | Yes | EMA lookback (default 20). |
| `atr_period` | `integer` | Yes | ATR lookback (default 10). |
| `multiplier` | `number` | Yes | ATR multiplier (default 2). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "keltner_channels",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "ema_period": 0,
    "atr_period": 0,
    "multiplier": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "keltner_channels"`.
