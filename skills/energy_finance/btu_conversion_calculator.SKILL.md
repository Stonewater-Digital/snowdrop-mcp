---
skill: btu_conversion_calculator
category: energy_finance
description: Convert between energy units: BTU, kWh, MJ, therms, gallons_oil, and cubic_feet_gas.
tier: free
inputs: amount, from_unit, to_unit
---

# Btu Conversion Calculator

## Description
Convert between energy units: BTU, kWh, MJ, therms, gallons_oil, and cubic_feet_gas.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amount` | `number` | Yes | Amount of energy to convert. |
| `from_unit` | `string` | Yes | Source energy unit. |
| `to_unit` | `string` | Yes | Target energy unit. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "btu_conversion_calculator",
  "arguments": {
    "amount": 0,
    "from_unit": "<from_unit>",
    "to_unit": "<to_unit>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "btu_conversion_calculator"`.
