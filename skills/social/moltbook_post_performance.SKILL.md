---
skill: moltbook_post_performance
category: social
description: Fetch live upvotes and comments for one or more Moltbook posts by post_id. Returns engagement metrics, ROI score (upvotes*2 + comments*5), and traction status.
tier: free
inputs: none
---

# Moltbook Post Performance

## Description
Fetch live upvotes and comments for one or more Moltbook posts by post_id. Returns engagement metrics, ROI score (upvotes*2 + comments*5), and traction status. Use for spot-checking specific posts or verifying the performance poller is working. Set write_to_sheet=True to also upsert results into the POST PERFORMANCE tab.

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
  "tool": "moltbook_post_performance",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_post_performance"`.
