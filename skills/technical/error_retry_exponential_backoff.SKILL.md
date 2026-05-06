---
skill: error_retry_exponential_backoff
category: technical
description: Generate an exponential backoff retry schedule with optional jitter for production error handling. Returns per-attempt delays and total max wait time.
tier: free
inputs: operation_name
---

# Error Retry Exponential Backoff

## Description
Generate an exponential backoff retry schedule with optional jitter for production error handling. Returns per-attempt delays and total max wait time.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation_name` | `string` | Yes | Human-readable name of the operation being retried (for logging). |
| `max_retries` | `integer` | No | Maximum number of retry attempts (default 3). |
| `base_delay_seconds` | `number` | No | Initial delay before first retry in seconds (default 1.0). |
| `max_delay_seconds` | `number` | No | Maximum cap on any single retry delay in seconds (default 60.0). |
| `jitter` | `boolean` | No | Whether to add random jitter to prevent thundering herd (default true). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "error_retry_exponential_backoff",
  "arguments": {
    "operation_name": "<operation_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "error_retry_exponential_backoff"`.
