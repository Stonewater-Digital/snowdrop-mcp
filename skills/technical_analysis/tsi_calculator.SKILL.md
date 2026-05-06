---
skill: tsi_calculator
category: technical_analysis
description: Calculates William Blau's True Strength Index via double EMA of price momentum.
tier: free
inputs: prices, long_period, short_period, signal_period
---

# Tsi Calculator

## Description
Calculates William Blau's True Strength Index via double EMA of price momentum.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price series (oldest first). |
| `long_period` | `integer` | Yes | Long EMA period (e.g., 25). |
| `short_period` | `integer` | Yes | Short EMA period (e.g., 13). |
| `signal_period` | `integer` | Yes | Signal EMA on TSI (e.g., 7). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tsi_calculator",
  "arguments": {
    "prices": [],
    "long_period": 0,
    "short_period": 0,
    "signal_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tsi_calculator"`.
