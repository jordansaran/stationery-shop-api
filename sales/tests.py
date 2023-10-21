from typing import Any, Dict, List
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from sales.models import Sale, Item


class SaleTest(APITestCase):
    basename: str = 'sale'
    fixtures = ["products.json", "people.json", "sellers.json",
                "customers.json", "commissions.json", "sales.json",
                "items.json"]
    payload: Dict[str, Any] = {
          "client": "3",
          "seller": "1",
          "dateSale": "2023-10-13T18:22:38.537Z",
          "items": [
            {
              "product": 1,
              "quantity": 2
            },
            {
              "product": 2,
              "quantity": 3
            }
          ]
        }

    def test_get_sale_by_pk(self):
        sale: Sale = Sale.objects.get(pk=3)
        datetime_saler = datetime(2023, 10, 6, 19, 32, 48, 175)
        self.assertEqual(sale.client, 3)
        self.assertEqual(sale.seller, 1)
        self.assertEqual(sale.date_sale, datetime_saler)

    def test_list_sales(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_sale(self):
        url = reverse(f'{self.basename}-detail', args=[3])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_sale(self):
        url = reverse(f'{self.basename}-detail', args=[3])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_sale(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        items = self.payload.get("items")
        self.payload.pop("items")
        sale: Sale = Sale.objects.filter(**self.payload).first()
        datetime_sale = datetime(2023, 10, 13, 18, 22, 38, 537)
        if sale:
            self.assertEqual(sale.client, "3")
            self.assertEqual(sale.seller, "1")
            self.assertEqual(sale.date_sale, datetime_sale)
            list_items: List[Item] = []
            for item in items:
                list_items.append(Item.objects.filter(**item).first())
            self.assertEqual(list_items[0].product.pk, 3)
            self.assertEqual(list_items[0].sale.pk, sale.pk)
            self.assertEqual(list_items[0].quantity, 2)
            self.assertEqual(list_items[1].product.pk, 2)
            self.assertEqual(list_items[1].sale.pk, sale.pk)
            self.assertEqual(list_items[1].quantity, 3)
