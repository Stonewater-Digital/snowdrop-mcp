---
skill: commodity_channel_index_calculator
category: technical_analysis
description: Calculate the Commodity Channel Index (CCI), an oscillator measuring deviation from the statistical mean. Values above +100 suggest overbought; below -100 suggest oversold.
tier: free
inputs: highs, lows, closes
---

# Commodity Channel Index Calculator

## Description
Calculate the Commodity Channel Index (CCI), an oscillator measuring deviation from the statistical mean. Values above +100 suggest overbought; below -100 suggest oversold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |
| `period` | `integer` | No | CCI lookback period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commodity_channel_index_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_channel_index_calculator"`.
