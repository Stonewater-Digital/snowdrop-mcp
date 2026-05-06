---
skill: token_standard_prospectus_linker
category: crypto_rwa
description: Ensures wallets receive the latest prospectus hash before participating in offerings.
tier: free
inputs: none
---

# Token Standard Prospectus Linker

## Description
Ensures wallets receive the latest prospectus hash before participating in offerings.

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
  "tool": "token_standard_prospectus_linker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_prospectus_linker"`.
