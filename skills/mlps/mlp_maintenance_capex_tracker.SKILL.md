---
skill: mlp_maintenance_capex_tracker
category: mlps
description: Aggregates maintenance capex budgets vs actuals per asset to surface overruns. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Maintenance Capex Tracker

## Description
Aggregates maintenance capex budgets vs actuals per asset to surface overruns. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_maintenance_capex_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_maintenance_capex_tracker"`.
