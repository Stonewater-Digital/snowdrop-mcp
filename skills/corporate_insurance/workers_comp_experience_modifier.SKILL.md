---
skill: workers_comp_experience_modifier
category: corporate_insurance
description: Calculates WC experience modifier from actual and expected losses.
tier: free
inputs: actual_losses, expected_losses
---

# Workers Comp Experience Modifier

## Description
Calculates WC experience modifier from actual and expected losses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `actual_losses` | `number` | Yes |  |
| `expected_losses` | `number` | Yes |  |
| `credibility_factor` | `number` | No |  |
| `primary_threshold` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "workers_comp_experience_modifier",
  "arguments": {
    "actual_losses": 0,
    "expected_losses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "workers_comp_experience_modifier"`.
