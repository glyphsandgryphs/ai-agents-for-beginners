"""Evaluation and monitoring utilities for the e-shop agents."""
import logging
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InteractionLogger:
    """Simple in-memory interaction logger."""
    messages: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        logging.info(message)
        self.messages.append(message)


def measure_task_success(logger: InteractionLogger) -> float:
    """Compute the fraction of logged messages that mention success."""
    successes = [m for m in logger.messages if "success" in m.lower()]
    return len(successes) / len(logger.messages) if logger.messages else 0.0


def compute_cost_metrics(costs: List[float]) -> Dict[str, float]:
    """Compute basic cost statistics for a list of numerical costs."""
    total = sum(costs)
    average = total / len(costs) if costs else 0.0
    return {"total": total, "average": average}


def generate_report(logger: InteractionLogger, costs: List[float]) -> Dict[str, float]:
    """Generate a summary report of success and cost metrics."""
    report = {"success_rate": measure_task_success(logger)}
    report.update(compute_cost_metrics(costs))
    logging.info("Evaluation report: %s", report)
    return report


# Configuration for alert thresholds in production deployments.
ALERT_THRESHOLDS = {
    "latency_ms": 1_000,
    "api_failures": 5,
}
