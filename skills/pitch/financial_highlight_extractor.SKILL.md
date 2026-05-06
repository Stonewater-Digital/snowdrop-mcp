---
skill: financial_highlight_extractor
category: pitch
description: Summarizes headline metrics, growth narratives, and risks for presentations.
tier: free
inputs: financials
---

# Financial Highlight Extractor

## Description
Summarizes headline metrics, growth narratives, and risks for presentations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `financials` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "financial_highlight_extractor",
  "arguments": {
    "financials": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "financial_highlight_extractor"`.
