---
skill: token_standard_prospectus_linker
category: crypto_rwa
description: Ensures wallets receive the latest prospectus hash before participating in offerings.
tier: free
inputs: payload
---

# Token Standard Prospectus Linker

## Description
Ensures wallets receive the latest prospectus hash before participating in offerings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_standard_prospectus_linker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_prospectus_linker"`.
