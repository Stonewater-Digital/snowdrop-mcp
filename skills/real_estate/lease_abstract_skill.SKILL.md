---
skill: lease_abstract_skill
category: real_estate
description: Extracts key commercial lease terms from raw lease text using regex-based pattern matching. Targets commencement date, expiration date, base rent, escalation rate, renewal options, and break clauses.
tier: free
inputs: lease_text
---

# Lease Abstract Skill

## Description
Extracts key commercial lease terms from raw lease text using regex-based pattern matching. Targets commencement date, expiration date, base rent, escalation rate, renewal options, and break clauses. Returns confidence score and list of fields that could not be extracted.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lease_text` | `string` | Yes | Full or partial lease document text to parse. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lease_abstract_skill",
  "arguments": {
    "lease_text": "<lease_text>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lease_abstract_skill"`.
