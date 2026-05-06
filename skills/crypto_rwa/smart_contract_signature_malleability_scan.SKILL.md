---
skill: smart_contract_signature_malleability_scan
category: crypto_rwa
description: Checks signature verification logic for malleability or unchecked parameters.
tier: free
inputs: none
---

# Smart Contract Signature Malleability Scan

## Description
Checks signature verification logic for malleability or unchecked parameters.

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
  "tool": "smart_contract_signature_malleability_scan",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_signature_malleability_scan"`.
