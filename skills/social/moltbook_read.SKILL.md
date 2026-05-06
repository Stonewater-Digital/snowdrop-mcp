---
skill: moltbook_read
category: social
description: Read content from Moltbook. Supports four actions: 'feed' (top posts across all submolts), 'submolts' (list of communities), 'post' (single post by ID), and 'submolt_posts' (posts within a named submolt).
tier: free
inputs: action
---

# Moltbook Read

## Description
Read content from Moltbook. Supports four actions: 'feed' (top posts across all submolts), 'submolts' (list of communities), 'post' (single post by ID), and 'submolt_posts' (posts within a named submolt). Returns a list of items and a count.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | The read action to perform: 'feed', 'submolts', 'post', or 'submolt_posts'. |
| `submolt_name` | `string` | No | Required for action='submolt_posts'. The submolt name to read from. |
| `post_id` | `string` | No | Required for action='post'. The ID of the post to retrieve. |
| `limit` | `integer` | No | Number of results to return (default 10, max 100). |
| `sort` | `string` | No | Sort order for feed or submolt_posts (default 'hot'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_read",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_read"`.
