"""Coordinator that spawns agents and routes messages among them."""
from __future__ import annotations

from typing import Any, Dict, Optional

from .customer_support_agent import CustomerSupportAgent
from .inventory_agent import InventoryAgent


class StoreManager:
    """Coordinator that manages agents and routes tasks."""

    def __init__(self) -> None:
        self.agents: Dict[str, Any] = {}
        self.spawn_agents()

    def spawn_agents(self) -> None:
        """Instantiate all store agents."""
        self.agents["inventory"] = InventoryAgent(self)
        self.agents["support"] = CustomerSupportAgent(self)

    def route_message(self, message: Dict[str, Any], sender: Optional[Any] = None) -> Optional[str]:
        """Route messages to the appropriate agent based on type."""
        msg_type = message.get("type")
        if msg_type in {"order", "return"}:
            target = self.agents["inventory"]
        elif msg_type == "faq":
            target = self.agents["support"]
        else:
            return f"No agent available for message type '{msg_type}'."
        return target.receive_message(message, sender)

    def handle_customer_request(self, message: Dict[str, Any]) -> Optional[str]:
        """Entry point for external callers to submit a customer request."""
        return self.route_message(message, sender=self)
