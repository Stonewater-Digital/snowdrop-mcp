---
skill: triple_net_reconciliation
category: real_estate
description: Reconciles estimated NNN (triple-net) lease pass-through charges (CAM, insurance, property taxes) against actual year-end costs. Determines per-category variance and whether the tenant owes a true-up payment or is owed a credit.
tier: free
inputs: lease_terms, actuals, period
---

# Triple Net Reconciliation

## Description
Reconciles estimated NNN (triple-net) lease pass-through charges (CAM, insurance, property taxes) against actual year-end costs. Determines per-category variance and whether the tenant owes a true-up payment or is owed a credit.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lease_terms` | `object` | Yes | Estimated charges billed to tenant throughout the period. |
| `actuals` | `object` | Yes | Actual costs incurred by the landlord for the period. |
| `period` | `string` | Yes | Reconciliation period label (e.g., '2025', 'Q4-2025'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "triple_net_reconciliation",
  "arguments": {
    "lease_terms": {},
    "actuals": {},
    "period": "<period>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "triple_net_reconciliation"`.
