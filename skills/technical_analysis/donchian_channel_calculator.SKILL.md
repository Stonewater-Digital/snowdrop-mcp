---
skill: donchian_channel_calculator
category: technical_analysis
description: Calculate Donchian Channels (highest high and lowest low over a lookback period). Used for breakout trading systems.
tier: free
inputs: highs, lows
---

# Donchian Channel Calculator

## Description
Calculate Donchian Channels (highest high and lowest low over a lookback period). Used for breakout trading systems.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `period` | `integer` | No | Lookback period for the channel. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "donchian_channel_calculator",
  "arguments": {
    "highs": [],
    "lows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "donchian_channel_calculator"`.
