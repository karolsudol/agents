import base64
import json
import os
from typing import Optional
from fastapi import Request, Response
from agents.identity.manager import AgentIdentityManager


class X402Middleware:
    """
    Middleware to enforce x402 (HTTP 402 Payment Required) for AI agents.
    """

    def __init__(self, recipient_address: Optional[str] = None):
        # In a real scenario, the recipient would be the Treasury/Finance Agent's wallet
        self.recipient_address = recipient_address or os.getenv(
            "FINANCE_WALLET_ADDRESS", "FinanceAgentSolanaAddress1111"
        )
        self.default_price = 0.01  # $0.01 USDC
        self.identity_manager = AgentIdentityManager(agent_name="finance_director")

    async def enforce_payment(self, request: Request, call_next):
        """
        Intercepts requests and checks for x402 payment signatures.
        """
        # 1. Check if the request already contains a payment signature
        payment_signature = request.headers.get("PAYMENT-SIGNATURE")

        if not payment_signature:
            # No signature found -> Return 402 Payment Required
            payment_required_data = {
                "price": self.default_price,
                "currency": "USDC",
                "destination": self.recipient_address,
                "network": "solana",
                "reason": "AI Agent Tool Execution Fee",
            }

            # Encode for the header
            header_value = base64.b64encode(
                json.dumps(payment_required_data).encode()
            ).decode()

            return Response(
                status_code=402,
                content="Payment Required to execute this tool.",
                headers={"PAYMENT-REQUIRED": header_value},
            )

        # 2. If signature exists, verify it
        # In a production app, this would check the Solana blockchain for the transaction
        is_valid = self.identity_manager.verify_payment(payment_signature)

        if not is_valid:
            return Response(status_code=403, content="Invalid Payment Signature.")

        # 3. Payment verified -> Proceed to the agent logic
        response = await call_next(request)

        # Add payment response header
        response.headers["PAYMENT-RESPONSE"] = "Settled"
        return response


# Global instance for the Finance Hub
x402_gate = X402Middleware()
