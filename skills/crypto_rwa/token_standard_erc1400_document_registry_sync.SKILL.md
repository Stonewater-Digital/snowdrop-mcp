---
skill: token_standard_erc1400_document_registry_sync
category: crypto_rwa
description: Keeps ERC-1400 document URIs synced with latest prospectus filings.
tier: free
inputs: none
---

# Token Standard Erc1400 Document Registry Sync

## Description
Keeps ERC-1400 document URIs synced with latest prospectus filings.

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
  "tool": "token_standard_erc1400_document_registry_sync",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_erc1400_document_registry_sync"`.
