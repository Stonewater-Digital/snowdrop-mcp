---
skill: token_standard_transfer_restriction_matrix
category: crypto_rwa
description: Generates restriction matrices mapping jurisdiction plus investor tier combinations.
tier: free
inputs: none
---

# Token Standard Transfer Restriction Matrix

## Description
Generates restriction matrices mapping jurisdiction plus investor tier combinations.

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
  "tool": "token_standard_transfer_restriction_matrix",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_transfer_restriction_matrix"`.
