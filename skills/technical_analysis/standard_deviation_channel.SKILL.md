---
skill: standard_deviation_channel
category: technical_analysis
description: Performs least-squares regression on prices and offsets by standard deviation bands.
tier: free
inputs: prices, period, num_std
---

# Standard Deviation Channel

## Description
Performs least-squares regression on prices and offsets by standard deviation bands.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price series. |
| `period` | `integer` | Yes | Number of observations used for regression. |
| `num_std` | `number` | Yes | Standard deviation multiplier for channel width. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "standard_deviation_channel",
  "arguments": {
    "prices": [],
    "period": 0,
    "num_std": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "standard_deviation_channel"`.
