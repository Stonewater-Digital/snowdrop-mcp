---
skill: reinsurance_treaty_analyzer
category: corporate_insurance
description: Compares QS and XL treaties for cost, protection, and leverage impacts.
tier: free
inputs: treaty_type, gross_losses, gross_premium
---

# Reinsurance Treaty Analyzer

## Description
Compares QS and XL treaties for cost, protection, and leverage impacts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `treaty_type` | `string` | Yes |  |
| `gross_losses` | `number` | Yes |  |
| `gross_premium` | `number` | Yes |  |
| `cession_pct` | `number` | No |  |
| `retention` | `number` | No |  |
| `limit` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reinsurance_treaty_analyzer",
  "arguments": {
    "treaty_type": "<treaty_type>",
    "gross_losses": 0,
    "gross_premium": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reinsurance_treaty_analyzer"`.
