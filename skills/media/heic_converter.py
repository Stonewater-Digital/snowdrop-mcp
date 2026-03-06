"""
Executive Summary: Convert HEIC/HEIF images to JPEG or PNG format.

Supports two input modes — base64-encoded content (primary, for remote MCP callers
on Cloud Run) and local file paths (for on-node use). Output mirrors the input
mode: if no output_path is given, returns base64-encoded image data.

Table of Contents:
- TOOL_META: MCP tool descriptor
- heic_converter: Main conversion callable
"""
import base64
import io
import logging
from typing import Any

from skills.utils import log_lesson, get_iso_timestamp

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "heic_converter",
    "description": (
        "Converts a HEIC/HEIF image to JPEG or PNG. "
        "Accepts input as a local file path or base64-encoded content. "
        "Returns the converted image as a local file or base64 string."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "input_path": {
                "type": "string",
                "description": "Absolute or relative path to the source HEIC/HEIF file (local filesystem only).",
            },
            "input_base64": {
                "type": "string",
                "description": "Base64-encoded HEIC/HEIF file content. Use this when calling from a remote MCP client.",
            },
            "output_path": {
                "type": "string",
                "description": (
                    "Path where the converted image will be saved. "
                    "If omitted, the converted image is returned as base64 in the response."
                ),
            },
            "format": {
                "type": "string",
                "enum": ["JPEG", "PNG"],
                "default": "JPEG",
                "description": "Output image format. JPEG is smaller; PNG is lossless.",
            },
            "quality": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "default": 95,
                "description": "JPEG compression quality (1–100). Ignored for PNG.",
            },
            "preserve_exif": {
                "type": "boolean",
                "default": True,
                "description": "Whether to copy EXIF metadata (camera info, GPS, etc.) to the output image.",
            },
        },
        "oneOf": [
            {"required": ["input_path"]},
            {"required": ["input_base64"]},
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "output_path": {"type": ["string", "null"]},
            "output_base64": {"type": ["string", "null"]},
            "format": {"type": "string"},
            "width": {"type": "integer"},
            "height": {"type": "integer"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}


def heic_converter(
    input_path: str | None = None,
    input_base64: str | None = None,
    output_path: str | None = None,
    format: str = "JPEG",
    quality: int = 95,
    preserve_exif: bool = True,
) -> dict[str, Any]:
    """Convert a HEIC/HEIF image to JPEG or PNG.

    Args:
        input_path: Local path to the source HEIC/HEIF file.
        input_base64: Base64-encoded HEIC/HEIF content (alternative to input_path).
        output_path: Destination file path. If None, the result is returned as base64.
        format: Output format — "JPEG" or "PNG".
        quality: JPEG quality (1–100). Ignored for PNG.
        preserve_exif: If True, copies EXIF metadata to the output image.

    Returns:
        Dict with status, image dimensions, and either output_path or output_base64.
    """
    try:
        # Import here so the module loads even if pillow-heif is absent at import time,
        # giving a cleaner error message in the except block below.
        import pillow_heif
        from PIL import Image

        if not input_path and not input_base64:
            raise ValueError("Provide either input_path or input_base64.")

        fmt = format.upper()
        if fmt not in ("JPEG", "PNG"):
            raise ValueError(f"Unsupported format '{format}'. Must be JPEG or PNG.")

        pillow_heif.register_heif_opener()

        if input_base64:
            raw_bytes = base64.b64decode(input_base64)
            image: Image.Image = Image.open(io.BytesIO(raw_bytes))
        else:
            image = Image.open(input_path)

        # HEIC images can have a rotation flag in EXIF; apply it so the output
        # is correctly oriented regardless of viewer EXIF support.
        from PIL import ImageOps
        image = ImageOps.exif_transpose(image)

        # JPEG does not support an alpha channel — convert RGBA/P to RGB.
        if fmt == "JPEG" and image.mode in ("RGBA", "P", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode in ("RGBA", "LA"):
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)
            image = background

        width, height = image.size

        save_kwargs: dict[str, Any] = {"format": fmt}
        if fmt == "JPEG":
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True
        if preserve_exif and (exif_data := image.info.get("exif")):
            save_kwargs["exif"] = exif_data

        result_base64: str | None = None

        if output_path:
            image.save(output_path, **save_kwargs)
        else:
            buf = io.BytesIO()
            image.save(buf, **save_kwargs)
            result_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        return {
            "status": "success",
            "output_path": output_path,
            "output_base64": result_base64,
            "format": fmt,
            "width": width,
            "height": height,
            "timestamp": get_iso_timestamp(),
        }

    except Exception as exc:
        log_lesson(f"heic_converter: {exc}")
        logger.error("heic_converter failed: %s", exc)
        return {
            "status": "error",
            "error": str(exc),
            "output_path": None,
            "output_base64": None,
            "format": format,
            "width": None,
            "height": None,
            "timestamp": get_iso_timestamp(),
        }
