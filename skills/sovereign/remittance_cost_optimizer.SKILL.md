---
skill: remittance_cost_optimizer
category: sovereign
description: Ranks cross-border remittance corridors by total cost, identifies cheapest and fastest options, and filters by urgency.
tier: free
inputs: transfer, corridors
---

# Remittance Cost Optimizer

## Description
Ranks cross-border remittance corridors by total cost, identifies cheapest and fastest options, and filters by urgency.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transfer` | `object` | Yes | Transfer requirements |
| `corridors` | `array` | Yes | Available remittance providers/corridors |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "remittance_cost_optimizer",
  "arguments": {
    "transfer": {},
    "corridors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "remittance_cost_optimizer"`.
