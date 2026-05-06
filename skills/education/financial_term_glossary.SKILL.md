---
skill: financial_term_glossary
category: education
description: Look up definitions, categories, and related terms for 30+ common financial terms.
tier: free
inputs: term
---

# Financial Term Glossary

## Description
Look up definitions, categories, and related terms for 30+ common financial terms.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `term` | `string` | Yes | The financial term to look up. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "financial_term_glossary",
  "arguments": {
    "term": "<term>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "financial_term_glossary"`.
