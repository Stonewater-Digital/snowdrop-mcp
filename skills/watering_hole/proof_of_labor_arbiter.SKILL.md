---
skill: proof_of_labor_arbiter
category: watering_hole
description: Scores labor contributions and returns credit recommendations.
tier: free
inputs: labor_type, evidence
---

# Proof Of Labor Arbiter

## Description
Scores labor contributions and returns credit recommendations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `labor_type` | `string` | Yes |  |
| `evidence` | `object` | Yes | Evidence dict containing hours/referrals/GitHub metadata. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "proof_of_labor_arbiter",
  "arguments": {
    "labor_type": "<labor_type>",
    "evidence": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "proof_of_labor_arbiter"`.
