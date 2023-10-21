from _decimal import Decimal
from typing import List, Dict, Any

from django.db import connection

from sales.data import Item, ReportSales, Cart, EditSale, ItemEdit
from sales.models import Sale
from vendor.utils import dictfetchall


def get_percentage_commission(percentage_commission, commission):
    if commission:
        if percentage_commission < commission.min:
            percentage_commission = commission.min
        elif percentage_commission > commission.max:
            percentage_commission = commission.max
    return percentage_commission


def get_commission(commission, item, product_price) -> tuple[Decimal, Decimal, Decimal]:
    percentage_commission = get_percentage_commission(item.product.commission, commission)
    set_comission_to_product = percentage_commission / 100
    total_product = product_price * Decimal(1 + set_comission_to_product)
    commission = total_product * Decimal(set_comission_to_product)
    return total_product, commission, Decimal(set_comission_to_product)


def get_sale_by_pk(sale: Sale):
    list_items_by_sale = (Sale
                          .objects
                          .prefetch_related('items')
                          .filter(invoice=sale.invoice)
                          .values('item__product__product',
                                  'item__quantity',
                                  'item__unitary_price_commission',
                                  'item__product_id',
                                  'item__total_product'))
    items: List[ItemEdit] = []
    total_sales = Decimal(0.00)
    for item_by_sale in list_items_by_sale:
        items.append(
            ItemEdit(id=item_by_sale['item__product_id'],
                     label=f"{str(item_by_sale['item__product_id']).zfill(3)} - {item_by_sale['item__product__product']}",
                     price=item_by_sale['item__unitary_price_commission'],
                     quantity=item_by_sale['item__quantity'],
                     total=item_by_sale['item__total_product'])
            )
        total_sales += Decimal(item_by_sale['item__total_product'])
    return EditSale(
        invoice=sale.invoice,
        seller=sale.seller.pk,
        client=sale.client.pk,
        items=items,
        date=sale.date_sale.isoformat(),
        total_sale=total_sales
    ).to_dict()


def get_report_sales() -> List[Dict[str, Any]]:
    list_sales_finished: List[ReportSales] = []
    list_sales = Sale.objects.values('invoice', 'seller__name', 'client__name', 'created_at')
    for sale in list_sales:
        invoice_label = f"{str(sale['invoice']).zfill(8)}"
        list_items_by_sale = (Sale
                              .objects
                              .prefetch_related('items')
                              .filter(invoice=sale['invoice'])
                              .values('item__product__product', 'item__quantity',
                                      'item__unitary_price_commission',
                                      'item__commission', 'item__product_id', 'items__id',
                                      'item__percentage_commission', 'item__total_product'))
        items: List[Item] = []
        total_sales = Decimal(0.00)
        total_commisison = Decimal(0.00)
        for item_by_sale in list_items_by_sale:
            items.append(
                Item(id=item_by_sale['items__id'],
                     product_id=item_by_sale['item__product_id'],
                     product_name=item_by_sale['item__product__product'],
                     unitary_price_commission=item_by_sale['item__unitary_price_commission'],
                     quantity=item_by_sale['item__quantity'],
                     total_product=item_by_sale['item__total_product'],
                     percentage_commission=item_by_sale['item__percentage_commission'],
                     commission=item_by_sale['item__commission'])
            )
            total_commisison += Decimal(item_by_sale['item__commission'])
            total_sales += Decimal(item_by_sale['item__total_product'])
        cart = Cart(
            total_sale=total_sales,
            total_commission=total_commisison,
            items=items
        )
        list_sales_finished.append(
            ReportSales(
                invoice=sale['invoice'],
                invoice_label=invoice_label,
                seller=sale['seller__name'],
                client=sale['client__name'],
                cart=cart,
                date=sale['created_at'],
                total_sale=total_sales
            )
        )
    return [sale_finished.to_dict() for sale_finished in list_sales_finished]


def get_report_commission(date_start: str, date_end: str):
    sql = ("select DISTINCT "
           "pp.id as id, "
           "pp.name as name, "
           "(select count(*) from sales_sale  where seller_id = ss.seller_id) as total_sales, "
           "(select sum(sales_item.commission) "
           "from sales_sale inner join sales_item on sales_sale.invoice = sales_item.sale_id "
           "where sales_sale.seller_id = ss.seller_id) as total_commission "
           "from sales_sale ss "
           "inner join main.people_seller ps on ps.people_ptr_id = ss.seller_id "
           "inner join main.people_people pp on pp.id = ps.people_ptr_id ")
    if date_start and date_end:
        sql += f"where date_sale between '{date_start}' and '{date_end}'"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)
