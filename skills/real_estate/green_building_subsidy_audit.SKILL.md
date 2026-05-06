---
skill: green_building_subsidy_audit
category: real_estate
description: Audits a commercial building's eligibility for green building tax incentives including the Investment Tax Credit (ITC) for solar, Section 179D energy efficiency deduction, and a curated set of state-level ESG incentives. Returns eligible programs, estimated values, and requirements met.
tier: free
inputs: building_data
---

# Green Building Subsidy Audit

## Description
Audits a commercial building's eligibility for green building tax incentives including the Investment Tax Credit (ITC) for solar, Section 179D energy efficiency deduction, and a curated set of state-level ESG incentives. Returns eligible programs, estimated values, and requirements met.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `building_data` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "green_building_subsidy_audit",
  "arguments": {
    "building_data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "green_building_subsidy_audit"`.
