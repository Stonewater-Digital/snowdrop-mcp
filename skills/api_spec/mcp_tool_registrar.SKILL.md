---
skill: mcp_tool_registrar
category: api_spec
description: Produces a JSON-RPC compliant MCP tools/list response for Snowdrop skills.
tier: free
inputs: skills
---

# Mcp Tool Registrar

## Description
Produces a JSON-RPC compliant MCP tools/list response for Snowdrop skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills` | `array` | Yes |  |
| `server_name` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mcp_tool_registrar",
  "arguments": {
    "skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mcp_tool_registrar"`.
