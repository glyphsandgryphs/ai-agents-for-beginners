"""Inventory agent responsible for managing stock and returns."""
from __future__ import annotations

from typing import Any, Dict, Optional


class InventoryAgent:
    """Handles order fulfillment and returns."""

    def __init__(self, manager: "StoreManager") -> None:
        self.manager = manager
        self.name = "inventory"

    def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message via the store manager."""
        self.manager.route_message(message, sender=self)

    def receive_message(self, message: Dict[str, Any], sender: Optional[Any] = None) -> str:
        """Process inbound messages related to inventory tasks."""
        msg_type = message.get("type")
        content = message.get("content", {})
        if msg_type == "order":
            item = content.get("item", "unknown item")
            return f"Order confirmed for {item}."
        if msg_type == "return":
            item = content.get("item", "unknown item")
            return f"Return processed for {item}."
        return "InventoryAgent cannot handle this message."
