---
skill: klinger_oscillator
category: technical_analysis
description: Implements the Klinger Volume Oscillator (fast/slow EMAs of volume force) with signal histogram.
tier: free
inputs: highs, lows, closes, volumes, fast, slow, signal
---

# Klinger Oscillator

## Description
Implements the Klinger Volume Oscillator (fast/slow EMAs of volume force) with signal histogram.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volume data. |
| `fast` | `integer` | Yes | Fast EMA length (34). |
| `slow` | `integer` | Yes | Slow EMA length (55). |
| `signal` | `integer` | Yes | Signal EMA length (13). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "klinger_oscillator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "volumes": [],
    "fast": 0,
    "slow": 0,
    "signal": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "klinger_oscillator"`.
