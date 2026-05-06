---
skill: nmtc_compliance_checker
category: nmtc
description: Evaluates census tract, QALICB, and substantially-all tests for NMTC projects.
tier: free
inputs: project, qlici, substantially_all_test
---

# Nmtc Compliance Checker

## Description
Evaluates census tract, QALICB, and substantially-all tests for NMTC projects.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project` | `object` | Yes |  |
| `qlici` | `object` | Yes |  |
| `substantially_all_test` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nmtc_compliance_checker",
  "arguments": {
    "project": {},
    "qlici": {},
    "substantially_all_test": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nmtc_compliance_checker"`.
