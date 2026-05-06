---
skill: rwa_treasury_cusip_whitelist_verifier
category: crypto_rwa
description: Ensures only approved CUSIPs appear in wrapped Treasury vaults by reconciling mint payloads with issuance calendars.
tier: free
inputs: none
---

# Rwa Treasury Cusip Whitelist Verifier

## Description
Ensures only approved CUSIPs appear in wrapped Treasury vaults by reconciling mint payloads with issuance calendars.

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
  "tool": "rwa_treasury_cusip_whitelist_verifier",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_cusip_whitelist_verifier"`.
