"""Agent responsible for inventory related tasks.

Illustrates the multi-agent design pattern by handling messages pertaining to
product stock and catalog management.
"""
import logging
from typing import Any, Dict, List


class InventoryAgent:
    def __init__(self) -> None:
        self.inbox: List[Dict[str, Any]] = []

    def send_message(self, recipient: "InventoryAgent", message: Dict[str, Any]) -> None:
        """Send a message to another agent."""
        logging.debug("InventoryAgent sending message: %s", message)
        recipient.receive_message(message)

    def receive_message(self, message: Dict[str, Any]) -> None:
        """Receive a message and store it for later processing."""
        logging.info("InventoryAgent received message: %s", message)
        self.inbox.append(message)
