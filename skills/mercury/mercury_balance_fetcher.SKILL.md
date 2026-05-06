---
skill: mercury_balance_fetcher
category: mercury
description: Retrieves account balances from Mercury's /api/v1/accounts endpoint.
tier: free
inputs: none
---

# Mercury Balance Fetcher

## Description
Retrieves account balances from Mercury's /api/v1/accounts endpoint.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `status` | `string` | No | Optional Mercury status filter (active/closed). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mercury_balance_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mercury_balance_fetcher"`.
