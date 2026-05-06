---
skill: linear_regression_forecaster
category: forecasting
description: Fits y = mx + b and projects forward values with r-squared diagnostics.
tier: free
inputs: data_points
---

# Linear Regression Forecaster

## Description
Fits y = mx + b and projects forward values with r-squared diagnostics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data_points` | `array` | Yes |  |
| `forecast_periods` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "linear_regression_forecaster",
  "arguments": {
    "data_points": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "linear_regression_forecaster"`.
