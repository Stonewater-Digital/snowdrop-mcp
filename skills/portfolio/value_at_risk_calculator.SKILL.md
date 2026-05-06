---
skill: value_at_risk_calculator
category: portfolio
description: Calculates historical Value at Risk (VaR) at a given confidence level, representing the maximum expected loss over a period.
tier: free
inputs: returns
---

# Value At Risk Calculator

## Description
Calculates historical Value at Risk (VaR) at a given confidence level, representing the maximum expected loss over a period.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns as decimals. |
| `confidence` | `number` | No | Confidence level (default 0.95 for 95%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "value_at_risk_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "value_at_risk_calculator"`.
