---
skill: rwa_treasury_sanctions_screen
category: crypto_rwa
description: Screens custodians and counterparties for OFAC flags before settlement.
tier: free
inputs: none
---

# Rwa Treasury Sanctions Screen

## Description
Screens custodians and counterparties for OFAC flags before settlement.

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
  "tool": "rwa_treasury_sanctions_screen",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_sanctions_screen"`.
