---
skill: metals_supply_demand_analyzer
category: commodities
description: Builds supply/demand surplus or deficit tallies for base metals, computes inventory coverage in months, and flags deficit conditions.
tier: free
inputs: metals
---

# Metals Supply Demand Analyzer

## Description
Builds supply/demand surplus or deficit tallies for base metals, computes inventory coverage in months, and flags deficit conditions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `metals` | `array` | Yes | List of metals with supply and demand data. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "metals_supply_demand_analyzer",
  "arguments": {
    "metals": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "metals_supply_demand_analyzer"`.
