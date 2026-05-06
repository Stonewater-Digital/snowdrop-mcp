---
skill: vendor_risk_assessor
category: vendor_eval
description: Evaluates concentration risk, SPOFs, and diversification across vendors.
tier: free
inputs: vendors
---

# Vendor Risk Assessor

## Description
Evaluates concentration risk, SPOFs, and diversification across vendors.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vendors` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vendor_risk_assessor",
  "arguments": {
    "vendors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_risk_assessor"`.
