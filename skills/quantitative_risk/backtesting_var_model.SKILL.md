---
skill: backtesting_var_model
category: quantitative_risk
description: Evaluates VaR performance using Basel traffic light thresholds and Kupiec LR test.
tier: free
inputs: predicted_var, actual_pnl, confidence_level
---

# Backtesting Var Model

## Description
Evaluates VaR performance using Basel traffic light thresholds and Kupiec LR test.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `predicted_var` | `array` | Yes | Daily VaR predictions (positive numbers). |
| `actual_pnl` | `array` | Yes | Actual P&L observations aligned with predicted VaR (negative=loss). |
| `confidence_level` | `number` | Yes | Confidence level used in VaR calibration. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "backtesting_var_model",
  "arguments": {
    "predicted_var": [],
    "actual_pnl": [],
    "confidence_level": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "backtesting_var_model"`.
