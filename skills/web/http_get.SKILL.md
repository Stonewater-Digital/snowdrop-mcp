---
skill: http_get
category: web
description: Make an HTTP GET request to any URL and return the response. Optionally pass custom headers (e.g.
tier: free
inputs: url
---

# Http Get

## Description
Make an HTTP GET request to any URL and return the response. Optionally pass custom headers (e.g. Authorization). Parses response as JSON by default; set json_only=false to get raw text instead. Returns status_code, body, response headers, and the final URL after any redirects.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | `string` | Yes | Full URL to fetch, including scheme (https://). |
| `headers` | `object` | No | Optional key-value pairs to send as HTTP request headers, e.g. {"Authorization": "Bearer token"}. |
| `timeout` | `integer` | No | Request timeout in seconds (default 15, max 120). |
| `json_only` | `boolean` | No | If true (default), attempt to parse the response as JSON. If false, return the raw response text. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "http_get",
  "arguments": {
    "url": "<url>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "http_get"`.
