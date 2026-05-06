---
skill: insurance_tower_allocation_optimizer
category: corporate_insurance
description: Aligns tower layers with modeled loss percentiles to minimize gaps.
tier: free
inputs: layers, loss_percentiles
---

# Insurance Tower Allocation Optimizer

## Description
Aligns tower layers with modeled loss percentiles to minimize gaps.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `layers` | `array` | Yes |  |
| `loss_percentiles` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "insurance_tower_allocation_optimizer",
  "arguments": {
    "layers": [],
    "loss_percentiles": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "insurance_tower_allocation_optimizer"`.
