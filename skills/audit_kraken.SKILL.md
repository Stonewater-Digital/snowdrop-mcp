---
skill: audit_kraken
category: root
description: Retrieves live Kraken exchange balances for TON, SOL, and USDC, converts to USD, and returns a structured balance report.
tier: free
inputs: none
---

# Audit Kraken

## Description
Retrieves live Kraken exchange balances for TON, SOL, and USDC, converts to USD, and returns a structured balance report.

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
  "tool": "audit_kraken",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "audit_kraken"`.
