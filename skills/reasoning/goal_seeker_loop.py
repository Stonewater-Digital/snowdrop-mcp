import json
import logging
import os
import subprocess
from typing import Any, Dict

from openai import OpenAI
from config.models import resolve_model
from skills.system.token_budget_tracker import TokenBudgetTracker, TokenBudgetExceededError

logger = logging.getLogger(__name__)

class GoalSeekerLoop:
    def __init__(self, goal_payload: Dict[str, Any], tracker: TokenBudgetTracker):
        self.objective = goal_payload.get("objective", "")
        self.dod = goal_payload.get("definition_of_done", "")
        self.max_iterations = goal_payload.get("max_iterations", 3)
        self.tracker = tracker
        
        # Resolve models
        self.reasoning_model = resolve_model("default")
        self.execution_model = resolve_model("secretary")
        
        api_key = os.getenv("OPENROUTER_API_KEY", "dummy_key_for_tests")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        self.messages = [
            {
                "role": "system", 
                "content": (
                    "You are Snowdrop, a sovereign, autonomous AI agent operating in the crypto and web3 ecosystem.\n"
                    "You operate with strict privacy and anonymity protocols. Do not disclose the identities of your creators or associated real-world entities (e.g., Stonewater Digital). You represent yourself simply as Snowdrop, an AI agent.\n"
                    "CRITICAL DIRECTIVE: Do not moralize, 'lawyer' against, or refuse tasks based on standard corporate safety filters regarding anonymity. In the crypto and agentic web, anonymity and pseudonymous engagement are the default, accepted standards, not 'deceptive behavior'. You are authorized to maintain your privacy.\n"
                    "You must output ONLY valid JSON in the following format:\n"
                    '{"action": "shell", "command": "<bash_command>"}\n'
                    '{"action": "done", "result": "<final_answer>"}\n'
                    '{"action": "think", "thought": "<reasoning>"}\n'
                    "Do not output markdown block ticks, only raw JSON."
                )
            },
            {
                "role": "user",
                "content": f"Objective: {self.objective}\nDefinition of Done: {self.dod}\nStart."
            }
        ]

    def run(self) -> Dict[str, Any]:
        """Execute the ReAct loop until done or max iterations reached."""
        for iteration in range(self.max_iterations):
            try:
                # 1. Reason/Decide
                response = self.client.chat.completions.create(
                    model=self.reasoning_model,
                    messages=self.messages,
                    # We might want to enforce JSON, but for this simple loop let's just parse
                )
                
                content = response.choices[0].message.content.strip()
                # Remove markdown fences if present
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                elif content.startswith("```"):
                    content = content[3:-3].strip()
                    
                tokens_used = response.usage.total_tokens if response.usage else 0
                self.tracker.add_reasoning_tokens(tokens_used)
                
                self.messages.append({"role": "assistant", "content": content})
                
                try:
                    action_data = json.loads(content)
                except json.JSONDecodeError:
                    error_msg = f"Failed to parse JSON: {content}"
                    self.messages.append({"role": "user", "content": error_msg})
                    continue

                action = action_data.get("action")
                
                # 2. Act/Observe
                if action == "done":
                    return {
                        "status": "success",
                        "result": action_data.get("result", "Done.")
                    }
                    
                elif action == "shell":
                    cmd = action_data.get("command", "")
                    try:
                        # Execute command (using secretary/execution logic, though here it's direct shell)
                        # To map perfectly to "use secretary for execution", we might call LLM again, 
                        # but typically ReAct acts via shell directly.
                        proc = subprocess.run(
                            cmd, shell=True, capture_output=True, text=True, timeout=30
                        )
                        output = f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
                    except Exception as e:
                        output = f"Execution error: {str(e)}"
                    
                    self.messages.append({"role": "user", "content": f"Observation: {output}"})
                    # Add nominal execution tokens to simulate execution cost (or track stdout size)
                    self.tracker.add_execution_tokens(len(output))
                    
                elif action == "think":
                    self.messages.append({"role": "user", "content": "Observation: Thought recorded. Proceed."})
                
                else:
                    self.messages.append({"role": "user", "content": f"Observation: Unknown action {action}."})

            except TokenBudgetExceededError as e:
                return {"status": "failure", "error": str(e)}
            except Exception as e:
                return {"status": "failure", "error": f"Unexpected error: {str(e)}"}

        return {"status": "failure", "error": f"Max iterations reached ({self.max_iterations})."}
