---
skill: bonding_curve_pricer
category: watering_hole
description: Calculates Watering Hole bonding curve prices using time decay, demand velocity, and snap-back protections.
tier: free
inputs: base_price, decay_rate, time_elapsed_hours, slope, delta_units, delta_time_hours
---

# Bonding Curve Pricer

## Description
Calculates Watering Hole bonding curve prices using time decay, demand velocity, and snap-back protections.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_price` | `number` | Yes | Starting price before decay and demand adjustments (USD). |
| `decay_rate` | `number` | Yes | Exponential decay constant k for time-based cooling. |
| `time_elapsed_hours` | `number` | Yes | Hours since the last pricing event (t). |
| `slope` | `number` | Yes | Demand slope m that translates unit velocity to price delta. |
| `delta_units` | `number` | Yes | Change in filled units since the last evaluation (Δn). |
| `delta_time_hours` | `number` | Yes | Time window in hours for the demand change (Δt). |
| `last_clearing_price` | `number` | No | Most recent executed price for snap-back comparisons. |
| `snap_back_threshold_pct` | `number` | No | Maximum allowed deviation (e.g. 0.25 = 25%) from the last clearing price before enforcing snap-back caps. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bonding_curve_pricer",
  "arguments": {
    "base_price": 0,
    "decay_rate": 0,
    "time_elapsed_hours": 0,
    "slope": 0,
    "delta_units": 0,
    "delta_time_hours": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bonding_curve_pricer"`.
