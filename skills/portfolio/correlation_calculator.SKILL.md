---
skill: correlation_calculator
category: portfolio
description: Calculates the Pearson correlation coefficient between two data series, measuring the linear relationship between them.
tier: free
inputs: series_a, series_b
---

# Correlation Calculator

## Description
Calculates the Pearson correlation coefficient between two data series, measuring the linear relationship between them.

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
  "tool": "correlation_calculator",
  "arguments": {
    "series_a": [],
    "series_b": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "correlation_calculator"`.
