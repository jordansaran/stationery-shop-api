from decimal import Decimal
from typing import List, Dict, Any

from products.data import Item
from products.models import Product
from datetime import datetime

from sales.controllers import get_percentage_commission
from sales.models import Commission


def get_list_items_plus_commission() -> List[Dict[str, Any]]:
    list_products = Product.objects.all()
    iso_week_day = datetime.today().date().isoweekday()
    commission = Commission.objects.filter(day_week=iso_week_day).first()
    list_items: List[Dict[str, any]] = []
    for product in list_products:
        percentage_commission = get_percentage_commission(product.commission, commission)
        value = product.unitary_price * Decimal((1 + (percentage_commission / 100)))
        label = f"{str(product.id).zfill(3)} - {product.product}"
        item = Item(id=product.id, product=label, value=value)
        list_items.append(item.__dict__)
    return list_items
