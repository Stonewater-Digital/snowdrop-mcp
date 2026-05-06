---
skill: invoice_generator
category: billing
description: Generates franchise-friendly invoices with royalty handling.
tier: free
inputs: agent_id, line_items, due_date
---

# Invoice Generator

## Description
Generates franchise-friendly invoices with royalty handling.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `line_items` | `array` | Yes |  |
| `currency` | `string` | No |  |
| `due_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "invoice_generator",
  "arguments": {
    "agent_id": "<agent_id>",
    "line_items": [],
    "due_date": "<due_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "invoice_generator"`.
