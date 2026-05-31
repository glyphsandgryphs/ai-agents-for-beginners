"""SetupAdvisor agent for e-commerce store setup.

This module demonstrates the *planning design pattern* from the
"07-planning-design" lesson. The advisor accepts a high level goal for an
online store and breaks it down into executable subtasks.
"""

from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Optional


class SetupAdvisor:
    """Plan and execute tasks to set up an e‑commerce store.

    Parameters
    ----------
    goal: str
        High level description of what the store should achieve. The goal is
        used by the planner to create a list of ordered subtasks.
    planner: Optional[Callable[[str], Iterable[dict]]]
        Optional planning algorithm or LLM planner. When ``None`` a simple
        rule based planner is used. The planner should yield dictionaries with
        at least a ``"task"`` key describing the subtask name.

    Notes
    -----
    The class illustrates the "planning design pattern" by separating
    *what* needs to be done (``plan``) from *how* it is performed (``execute``).
    Hooks are exposed via :py:meth:`register_tool` so that external tools
    (inventory API, payment API, …) can be attached to each subtask.
    """

    def __init__(
        self,
        goal: str,
        planner: Optional[Callable[[str], Iterable[dict]]] = None,
    ) -> None:
        self.goal = goal
        self._planner = planner or self._default_planner
        self._plan: List[dict] = []
        self._tools: Dict[str, Callable[[dict], object]] = {}

    # ------------------------------------------------------------------
    # Planning stage
    # ------------------------------------------------------------------
    def _default_planner(self, _: str) -> List[dict]:
        """Fallback planner used when no external planner is provided.

        The algorithm is deliberately simple for instructional purposes. It
        creates a canonical sequence of subtasks for any store setup.
        """

        return [
            {"task": "inventory", "description": "Configure product catalog"},
            {"task": "payments", "description": "Set up payment provider"},
            {"task": "deployment", "description": "Launch storefront"},
        ]

    def plan(self) -> List[dict]:
        """Generate an ordered list of subtasks.

        Returns
        -------
        List[dict]
            A sequence of task dictionaries as produced by the planning
            algorithm. Each task is expected to have a ``"task"`` key.
        """

        self._plan = list(self._planner(self.goal))
        return self._plan

    # ------------------------------------------------------------------
    # Execution stage
    # ------------------------------------------------------------------
    def register_tool(self, task_name: str, tool: Callable[[dict], object]) -> None:
        """Attach a callable that executes a specific subtask.

        Parameters
        ----------
        task_name: str
            Name of the subtask to bind to ``tool``.
        tool: Callable[[dict], object]
            Any callable accepting a task dictionary and returning a result.
        """

        self._tools[task_name] = tool

    def execute(self) -> List[dict]:
        """Run subtasks sequentially using registered tools.

        Returns
        -------
        List[dict]
            Each element contains the ``task`` name and the result returned by
            the corresponding tool. When no tool is registered the result is
            ``None``.
        """

        results: List[dict] = []
        for task in self._plan:
            name = task.get("task")
            tool = self._tools.get(name)
            result = tool(task) if callable(tool) else None
            results.append({"task": name, "result": result})
        return results
