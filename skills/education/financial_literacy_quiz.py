"""Provide goodwill financial literacy quizzes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

_BUDGETING = [
    ("What is the 50/30/20 rule used for?", ["Allocating investments", "Balancing a monthly budget", "Setting interest rates", "Determining credit scores"], 1, "50% needs, 30% wants, 20% savings/debt"),
    ("Which expense is a fixed cost?", ["Streaming services", "Groceries", "Rent", "Ride sharing"], 2, "Rent payments stay consistent"),
    ("An emergency fund should cover?", ["One week", "One month", "3-6 months", "Two years"], 2, "Aim for at least 3 months"),
    ("Zero-based budgeting means?", ["Spending zero", "Assigning every dollar a job", "Only cash envelopes", "No tracking"], 1, "Income minus expenses equals zero"),
    ("Which category is a want?", ["Insurance", "Groceries", "Streaming", "Rent"], 2, "Subscriptions are discretionary"),
    ("Why track variable expenses?", ["Lower taxes", "Reduce surprises", "Improve credit", "Earn rewards"], 1, "Helps avoid overspending"),
    ("Debt snowball prioritizes?", ["Lowest balance", "Highest interest", "Oldest debt", "Secured loans"], 0, "Focus on quick wins"),
    ("Cash flow is?", ["Net worth", "Money in minus out", "Credit limit", "Salary"], 1, "Shows spending power"),
    ("Sinking funds help with?", ["Random windfalls", "Planned irregular costs", "Retirement", "Taxes"], 1, "Save ahead for predictable expenses"),
    ("Envelope method enforces?", ["Digital tracking", "Spending caps", "Investment goals", "Tax filing"], 1, "Once envelope is empty, stop spending"),
]

_INVESTING = [
    ("Diversification helps reduce what?", ["Taxes", "Inflation", "Risk", "Time"], 2, "Spreading holdings lowers risk"),
    ("An index fund typically aims to?", ["Beat market", "Match benchmark", "Guarantee gains", "Hold bonds"], 1, "Follows an index"),
    ("Compound interest means?", ["Interest on principal only", "Interest on interest", "Only annual", "Simple growth"], 1, "Earn on previous earnings"),
    ("Dollar-cost averaging does what?", ["Times the market", "Invests equal amounts regularly", "Shorts stocks", "Eliminates risk"], 1, "Reduces timing risk"),
    ("Bonds generally offer?", ["Highest risk", "Ownership", "Fixed income", "Crypto exposure"], 2, "They pay periodic interest"),
    ("What’s ETF stand for?", ["Equity Trust Fund", "Exchange-Traded Fund", "Extended Tax Fund", "Energy Trade Fund"], 1, "Funds that trade like stocks"),
    ("Risk tolerance measures?", ["Return", "Age", "Ability to handle volatility", "Dividends"], 2, "Emotional + financial capacity"),
    ("Rebalancing means?", ["Selling all", "Restoring target allocations", "Timing the market", "Avoiding taxes"], 1, "Keeps risk level in check"),
    ("What is beta?", ["Dividend", "Volatility vs market", "Bond yield", "Alpha"], 1, "Measures relative volatility"),
    ("ESG investing considers?", ["Only profits", "Environmental, social, governance factors", "Lottery odds", "Short squeezes"], 1, "Values-based screens"),
]

_GENERAL = [
    ("What does APR stand for?", ["Annual Percentage Rate", "Average Price Ratio", "Active Payment Rate", "Adjusted Portfolio Return"], 0, "Annualized cost of borrowing"),
    ("Emergency fund size?", ["1", "2", "3-6", "12"], 2, "3-6 months recommended"),
    ("Credit utilization ideally below?", ["10%", "30%", "60%", "90%"], 1, "Staying under 30% aids scores"),
    ("Net worth formula?", ["Assets - liabilities", "Income - taxes", "Budget - spend", "Cash + debt"], 0, "What you own minus owe"),
    ("FDIC insurance covers?", ["Stocks", "Crypto", "Bank deposits", "Gold"], 2, "Deposits up to limits"),
    ("Simple interest calculates on?", ["Principal", "Interest", "Fees", "Bonuses"], 0, "Principal only"),
    ("What is inflation?", ["Falling prices", "Rising prices", "Currency peg", "Tax hike"], 1, "Costs trend upward"),
    ("Why monitor credit reports?", ["Entertainment", "Fraud detection", "Travel", "Weather"], 1, "Catches errors"),
    ("Gross pay vs net pay difference?", ["Bonuses", "Taxes and deductions", "Company match", "Retirement"], 1, "Net is take-home"),
    ("What is liquidity?", ["Profit", "Ease of converting to cash", "Loss", "Budget"], 1, "High liquidity = easy access"),
]

_TAXES = [
    ("W-4 form tells employers?", ["Where you live", "How much tax to withhold", "Health plan", "Investments"], 1, "Guides withholding"),
    ("Standard deduction is?", ["Tax credit", "Flat amount reducing taxable income", "Refund", "Penalty"], 1, "Reduces income"),
    ("Self-employed must pay?", ["VAT", "Self-employment tax", "Luxury tax", "Tariffs"], 1, "Covers Social Security & Medicare"),
    ("Capital gains apply when?", ["Earning interest", "Selling assets for profit", "Receiving salary", "Buying bonds"], 1, "Tax on appreciated assets"),
    ("Estimated taxes due?", ["Monthly", "Quarterly", "Annually", "Never"], 1, "Quarterly for many"),
    ("1099 forms report?", ["Wages", "Interest/dividends", "Property tax", "Mortgage"], 1, "Non-W-2 income"),
    ("Tax credits do what?", ["Reduce taxable income", "Directly lower owed tax", "Raise refunds", "Eliminate audits"], 1, "Dollar-for-dollar reduction"),
    ("Filing extension delays?", ["Tax payments", "Paperwork only", "Audits", "Penalties forever"], 1, "Payments still due"),
    ("HSA contributions are?", ["Taxable", "Pretax", "Penalized", "Mandatory"], 1, "Pretax with qualified expenses"),
    ("Crypto trades may trigger?", ["Capital gains", "Property tax", "Payroll tax", "Estate tax"], 0, "IRS treats as property"),
]

_CRYPTO = [
    ("Seed phrase best practice?", ["Share with friends", "Store offline", "Email it", "Tweet it"], 1, "Keep offline and secure"),
    ("Gas fees pay for?", ["Marketing", "Network validators", "Developers", "Taxes"], 1, "Compensate validators"),
    ("What is DeFi?", ["Traditional banking", "Decentralized finance", "Fiat exchange", "Stock market"], 1, "Financial services on-chain"),
    ("Liquidity pool purpose?", ["Hold fiat", "Provide tokens for swaps", "Print NFTs", "Mine BTC"], 1, "Enables AMMs"),
    ("Impermanent loss occurs when?", ["No trades", "Price diverges from deposit", "Gas zero", "Wallet lost"], 1, "Pool tokens shift vs market"),
    ("Staking rewards come from?", ["Validators", "Credit cards", "Banks", "Retailers"], 0, "Validators share fees"),
    ("Smart contracts are?", ["PDFs", "Self-executing code", "Human lawyers", "Phone apps"], 1, "Programs on-chain"),
    ("Bridge risk includes?", ["Exchange rate", "Security exploits", "Sales tax", "Dividends"], 1, "Cross-chain bridges get hacked"),
    ("What is MEV?", ["Minor error value", "Miner/Maximum extractable value", "Multi equity valuation", "Market entry variance"], 1, "Value extracted from ordering"),
    ("Hot wallet example?", ["Hardware device", "Exchange app", "Paper key", "Vault"], 1, "Connected to internet"),
]

QUESTION_BANK = {
    "budgeting": _BUDGETING,
    "investing": _INVESTING,
    "general": _GENERAL,
    "taxes": _TAXES,
    "crypto": _CRYPTO,
}

TOOL_META: dict[str, Any] = {
    "name": "financial_literacy_quiz",
    "description": "Provides educational quizzes for goodwill content.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "difficulty": {
                "type": "string",
                "enum": ["beginner", "intermediate", "advanced"],
            },
            "topic": {
                "type": "string",
                "enum": ["budgeting", "investing", "taxes", "crypto", "general"],
            },
            "num_questions": {"type": "integer", "default": 5},
        },
        "required": ["difficulty"],
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


def financial_literacy_quiz(
    difficulty: str,
    topic: str | None = None,
    num_questions: int = 5,
    **_: Any,
) -> dict[str, Any]:
    """Return a set of quiz questions for goodwill education."""
    try:
        topic = topic or "general"
        bank = QUESTION_BANK.get(topic, QUESTION_BANK["general"])
        selected = bank[: num_questions or len(bank)]
        questions = [
            {
                "question": item["question"],
                "options": item["options"],
                "correct_answer_index": item["answer"],
                "explanation": item["explanation"],
            }
            for item in selected
        ]
        data = {"questions": questions}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("financial_literacy_quiz", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
