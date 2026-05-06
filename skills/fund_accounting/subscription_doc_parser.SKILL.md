---
skill: subscription_doc_parser
category: fund_accounting
description: Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction. Returns structured data with per-field confidence scores.
tier: premium
inputs: document_text, fund_name
---

# Subscription Doc Parser

## Description
Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction. Returns structured data with per-field confidence scores. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `document_text` | `string` | Yes | Raw text extracted from the LP subscription agreement PDF. |
| `fund_name` | `string` | No | Expected fund name for validation against the parsed document text. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "subscription_doc_parser",
  "arguments": {
    "document_text": "LIMITED PARTNERSHIP AGREEMENT\n\nThis Subscription Agreement is entered into by State Teachers Retirement System of Ohio ('Limited Partner') committing Ten Million Dollars ($10,000,000) to Snowdrop Growth Equity Fund II, L.P., a Delaware limited partnership. The Limited Partner is a public pension fund organized under the laws of the State of Ohio...",
    "fund_name": "Snowdrop Growth Equity Fund II, L.P."
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "subscription_doc_parser"`.
