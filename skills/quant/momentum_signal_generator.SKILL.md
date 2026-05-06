---
skill: momentum_signal_generator
category: quant
description: Calculates short vs long lookback momentum and standardized signal strength.
tier: free
inputs: price_series
---

# Momentum Signal Generator

## Description
Calculates short vs long lookback momentum and standardized signal strength.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_series` | `array` | Yes |  |
| `short_window` | `integer` | No |  |
| `long_window` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "momentum_signal_generator",
  "arguments": {
    "price_series": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "momentum_signal_generator"`.
