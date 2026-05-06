---
skill: firebase_hosting_deploy
category: root
description: Deploy files to a Firebase Hosting site or channel via the Firebase Hosting REST API. Returns the channel URL and release version.
tier: free
inputs: site_id, files
---

# Firebase Hosting Deploy

## Description
Deploy files to a Firebase Hosting site or channel via the Firebase Hosting REST API. Returns the channel URL and release version.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `site_id` | `string` | Yes |  |
| `files` | `any` | Yes |  |
| `channel_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_hosting_deploy",
  "arguments": {
    "site_id": "<site_id>",
    "files": "<files>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_hosting_deploy"`.
