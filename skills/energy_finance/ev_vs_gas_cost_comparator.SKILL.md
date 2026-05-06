---
skill: ev_vs_gas_cost_comparator
category: energy_finance
description: Compare annual fuel costs between an EV and a gasoline vehicle based on annual miles, efficiency, and energy prices.
tier: free
inputs: annual_miles
---

# Ev Vs Gas Cost Comparator

## Description
Compare annual fuel costs between an EV and a gasoline vehicle based on annual miles, efficiency, and energy prices.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_miles` | `number` | Yes | Annual miles driven. |
| `ev_efficiency_kwh_per_mile` | `number` | No | EV energy consumption in kWh per mile. |
| `gas_mpg` | `number` | No | Gasoline vehicle fuel efficiency in miles per gallon. |
| `electricity_rate` | `number` | No | Electricity cost in $/kWh. |
| `gas_price` | `number` | No | Gasoline price in $/gallon. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ev_vs_gas_cost_comparator",
  "arguments": {
    "annual_miles": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ev_vs_gas_cost_comparator"`.
