---
skill: management_fee_calculator
category: fund_admin
description: Computes management fees with investment period step-down: before step_down_year, fees are based on committed capital; after step_down_year, fees step down to invested/cost basis. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Management Fee Calculator

## Description
Computes management fees with investment period step-down: before step_down_year, fees are based on committed capital; after step_down_year, fees step down to invested/cost basis. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "management_fee_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "management_fee_calculator"`.
