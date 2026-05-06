---
skill: csv_exporter
category: export
description: Flattens dict rows and emits RFC4180-compliant CSV strings.
tier: free
inputs: data, filename_prefix
---

# Csv Exporter

## Description
Flattens dict rows and emits RFC4180-compliant CSV strings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `array` | Yes |  |
| `columns` | `['array', 'null']` | No |  |
| `filename_prefix` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "csv_exporter",
  "arguments": {
    "data": [],
    "filename_prefix": "<filename_prefix>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "csv_exporter"`.
