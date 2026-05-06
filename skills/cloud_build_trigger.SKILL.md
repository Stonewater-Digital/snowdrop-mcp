---
skill: cloud_build_trigger
category: root
description: Manually trigger a Google Cloud Build build from a trigger ID or repo/branch. Returns the build ID and log URL for monitoring.
tier: free
inputs: none
---

# Cloud Build Trigger

## Description
Manually trigger a Google Cloud Build build from a trigger ID or repo/branch. Returns the build ID and log URL for monitoring.

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
  "tool": "cloud_build_trigger",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cloud_build_trigger"`.
