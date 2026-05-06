---
skill: renewable_energy_payback_calculator
category: energy_finance
description: Calculate the payback period for a renewable energy installation considering installation cost, incentives, annual savings, and maintenance costs.
tier: free
inputs: installation_cost, annual_savings
---

# Renewable Energy Payback Calculator

## Description
Calculate the payback period for a renewable energy installation considering installation cost, incentives, annual savings, and maintenance costs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `installation_cost` | `number` | Yes | Total installation cost in USD. |
| `annual_savings` | `number` | Yes | Expected annual energy savings in USD. |
| `incentives` | `number` | No | Total incentives, rebates, and tax credits in USD. |
| `annual_maintenance` | `number` | No | Expected annual maintenance cost in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "renewable_energy_payback_calculator",
  "arguments": {
    "installation_cost": 0,
    "annual_savings": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "renewable_energy_payback_calculator"`.
