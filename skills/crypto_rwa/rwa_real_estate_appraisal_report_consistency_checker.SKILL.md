---
skill: rwa_real_estate_appraisal_report_consistency_checker
category: crypto_rwa
description: Checks appraisal comparables and LTV metrics for consistency with disclosure packets.
tier: free
inputs: payload
---

# Rwa Real Estate Appraisal Report Consistency Checker

## Description
Checks appraisal comparables and LTV metrics for consistency with disclosure packets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_appraisal_report_consistency_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_appraisal_report_consistency_checker"`.
