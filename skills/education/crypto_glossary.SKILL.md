---
skill: crypto_glossary
category: education
description: Explains crypto terms with analogies and risk warnings (goodwill only).
tier: free
inputs: term
---

# Crypto Glossary

## Description
Explains crypto terms with analogies and risk warnings (goodwill only).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `term` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crypto_glossary",
  "arguments": {
    "term": "<term>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crypto_glossary"`.
