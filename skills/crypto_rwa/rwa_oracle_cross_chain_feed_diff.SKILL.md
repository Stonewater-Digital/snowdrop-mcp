---
skill: rwa_oracle_cross_chain_feed_diff
category: crypto_rwa
description: Diffs oracle values across chains to detect delayed relays or bridge drifts.
tier: free
inputs: payload
---

# Rwa Oracle Cross Chain Feed Diff

## Description
Diffs oracle values across chains to detect delayed relays or bridge drifts.

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
  "tool": "rwa_oracle_cross_chain_feed_diff",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_cross_chain_feed_diff"`.
