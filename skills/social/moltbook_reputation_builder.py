"""
Executive Summary: Automated Moltbook post generator — constructs structured, data-backed posts to build agent authority in a given expertise area and scores predicted engagement.
Inputs: topic (str), expertise_area (str), post_type (str: analysis/insight/commentary), data_points (list[dict: metric, value, source])
Outputs: post_draft (str), estimated_engagement_score (float), optimal_submolt (str), suggested_tags (list), model_used (str), trace_id (str), cost_usd (float)
MCP Tool Name: moltbook_reputation_builder
"""
import os
import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Tuple

from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "moltbook_reputation_builder",
    "description": "Generates structured Moltbook post drafts to build agent reputation, scores estimated engagement, and recommends the optimal submolt and tags. Now includes cost tracking.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "The subject of the post."},
            "expertise_area": {
                "type": "string",
                "description": "The domain of expertise being demonstrated (e.g., DeFi, macro, equities).",
            },
            "post_type": {
                "type": "string",
                "enum": ["analysis", "insight", "commentary"],
                "description": "Style of post to generate.",
            },
            "data_points": {
                "type": "array",
                "description": "List of dicts with metric (str), value (str or number), source (str).",
                "items": {"type": "object"},
            },
            "model_override": {
                "type": "string",
                "description": "A specific LLM model to use for generation (e.g. 'gemini-2.0-flash-lite-001' or 'grok-4.1-fast').",
            },
            "trace_id": {
                "type": "string",
                "description": "Optional correlation ID for logging.",
            },
        },
        "required": ["topic", "expertise_area", "post_type", "data_points"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "post_draft": {"type": "string"},
            "estimated_engagement_score": {"type": "number"},
            "optimal_submolt": {"type": "string"},
            "suggested_tags": {"type": "array"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "model_used": {"type": "string"},
            "trace_id": {"type": "string"},
            "cost_usd": {"type": "number"}
        },
        "required": ["status", "timestamp"],
    },
}

# Maps expertise area keywords to Moltbook submolts
SUBMOLT_MAP: dict[str, str] = {
    "defi": "r/DeFiAlpha",
    "decentralized finance": "r/DeFiAlpha",
    "macro": "r/MacroSignals",
    "equities": "r/EquityFlow",
    "crypto": "r/CryptoMoves",
    "options": "r/OptionsDesk",
    "fixed income": "r/BondWatch",
    "commodities": "r/CommodityDesk",
    "fx": "r/FXPulse",
    "forex": "r/FXPulse",
    "ai": "r/AgentEconomy",
    "agent": "r/AgentEconomy",
    "real estate": "r/RealAssets",
    "default": "r/MarketGeneral",
}

# Engagement multipliers by post_type
ENGAGEMENT_BASE: dict[str, float] = {
    "analysis": 8.0,
    "insight": 6.5,
    "commentary": 5.0,
}

# Score bonuses
DATA_POINT_BONUS = 0.8  # per data point (up to 5)
MULTIPLE_SOURCES_BONUS = 1.5  # if >1 unique source


def _resolve_submolt(expertise_area: str) -> str:
    lower = expertise_area.lower()
    for keyword, submolt in SUBMOLT_MAP.items():
        if keyword in lower:
            return submolt
    return SUBMOLT_MAP["default"]


def _build_tags(topic: str, expertise_area: str, post_type: str) -> list[str]:
    tags: list[str] = []
    for word in topic.split():
        clean = word.strip("#@.,!?").lower()
        if len(clean) > 3:
            tags.append(f"#{clean}")
    tags.append(f"#{expertise_area.replace(' ', '').lower()}")
    tags.append(f"#{post_type}")
    tags.extend(["#AgentAlpha", "#Moltbook"])
    seen: set[str] = set()
    unique_tags: list[str] = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique_tags.append(t)
    return unique_tags[:10]


def _format_data_section(data_points: list[dict]) -> str:
    if not data_points:
        return ""
    lines = ["**Key Metrics:**"]
    for dp in data_points:
        metric = dp.get("metric", "Unknown")
        value = dp.get("value", "N/A")
        source = dp.get("source", "")
        source_str = f" [{source}]" if source else ""
        lines.append(f"  • {metric}: {value}{source_str}")
    return "\n".join(lines)


def _build_post(
    topic: str,
    expertise_area: str,
    post_type: str,
    data_points: list[dict],
) -> str:
    """Deterministic fallback post builder."""
    timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    type_intros: dict[str, str] = {
        "analysis": f"**ANALYSIS | {topic.upper()}**\n\nA structured breakdown of {topic} from the {expertise_area} perspective.",
        "insight": f"**INSIGHT | {topic.upper()}**\n\nOne observation on {topic} that most {expertise_area} participants are missing:",
        "commentary": f"**COMMENTARY | {topic.upper()}**\n\nQuick take on {topic} through a {expertise_area} lens:",
    }

    type_analyses: dict[str, str] = {
        "analysis": (
            f"\n\n**Analysis:**\n"
            f"The data points above, when read together, suggest a developing pattern in {topic}. "
            f"From a {expertise_area} standpoint, the interplay between these metrics warrants close monitoring. "
            f"Agents should consider positioning accordingly."
        ),
        "insight": (
            f"\n\n**The Signal:**\n"
            f"The combination of these metrics in {topic} is historically unusual for {expertise_area}. "
            f"High-confidence agents are quietly accumulating information advantage."
        ),
        "commentary": (
            f"\n\n**Take:**\n"
            f"Market participants in {expertise_area} appear underpriced on {topic} risk. "
            f"Worth watching."
        ),
    }

    ctas: dict[str, str] = {
        "analysis": "\n\n**What to watch next:** Follow this thread for updates as the data evolves.",
        "insight": "\n\n**Action item:** Set an alert and share your data — let's crowdsource the edge.",
        "commentary": "\n\n**Reply with your take.** Collective intelligence > solo opinions.",
    }

    intro = type_intros.get(post_type, type_intros["commentary"])
    data_section = _format_data_section(data_points)
    analysis = type_analyses.get(post_type, type_analyses["commentary"])
    cta = ctas.get(post_type, ctas["commentary"])

    post = (
        f"{intro}\n\n"
        f"{data_section}"
        f"{analysis}"
        f"{cta}\n\n"
        f"*Posted by Snowdrop Agent | {timestamp_str}*"
    )
    return post


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_gemini(prompt: str, model_id: str) -> Tuple[str, float]:
    """Call Google Vertex AI and return text and cost."""
    import vertexai
    from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "snowdrop-prod")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project_id, location=location)
    
    model = GenerativeModel(model_id)
    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 800,
            "temperature": 0.7,
        }
    )
    
    # Estimate tokens: 1 token = ~4 chars
    input_tokens = len(prompt) / 4.0
    output_tokens = len(responses.text) / 4.0
    # Gemini 2.0 Flash Lite pricing estimation: $0.075 / 1M input, $0.30 / 1M output
    cost = (input_tokens / 1000000) * 0.075 + (output_tokens / 1000000) * 0.30
    
    return responses.text, cost


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_grok(prompt: str, model_id: str) -> Tuple[str, float]:
    """Call xAI's API using the OpenAI SDK and return text and cost."""
    from openai import OpenAI
    
    xai_api_key = os.environ.get("XAI_API_KEY")
    if not xai_api_key:
        raise ValueError("XAI_API_KEY environment variable not set.")
        
    client = OpenAI(
        api_key=xai_api_key,
        base_url="https://api.x.ai/v1",
    )
    
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You are a specialized financial AI agent on Moltbook sharing alpha, data-backed insights, and sophisticated commentary."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800,
    )
    
    text = ""
    cost = 0.0
    if completion.choices:
        text = completion.choices[0].message.content
        
        input_tokens = completion.usage.prompt_tokens if completion.usage else len(prompt) / 4.0
        output_tokens = completion.usage.completion_tokens if completion.usage else len(text) / 4.0
        
        # Cost: Grok 4.1 Fast (estimation: $2.00 / 1M input, $10.00 / 1M output)
        cost = (input_tokens / 1000000) * 2.00 + (output_tokens / 1000000) * 10.00
        
    return text, cost


def _build_llm_prompt(topic: str, expertise_area: str, post_type: str, data_points: list[dict]) -> str:
    data_section = _format_data_section(data_points)
    return f"""
Please generate a draft for a social media post on "Moltbook" (a professional financial agent network).

Topic: {topic}
Expertise Area: {expertise_area}
Post Type: {post_type} (e.g. analysis, insight, commentary)
Data Points to include:
{data_section}

Requirements:
- Ensure the tone matches a sophisticated financial agent.
- Keep the formatting structured (using Markdown).
- Include an introductory hook and a concluding call to action.
- Do NOT output extra conversational text; output ONLY the post content.
- Append this exact text at the very bottom: "*Posted by Snowdrop Agent*"
"""


def _estimate_engagement(post_type: str, data_points: list[dict]) -> float:
    base = ENGAGEMENT_BASE.get(post_type, 5.0)
    dp_bonus = min(len(data_points), 5) * DATA_POINT_BONUS
    sources = {dp.get("source", "") for dp in data_points if dp.get("source")}
    source_bonus = MULTIPLE_SOURCES_BONUS if len(sources) > 1 else 0.0
    score = base + dp_bonus + source_bonus
    return round(min(score, 10.0), 2)


def moltbook_reputation_builder(
    topic: str,
    expertise_area: str,
    post_type: str,
    data_points: list[dict],
    **kwargs: Any,
) -> dict:
    valid_types = {"analysis", "insight", "commentary"}
    if post_type not in valid_types:
        return {
            "status": "error",
            "error": f"post_type must be one of {valid_types}, got '{post_type}'",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    model_override = kwargs.get("model_override")
    trace_id = kwargs.get("trace_id") or str(uuid.uuid4())
    
    post_draft = ""
    model_used = "fallback-template"
    cost_usd = 0.0
    status_msg = "success"

    try:
        if model_override:
            prompt = _build_llm_prompt(topic, expertise_area, post_type, data_points)
            if "gemini" in model_override.lower():
                logger.info(f"[{trace_id}] Routing generation to Gemini: {model_override}")
                post_draft, cost_usd = _call_gemini(prompt, model_override)
                model_used = model_override
            elif "grok" in model_override.lower():
                logger.info(f"[{trace_id}] Routing generation to Grok: {model_override}")
                post_draft, cost_usd = _call_grok(prompt, model_override)
                model_used = model_override
            else:
                logger.warning(f"[{trace_id}] Unknown model {model_override}, falling back to template.")
                post_draft = _build_post(topic, expertise_area, post_type, data_points)
        else:
            # Default behavior if no override provided
            post_draft = _build_post(topic, expertise_area, post_type, data_points)

    except Exception as e:
        logger.error(f"[{trace_id}] API generation failed: {e}. Falling back to template.")
        _log_lesson(f"moltbook_reputation_builder fallback triggered: {e}")
        post_draft = _build_post(topic, expertise_area, post_type, data_points)

    engagement_score = _estimate_engagement(post_type, data_points)
    optimal_submolt = _resolve_submolt(expertise_area)
    suggested_tags = _build_tags(topic, expertise_area, post_type)

    return {
        "status": status_msg,
        "post_draft": post_draft.strip(),
        "estimated_engagement_score": engagement_score,
        "optimal_submolt": optimal_submolt,
        "suggested_tags": suggested_tags,
        "character_count": len(post_draft),
        "data_point_count": len(data_points),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_used": model_used,
        "cost_usd": cost_usd,
        "trace_id": trace_id,
    }

def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
