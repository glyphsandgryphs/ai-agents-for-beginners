"""Configuration for monitoring alerts."""
from dataclasses import dataclass
import os


@dataclass
class AlertThresholds:
    """Thresholds for triggering monitoring alerts."""
    high_latency_ms: int = int(os.getenv("HIGH_LATENCY_MS", "1000"))
    api_failure_rate: float = float(os.getenv("API_FAILURE_RATE", "0.1"))
