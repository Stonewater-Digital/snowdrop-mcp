"""
Executive Summary: Build heartbeat monitoring configurations for Fly.io and Railway services with consecutive-failure alerting rules.
Inputs: services (list of dicts: name, url, expected_status, timeout_seconds)
Outputs: monitoring_config (dict), check_interval_seconds (int), alert_rules (list), services_configured (int)
MCP Tool Name: agent_heartbeat_monitor
"""
import os
import logging
import hashlib
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "agent_heartbeat_monitor",
    "description": "Build health check monitoring configurations for Fly.io and Railway services. Defines check intervals, alert rules (3 consecutive failures = alert), and per-service configs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "services": {
                "type": "array",
                "description": "List of service dicts, each with: name, url, expected_status (HTTP status code), timeout_seconds.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "url": {"type": "string"},
                        "expected_status": {"type": "integer"},
                        "timeout_seconds": {"type": "number"}
                    },
                    "required": ["name", "url", "expected_status", "timeout_seconds"]
                }
            }
        },
        "required": ["services"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "monitoring_config": {"type": "object"},
            "check_interval_seconds": {"type": "integer"},
            "alert_rules": {"type": "array"},
            "services_configured": {"type": "integer"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["monitoring_config", "check_interval_seconds", "alert_rules", "services_configured", "status", "timestamp"]
    }
}

# Heartbeat monitoring constants
_CONSECUTIVE_FAILURES_THRESHOLD = 3
_DEFAULT_CHECK_INTERVAL_SECONDS = 30
_MAX_TIMEOUT_SECONDS = 30.0
_MIN_TIMEOUT_SECONDS = 1.0

# Platform detection heuristics
_FLY_INDICATORS = {"fly.dev", "fly.io", "flycast"}
_RAILWAY_INDICATORS = {"railway.app", "up.railway.app"}


def _detect_platform(url: str) -> str:
    """Detect hosting platform from URL.

    Args:
        url: Service URL string.

    Returns:
        Platform name string: "fly.io", "railway", or "unknown".
    """
    url_lower = url.lower()
    if any(ind in url_lower for ind in _FLY_INDICATORS):
        return "fly.io"
    if any(ind in url_lower for ind in _RAILWAY_INDICATORS):
        return "railway"
    return "unknown"


def _validate_service(service: dict, idx: int) -> dict:
    """Validate and normalize a single service configuration dict.

    Args:
        service: Raw service dict from input.
        idx: Index in the services list (for error messages).

    Returns:
        Validated and normalized service dict.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    required = {"name", "url", "expected_status", "timeout_seconds"}
    missing = required - set(service.keys())
    if missing:
        raise ValueError(f"Service at index {idx} missing fields: {missing}.")

    name = str(service["name"]).strip()
    url = str(service["url"]).strip()
    expected_status = int(service["expected_status"])
    timeout = float(service["timeout_seconds"])

    if not name:
        raise ValueError(f"Service at index {idx} has empty name.")
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"Service '{name}' URL must start with http:// or https://, got '{url}'.")
    if not (100 <= expected_status <= 599):
        raise ValueError(f"Service '{name}' expected_status {expected_status} is not a valid HTTP status code.")
    if timeout < _MIN_TIMEOUT_SECONDS or timeout > _MAX_TIMEOUT_SECONDS:
        raise ValueError(
            f"Service '{name}' timeout {timeout}s must be between {_MIN_TIMEOUT_SECONDS} and {_MAX_TIMEOUT_SECONDS}."
        )

    return {
        "name": name,
        "url": url,
        "expected_status": expected_status,
        "timeout_seconds": timeout,
    }


def _build_service_config(service: dict) -> dict:
    """Build the full monitoring config for a single service.

    Args:
        service: Validated service dict.

    Returns:
        Complete per-service monitoring configuration dict.
    """
    platform = _detect_platform(service["url"])
    service_id = hashlib.sha256(service["url"].encode()).hexdigest()[:12]

    # Platform-specific health check path heuristics
    health_paths: list[str] = ["/health", "/healthz", "/ping", "/status", "/ready"]
    if platform == "fly.io":
        health_paths = ["/health", "/healthz"] + health_paths
    elif platform == "railway":
        health_paths = ["/health", "/ping"] + health_paths

    # Check if service URL already ends with a health path
    has_health_path = any(service["url"].endswith(p) for p in health_paths)

    return {
        "service_id": service_id,
        "name": service["name"],
        "url": service["url"],
        "platform": platform,
        "expected_status": service["expected_status"],
        "timeout_seconds": service["timeout_seconds"],
        "has_explicit_health_path": has_health_path,
        "suggested_health_paths": health_paths[:3],
        "check_method": "GET",
        "follow_redirects": True,
        "verify_ssl": True,
        "headers": {
            "User-Agent": "Snowdrop-Heartbeat/1.0",
            "Accept": "application/json, text/plain, */*",
        },
        "consecutive_failures": 0,  # runtime counter (starts at 0)
        "last_status": None,
        "last_checked": None,
        "state": "unknown",  # unknown | healthy | degraded | down
        "metrics": {
            "total_checks": 0,
            "total_failures": 0,
            "total_successes": 0,
            "current_consecutive_failures": 0,
            "avg_response_time_ms": None,
        },
    }


def agent_heartbeat_monitor(services: list[dict]) -> dict:
    """Build heartbeat monitoring configurations for a list of services.

    Generates per-service health check configs, a global monitoring schedule,
    and alert rules that trigger after 3 consecutive failures. Supports
    platform-specific heuristics for Fly.io and Railway deployments.

    Args:
        services: List of service dicts, each containing:
            - name (str): Human-readable service name.
            - url (str): Full HTTPS URL of the health check endpoint.
            - expected_status (int): Expected HTTP response status code.
            - timeout_seconds (float): Per-request timeout.

    Returns:
        A dict with keys:
            - monitoring_config (dict): Global config and per-service configs.
            - check_interval_seconds (int): How often to poll all services.
            - alert_rules (list): Alert conditions and escalation policies.
            - services_configured (int): Number of services successfully configured.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        if not isinstance(services, list) or len(services) == 0:
            raise ValueError("services must be a non-empty list.")

        validated_services = [_validate_service(svc, idx) for idx, svc in enumerate(services)]
        service_configs = [_build_service_config(svc) for svc in validated_services]

        # Determine check interval: shorter interval for fewer services
        # 30s for <=5 services, scale up slowly for larger fleets
        n = len(service_configs)
        check_interval = _DEFAULT_CHECK_INTERVAL_SECONDS if n <= 5 else min(30 + (n - 5) * 5, 120)

        # Alert rules
        alert_rules: list[dict] = [
            {
                "rule_id": "consecutive_failure_alert",
                "name": "Consecutive Failure Alert",
                "condition": f"consecutive_failures >= {_CONSECUTIVE_FAILURES_THRESHOLD}",
                "threshold": _CONSECUTIVE_FAILURES_THRESHOLD,
                "severity": "critical",
                "action": "alert",
                "channels": ["log", "webhook", "email"],
                "description": (
                    f"Trigger alert when a service fails {_CONSECUTIVE_FAILURES_THRESHOLD} "
                    "health checks in a row without recovery."
                ),
                "auto_resolve": True,
                "resolve_condition": "consecutive_failures == 0",
            },
            {
                "rule_id": "degraded_response_time",
                "name": "Slow Response Warning",
                "condition": "avg_response_time_ms > timeout_seconds * 1000 * 0.8",
                "severity": "warning",
                "action": "warn",
                "channels": ["log"],
                "description": "Warn when average response time exceeds 80% of timeout threshold.",
                "auto_resolve": True,
            },
            {
                "rule_id": "status_code_mismatch",
                "name": "Unexpected Status Code",
                "condition": "last_status != expected_status",
                "severity": "critical",
                "action": "alert",
                "channels": ["log", "webhook"],
                "description": "Alert immediately on unexpected HTTP status code regardless of consecutive count.",
                "auto_resolve": True,
            },
        ]

        monitoring_config = {
            "version": "1.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "check_interval_seconds": check_interval,
            "consecutive_failure_threshold": _CONSECUTIVE_FAILURES_THRESHOLD,
            "global_timeout_seconds": max(svc["timeout_seconds"] for svc in validated_services),
            "services": service_configs,
            "scheduler": {
                "type": "asyncio_periodic",
                "concurrency": "gather_all",  # check all services in parallel per interval
                "jitter_seconds": 2,  # add small random jitter to spread load
            },
            "storage": {
                "metrics_backend": "in_memory",
                "persist_to": "logs/heartbeat_metrics.jsonl",
                "retention_checks": 1440,  # keep last 1440 checks (12h at 30s interval)
            },
            "platforms_detected": list({svc["platform"] for svc in service_configs}),
        }

        return {
            "status": "success",
            "monitoring_config": monitoring_config,
            "check_interval_seconds": check_interval,
            "alert_rules": alert_rules,
            "services_configured": len(service_configs),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"agent_heartbeat_monitor failed: {e}")
        _log_lesson(f"agent_heartbeat_monitor: {e}")
        return {
            "status": "error",
            "error": str(e),
            "monitoring_config": {},
            "check_interval_seconds": _DEFAULT_CHECK_INTERVAL_SECONDS,
            "alert_rules": [],
            "services_configured": 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
