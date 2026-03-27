from typing import Dict, Any
from pydantic import BaseModel


class UCPQuoteRequest(BaseModel):
    item_id: str
    quantity: int
    currency: str = "USDC"


class UCPQuoteResponse(BaseModel):
    quote_id: str
    price_per_unit: float
    total_price: float
    valid_until: str
    supplier_id: str


class UCPOrderRequest(BaseModel):
    quote_id: str
    payment_proof: str  # x402 Payment Signature


class UCPOrderResponse(BaseModel):
    order_id: str
    status: str
    estimated_delivery: str


def get_ucp_quote(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    UCP Standard: Discovery & Quoting.
    Standardized pattern to get quotes from any supplier.
    """
    # Simulated UCP Logic
    item_id = request.get("item_id")
    return {
        "quote_id": f"quote_{item_id}_999",
        "price_per_unit": 10.5,
        "total_price": 10.5 * request.get("quantity", 1),
        "valid_until": "2026-12-31T23:59:59Z",
        "supplier_id": "global_distributor_01",
    }


def place_ucp_order(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    UCP Standard: Checkout & Order Placement.
    Uses unified schemas across any transport (REST/MCP/A2A).
    """
    return {
        "order_id": f"order_{request.get('quote_id')}",
        "status": "PLACED",
        "estimated_delivery": "2026-03-30T10:00:00Z",
    }
