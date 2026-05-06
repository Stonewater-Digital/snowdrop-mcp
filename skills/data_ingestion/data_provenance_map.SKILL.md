---
skill: data_provenance_map
category: data_ingestion
description: Construct lineage graph from ingestion artifacts and flag stale datasets or missing dependencies.
tier: free
inputs: artifacts
---

# Data Provenance Map

## Description
Construct lineage graph from ingestion artifacts and flag stale datasets or missing dependencies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `artifacts` | `array` | Yes | Lineage nodes with dataset, source_system, dependencies, last_updated. |
| `staleness_minutes` | `integer` | No | Minutes after which a dataset is considered stale. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "data_provenance_map",
  "arguments": {
    "artifacts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "data_provenance_map"`.
