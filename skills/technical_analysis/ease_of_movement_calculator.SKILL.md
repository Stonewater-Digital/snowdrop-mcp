---
skill: ease_of_movement_calculator
category: technical_analysis
description: Calculate the Ease of Movement (EMV) indicator, which relates price change to volume. Positive EMV = prices advancing on low volume; negative = declining.
tier: free
inputs: highs, lows, volumes
---

# Ease Of Movement Calculator

## Description
Calculate the Ease of Movement (EMV) indicator, which relates price change to volume. Positive EMV = prices advancing on low volume; negative = declining.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `volumes` | `array` | Yes | List of volume values (oldest to newest). |
| `period` | `integer` | No | SMA smoothing period for EMV. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ease_of_movement_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ease_of_movement_calculator"`.
