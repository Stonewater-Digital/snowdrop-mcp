---
skill: ctr_generator
category: compliance_reporting
description: Determines whether a CTR filing is required and drafts the payload.
tier: free
inputs: transaction, filing_entity
---

# Ctr Generator

## Description
Determines whether a CTR filing is required and drafts the payload.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transaction` | `object` | Yes |  |
| `filing_entity` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ctr_generator",
  "arguments": {
    "transaction": {},
    "filing_entity": "<filing_entity>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ctr_generator"`.
