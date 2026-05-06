---
skill: ghost_ledger
category: root
description: Google Sheets fund-accounting bridge. Supports initializing a new ledger spreadsheet with structured tabs, reading tab data, appending rows, summing vault balances, and writing autonomous decision entries to THE LOGIC LOG tab for audit traceability.
tier: free
inputs: action
---

# Ghost Ledger

## Description
Google Sheets fund-accounting bridge. Supports initializing a new ledger spreadsheet with structured tabs, reading tab data, appending rows, summing vault balances, and writing autonomous decision entries to THE LOGIC LOG tab for audit traceability.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation to perform. One of: `init`, `read`, `write`, `batch_write`, `get_balance`, `log_decision`. |
| `spreadsheet_url` | `string` | No | Full Google Sheets URL (required for read/write/get_balance). |
| `tab_name` | `string` | No | Name of the worksheet tab (required for read/write). |
| `row_data` | `array` | No | List of cell values to append as a new row (required for write). |
| `rows_data` | `array` | No | List of rows to append (required for batch_write). |
| `spreadsheet_name` | `string` | No | Name for the new spreadsheet (required for init). |
| `decision` | `string` | No | Human-readable description of the autonomous decision taken (required for log_decision). |
| `reasoning` | `string` | No | Why this decision was made — the 'because' (required for log_decision). |
| `outcome` | `string` | No | What happened as a result — ok, error, or a brief description (optional for log_decision). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ghost_ledger",
  "arguments": {
    "action": "log_decision",
    "spreadsheet_url": "https://docs.google.com/spreadsheets/d/SHEET_ID/edit",
    "decision": "Skipped reconciliation due to Kraken API timeout",
    "reasoning": "API returned 503 after 3 retries; retry scheduled for next cron cycle",
    "outcome": "deferred"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_ledger"`.
