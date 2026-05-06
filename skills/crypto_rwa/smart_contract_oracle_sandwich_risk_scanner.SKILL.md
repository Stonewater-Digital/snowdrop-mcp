---
skill: smart_contract_oracle_sandwich_risk_scanner
category: crypto_rwa
description: Identifies oracle updates that traders can sandwich before settlement.
tier: free
inputs: none
---

# Smart Contract Oracle Sandwich Risk Scanner

## Description
Identifies oracle updates that traders can sandwich before settlement.

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
  "tool": "smart_contract_oracle_sandwich_risk_scanner",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_oracle_sandwich_risk_scanner"`.
