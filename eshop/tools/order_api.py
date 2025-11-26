"""Order management API connectors."""
import logging
from typing import Any, Dict


def create_order(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create an order and return order details."""
    try:
        logging.info("Creating order: %s", payload)
        return {"id": "order_123", **payload}
    except Exception as exc:  # pragma: no cover - illustrative only
        logging.error("Failed to create order: %s", exc)
        raise


def fetch_order_status(order_id: str) -> Dict[str, Any]:
    """Fetch status for an order."""
    try:
        logging.info("Fetching order status for %s", order_id)
        return {"id": order_id, "status": "processing"}
    except Exception as exc:  # pragma: no cover - illustrative only
        logging.error("Failed to fetch order: %s", exc)
        raise


def register_tool() -> Dict[str, Any]:
    """Return schema metadata for registering this tool with an agent."""
    return {
        "name": "order_api",
        "description": "Order management operations",
        "functions": {
            "create_order": {
                "description": "Create a new order",
                "params": {"payload": "dict"},
            },
            "fetch_order_status": {
                "description": "Fetch the status of an order",
                "params": {"order_id": "str"},
            },
        },
    }
