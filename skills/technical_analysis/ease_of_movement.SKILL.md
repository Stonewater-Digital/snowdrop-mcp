---
skill: ease_of_movement
category: technical_analysis
description: Computes Richard Arms' Ease of Movement oscillator with SMA signal to judge efficient rallies/drops.
tier: free
inputs: highs, lows, volumes, period
---

# Ease Of Movement

## Description
Computes Richard Arms' Ease of Movement oscillator with SMA signal to judge efficient rallies/drops.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `volumes` | `array` | Yes | Volume per bar. |
| `period` | `integer` | Yes | SMA period for EMV signal (default 14). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ease_of_movement",
  "arguments": {
    "highs": [],
    "lows": [],
    "volumes": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ease_of_movement"`.
