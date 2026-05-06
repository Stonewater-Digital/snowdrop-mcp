---
skill: json_schema_validator
category: system
description: Validate a data object against a JSON schema-like rule set. Checks required fields, types, min/max constraints, and enum values.
tier: free
inputs: data, schema
---

# Json Schema Validator

## Description
Validate a data object against a JSON schema-like rule set. Checks required fields, types, min/max constraints, and enum values.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `object` | Yes | The data object to validate. |
| `schema` | `object` | Yes | Schema definition with 'properties' (field rules), 'required' (list of required field names). Each property can have: type (string/number/integer/boolean/array/object), minimum, maximum, enum, minLength, maxLength. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "json_schema_validator",
  "arguments": {
    "data": {},
    "schema": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "json_schema_validator"`.
