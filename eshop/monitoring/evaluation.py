"""Utilities for logging interactions and evaluating agent performance."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Iterable, List, Dict

try:  # Support running as a module or a script
    from .config import AlertThresholds
except ImportError:  # pragma: no cover - fallback for script execution
    from config import AlertThresholds

logger = logging.getLogger(__name__)


@dataclass
class Interaction:
    """Record of a single agent interaction."""
    timestamp: str
    task: str
    success: bool
    latency_ms: int
    cost: float


def log_interaction(
    task: str,
    success: bool,
    latency_ms: int,
    cost: float,
    log_file: str = "interaction_log.jsonl",
) -> None:
    """Append an interaction record to the log file."""
    interaction = Interaction(
        timestamp=datetime.utcnow().isoformat(),
        task=task,
        success=success,
        latency_ms=latency_ms,
        cost=cost,
    )
    with open(log_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(interaction)) + "\n")
    logger.info("Logged interaction for task %s", task)


def load_interactions(log_file: str) -> List[Interaction]:
    """Load interaction records from the given log file."""
    interactions: List[Interaction] = []
    if not os.path.exists(log_file):
        return interactions
    with open(log_file, "r", encoding="utf-8") as fh:
        for line in fh:
            try:
                data = json.loads(line)
                interactions.append(Interaction(**data))
            except json.JSONDecodeError:
                logger.warning("Skipping malformed log line: %s", line)
    return interactions


def measure_task_success(interactions: Iterable[Interaction]) -> float:
    """Return the fraction of successful tasks."""
    interactions = list(interactions)
    if not interactions:
        return 0.0
    successes = sum(1 for i in interactions if i.success)
    return successes / len(interactions)


def compute_cost_metrics(interactions: Iterable[Interaction]) -> Dict[str, float]:
    """Compute aggregate cost and latency metrics."""
    interactions = list(interactions)
    if not interactions:
        return {"total_cost": 0.0, "avg_latency_ms": 0.0, "avg_cost": 0.0}
    total_cost = sum(i.cost for i in interactions)
    avg_cost = total_cost / len(interactions)
    avg_latency = sum(i.latency_ms for i in interactions) / len(interactions)
    return {"total_cost": total_cost, "avg_latency_ms": avg_latency, "avg_cost": avg_cost}


def summarize_metrics(log_file: str, thresholds: AlertThresholds | None = None) -> Dict[str, float]:
    """Summarize metrics and return dictionary including potential alerts."""
    interactions = load_interactions(log_file)
    success_rate = measure_task_success(interactions)
    cost_metrics = compute_cost_metrics(interactions)
    metrics = {"success_rate": success_rate, **cost_metrics}

    thresholds = thresholds or AlertThresholds()
    alerts = []
    if cost_metrics["avg_latency_ms"] > thresholds.high_latency_ms:
        alerts.append("high_latency")
    failure_rate = 1 - success_rate
    if failure_rate > thresholds.api_failure_rate:
        alerts.append("high_failure_rate")
    if alerts:
        metrics["alerts"] = alerts
    return metrics


def generate_report(log_file: str = "interaction_log.jsonl") -> None:
    """Print a JSON report of key metrics."""
    metrics = summarize_metrics(log_file)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    generate_report()
