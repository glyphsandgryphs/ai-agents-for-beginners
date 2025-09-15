# E-Shop Multi-Agent Example

This example demonstrates a simple multi-agent architecture for an online shop.

## Agents

- **InventoryAgent** handles order fulfillment and return processing.
- **CustomerSupportAgent** answers FAQs and forwards return requests.
- **StoreManager** acts as a coordinator, spawning agents and routing messages.

Agents communicate through a lightweight message-passing interface consisting of
`send_message` and `receive_message`. The `StoreManager` uses the message type
(`order`, `return`, `faq`) to determine which agent should handle the request.

## Alignment with the Multi-Agent Design Pattern

The multi-agent pattern advocates specialized agents collaborating to accomplish
complex tasks. In this e-commerce scenario:

1. Each agent focuses on a specific responsibility—inventory or customer support.
2. Messages are routed via a central coordinator, enabling decoupled
   communication.
3. Agents can delegate tasks to one another (e.g., customer support forwarding
   return requests to inventory).

This structure showcases how multi-agent systems can be organized in a modular
and extensible manner.
