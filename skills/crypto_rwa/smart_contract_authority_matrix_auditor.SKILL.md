---
skill: smart_contract_authority_matrix_auditor
category: crypto_rwa
description: Builds a permission matrix for each method to catch privilege creep.
tier: free
inputs: none
---

# Smart Contract Authority Matrix Auditor

## Description
Builds a permission matrix for each method to catch privilege creep.

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
  "tool": "smart_contract_authority_matrix_auditor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_authority_matrix_auditor"`.
