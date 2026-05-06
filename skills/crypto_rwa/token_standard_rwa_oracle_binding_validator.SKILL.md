---
skill: token_standard_rwa_oracle_binding_validator
category: crypto_rwa
description: Verifies tokens consume signed oracle data per governance charter.
tier: free
inputs: none
---

# Token Standard Rwa Oracle Binding Validator

## Description
Verifies tokens consume signed oracle data per governance charter.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_standard_rwa_oracle_binding_validator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_rwa_oracle_binding_validator"`.
