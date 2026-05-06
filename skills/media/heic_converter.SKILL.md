---
skill: heic_converter
category: media
description: Converts a HEIC/HEIF image to JPEG or PNG. Accepts input as a local file path or base64-encoded content.
tier: free
inputs: none
---

# Heic Converter

## Description
Converts a HEIC/HEIF image to JPEG or PNG. Accepts input as a local file path or base64-encoded content. Returns the converted image as a local file or base64 string.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_path` | `string` | No | Absolute or relative path to the source HEIC/HEIF file (local filesystem only). |
| `input_base64` | `string` | No | Base64-encoded HEIC/HEIF file content. Use this when calling from a remote MCP client. |
| `output_path` | `string` | No | Path where the converted image will be saved. If omitted, the converted image is returned as base64 in the response. |
| `format` | `string` | No | Output image format. JPEG is smaller; PNG is lossless. |
| `quality` | `integer` | No | JPEG compression quality (1–100). Ignored for PNG. |
| `preserve_exif` | `boolean` | No | Whether to copy EXIF metadata (camera info, GPS, etc.) to the output image. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "heic_converter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "heic_converter"`.
