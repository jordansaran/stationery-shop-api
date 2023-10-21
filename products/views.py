from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.controllers import get_list_items_plus_commission
from products.models import Product
from products.serializers import ProductSerializer, ListItemsSerializer


class ProductViewSet(CreateAPIView,
                     UpdateAPIView,
                     ListAPIView,
                     RetrieveAPIView,
                     DestroyAPIView,
                     GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return []

    @swagger_auto_schema(request_body=ProductSerializer,
                         operation_description="Cadastrar um novo produto.",
                         responses={
                             status.HTTP_201_CREATED: ProductSerializer,
                             status.HTTP_404_NOT_FOUND: 'Produto não encontrado.',
                             status.HTTP_400_BAD_REQUEST: 'Lista de erros.'
                         })
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Listar todos os produtos.",
                         responses={status.HTTP_200_OK: ListItemsSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        queryset = get_list_items_plus_commission()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListItemsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ListItemsSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Retorna um produto a partir de seu identificador.",
                         responses={
                             status.HTTP_200_OK: ProductSerializer(many=True),
                             status.HTTP_404_NOT_FOUND: 'Produto não encontrado.'
                         })
    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Apagar um produto.",
                         responses={
                             status.HTTP_204_NO_CONTENT: 'Produto apagado com sucesso.',
                             status.HTTP_404_NOT_FOUND: 'Produto não encontrado.'
                         })
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Atualizar um produto a partir de seu identificador.",
                         responses={
                             status.HTTP_202_ACCEPTED: ProductSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização do produto.',
                             status.HTTP_404_NOT_FOUND: 'Produto não encontrada.'
                         })
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Atualiza apenas alguns campos do produto.",
                         responses={
                             status.HTTP_202_ACCEPTED: ProductSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização do produto.',
                             status.HTTP_404_NOT_FOUND: 'Produto não encontrada.'
                         })
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
