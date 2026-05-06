---
skill: vertex_ai_inference
category: root
description: Call Vertex AI Gemini models for text generation, analysis, or embeddings. Uses Vertex AI REST API with explicit service account credentials — no gcloud, no ADC.
tier: free
inputs: action
---

# Vertex Ai Inference

## Description
Call Vertex AI Gemini models for text generation, analysis, or embeddings. Uses Vertex AI REST API with explicit service account credentials — no gcloud, no ADC. Supports gemini-2.0-flash-exp (fastest), gemini-1.5-pro (most capable), gemini-1.5-flash.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation: generate text, analyze input, or create embeddings. |
| `prompt` | `string` | No | Text prompt (required for generate/analyze). |
| `text` | `string` | No | Text to embed (required for embed). |
| `model` | `string` | No | Gemini model ID. |
| `max_tokens` | `integer` | No |  |
| `temperature` | `number` | No |  |
| `project_id` | `string` | No | GCP project ID. |
| `region` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vertex_ai_inference",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vertex_ai_inference"`.
