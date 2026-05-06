---
skill: token_standard_multi_chain_supply_auditor
category: crypto_rwa
description: Audits circulating supply across chains to prevent double listings.
tier: free
inputs: none
---

# Token Standard Multi Chain Supply Auditor

## Description
Audits circulating supply across chains to prevent double listings.

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
  "tool": "token_standard_multi_chain_supply_auditor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_multi_chain_supply_auditor"`.
