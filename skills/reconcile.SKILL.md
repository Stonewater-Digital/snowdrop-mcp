---
skill: reconcile
category: root
description: Daily reconciliation engine. Compares live Kraken exchange balances against the Ghost Ledger (Google Sheets).
tier: free
inputs: spreadsheet_url
---

# Reconcile

## Description
Daily reconciliation engine. Compares live Kraken exchange balances against the Ghost Ledger (Google Sheets). Emits a CRITICAL alert to Thunder via Telegram if any discrepancy is detected. Zero-tolerance policy.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spreadsheet_url` | `string` | Yes | Full URL of the active Ghost Ledger Google Spreadsheet. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reconcile",
  "arguments": {
    "spreadsheet_url": "https://docs.google.com/spreadsheets/d/SHEET_ID/edit"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reconcile"`.
