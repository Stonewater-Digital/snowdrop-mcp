---
skill: supply_demand_guide
category: education
description: Returns educational content on supply and demand: law of supply/demand, equilibrium, elasticity, and shifts.
tier: free
inputs: none
---

# Supply Demand Guide

## Description
Returns educational content on supply and demand: law of supply/demand, equilibrium, elasticity, and shifts.

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
  "tool": "supply_demand_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "supply_demand_guide"`.
