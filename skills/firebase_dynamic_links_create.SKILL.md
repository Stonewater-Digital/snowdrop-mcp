---
skill: firebase_dynamic_links_create
category: root
description: Create a Firebase Dynamic Link (short URL) that routes users to the correct app or web destination based on their platform. Returns the short link and preview link.
tier: free
inputs: long_url, domain_uri_prefix
---

# Firebase Dynamic Links Create

## Description
Create a Firebase Dynamic Link (short URL) that routes users to the correct app or web destination based on their platform. Returns the short link and preview link.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `long_url` | `string` | Yes |  |
| `domain_uri_prefix` | `string` | Yes |  |
| `android_package_name` | `string` | No |  |
| `ios_bundle_id` | `string` | No |  |
| `suffix_option` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_dynamic_links_create",
  "arguments": {
    "long_url": "<long_url>",
    "domain_uri_prefix": "<domain_uri_prefix>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_dynamic_links_create"`.
