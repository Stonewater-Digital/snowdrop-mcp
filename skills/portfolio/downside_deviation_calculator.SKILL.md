---
skill: downside_deviation_calculator
category: portfolio
description: Calculates downside deviation, measuring the volatility of returns below a minimum acceptable return (MAR) threshold.
tier: free
inputs: returns
---

# Downside Deviation Calculator

## Description
Calculates downside deviation, measuring the volatility of returns below a minimum acceptable return (MAR) threshold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns as decimals. |
| `mar` | `number` | No | Minimum acceptable return threshold (default 0.0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "downside_deviation_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "downside_deviation_calculator"`.
