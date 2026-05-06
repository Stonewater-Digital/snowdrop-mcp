---
skill: hsa_contribution_optimizer
category: personal_finance
description: Calculate optimal HSA contribution limits based on coverage type and age. Shows 2024 limits, catch-up contributions, and tax savings estimates.
tier: free
inputs: none
---

# Hsa Contribution Optimizer

## Description
Calculate optimal HSA contribution limits based on coverage type and age. Shows 2024 limits, catch-up contributions, and tax savings estimates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `coverage_type` | `string` | No | Coverage type: 'self' (self-only) or 'family'. |
| `age` | `integer` | No | Account holder's age. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "hsa_contribution_optimizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hsa_contribution_optimizer"`.
