from dataclasses import dataclass
from typing import Optional

@dataclass
class TokenInfo:
    """Simple dataclass describing a tracked token.

    Attributes:
        name: Name of the token.
        symbol: Trading symbol.
        address: Contract address.
        chain: Blockchain network the token lives on.
        price: Current price in USD, if known.
        market_cap: Token market capitalisation in USD, if known.
        holders: Number of unique holders, if available.
        created_at: Token creation timestamp as an ISO formatted string.
        verified: Whether the contract source has been verified.
    """

    name: str
    symbol: str
    address: str
    chain: str
    price: Optional[float] = None
    market_cap: Optional[float] = None
    holders: Optional[int] = None
    created_at: Optional[str] = None
    verified: Optional[bool] = False
