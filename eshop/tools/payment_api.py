"""Payment processing API connectors."""
import logging
from typing import Any, Dict


def charge_card(amount: float, card_token: str) -> Dict[str, Any]:
    """Charge a credit card."""
    try:
        logging.info("Charging card %s for %.2f", card_token, amount)
        return {"status": "charged", "amount": amount}
    except Exception as exc:  # pragma: no cover - illustrative only
        logging.error("Charge failed: %s", exc)
        raise


def refund(payment_id: str, amount: float) -> Dict[str, Any]:
    """Refund a payment."""
    try:
        logging.info("Refunding payment %s for %.2f", payment_id, amount)
        return {"status": "refunded", "amount": amount}
    except Exception as exc:  # pragma: no cover - illustrative only
        logging.error("Refund failed: %s", exc)
        raise


def register_tool() -> Dict[str, Any]:
    """Return schema metadata for registering this tool with an agent."""
    return {
        "name": "payment_api",
        "description": "Payment processing operations",
        "functions": {
            "charge_card": {
                "description": "Charge a customer's card",
                "params": {"amount": "float", "card_token": "str"},
            },
            "refund": {
                "description": "Refund a payment",
                "params": {"payment_id": "str", "amount": "float"},
            },
        },
    }
