---
skill: invoice_aging_analyzer
category: small_business
description: Groups invoices into standard aging buckets, calculates outstanding exposure, and estimates collection performance and bad debt reserves.
tier: free
inputs: invoices
---

# Invoice Aging Analyzer

## Description
Groups invoices into standard aging buckets, calculates outstanding exposure, and estimates collection performance and bad debt reserves.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `invoices` | `array` | Yes | List of invoices with id, amount, issue_date, due_date, paid_date (optional). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "invoice_aging_analyzer",
  "arguments": {
    "invoices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "invoice_aging_analyzer"`.
