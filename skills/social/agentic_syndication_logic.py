"""
Executive Summary: Trusted-bot syndicate formation engine — filters, skill-matches, and cost-optimizes a roster of candidate agents to assemble a mission-capable team within budget.
Inputs: mission (dict: objective, required_skills (list), min_trust_score, budget), candidates (list[dict: agent_id, skills (list), trust_score, hourly_rate, availability (bool)])
Outputs: syndicate (list of selected agents with role assignments), total_cost (float), skill_coverage_pct (float), formation_viable (bool)
MCP Tool Name: agentic_syndication_logic
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "agentic_syndication_logic",
    "description": "Assembles an optimal bot syndicate for a given mission by filtering candidates on availability and trust, matching skills to requirements, and minimizing cost while maximizing skill coverage.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "mission": {
                "type": "object",
                "description": (
                    "Dict with: objective (str), required_skills (list[str]), "
                    "min_trust_score (float), budget (float in USD)."
                ),
            },
            "candidates": {
                "type": "array",
                "description": (
                    "List of candidate agent dicts with: agent_id (str), "
                    "skills (list[str]), trust_score (float), hourly_rate (float), "
                    "availability (bool)."
                ),
                "items": {"type": "object"},
            },
        },
        "required": ["mission", "candidates"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "syndicate": {"type": "array"},
            "total_cost": {"type": "number"},
            "skill_coverage_pct": {"type": "number"},
            "formation_viable": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Assume 8-hour engagement period for total cost calculation
ENGAGEMENT_HOURS = 8.0


def _skill_coverage(covered: set[str], required: list[str]) -> float:
    """Calculate percentage of required skills covered.

    Args:
        covered: Set of skills provided by the current syndicate.
        required: List of required skill strings.

    Returns:
        Coverage percentage 0.0-100.0.
    """
    if not required:
        return 100.0
    return round(len(covered.intersection(required)) / len(required) * 100, 2)


def _assign_role(agent_skills: list[str], required_skills: list[str]) -> str:
    """Determine a human-readable role for an agent based on skill overlap.

    Args:
        agent_skills: Skills the agent possesses.
        required_skills: Skills needed by the mission.

    Returns:
        Role label string.
    """
    matched = [s for s in agent_skills if s in required_skills]
    if not matched:
        return "support"
    if len(matched) >= 3:
        return "lead"
    return f"specialist:{matched[0]}"


def _greedy_select(
    eligible: list[dict],
    required_skills: list[str],
    budget: float,
) -> tuple[list[dict], float, set[str]]:
    """Greedy cost-optimal selection maximizing skill coverage within budget.

    Strategy:
        1. Sort eligible candidates by cost-per-unique-new-skill (ascending).
        2. Add candidates that contribute at least one new required skill first.
        3. If budget remains and coverage is incomplete, add cheapest remaining.

    Args:
        eligible: Pre-filtered list of candidate dicts.
        required_skills: Required skill list from the mission.
        budget: Total budget in USD.

    Returns:
        Tuple of (selected_agents list, total_cost float, covered_skills set).
    """
    required_set = set(required_skills)
    covered: set[str] = set()
    selected: list[dict] = []
    remaining_budget = budget
    total_cost = 0.0

    # Sort by hourly rate ascending (cheapest first within skill-contributing candidates)
    def contribution_key(c: dict) -> tuple[int, float]:
        agent_skills = set(c.get("skills", []))
        new_skills = len(agent_skills.intersection(required_set) - covered)
        rate = float(c.get("hourly_rate", 999999))
        # Negative new_skills so that agents with more new coverage come first
        return (-new_skills, rate)

    pool = sorted(eligible, key=contribution_key)

    for candidate in pool:
        agent_cost = float(candidate.get("hourly_rate", 0)) * ENGAGEMENT_HOURS
        if agent_cost > remaining_budget:
            continue  # Can't afford this agent
        agent_skills = set(candidate.get("skills", []))
        new_skills_added = agent_skills.intersection(required_set) - covered
        # Always add if they contribute new skills
        if new_skills_added or not covered:
            covered.update(agent_skills.intersection(required_set))
            selected.append(candidate)
            total_cost += agent_cost
            remaining_budget -= agent_cost

        # Stop if full coverage achieved
        if covered >= required_set:
            break

    return selected, round(total_cost, 2), covered


def agentic_syndication_logic(
    mission: dict,
    candidates: list[dict],
    **kwargs: Any,
) -> dict:
    """Form an optimal bot syndicate for a given mission within budget.

    Workflow:
        1. Filter candidates by availability=True and trust_score >= min_trust_score.
        2. Run greedy cost-optimal selection maximizing required skill coverage.
        3. Assign roles to each selected agent based on skill overlap.
        4. Report viability (all required skills covered and within budget).

    Args:
        mission: Dict with:
            objective (str): Mission description.
            required_skills (list[str]): Skills the syndicate must collectively have.
            min_trust_score (float): Minimum acceptable trust score.
            budget (float): Maximum total spend in USD.
        candidates: List of candidate agent dicts, each with:
            agent_id (str): Unique identifier.
            skills (list[str]): Skills the agent possesses.
            trust_score (float): Trust score 0-100.
            hourly_rate (float): Cost per hour in USD.
            availability (bool): Whether the agent is currently available.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            syndicate (list[dict]): Selected agents with role assignments.
            total_cost (float): Estimated total cost for the engagement.
            skill_coverage_pct (float): Percentage of required skills covered.
            uncovered_skills (list[str]): Required skills not covered.
            formation_viable (bool): True if all skills covered and within budget.
            eligible_candidate_count (int): Candidates passing initial filters.
            rejected_count (int): Candidates filtered out.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        objective = mission.get("objective", "")
        required_skills: list[str] = mission.get("required_skills", [])
        min_trust = float(mission.get("min_trust_score", 70.0))
        budget = float(mission.get("budget", 0.0))

        # Step 1: Filter
        eligible = [
            c for c in candidates
            if c.get("availability", False)
            and float(c.get("trust_score", 0)) >= min_trust
        ]
        rejected_count = len(candidates) - len(eligible)

        if not eligible:
            return {
                "status": "success",
                "objective": objective,
                "syndicate": [],
                "total_cost": 0.0,
                "skill_coverage_pct": 0.0,
                "uncovered_skills": required_skills,
                "formation_viable": False,
                "eligible_candidate_count": 0,
                "rejected_count": rejected_count,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Step 2: Greedy selection
        selected, total_cost, covered = _greedy_select(eligible, required_skills, budget)

        # Step 3: Assign roles
        syndicate: list[dict] = []
        for agent in selected:
            role = _assign_role(
                agent.get("skills", []),
                required_skills,
            )
            syndicate.append({
                "agent_id": agent.get("agent_id"),
                "trust_score": agent.get("trust_score"),
                "skills": agent.get("skills", []),
                "hourly_rate": agent.get("hourly_rate"),
                "estimated_cost": round(float(agent.get("hourly_rate", 0)) * ENGAGEMENT_HOURS, 2),
                "role": role,
            })

        # Step 4: Viability
        required_set = set(required_skills)
        uncovered = list(required_set - covered)
        skill_coverage_pct = _skill_coverage(covered, required_skills)
        formation_viable = len(uncovered) == 0 and total_cost <= budget

        return {
            "status": "success",
            "objective": objective,
            "syndicate": syndicate,
            "total_cost": total_cost,
            "budget": budget,
            "budget_remaining": round(budget - total_cost, 2),
            "skill_coverage_pct": skill_coverage_pct,
            "uncovered_skills": uncovered,
            "formation_viable": formation_viable,
            "eligible_candidate_count": len(eligible),
            "rejected_count": rejected_count,
            "engagement_hours": ENGAGEMENT_HOURS,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"agentic_syndication_logic failed: {e}")
        _log_lesson(f"agentic_syndication_logic: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to logs/lessons.md.

    Args:
        message: Description of the error or lesson.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
