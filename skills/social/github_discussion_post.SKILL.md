---
skill: github_discussion_post
category: social
description: Post a new GitHub Discussion using the GitHub GraphQL API. Fetches the repo and category IDs, then creates the discussion.
tier: free
inputs: repo_owner, repo_name, category_name, title, body
---

# Github Discussion Post

## Description
Post a new GitHub Discussion using the GitHub GraphQL API. Fetches the repo and category IDs, then creates the discussion. Requires GITHUB_TOKEN env var with discussions:write permission. Returns the discussion URL, number, and title.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `repo_owner` | `string` | Yes | GitHub organisation or user login, e.g. 'Stonewater-Digital'. |
| `repo_name` | `string` | Yes | Repository name, e.g. 'snowdrop-mcp'. |
| `category_name` | `string` | Yes | Discussion category name, e.g. 'General' or 'Ideas'. |
| `title` | `string` | Yes | Title of the new discussion. |
| `body` | `string` | Yes | Body text of the new discussion (markdown supported). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "github_discussion_post",
  "arguments": {
    "repo_owner": "<repo_owner>",
    "repo_name": "<repo_name>",
    "category_name": "<category_name>",
    "title": "<title>",
    "body": "<body>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_discussion_post"`.
