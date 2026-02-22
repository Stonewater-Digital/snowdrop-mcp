"""Validate Snowdrop config dictionaries."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "config_validator",
    "description": "Ensures config.yaml content meets Snowdrop schema expectations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "config": {"type": "object"},
            "required_sections": {
                "type": "array",
                "items": {"type": "string"},
                "default": [
                    "models",
                    "assembly_line",
                    "budget",
                    "wallets",
                    "ghost_ledger",
                ],
            },
        },
        "required": ["config"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def config_validator(
    config: dict[str, Any],
    required_sections: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Validate core config schema elements."""
    try:
        errors: list[dict[str, Any]] = []
        warnings: list[dict[str, Any]] = []
        required = required_sections or ["models", "assembly_line", "budget", "wallets", "ghost_ledger"]
        found_sections = list(config.keys())
        for section in required:
            if section not in config:
                errors.append({"section": section, "message": "Missing required section"})

        models = config.get("models", {}) or {}
        if not isinstance(models, dict) or not models:
            errors.append({"section": "models", "message": "Models must be a non-empty mapping"})
        else:
            for name, model in models.items():
                if not model:
                    warnings.append({"section": f"models.{name}", "message": "Model definition empty"})

        budget = config.get("budget", {}) or {}
        cap = budget.get("monthly_cap")
        if cap is None or float(cap) <= 0:
            errors.append({"section": "budget", "message": "monthly_cap must be positive"})

        wallets = config.get("wallets", {}) or {}
        for key, value in wallets.items():
            if not isinstance(value, str) or not value.strip():
                errors.append({"section": f"wallets.{key}", "message": "Wallet address missing"})

        data = {
            "valid": not errors,
            "errors": errors,
            "warnings": warnings,
            "sections_found": found_sections,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("config_validator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
