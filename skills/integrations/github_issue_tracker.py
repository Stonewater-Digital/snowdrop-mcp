"""Monitor GitHub issues for Proof of Labor tracking."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

TOOL_META: dict[str, Any] = {
    "name": "github_issue_tracker",
    "description": "Fetches labeled GitHub issues and estimates difficulty.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "repo": {"type": "string"},
            "labels": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["repo"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "issues": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def github_issue_tracker(
    repo: str,
    labels: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return open issues filtered by labels with difficulty estimates."""

    try:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN missing; see .env.template")

        endpoint = f"https://api.github.com/repos/{repo}/issues"
        params = {"state": "open"}
        if labels:
            params["labels"] = ",".join(labels)
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        issues_payload = response.json()
        issues = []
        for issue in issues_payload:
            if "pull_request" in issue:
                continue
            label_names = [label["name"].lower() for label in issue.get("labels", [])]
            issues.append(
                {
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "labels": label_names,
                    "difficulty": _difficulty_from_labels(label_names),
                    "url": issue.get("html_url"),
                }
            )

        return {
            "status": "success",
            "data": {"issues": issues},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("github_issue_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _difficulty_from_labels(labels: list[str]) -> str:
    if any(label in {"easy", "good first issue"} for label in labels):
        return "low"
    if any(label in {"medium", "intermediate"} for label in labels):
        return "medium"
    if any(label in {"hard", "complex"} for label in labels):
        return "high"
    return "unknown"


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
