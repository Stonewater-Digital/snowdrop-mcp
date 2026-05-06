---
skill: exchange_1031_analyzer
category: tax_advanced
description: Calculates gains, boot, and deadlines for like-kind exchanges.
tier: free
inputs: relinquished, replacement_candidates, sale_date
---

# Exchange 1031 Analyzer

## Description
Calculates gains, boot, and deadlines for like-kind exchanges.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `relinquished` | `object` | Yes |  |
| `replacement_candidates` | `array` | Yes |  |
| `sale_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "exchange_1031_analyzer",
  "arguments": {
    "relinquished": {},
    "replacement_candidates": [],
    "sale_date": "<sale_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exchange_1031_analyzer"`.
