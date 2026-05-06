---
skill: token_standard_sanctions_attestor
category: crypto_rwa
description: Confirms sanctions screening proofs are attached to each restricted transfer.
tier: free
inputs: none
---

# Token Standard Sanctions Attestor

## Description
Confirms sanctions screening proofs are attached to each restricted transfer.

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
  "tool": "token_standard_sanctions_attestor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_sanctions_attestor"`.
