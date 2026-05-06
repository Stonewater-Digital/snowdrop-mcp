---
skill: default_rate_calculator
category: private_credit
description: Calculates period and trailing default rates from cohort data.
tier: free
inputs: defaults_by_period, outstandings_by_period
---

# Default Rate Calculator

## Description
Calculates period and trailing default rates from cohort data.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `defaults_by_period` | `array` | Yes |  |
| `outstandings_by_period` | `array` | Yes |  |
| `lookback_periods` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "default_rate_calculator",
  "arguments": {
    "defaults_by_period": [],
    "outstandings_by_period": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "default_rate_calculator"`.
