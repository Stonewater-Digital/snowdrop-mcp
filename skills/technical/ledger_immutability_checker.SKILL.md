---
skill: ledger_immutability_checker
category: technical
description: Build a SHA-256 hash chain over ledger entries to detect tampering and verify immutability. Each entry hash includes the prior hash, forming a blockchain-style chain.
tier: free
inputs: ledger_entries
---

# Ledger Immutability Checker

## Description
Build a SHA-256 hash chain over ledger entries to detect tampering and verify immutability. Each entry hash includes the prior hash, forming a blockchain-style chain.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ledger_entries` | `array` | Yes | List of ledger entry dicts (any structure — will be serialized consistently). |
| `previous_hash` | `string` | No | Optional prior chain tip hash. If provided, the chain is verified to extend from it. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ledger_immutability_checker",
  "arguments": {
    "ledger_entries": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ledger_immutability_checker"`.
