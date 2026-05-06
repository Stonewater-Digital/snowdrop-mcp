---
skill: audit_24h_reconstructor
category: fund_accounting
description: Filters ledger activity to a 24h window and produces a running balance. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Audit 24h Reconstructor

## Description
Filters ledger activity to a 24h window and produces a running balance. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "audit_24h_reconstructor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "audit_24h_reconstructor"`.
