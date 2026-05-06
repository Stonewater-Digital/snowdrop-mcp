---
skill: ccar_capital_planning
category: quantitative_risk
description: Projects CET1 ratio over stress horizon using Fed CCAR methodology.
tier: free
inputs: starting_capital, projected_losses, ppnr, rwa_growth_pct
---

# Ccar Capital Planning

## Description
Projects CET1 ratio over stress horizon using Fed CCAR methodology.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `starting_capital` | `object` | Yes | Starting CET1 capital and RWA. |
| `projected_losses` | `array` | Yes | Quarterly losses over the stress horizon. |
| `ppnr` | `array` | Yes | Pre-provision net revenue per quarter. |
| `dividend_schedule` | `array` | No | Planned dividend distributions per quarter. |
| `rwa_growth_pct` | `number` | Yes | Percentage growth in RWA per quarter. |
| `buffer_requirement_pct` | `number` | No | Combined buffer requirement (default 4.5+buffers). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ccar_capital_planning",
  "arguments": {
    "starting_capital": {},
    "projected_losses": [],
    "ppnr": [],
    "rwa_growth_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ccar_capital_planning"`.
