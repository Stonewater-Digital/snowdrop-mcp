---
skill: pdf_report_formatter
category: export
description: Creates a layout-ready dict for PDF renderers (sections, TOC, metadata).
tier: free
inputs: title, sections, date
---

# Pdf Report Formatter

## Description
Creates a layout-ready dict for PDF renderers (sections, TOC, metadata).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | `string` | Yes |  |
| `sections` | `array` | Yes |  |
| `author` | `string` | No |  |
| `date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pdf_report_formatter",
  "arguments": {
    "title": "<title>",
    "sections": [],
    "date": "<date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pdf_report_formatter"`.
