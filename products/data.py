from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Item:
    id: int
    product: str
    value: Decimal
