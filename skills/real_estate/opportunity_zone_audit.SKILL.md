---
skill: opportunity_zone_audit
category: real_estate
description: Audits Qualified Opportunity Zone (QOZ) investment compliance per IRC §1400Z-2. Checks the 180-day reinvestment window, 10-year hold for full exclusion, substantial improvement test (must double basis in improvements), and original use doctrine.
tier: free
inputs: investment_details
---

# Opportunity Zone Audit

## Description
Audits Qualified Opportunity Zone (QOZ) investment compliance per IRC §1400Z-2. Checks the 180-day reinvestment window, 10-year hold for full exclusion, substantial improvement test (must double basis in improvements), and original use doctrine. Estimates tax benefits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `investment_details` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "opportunity_zone_audit",
  "arguments": {
    "investment_details": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "opportunity_zone_audit"`.
