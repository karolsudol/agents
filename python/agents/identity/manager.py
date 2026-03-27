import os
import json
from typing import Dict, Any, Optional
import ows


class AgentIdentityManager:
    """
    Manages OWS-compliant identities and wallets for agents.
    Uses the open-wallet-standard (ows) library.
    """

    def __init__(self, agent_name: str, passphrase: Optional[str] = None):
        self.agent_name = agent_name
        self.passphrase = passphrase or os.getenv(
            "OWS_WALLET_PASSPHRASE", "default-dev-passphrase"
        )
        self.setup_wallet()

    def setup_wallet(self) -> None:
        """
        Ensures a wallet exists for the agent.
        """
        try:
            wallet = ows.get_wallet(self.agent_name)
            if not wallet:
                ows.create_wallet(name=self.agent_name, passphrase=self.passphrase)
        except Exception:
            # If get_wallet fails because it doesn't exist, create it
            ows.create_wallet(name=self.agent_name, passphrase=self.passphrase)

    def sign_action(self, action_data: Dict[str, Any], chain: str = "evm") -> str:
        """
        Signs an agent action for AP2/OWS compliance.
        By default uses EVM chain for signing.
        """
        message = json.dumps(action_data, sort_keys=True)
        return ows.sign_message(
            wallet=self.agent_name,
            chain=chain,
            message=message,
            passphrase=self.passphrase,
        )

    def get_address(self, chain: str = "solana") -> str:
        """
        Retrieves the agent's address for a specific chain.
        """
        # Note: derive_address might be needed if get_wallet doesn't provide it directly
        # For now, we'll use derive_address as a fallback or primary method
        return ows.derive_address(
            wallet=self.agent_name, chain=chain, passphrase=self.passphrase
        )

    def verify_payment(self, payment_proof: str) -> bool:
        """
        Verifies an x402 payment proof on Solana.
        (Placeholder for actual Solana RPC verification logic)
        """
        return True
