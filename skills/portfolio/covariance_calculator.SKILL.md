---
skill: covariance_calculator
category: portfolio
description: Calculates the sample covariance between two data series, measuring how they vary together.
tier: free
inputs: series_a, series_b
---

# Covariance Calculator

## Description
Calculates the sample covariance between two data series, measuring how they vary together.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `series_a` | `array` | Yes | First data series. |
| `series_b` | `array` | Yes | Second data series (same length as series_a). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "covariance_calculator",
  "arguments": {
    "series_a": [],
    "series_b": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "covariance_calculator"`.
