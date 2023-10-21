from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List


@dataclass
class ItemEdit:
    id: int
    label: str
    quantity: int
    price: Decimal
    total: Decimal


@dataclass
class Item:
    id: int
    product_id: int
    product_name: str
    quantity: int
    total_product: Decimal
    unitary_price_commission: Optional[Decimal] = None
    percentage_commission: Optional[Decimal] = None
    commission: Optional[Decimal] = None


@dataclass
class Cart:
    total_sale: Decimal
    items: List[Item] = field(default_factory=list)
    total_commission: Optional[Decimal] = None

    def to_dict(self):
        return {
            'total_commission': self.total_commission if self.total_commission else "0.00",
            'total_sale': self.total_sale,
            'items': [{
                key: value
                for key, value in item.__dict__.items()
                if value is not None
            }
                for item in self.items]
        }


@dataclass
class EditSale:
    invoice: int
    seller: int
    client: int
    date: str
    total_sale: Optional[Decimal] = 0.00
    items: List[ItemEdit] = field(default_factory=list)

    def to_dict(self):
        return {
            'invoice': self.invoice,
            'seller': self.seller,
            'client': self.client,
            'date': self.date,
            'total_sale': self.total_sale,
            'items': [{
                key: value
                for key, value in item.__dict__.items()
                if value is not None
            }
                for item in self.items]
        }

@dataclass
class ReportSales:
    invoice: int
    invoice_label: str
    seller: str
    client: str
    date: str
    cart: Cart
    total_sale: Optional[Decimal] = 0.00
    items: List[Item] = field(default_factory=list)

    def to_dict(self):
        return {
            'invoice': self.invoice,
            'invoice_label': self.invoice_label,
            'seller': self.seller,
            'client': self.client,
            'date': self.date,
            'total_sale': self.total_sale,
            'cart': self.cart.to_dict()
        }
