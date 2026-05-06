---
skill: token_standard_erc3643_whitelist_enforcer
category: crypto_rwa
description: Validates ERC-3643 allowlists against investor registries before transfers.
tier: free
inputs: none
---

# Token Standard Erc3643 Whitelist Enforcer

## Description
Validates ERC-3643 allowlists against investor registries before transfers.

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
  "tool": "token_standard_erc3643_whitelist_enforcer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_erc3643_whitelist_enforcer"`.
