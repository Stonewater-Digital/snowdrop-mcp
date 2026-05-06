---
skill: climate_risk_transition
category: quantitative_risk
description: Applies NGFS transition scenarios to sector PDs and estimates RWA impact and stranded assets.
tier: free
inputs: portfolio_sector_exposures, transition_scenario
---

# Climate Risk Transition

## Description
Applies NGFS transition scenarios to sector PDs and estimates RWA impact and stranded assets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_sector_exposures` | `array` | Yes | Sector exposures with base PD, LGD, and carbon intensity (tons CO2e/USDm). |
| `transition_scenario` | `string` | Yes | Scenario label (orderly, disorderly, hothouse). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "climate_risk_transition",
  "arguments": {
    "portfolio_sector_exposures": [],
    "transition_scenario": "<transition_scenario>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "climate_risk_transition"`.
