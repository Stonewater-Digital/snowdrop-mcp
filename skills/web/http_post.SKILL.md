---
skill: http_post
category: web
description: Make an HTTP POST request with a JSON body to any URL and return the response. Optionally pass custom headers (e.g.
tier: free
inputs: url, body
---

# Http Post

## Description
Make an HTTP POST request with a JSON body to any URL and return the response. Optionally pass custom headers (e.g. Authorization). Always sends Content-Type: application/json. Returns status_code, parsed body (or raw text on JSON parse failure), and the final URL.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | `string` | Yes | Full URL to POST to, including scheme (https://). |
| `body` | `object` | Yes | JSON-serialisable object to send as the request body. |
| `headers` | `object` | No | Optional key-value pairs merged into the request headers. Content-Type: application/json is always set. |
| `timeout` | `integer` | No | Request timeout in seconds (default 15, max 120). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "http_post",
  "arguments": {
    "url": "<url>",
    "body": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "http_post"`.
