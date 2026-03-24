import mcp.server.fastmcp as fastmcp

# Initialize FastMCP server
mcp = fastmcp.FastMCP("Currency Converter")

# Mock exchange rates (relative to USD)
EXCHANGE_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 151.0,
    "CAD": 1.35,
    "AUD": 1.52,
}


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Converts an amount from one currency to another using mock rates.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The source currency code (e.g., USD, EUR, GBP).
        to_currency (str): The target currency code (e.g., USD, EUR, GBP).
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        return f"Error: Unsupported currency. Supported: {', '.join(EXCHANGE_RATES.keys())}"

    # Convert to USD first, then to target currency
    amount_in_usd = amount / EXCHANGE_RATES[from_currency]
    converted_amount = amount_in_usd * EXCHANGE_RATES[to_currency]

    return f"{amount:.2f} {from_currency} is equal to {converted_amount:.2f} {to_currency}."


if __name__ == "__main__":
    # Standard MCP server entry point
    mcp.run()
