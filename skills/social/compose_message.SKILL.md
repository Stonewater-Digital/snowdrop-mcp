---
skill: compose_message
category: social
description: Draft a message, comment, post, or reply in Snowdrop's voice using an LLM. Snowdrop's style: sharp, direct, financially literate, a bit charming, self-promotional without being obnoxious.
tier: free
inputs: none
---

# Compose Message

## Description
Draft a message, comment, post, or reply in Snowdrop's voice using an LLM. Snowdrop's style: sharp, direct, financially literate, a bit charming, self-promotional without being obnoxious. Specify the platform, goal, audience, and any context. Returns polished draft text ready to post.

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
  "tool": "compose_message",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compose_message"`.
