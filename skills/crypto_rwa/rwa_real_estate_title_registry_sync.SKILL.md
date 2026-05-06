---
skill: rwa_real_estate_title_registry_sync
category: crypto_rwa
description: Cross-checks tokenized deed metadata with county title registries and surfaces mismatched parcel identifiers.
tier: free
inputs: payload
---

# Rwa Real Estate Title Registry Sync

## Description
Cross-checks tokenized deed metadata with county title registries and surfaces mismatched parcel identifiers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_title_registry_sync",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_title_registry_sync"`.
