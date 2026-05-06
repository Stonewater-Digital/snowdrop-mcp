---
skill: detrended_price_oscillator_calculator
category: technical_analysis
description: Calculate the Detrended Price Oscillator (DPO), which removes the trend from prices to identify cycles. DPO = Close[-(period/2+1)] - SMA(period).
tier: free
inputs: closes
---

# Detrended Price Oscillator Calculator

## Description
Calculate the Detrended Price Oscillator (DPO), which removes the trend from prices to identify cycles. DPO = Close[-(period/2+1)] - SMA(period).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |
| `period` | `integer` | No | DPO lookback period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "detrended_price_oscillator_calculator",
  "arguments": {
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "detrended_price_oscillator_calculator"`.
