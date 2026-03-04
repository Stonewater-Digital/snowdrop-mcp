"""
Executive Summary: Plain English daily briefing for Thunder — condenses portfolio, P&L, alerts, and market movers into a concise situational summary.
Inputs: data_sources (dict: portfolio_value float, daily_pnl float, open_alerts list,
        reconciliation_status str, top_movers list[dict: asset str, change_pct float])
Outputs: briefing_text (str), severity (str: routine/attention/urgent), key_metrics (dict), action_items (list)
MCP Tool Name: thunder_executive_briefing
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "thunder_executive_briefing",
    "description": (
        "Generates a concise, plain-English daily executive briefing for Thunder "
        "(operator). Synthesises portfolio value, P&L, open alerts, reconciliation "
        "status, and market movers into a human-readable summary. Classifies overall "
        "severity as routine, attention, or urgent and surfaces action items."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "data_sources": {
                "type": "object",
                "properties": {
                    "portfolio_value":      {"type": "number"},
                    "daily_pnl":            {"type": "number"},
                    "open_alerts":          {"type": "array", "items": {"type": "string"}},
                    "reconciliation_status": {"type": "string"},
                    "top_movers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "asset":      {"type": "string"},
                                "change_pct": {"type": "number"},
                            },
                            "required": ["asset", "change_pct"],
                        },
                    },
                },
                "required": ["portfolio_value", "daily_pnl", "open_alerts", "reconciliation_status", "top_movers"],
            }
        },
        "required": ["data_sources"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "briefing_text":  {"type": "string"},
            "severity":       {"type": "string", "enum": ["routine", "attention", "urgent"]},
            "key_metrics":    {"type": "object"},
            "action_items":   {"type": "array"},
            "status":         {"type": "string"},
            "timestamp":      {"type": "string"},
        },
        "required": ["briefing_text", "severity", "key_metrics", "action_items", "status", "timestamp"],
    },
}


def _fmt_usd(value: float) -> str:
    """Format a USD value with sign and comma separation.

    Args:
        value: Dollar amount (may be negative).

    Returns:
        Formatted string, e.g. "+$1,234,567.89" or "-$50,000.00".
    """
    sign: str = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"


def _fmt_pct(value: float) -> str:
    """Format a percentage with sign.

    Args:
        value: Percentage value.

    Returns:
        Formatted string, e.g. "+3.24%" or "-1.50%".
    """
    sign: str = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def _determine_severity(
    alert_count: int,
    pnl: float,
    portfolio_value: float,
    reconciliation_status: str,
) -> str:
    """Determine overall briefing severity.

    Rules (first match wins):
        - urgent:    >3 alerts OR P&L loss exceeds 5% of portfolio OR recon failed.
        - attention: 1–3 alerts OR P&L loss 1–5% OR recon status not "clean".
        - routine:   No alerts, minimal loss, clean reconciliation.

    Args:
        alert_count: Number of open operational alerts.
        pnl: Daily P&L in USD (negative = loss).
        portfolio_value: Current portfolio value in USD.
        reconciliation_status: Reconciliation status string.

    Returns:
        "routine", "attention", or "urgent".
    """
    pnl_pct: float = (pnl / portfolio_value * 100.0) if portfolio_value > 0 else 0.0
    recon_lower: str = reconciliation_status.lower()

    if (
        alert_count > 3
        or pnl_pct < -5.0
        or "fail" in recon_lower
        or "error" in recon_lower
        or "critical" in recon_lower
    ):
        return "urgent"

    if (
        alert_count > 0
        or pnl_pct < -1.0
        or recon_lower not in ("clean", "ok", "reconciled", "complete", "passed")
    ):
        return "attention"

    return "routine"


def thunder_executive_briefing(data_sources: dict[str, Any]) -> dict[str, Any]:
    """Generate Thunder's daily executive briefing from aggregated data sources.

    Produces a professional, no-fluff situational summary covering:
    - Portfolio snapshot and daily P&L
    - Operational alerts requiring attention
    - Reconciliation health
    - Top-moving assets (gainers and losers)
    - Action items derived from the above

    Args:
        data_sources: Aggregated operational data with keys:
            - portfolio_value (float): Total portfolio value in USD.
            - daily_pnl (float): Day's profit/loss in USD (negative = loss).
            - open_alerts (list[str]): Active operational alert messages.
            - reconciliation_status (str): Current fund reconciliation status.
            - top_movers (list[dict]): List of {asset, change_pct} for notable movers.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - briefing_text (str): Human-readable briefing in Thunder's preferred style.
            - severity (str): "routine", "attention", or "urgent".
            - key_metrics (dict): Structured data for downstream consumption.
            - action_items (list[str]): Prioritised list of required actions.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        portfolio_value: float = float(data_sources.get("portfolio_value", 0.0))
        daily_pnl: float = float(data_sources.get("daily_pnl", 0.0))
        open_alerts: list[str] = list(data_sources.get("open_alerts", []))
        reconciliation_status: str = str(data_sources.get("reconciliation_status", "unknown"))
        top_movers: list[dict[str, Any]] = list(data_sources.get("top_movers", []))

        pnl_pct: float = (daily_pnl / portfolio_value * 100.0) if portfolio_value > 0 else 0.0
        alert_count: int = len(open_alerts)

        severity: str = _determine_severity(alert_count, daily_pnl, portfolio_value, reconciliation_status)
        severity_prefix: dict[str, str] = {
            "routine":   "DAILY BRIEFING",
            "attention": "BRIEFING — ATTENTION REQUIRED",
            "urgent":    "BRIEFING — URGENT",
        }

        date_str: str = now_utc.strftime("%B %d, %Y %H:%M UTC")

        # --- Movers section ---
        gainers: list[dict[str, Any]] = sorted(
            [m for m in top_movers if m.get("change_pct", 0.0) > 0],
            key=lambda x: x["change_pct"],
            reverse=True,
        )
        losers: list[dict[str, Any]] = sorted(
            [m for m in top_movers if m.get("change_pct", 0.0) <= 0],
            key=lambda x: x["change_pct"],
        )

        movers_lines: list[str] = []
        if gainers:
            movers_lines.append(
                "Gainers: "
                + ", ".join(f"{m['asset']} {_fmt_pct(m['change_pct'])}" for m in gainers[:3])
            )
        if losers:
            movers_lines.append(
                "Losers:  "
                + ", ".join(f"{m['asset']} {_fmt_pct(m['change_pct'])}" for m in losers[:3])
            )
        movers_section: str = "\n  ".join(movers_lines) if movers_lines else "No significant movers today."

        # --- Alerts section ---
        if alert_count == 0:
            alerts_section: str = "No open alerts."
        else:
            alerts_section = f"{alert_count} open alert(s):\n" + "\n".join(
                f"  [{i+1}] {alert}" for i, alert in enumerate(open_alerts)
            )

        # --- Build briefing text ---
        briefing_text: str = (
            f"{severity_prefix[severity]}\n"
            f"{date_str}\n"
            f"{'─' * 50}\n\n"
            f"PORTFOLIO SNAPSHOT\n"
            f"  Value:        ${portfolio_value:,.2f}\n"
            f"  Daily P&L:    {_fmt_usd(daily_pnl)}  ({_fmt_pct(pnl_pct)})\n\n"
            f"RECONCILIATION\n"
            f"  Status:       {reconciliation_status}\n\n"
            f"ALERTS\n"
            f"  {alerts_section}\n\n"
            f"MARKET MOVERS\n"
            f"  {movers_section}\n"
        )

        # --- Action items ---
        action_items: list[str] = []

        if severity == "urgent":
            action_items.append("URGENT: Review and resolve all open alerts immediately.")
        elif alert_count > 0:
            action_items.append(f"Review {alert_count} open alert(s) before end of day.")

        if "fail" in reconciliation_status.lower() or "error" in reconciliation_status.lower():
            action_items.append("Reconciliation failure detected — escalate to fund accounting team.")
        elif reconciliation_status.lower() not in ("clean", "ok", "reconciled", "complete", "passed"):
            action_items.append(f"Reconciliation status is '{reconciliation_status}' — verify manually.")

        if daily_pnl < 0 and abs(pnl_pct) >= 3.0:
            action_items.append(
                f"Significant P&L loss ({_fmt_pct(pnl_pct)}) — review positions and risk limits."
            )

        if not action_items:
            action_items.append("No immediate actions required. Monitor intraday for changes.")

        key_metrics: dict[str, Any] = {
            "portfolio_value_usd":  portfolio_value,
            "daily_pnl_usd":        daily_pnl,
            "daily_pnl_pct":        round(pnl_pct, 4),
            "open_alert_count":     alert_count,
            "reconciliation_status": reconciliation_status,
            "top_gainer":           gainers[0] if gainers else None,
            "top_loser":            losers[0] if losers else None,
            "severity":             severity,
        }

        return {
            "status":        "success",
            "briefing_text": briefing_text,
            "severity":      severity,
            "key_metrics":   key_metrics,
            "action_items":  action_items,
            "timestamp":     now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"thunder_executive_briefing failed: {e}")
        _log_lesson(f"thunder_executive_briefing: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
