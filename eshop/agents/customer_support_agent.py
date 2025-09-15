"""Customer support agent capable of answering FAQs and initiating returns."""
from __future__ import annotations

from typing import Any, Dict, Optional


class CustomerSupportAgent:
    """Handles customer FAQs and delegates return processing."""

    def __init__(self, manager: "StoreManager") -> None:
        self.manager = manager
        self.name = "support"

    def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message via the store manager."""
        self.manager.route_message(message, sender=self)

    def receive_message(self, message: Dict[str, Any], sender: Optional[Any] = None) -> str:
        """Process customer support queries."""
        msg_type = message.get("type")
        content = message.get("content", {})
        if msg_type == "faq":
            question = content.get("question", "")
            return f"FAQ response: Sorry, I don't have an answer for '{question}' yet."
        if msg_type == "return":
            # Delegate return processing to InventoryAgent
            item = content.get("item", "unknown item")
            self.send_message({"type": "return", "content": {"item": item}})
            return f"Return request for {item} forwarded to inventory."
        return "CustomerSupportAgent cannot handle this message."
