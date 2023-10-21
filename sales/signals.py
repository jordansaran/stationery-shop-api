from sales.controllers import get_commission
from sales.models import Commission


def update_fields_item(sender, instance, raw, using, update_fields, **kwargs):
    commission = Commission.objects.filter(day_week=instance.sale.date_sale.isoweekday()).first()
    total_product = instance.product.unitary_price * instance.quantity
    total_product, commission, percentage_commission = get_commission(commission, instance,total_product)
    instance.unitary_price_commission = instance.product.unitary_price * (1 + percentage_commission)
    instance.total_product = total_product
    instance.commission = commission
    instance.percentage_commission = percentage_commission
