---
skill: context7_docs
category: docs
description: Fetch up-to-date library documentation via Context7 MCP. Resolves a library name to its Context7 ID, then fetches current version-specific docs.
tier: free
inputs: none
---

# Context7 Docs

## Description
Fetch up-to-date library documentation via Context7 MCP. Resolves a library name to its Context7 ID, then fetches current version-specific docs. Use before implementing code that uses any third-party library (gspread, FastMCP, requests, anthropic, gcloud, etc.) to ensure modern best practices. Requires CONTEXT7_API_KEY env var (free at context7.com/dashboard).

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
  "tool": "context7_docs",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "context7_docs"`.
