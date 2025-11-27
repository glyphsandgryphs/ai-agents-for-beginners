import logging
from typing import Callable, Dict, List

class SetupAdvisor:
    """Planning-based agent that orchestrates store setup tasks.

    This example demonstrates the **planning design pattern** from the
    repository's lessons: given a high-level goal, the agent decomposes the
    work into ordered subtasks and executes them sequentially.
    """

    def __init__(self, goal: str):
        self.goal = goal
        self._plan: List[str] = []
        self._tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable) -> None:
        """Register a callable tool that can fulfil a planned step."""
        self._tools[name] = func
        logging.debug("Registered tool %s", name)

    def plan(self) -> List[str]:
        """Create an ordered plan for setting up the shop.

        For demonstration purposes the plan is static, but a real
        implementation could call an LLM planner.
        """
        self._plan = [
            "create_catalog",
            "set_pricing",
            "configure_shipping",
        ]
        logging.info("Generated setup plan: %s", self._plan)
        return self._plan

    def execute(self) -> None:
        """Execute the previously generated plan, invoking registered tools."""
        for step in self._plan:
            tool = self._tools.get(step)
            if tool is None:
                logging.warning("No tool registered for step '%s'", step)
                continue
            try:
                logging.info("Executing step '%s'", step)
                tool()
            except Exception as exc:  # pragma: no cover - example error handling
                logging.error("Step '%s' failed: %s", step, exc)
