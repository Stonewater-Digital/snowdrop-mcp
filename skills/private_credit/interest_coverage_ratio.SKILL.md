---
skill: interest_coverage_ratio
category: private_credit
description: Calculates interest and fixed charge coverage ratios.
tier: free
inputs: ebitda, interest_expense
---

# Interest Coverage Ratio

## Description
Calculates interest and fixed charge coverage ratios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ebitda` | `number` | Yes |  |
| `interest_expense` | `number` | Yes |  |
| `fixed_charges` | `number` | No |  |
| `stress_decline_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "interest_coverage_ratio",
  "arguments": {
    "ebitda": 0,
    "interest_expense": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "interest_coverage_ratio"`.
