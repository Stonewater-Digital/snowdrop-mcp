---
skill: smart_contract_delegatecall_guardrail
category: crypto_rwa
description: Inspects delegatecall targets to ensure they respect access control and immutability assumptions.
tier: free
inputs: none
---

# Smart Contract Delegatecall Guardrail

## Description
Inspects delegatecall targets to ensure they respect access control and immutability assumptions.

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
  "tool": "smart_contract_delegatecall_guardrail",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_delegatecall_guardrail"`.
