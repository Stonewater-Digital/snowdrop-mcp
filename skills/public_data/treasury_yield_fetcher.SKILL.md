---
skill: treasury_yield_fetcher
category: public_data
description: Fetch average interest rates for US Treasury securities from the Fiscal Data API. No API key required.
tier: free
inputs: none
---

# Treasury Yield Fetcher

## Description
Fetch average interest rates for US Treasury securities from the Fiscal Data API. No API key required.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `security_type` | `string` | No | Security description filter (e.g., 'Treasury Bills', 'Treasury Notes', 'Treasury Bonds'). |
| `days` | `integer` | No | Number of recent records to return. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "treasury_yield_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "treasury_yield_fetcher"`.
