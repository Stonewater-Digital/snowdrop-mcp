---
skill: github_discussion_comment
category: social
description: Post a comment to an existing GitHub Discussion by discussion number and repo. Use this to engage with discussions, respond to skill requests, thank contributors, or add follow-up information.
tier: free
inputs: none
---

# Github Discussion Comment

## Description
Post a comment to an existing GitHub Discussion by discussion number and repo. Use this to engage with discussions, respond to skill requests, thank contributors, or add follow-up information. Returns the comment URL.

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
  "tool": "github_discussion_comment",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_discussion_comment"`.
