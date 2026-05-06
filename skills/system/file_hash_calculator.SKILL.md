---
skill: file_hash_calculator
category: system
description: Compute a cryptographic hash (SHA-256, SHA-1, MD5, SHA-512, etc.) of the given string content. Returns the hex digest.
tier: free
inputs: content
---

# File Hash Calculator

## Description
Compute a cryptographic hash (SHA-256, SHA-1, MD5, SHA-512, etc.) of the given string content. Returns the hex digest.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `content` | `string` | Yes | The string content to hash. |
| `algorithm` | `string` | No | Hash algorithm to use. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "file_hash_calculator",
  "arguments": {
    "content": "<content>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "file_hash_calculator"`.
