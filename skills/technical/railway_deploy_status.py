"""Construct Railway GraphQL calls to inspect deployment health."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "railway_deploy_status",
    "description": "Builds Railway GraphQL queries and parses deployment states when provided.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "project_id": {"type": "string"},
            "service_id": {"type": "string"},
            "environment_id": {"type": "string"},
            "api_response": {
                "type": "object",
                "description": "Optional GraphQL response to parse for status.",
            },
        },
        "required": ["project_id", "service_id"],
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


def railway_deploy_status(
    project_id: str,
    service_id: str,
    environment_id: str | None = None,
    api_response: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return the prepared GraphQL payload and parsed deployment status.

    Args:
        project_id: Railway project identifier.
        service_id: Railway service identifier.
        environment_id: Optional environment override (prod/stage).
        api_response: Optional GraphQL response to parse immediately.

    Returns:
        Envelope containing the prepared request details and deployment summary.
    """

    try:
        token = os.getenv("RAILWAY_TOKEN")
        if not token:
            raise ValueError("RAILWAY_TOKEN missing; see .env.template")

        query = (
            "query DeploymentStatus($projectId: ID!, $serviceId: ID!, $environmentId: ID) {"
            "  service(id: $serviceId, projectId: $projectId) {"
            "    deployments(environmentId: $environmentId, first: 1) {"
            "      edges { node { id environments { id } updatedAt status } }"
            "    }"
            "  }"
            "}"
        )
        variables = {
            "projectId": project_id,
            "serviceId": service_id,
            "environmentId": environment_id,
        }

        prepared_request = {
            "url": "https://backboard.railway.app/graphql/v2",
            "headers": {"Authorization": "Bearer ***redacted***"},
            "body": {"query": query, "variables": variables},
        }

        deployment = _parse_response(api_response) if api_response else None

        data = {
            "prepared_request": prepared_request,
            "deployment": deployment,
            "submission_status": "pending_thunder_approval" if not api_response else "parsed",
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("railway_deploy_status", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_response(api_response: dict[str, Any] | None) -> dict[str, Any] | None:
    if not api_response:
        return None
    try:
        edges = (
            api_response["data"]["service"]["deployments"]["edges"]
        )
        if not edges:
            return None
        node = edges[0]["node"]
        return {
            "deployment_id": node.get("id"),
            "status": node.get("status"),
            "last_updated": node.get("updatedAt"),
        }
    except (KeyError, TypeError):
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
