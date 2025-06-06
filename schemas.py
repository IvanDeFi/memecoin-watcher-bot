from dataclasses import dataclass
from typing import Optional

@dataclass
class TokenInfo:
    name: str
    symbol: str
    address: str
    chain: str
    price: Optional[float] = None
    market_cap: Optional[float] = None
    holders: Optional[int] = None
    created_at: Optional[str] = None
    verified: Optional[bool] = False