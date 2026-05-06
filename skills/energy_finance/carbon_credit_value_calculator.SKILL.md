---
skill: carbon_credit_value_calculator
category: energy_finance
description: Calculate the monetary value of carbon credits/offsets and compare across EU ETS, compliance, and voluntary carbon markets.
tier: free
inputs: tons_co2
---

# Carbon Credit Value Calculator

## Description
Calculate the monetary value of carbon credits/offsets and compare across EU ETS, compliance, and voluntary carbon markets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tons_co2` | `number` | Yes | Metric tons of CO2 equivalent. |
| `price_per_ton` | `number` | No | Price per metric ton of CO2 in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "carbon_credit_value_calculator",
  "arguments": {
    "tons_co2": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carbon_credit_value_calculator"`.
