from typing import Any, Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from people.models import Seller, Client


class SellerTest(APITestCase):
    basename: str = 'seller'
    fixtures = ["people.json", "sellers.json"]
    payload: Dict[str, Any] = {
        "name": "Sandra Caetano",
        "email": "sandra@gmail.com",
        "phone": "888888888"
    }

    def test_get_seller_by_pk(self):
        seller: Seller = Seller.objects.get(pk=1)
        self.assertEqual(seller.name, "Regina Souza")
        self.assertEqual(seller.email, "regina@gmail.com")
        self.assertEqual(seller.phone, "11111111111")

    def test_list_sellers(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_seller(self):
        url = reverse(f'{self.basename}-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_seller(self):
        url = reverse(f'{self.basename}-detail', args=[1])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_seller(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        seller: Seller = Seller.objects.filter(**self.payload).first()
        if seller:
            self.assertEqual(seller.name, self.payload.get("name"))
            self.assertEqual(seller.email, self.payload.get("email"))
            self.assertEqual(seller.phone, self.payload.get("phone"))


class ClientTest(APITestCase):
    basename: str = 'client'
    fixtures = ["people.json", "customers.json"]
    payload: Dict[str, Any] = {
        "name": "Jose Aparecido",
        "email": "jose@gmail.com",
        "phone": "9999999999"
    }

    def test_get_client_by_pk(self):
        client: Client = Client.objects.get(pk=3)
        self.assertEqual(client.name, "Lucas Montano")
        self.assertEqual(client.email, "lucas@gmail.com")
        self.assertEqual(client.phone, "33333333333")

    def test_list_customers(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_client(self):
        url = reverse(f'{self.basename}-detail', args=[3])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_client(self):
        url = reverse(f'{self.basename}-detail', args=[3])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_client(self):
        url = reverse(f'{self.basename}-list')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        seller: Seller = Seller.objects.filter(**self.payload).first()
        if seller:
            self.assertEqual(seller.name, self.payload.get("name"))
            self.assertEqual(seller.email, self.payload.get("email"))
            self.assertEqual(seller.phone, self.payload.get("phone"))
