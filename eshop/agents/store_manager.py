"""Coordinator agent that routes tasks to specialized agents.

This module aligns with the **multi-agent design pattern**, delegating work to
specialised agents based on message type.
"""
import logging
from typing import Any, Dict

from .inventory_agent import InventoryAgent
from .customer_support_agent import CustomerSupportAgent


class StoreManager:
    def __init__(self) -> None:
        self.inventory_agent = InventoryAgent()
        self.customer_support_agent = CustomerSupportAgent()
        self.agents = {
            "inventory": self.inventory_agent,
            "support": self.customer_support_agent,
        }

    def send_message(self, message_type: str, message: Dict[str, Any]) -> None:
        """Route a message to the appropriate agent based on type."""
        agent = self.agents.get(message_type)
        if agent:
            logging.debug("Routing %s message: %s", message_type, message)
            agent.receive_message(message)
        else:
            logging.warning("No agent registered for message type '%s'", message_type)
