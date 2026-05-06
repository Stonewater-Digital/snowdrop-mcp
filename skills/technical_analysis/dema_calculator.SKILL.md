---
skill: dema_calculator
category: technical_analysis
description: Computes the Double Exponential Moving Average (2*EMA - EMA(EMA)) to highlight early momentum turns.
tier: free
inputs: prices, period
---

# Dema Calculator

## Description
Computes the Double Exponential Moving Average (2*EMA - EMA(EMA)) to highlight early momentum turns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Chronological price series used for the base EMA calculation. |
| `period` | `integer` | Yes | Lookback period for both EMA layers. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dema_calculator",
  "arguments": {
    "prices": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dema_calculator"`.
