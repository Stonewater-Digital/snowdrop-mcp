---
skill: custodian_feed_harmonizer
category: data_ingestion
description: Normalize custodian statement payloads into a canonical schema with validation flags.
tier: free
inputs: records, field_mappings
---

# Custodian Feed Harmonizer

## Description
Normalize custodian statement payloads into a canonical schema with validation flags.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `records` | `array` | Yes | Raw custodian rows that include at least a 'source' key. |
| `field_mappings` | `object` | Yes | Mapping per source -> canonical field map (e.g., {'custody_bank': {'account_id': 'acct'}}). |
| `default_currency` | `string` | No | Currency to backfill when a record omits the field. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "custodian_feed_harmonizer",
  "arguments": {
    "records": [],
    "field_mappings": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "custodian_feed_harmonizer"`.
