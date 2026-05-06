---
skill: csv_column_analyzer
category: system
description: Analyze CSV-like tabular data (list of rows). For each column: infer type, count nulls, count unique values, compute min/max for numbers, and show sample values.
tier: free
inputs: rows
---

# Csv Column Analyzer

## Description
Analyze CSV-like tabular data (list of rows). For each column: infer type, count nulls, count unique values, compute min/max for numbers, and show sample values.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `rows` | `array` | Yes | List of rows, where each row is a list of cell values. |
| `has_header` | `boolean` | No | Whether the first row is a header row. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "csv_column_analyzer",
  "arguments": {
    "rows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "csv_column_analyzer"`.
