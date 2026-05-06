---
skill: historical_volatility
category: technical_analysis
description: Computes realized volatility via close-to-close, Parkinson, Garman-Klass, or Yang-Zhang estimators.
tier: free
inputs: period, method
---

# Historical Volatility

## Description
Computes realized volatility via close-to-close, Parkinson, Garman-Klass, or Yang-Zhang estimators.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | No | Generic closing price list for close_to_close. |
| `highs` | `array` | No | High prices for high-low based estimators. |
| `lows` | `array` | No | Low prices aligned with highs. |
| `opens` | `array` | No | Open prices for Garman-Klass/Yang-Zhang. |
| `closes` | `array` | No | Close prices for open-close estimators. |
| `period` | `integer` | Yes | Number of observations used in the volatility window. |
| `method` | `string` | Yes | Estimator: close_to_close, parkinson, garman_klass, yang_zhang. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "historical_volatility",
  "arguments": {
    "period": 0,
    "method": "<method>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "historical_volatility"`.
