---
skill: defi_yield_comparator
category: defi
description: Filters DeFi protocols by safety heuristics and ranks risk-adjusted yield.
tier: free
inputs: protocols
---

# Defi Yield Comparator

## Description
Filters DeFi protocols by safety heuristics and ranks risk-adjusted yield.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `protocols` | `array` | Yes |  |
| `min_tvl` | `number` | No |  |
| `require_audit` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "defi_yield_comparator",
  "arguments": {
    "protocols": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "defi_yield_comparator"`.
