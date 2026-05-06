---
skill: keltner_channel_calculator
category: technical_analysis
description: Calculate Keltner Channels (middle EMA band with ATR-based upper/lower channels). Used for trend direction and volatility-based breakouts.
tier: free
inputs: prices
---

# Keltner Channel Calculator

## Description
Calculate Keltner Channels (middle EMA band with ATR-based upper/lower channels). Used for trend direction and volatility-based breakouts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | List of closing prices (oldest to newest). |
| `period` | `integer` | No | EMA and ATR lookback period. |
| `atr_multiplier` | `number` | No | Multiplier for ATR to set channel width. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "keltner_channel_calculator",
  "arguments": {
    "prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "keltner_channel_calculator"`.
