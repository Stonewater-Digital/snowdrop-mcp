---
skill: github_discussion_poster
category: recruiting
description: Post or update comments on GitHub Discussions via GraphQL. Supports addDiscussionComment and updateDiscussionComment mutations.
tier: free
inputs: action, body
---

# Github Discussion Poster

## Description
Post or update comments on GitHub Discussions via GraphQL. Supports addDiscussionComment and updateDiscussionComment mutations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes |  |
| `repo` | `string` | No | Repository in owner/name format (e.g. Stonewater-Digital/the-watering-hole) |
| `discussion_number` | `integer` | No | Discussion number (required for post_comment) |
| `comment_id` | `string` | No | GraphQL node ID of comment (required for update_comment) |
| `body` | `string` | Yes | Markdown body of the comment |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "github_discussion_poster",
  "arguments": {
    "action": "<action>",
    "body": "<body>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_discussion_poster"`.
