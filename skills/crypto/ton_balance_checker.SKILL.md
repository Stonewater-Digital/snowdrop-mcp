---
skill: ton_balance_checker
category: crypto
description: Queries TON Center for the configured wallet and returns TON balances.
tier: free
inputs: none
---

# Ton Balance Checker

## Description
Queries TON Center for the configured wallet and returns TON balances.

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
  "tool": "ton_balance_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ton_balance_checker"`.
