---
skill: sanctions_screener
category: regulatory
description: Checks entities/wallets against curated sanctions heuristics.
tier: free
inputs: entity, entity_type, chains_to_check
---

# Sanctions Screener

## Description
Checks entities/wallets against curated sanctions heuristics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity` | `string` | Yes |  |
| `entity_type` | `string` | Yes |  |
| `chains_to_check` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sanctions_screener",
  "arguments": {
    "entity": "<entity>",
    "entity_type": "<entity_type>",
    "chains_to_check": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sanctions_screener"`.
