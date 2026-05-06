---
skill: awesome_oscillator
category: technical_analysis
description: Calculates Bill Williams' Awesome Oscillator using 5/34 SMA of median price to highlight momentum shifts.
tier: free
inputs: highs, lows
---

# Awesome Oscillator

## Description
Calculates Bill Williams' Awesome Oscillator using 5/34 SMA of median price to highlight momentum shifts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices (oldest first). |
| `lows` | `array` | Yes | Low prices aligned with highs. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "awesome_oscillator",
  "arguments": {
    "highs": [],
    "lows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "awesome_oscillator"`.
