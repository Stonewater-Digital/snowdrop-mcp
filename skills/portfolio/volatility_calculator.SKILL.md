---
skill: volatility_calculator
category: portfolio
description: Calculates historical volatility (standard deviation of returns), optionally annualized using sqrt(252) for daily data.
tier: free
inputs: returns
---

# Volatility Calculator

## Description
Calculates historical volatility (standard deviation of returns), optionally annualized using sqrt(252) for daily data.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns as decimals. |
| `annualize` | `boolean` | No | Whether to annualize using sqrt(252) (default true). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "volatility_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "volatility_calculator"`.
