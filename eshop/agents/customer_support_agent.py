"""Agent responsible for handling customer support messages."""
import logging
from typing import Any, Dict, List


class CustomerSupportAgent:
    def __init__(self) -> None:
        self.inbox: List[Dict[str, Any]] = []

    def send_message(self, recipient: "CustomerSupportAgent", message: Dict[str, Any]) -> None:
        """Send a message to another agent."""
        logging.debug("CustomerSupportAgent sending message: %s", message)
        recipient.receive_message(message)

    def receive_message(self, message: Dict[str, Any]) -> None:
        """Receive a message and store it for later processing."""
        logging.info("CustomerSupportAgent received message: %s", message)
        self.inbox.append(message)
