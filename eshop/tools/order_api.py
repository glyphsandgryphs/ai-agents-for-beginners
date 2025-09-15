import logging
import os
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("ORDER_API_URL", "https://api.example.com/orders")


def create_order(order: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new order in the order service."""
    try:
        response = requests.post(f"{BASE_URL}/", json=order, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:  # pragma: no cover - network error
        logger.error("Failed to create order: %s", exc)
        raise RuntimeError("Order service error") from exc


def fetch_order_status(order_id: str) -> Dict[str, Any]:
    """Fetch the status of an existing order."""
    try:
        response = requests.get(f"{BASE_URL}/{order_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:  # pragma: no cover - network error
        logger.error("Failed to fetch order %s: %s", order_id, exc)
        raise RuntimeError("Order service error") from exc


def register_tool() -> list[Dict[str, Any]]:
    """Return tool metadata for agent registration."""
    return [
        {
            "name": "create_order",
            "func": create_order,
            "description": "Create a new order in the order service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order": {
                        "type": "object",
                        "description": "Order payload to create.",
                    }
                },
                "required": ["order"],
            },
        },
        {
            "name": "fetch_order_status",
            "func": fetch_order_status,
            "description": "Fetch the current status for an order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Identifier of the order",
                    },
                },
                "required": ["order_id"],
            },
        },
    ]
