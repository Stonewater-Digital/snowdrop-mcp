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
| `current_cash` | `number` | Yes |  |
| `base_monthly_burn` | `number` | Yes |  |
| `base_monthly_revenue` | `number` | Yes |  |

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
    "current_cash": 0,
    "base_monthly_burn": 0,
    "base_monthly_revenue": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "runway_scenario_modeler"`.
