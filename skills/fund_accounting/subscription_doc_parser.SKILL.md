---
skill: subscription_doc_parser
category: fund_accounting
description: Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction. Returns structured data with per-field confidence scores.
tier: premium
inputs: none
---

# Subscription Doc Parser

## Description
Parses LP subscription agreement text extracted from PDF to identify the limited partner name, committed capital amount, legal entity type, and jurisdiction. Returns structured data with per-field confidence scores. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "subscription_doc_parser",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "subscription_doc_parser"`.
