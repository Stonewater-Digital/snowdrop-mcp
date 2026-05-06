---
skill: model_risk_validator
category: quantitative_risk
description: Computes discrimination and stability metrics for regulatory model validation.
tier: free
inputs: model_predictions, actuals, benchmark_predictions
---

# Model Risk Validator

## Description
Computes discrimination and stability metrics for regulatory model validation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `model_predictions` | `array` | Yes | Model PD or score outputs. |
| `actuals` | `array` | Yes | Observed outcomes (1=default). |
| `benchmark_predictions` | `array` | Yes | Benchmark or prior-period predictions for PSI. |
| `num_bins` | `integer` | No | Number of bins for PSI calculation (default 10). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "model_risk_validator",
  "arguments": {
    "model_predictions": [],
    "actuals": [],
    "benchmark_predictions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "model_risk_validator"`.
