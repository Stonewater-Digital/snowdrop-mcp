---
skill: vendor_due_diligence
category: vendor_eval
description: Scores vendor fit based on uptime, pricing, certifications, and experience.
tier: free
inputs: vendor, requirements
---

# Vendor Due Diligence

## Description
Scores vendor fit based on uptime, pricing, certifications, and experience.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vendor` | `object` | Yes |  |
| `requirements` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vendor_due_diligence",
  "arguments": {
    "vendor": {},
    "requirements": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_due_diligence"`.
