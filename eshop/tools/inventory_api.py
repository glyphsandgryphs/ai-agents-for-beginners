import logging
import os
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("INVENTORY_API_URL", "https://api.example.com/inventory")


def list_products() -> Dict[str, Any]:
    """Retrieve a list of products from the inventory service."""
    try:
        response = requests.get(f"{BASE_URL}/products", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:  # pragma: no cover - network error
        logger.error("Failed to list products: %s", exc)
        raise RuntimeError("Inventory service error") from exc


def update_stock(product_id: str, quantity: int) -> Dict[str, Any]:
    """Update the stock level for a given product.

    Args:
        product_id: Identifier of the product to update.
        quantity: New quantity to set for the product.
    """
    payload = {"quantity": quantity}
    try:
        response = requests.post(
            f"{BASE_URL}/products/{product_id}/stock", json=payload, timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:  # pragma: no cover - network error
        logger.error("Failed to update stock for %s: %s", product_id, exc)
        raise RuntimeError("Inventory service error") from exc


def register_tool() -> list[Dict[str, Any]]:
    """Return tool metadata for agent registration."""
    return [
        {
            "name": "list_products",
            "func": list_products,
            "description": "Retrieve a list of products from the inventory service.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        {
            "name": "update_stock",
            "func": update_stock,
            "description": "Update the stock quantity for a product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Identifier of the product to update",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "New stock quantity",
                    },
                },
                "required": ["product_id", "quantity"],
            },
        },
    ]
