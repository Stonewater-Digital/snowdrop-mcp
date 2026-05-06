---
skill: trend_line_calculator
category: technical_analysis
description: Constructs trendlines using linear regression or peak/trough anchors to monitor price breaks.
tier: free
inputs: prices, lookback, method
---

# Trend Line Calculator

## Description
Constructs trendlines using linear regression or peak/trough anchors to monitor price breaks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price series. |
| `lookback` | `integer` | Yes | Number of bars used for the analysis. |
| `method` | `string` | Yes | linear_regression or peak_trough. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trend_line_calculator",
  "arguments": {
    "prices": [],
    "lookback": 0,
    "method": "<method>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trend_line_calculator"`.
