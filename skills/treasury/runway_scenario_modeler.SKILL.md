---
skill: runway_scenario_modeler
category: treasury
description: Projects runway months under bull/base/bear net burn assumptions.
tier: free
inputs: current_cash, base_monthly_burn, base_monthly_revenue
---

# Runway Scenario Modeler

## Description
Projects runway months under bull/base/bear net burn assumptions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_cash` | `number` | Yes | Total cash on hand in USD. Must be >= 0. |
| `base_monthly_burn` | `number` | Yes | Baseline gross monthly expenses in USD (the base scenario). Must be >= 0. |
| `base_monthly_revenue` | `number` | Yes | Baseline monthly revenue in USD (the base scenario). Must be >= 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "runway_scenario_modeler",
  "arguments": {
    "current_cash": 500000,
    "base_monthly_burn": 45000,
    "base_monthly_revenue": 22000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "runway_scenario_modeler"`.
