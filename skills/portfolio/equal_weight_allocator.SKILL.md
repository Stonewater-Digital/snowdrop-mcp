---
skill: equal_weight_allocator
category: portfolio
description: Allocates a total portfolio value equally across a specified number of assets, returning weight and dollar allocation per asset.
tier: free
inputs: num_assets
---

# Equal Weight Allocator

## Description
Allocates a total portfolio value equally across a specified number of assets, returning weight and dollar allocation per asset.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `num_assets` | `integer` | Yes | Number of assets to allocate across (must be > 0). |
| `total_value` | `number` | No | Total portfolio value to allocate (default 10000). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "equal_weight_allocator",
  "arguments": {
    "num_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "equal_weight_allocator"`.
