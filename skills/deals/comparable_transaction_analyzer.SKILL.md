---
skill: comparable_transaction_analyzer
category: deals
description: Derives valuation ranges from comps using EV/Revenue and EV/EBITDA multiples.
tier: free
inputs: target, comparables
---

# Comparable Transaction Analyzer

## Description
Derives valuation ranges from comps using EV/Revenue and EV/EBITDA multiples.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target` | `object` | Yes |  |
| `comparables` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "comparable_transaction_analyzer",
  "arguments": {
    "target": {},
    "comparables": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "comparable_transaction_analyzer"`.
