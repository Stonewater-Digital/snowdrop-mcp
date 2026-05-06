---
skill: collateral_management_optimizer
category: middle_office
description: Ranks collateral by haircut-adjusted funding cost versus yield.
tier: free
inputs: collateral_pool
---

# Collateral Management Optimizer

## Description
Ranks collateral by haircut-adjusted funding cost versus yield.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `collateral_pool` | `array` | Yes |  |
| `funding_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "collateral_management_optimizer",
  "arguments": {
    "collateral_pool": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "collateral_management_optimizer"`.
