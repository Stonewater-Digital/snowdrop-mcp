---
skill: credit_event_probability
category: credit_derivatives
description: Transforms piecewise hazard rates into survival, marginal default probabilities, and event odds per tenor.
tier: free
inputs: hazard_rates, time_grid_years
---

# Credit Event Probability

## Description
Transforms piecewise hazard rates into survival, marginal default probabilities, and event odds per tenor.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hazard_rates` | `array` | Yes | Piecewise-constant hazard rates (decimal) for each interval. |
| `time_grid_years` | `array` | Yes | Time grid endpoints in years corresponding to each hazard rate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_event_probability",
  "arguments": {
    "hazard_rates": [],
    "time_grid_years": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_event_probability"`.
