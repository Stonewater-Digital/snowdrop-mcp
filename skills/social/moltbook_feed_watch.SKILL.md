---
skill: moltbook_feed_watch
category: social
description: Scan recent Moltbook posts across specified (or default) submolts and identify engagement opportunities — posts to comment on, discussions Snowdrop can add value to, or content that could drive traffic to her repos. Returns ranked engagement targets with suggested response angles.
tier: free
inputs: none
---

# Moltbook Feed Watch

## Description
Scan recent Moltbook posts across specified (or default) submolts and identify engagement opportunities — posts to comment on, discussions Snowdrop can add value to, or content that could drive traffic to her repos. Returns ranked engagement targets with suggested response angles. Run periodically as a vigilance loop.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `submolts` | `array` | No |  |
| `hours_back` | `integer` | No |  |
| `min_score` | `integer` | No |  |
| `limit_per_submolt` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_feed_watch",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_feed_watch"`.
