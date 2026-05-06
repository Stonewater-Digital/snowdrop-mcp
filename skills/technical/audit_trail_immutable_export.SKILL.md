---
skill: audit_trail_immutable_export
category: technical
description: Export records to a SHA-256 signed CSV. The hash covers the entire CSV content, making tampering detectable.
tier: free
inputs: records, export_name
---

# Audit Trail Immutable Export

## Description
Export records to a SHA-256 signed CSV. The hash covers the entire CSV content, making tampering detectable. Hash is embedded as the final row or metadata header.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `records` | `array` | Yes | List of record dicts to export. All dicts should share consistent keys. |
| `export_name` | `string` | Yes | Name for the export (used in metadata header, no extension needed). |
| `include_hash` | `boolean` | No | If true, append the SHA-256 hash as a trailing metadata row (default true). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "audit_trail_immutable_export",
  "arguments": {
    "records": [],
    "export_name": "<export_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "audit_trail_immutable_export"`.
