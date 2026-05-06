---
skill: energy_cost_per_kwh_calculator
category: energy_finance
description: Calculate electricity cost per kWh from monthly bill and usage. Compares to the US national average (~$0.16/kWh).
tier: free
inputs: monthly_bill, kwh_used
---

# Energy Cost Per Kwh Calculator

## Description
Calculate electricity cost per kWh from monthly bill and usage. Compares to the US national average (~$0.16/kWh).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_bill` | `number` | Yes | Monthly electricity bill in USD. |
| `kwh_used` | `number` | Yes | Kilowatt-hours consumed in the billing period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "energy_cost_per_kwh_calculator",
  "arguments": {
    "monthly_bill": 0,
    "kwh_used": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "energy_cost_per_kwh_calculator"`.
