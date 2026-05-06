---
skill: omega_ratio_calculator
category: portfolio
description: Calculates the Omega ratio, the ratio of cumulative gains above a threshold to cumulative losses below it.
tier: free
inputs: returns
---

# Omega Ratio Calculator

## Description
Calculates the Omega ratio, the ratio of cumulative gains above a threshold to cumulative losses below it.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns as decimals. |
| `threshold` | `number` | No | Minimum acceptable return threshold (default 0.0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "omega_ratio_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "omega_ratio_calculator"`.
