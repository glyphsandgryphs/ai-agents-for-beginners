import logging
import os
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("PAYMENT_API_URL", "https://api.example.com/payments")


def charge_card(card: Dict[str, Any], amount: float) -> Dict[str, Any]:
    """Charge a customer's card for the specified amount."""
    payload = {"card": card, "amount": amount}
    try:
        response = requests.post(f"{BASE_URL}/charge", json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:  # pragma: no cover - network error
        logger.error("Failed to charge card: %s", exc)
        raise RuntimeError("Payment service error") from exc


def refund(transaction_id: str, amount: float) -> Dict[str, Any]:
    """Refund a previously charged transaction."""
    payload = {"amount": amount}
    try:
        response = requests.post(
            f"{BASE_URL}/refunds/{transaction_id}", json=payload, timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:  # pragma: no cover - network error
        logger.error("Failed to refund %s: %s", transaction_id, exc)
        raise RuntimeError("Payment service error") from exc


def register_tool() -> list[Dict[str, Any]]:
    """Return tool metadata for agent registration."""
    return [
        {
            "name": "charge_card",
            "func": charge_card,
            "description": "Charge a customer's card.",
            "parameters": {
                "type": "object",
                "properties": {
                    "card": {
                        "type": "object",
                        "description": "Card details including number, exp_month, exp_year, cvc",
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount to charge",
                    },
                },
                "required": ["card", "amount"],
            },
        },
        {
            "name": "refund",
            "func": refund,
            "description": "Refund a transaction by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "Identifier of the transaction",
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount to refund",
                    },
                },
                "required": ["transaction_id", "amount"],
            },
        },
    ]
