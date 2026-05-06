---
skill: sar_generator
category: compliance_reporting
description: Drafts FinCEN SAR payloads without auto-filing.
tier: free
inputs: subject_id, account, activity_type, suspicious_activity
---

# Sar Generator

## Description
Drafts FinCEN SAR payloads without auto-filing.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subject_id` | `string` | Yes |  |
| `account` | `object` | Yes |  |
| `activity_type` | `string` | Yes |  |
| `suspicious_activity` | `object` | Yes | Details about the suspicious activity including description and amount. |
| `filing_entity` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sar_generator",
  "arguments": {
    "subject_id": "<subject_id>",
    "account": {},
    "activity_type": "<activity_type>",
    "suspicious_activity": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sar_generator"`.
