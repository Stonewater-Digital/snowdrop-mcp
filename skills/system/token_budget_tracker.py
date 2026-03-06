class TokenBudgetExceededError(Exception):
    """Exception raised when a token budget is exceeded."""
    pass

class TokenBudgetTracker:
    def __init__(self, reasoning_budget: int = 50000, execution_budget: int = 50000):
        self.reasoning_budget = reasoning_budget
        self.execution_budget = execution_budget
        self.reasoning_used = 0
        self.execution_used = 0

    @property
    def total_used(self) -> int:
        return self.reasoning_used + self.execution_used

    def add_reasoning_tokens(self, amount: int) -> None:
        """Add tokens to reasoning usage and check budget."""
        if self.reasoning_used + amount > self.reasoning_budget:
            raise TokenBudgetExceededError(f"Reasoning budget exceeded. Used {self.reasoning_used}, attempted to add {amount}, limit {self.reasoning_budget}.")
        self.reasoning_used += amount

    def add_execution_tokens(self, amount: int) -> None:
        """Add tokens to execution usage and check budget."""
        if self.execution_used + amount > self.execution_budget:
            raise TokenBudgetExceededError(f"Execution budget exceeded. Used {self.execution_used}, attempted to add {amount}, limit {self.execution_budget}.")
        self.execution_used += amount

    def reset(self) -> None:
        """Reset token usage for a new task."""
        self.reasoning_used = 0
        self.execution_used = 0
