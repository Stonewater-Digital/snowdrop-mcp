---
skill: recovery_rate_estimator
category: credit_derivatives
description: Computes seniority-specific recovery estimates using historical averages and dispersion statistics.
tier: free
inputs: seniority_levels, historical_recoveries
---

# Recovery Rate Estimator

## Description
Computes seniority-specific recovery estimates using historical averages and dispersion statistics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `seniority_levels` | `array` | Yes | List of instrument seniority labels (e.g., 'Sr Secured', 'Unsecured'). |
| `historical_recoveries` | `array` | Yes | Historical recovery realizations in decimal form. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "recovery_rate_estimator",
  "arguments": {
    "seniority_levels": [],
    "historical_recoveries": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recovery_rate_estimator"`.
