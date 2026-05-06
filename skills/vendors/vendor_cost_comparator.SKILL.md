---
skill: vendor_cost_comparator
category: vendors
description: Computes daily/monthly spend per provider and ranks by cost-effectiveness.
tier: free
inputs: task_profile, providers
---

# Vendor Cost Comparator

## Description
Computes daily/monthly spend per provider and ranks by cost-effectiveness.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_profile` | `object` | Yes | Describes the workload: `token_count` (int), `frequency_per_day` (int), and `task_type` (string, e.g. "inference"). |
| `providers` | `array` | Yes | List of provider objects, each with `name` (string), `cost_per_1k_tokens` (float), and optional `tier` (string). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vendor_cost_comparator",
  "arguments": {
    "task_profile": {"token_count": 2000, "frequency_per_day": 50, "task_type": "inference"},
    "providers": [
      {"name": "OpenRouter", "cost_per_1k_tokens": 0.005, "tier": "standard"},
      {"name": "Anthropic", "cost_per_1k_tokens": 0.008, "tier": "premium"}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_cost_comparator"`.
