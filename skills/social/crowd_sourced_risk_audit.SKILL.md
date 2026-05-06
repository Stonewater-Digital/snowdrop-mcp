---
skill: crowd_sourced_risk_audit
category: social
description: Aggregates multi-assessor risk scores into a confidence-weighted consensus, surfaces statistical outliers, and classifies overall consensus strength.
tier: free
inputs: asset_id, assessments
---

# Crowd Sourced Risk Audit

## Description
Aggregates multi-assessor risk scores into a confidence-weighted consensus, surfaces statistical outliers, and classifies overall consensus strength.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_id` | `string` | Yes | Identifier for the asset being audited. |
| `assessments` | `array` | Yes | List of assessment dicts with: assessor_id (str), risk_score (float 1-10), confidence (float 0-1), rationale (str). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crowd_sourced_risk_audit",
  "arguments": {
    "asset_id": "<asset_id>",
    "assessments": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crowd_sourced_risk_audit"`.
