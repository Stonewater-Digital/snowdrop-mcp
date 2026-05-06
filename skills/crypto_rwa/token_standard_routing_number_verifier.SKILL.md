---
skill: token_standard_routing_number_verifier
category: crypto_rwa
description: Validates routing and account numbers used for fiat bridges in compliance workflows.
tier: free
inputs: none
---

# Token Standard Routing Number Verifier

## Description
Validates routing and account numbers used for fiat bridges in compliance workflows.

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
  "tool": "token_standard_routing_number_verifier",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_routing_number_verifier"`.
