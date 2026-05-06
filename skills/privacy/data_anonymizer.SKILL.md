---
skill: data_anonymizer
category: privacy
description: Transforms sensitive fields using hash/mask/redact/generalize strategies.
tier: free
inputs: data, fields_to_anonymize, method
---

# Data Anonymizer

## Description
Transforms sensitive fields using hash/mask/redact/generalize strategies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `array` | Yes |  |
| `fields_to_anonymize` | `array` | Yes |  |
| `method` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "data_anonymizer",
  "arguments": {
    "data": [],
    "fields_to_anonymize": [],
    "method": "<method>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "data_anonymizer"`.
