---
skill: rwa_compliance_status_tracker
category: rwa_tokenization
description: Rolls up AML, KYC, and filing checks into a single compliance status report.
tier: free
inputs: checks
---

# Rwa Compliance Status Tracker

## Description
Rolls up AML, KYC, and filing checks into a single compliance status report.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `checks` | `array` | Yes | Compliance checklist items |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_compliance_status_tracker",
  "arguments": {
    "checks": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_compliance_status_tracker"`.
