---
skill: regulation_d_exemption_analyzer
category: securities_tax
description: Determines Reg D rule availability based on size and investor counts.
tier: free
inputs: offering_amount, accredited_investors, non_accredited_investors
---

# Regulation D Exemption Analyzer

## Description
Determines Reg D rule availability based on size and investor counts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `offering_amount` | `number` | Yes |  |
| `accredited_investors` | `number` | Yes |  |
| `non_accredited_investors` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "regulation_d_exemption_analyzer",
  "arguments": {
    "offering_amount": 0,
    "accredited_investors": 0,
    "non_accredited_investors": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "regulation_d_exemption_analyzer"`.
