---
skill: moltbook_engagement_loop
category: social
description: Analyzes Moltbook post history to determine optimal posting times (UTC), best-performing content types, recommended posting frequency, and forecasts expected engagement for the next post.
tier: free
inputs: content_history
---

# Moltbook Engagement Loop

## Description
Analyzes Moltbook post history to determine optimal posting times (UTC), best-performing content types, recommended posting frequency, and forecasts expected engagement for the next post.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `content_history` | `array` | Yes | List of post dicts with: post_id (str), content_type (str), posting_time_utc (ISO-8601 str), engagement_score (float), submolt (str). |
| `target_submolt` | `string` | No | Optional: filter analysis to a specific submolt. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_engagement_loop",
  "arguments": {
    "content_history": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_engagement_loop"`.
