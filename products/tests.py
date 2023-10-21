from typing import Any, Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product


class ProductTest(APITestCase):
    basename: str = 'product'
    fixtures = ["products.json"]
    payload: Dict[str, Any] = {
        "product": "Caderno de 10 materias",
        "unitary_price": "19.90",
        "commission": 10
    }

    def test_get_product_by_pk(self):
        product: Product = Product.objects.get(pk=1)
        self.assertEqual(product.product, "Caderno de Brochura")
        self.assertEqual(product.unitary_price, "8.20")
        self.assertEqual(product.commission, 5)

    def test_list_products(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        url = reverse(f'{self.basename}-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        url = reverse(f'{self.basename}-detail', args=[1])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_product(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product: Product = Product.objects.filter(**self.payload).first()
        if product:
            self.assertEqual(product.product, "Caderno de 10 materias")
            self.assertEqual(product.unitary_price, "19.90")
            self.assertEqual(product.commission, 10)

    def test_unique_product(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
