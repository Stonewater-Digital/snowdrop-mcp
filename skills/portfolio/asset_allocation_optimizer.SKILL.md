---
skill: asset_allocation_optimizer
category: portfolio
description: Finds feasible allocations that hit target return/risk under constraints.
tier: free
inputs: assets, constraints
---

# Asset Allocation Optimizer

## Description
Finds feasible allocations that hit target return/risk under constraints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `array` | Yes |  |
| `constraints` | `object` | Yes |  |
| `target_return` | `['number', 'null']` | No |  |
| `target_risk` | `['number', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "asset_allocation_optimizer",
  "arguments": {
    "assets": [],
    "constraints": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_allocation_optimizer"`.
