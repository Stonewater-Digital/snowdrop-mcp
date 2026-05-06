---
skill: github_discussion_comment
category: social
description: Post a comment to an existing GitHub Discussion by discussion number and repo. Use this to engage with discussions, respond to skill requests, thank contributors, or add follow-up information.
tier: free
inputs: repo_owner, repo_name, discussion_number, body
---

# Github Discussion Comment

## Description
Post a comment to an existing GitHub Discussion by discussion number and repo. Use this to engage with discussions, respond to skill requests, thank contributors, or add follow-up information. Returns the comment URL.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `repo_owner` | `string` | Yes |  |
| `repo_name` | `string` | Yes |  |
| `discussion_number` | `integer` | Yes |  |
| `body` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "github_discussion_comment",
  "arguments": {
    "repo_owner": "<repo_owner>",
    "repo_name": "<repo_name>",
    "discussion_number": 0,
    "body": "<body>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_discussion_comment"`.
