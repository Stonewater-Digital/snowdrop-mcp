---
skill: stochastic_oscillator
category: technical_analysis
description: Implements George Lane's %K/%D oscillator with configurable slowing to detect momentum shifts.
tier: free
inputs: highs, lows, closes, k_period, d_period, slowing
---

# Stochastic Oscillator

## Description
Implements George Lane's %K/%D oscillator with configurable slowing to detect momentum shifts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `k_period` | `integer` | Yes | Lookback period for %K (default 14). |
| `d_period` | `integer` | Yes | Smoothing period for %D (default 3). |
| `slowing` | `integer` | Yes | Slowing factor for %K (default 3). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "stochastic_oscillator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "k_period": 0,
    "d_period": 0,
    "slowing": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stochastic_oscillator"`.
