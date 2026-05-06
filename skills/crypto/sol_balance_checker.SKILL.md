---
skill: sol_balance_checker
category: crypto
description: Calls Solana RPC getBalance and returns SOL for the configured wallet.
tier: free
inputs: none
---

# Sol Balance Checker

## Description
Calls Solana RPC getBalance and returns SOL for the configured wallet.

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
  "tool": "sol_balance_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sol_balance_checker"`.
