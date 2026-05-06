---
skill: document_vault_ocr_router
category: data_ingestion
description: Assign vault documents to OCR models based on mime type, priority, and presence of embedded text.
tier: free
inputs: documents
---

# Document Vault Ocr Router

## Description
Assign vault documents to OCR models based on mime type, priority, and presence of embedded text.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `documents` | `array` | Yes | Documents with doc_id, mime_type, page_count, priority, contains_text, source. |
| `ocr_profiles` | `object` | No | Optional mime_type -> model overrides. |
| `max_batch` | `integer` | No | Maximum number of documents to route in this call. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "document_vault_ocr_router",
  "arguments": {
    "documents": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "document_vault_ocr_router"`.
