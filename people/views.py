from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView
from rest_framework.viewsets import GenericViewSet

from people.models import Client, Seller
from people.serializers import ClientSerializer, SellerSerializer


class ClientViewSet(CreateAPIView,
                    UpdateAPIView,
                    RetrieveAPIView,
                    ListAPIView,
                    DestroyAPIView,
                    GenericViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return []

    @swagger_auto_schema(request_body=ClientSerializer,
                         operation_description="Cadastrar um cliente.",
                         responses={
                             status.HTTP_201_CREATED: ClientSerializer,
                             status.HTTP_404_NOT_FOUND: 'Cliente não encontrado.',
                             status.HTTP_400_BAD_REQUEST: 'Lista de erros.'
                         })
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Lista de todos os clientes",
                         responses={status.HTTP_200_OK: ClientSerializer(many=True),
                                    status.HTTP_404_NOT_FOUND: 'Lista de clientes vazia.'})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retorna um cliente a partir de seu identificador.",
                         responses={
                             status.HTTP_200_OK: ClientSerializer(many=True),
                             status.HTTP_404_NOT_FOUND: 'Cliente não encontrado.'
                         })
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Apagar um cliente.",
                         responses={
                             status.HTTP_204_NO_CONTENT: 'Cliente apagado com sucesso.',
                             status.HTTP_404_NOT_FOUND: 'Cliente não encontrado.'
                         })
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Atualiza um imóvel a partir de seu UUID.",
                         responses={
                             status.HTTP_202_ACCEPTED: ClientSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização do imóvel.',
                             status.HTTP_404_NOT_FOUND: 'Imóvel não encontrada.'
                         })
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Atualiza dados do cliente.",
                         responses={
                             status.HTTP_202_ACCEPTED: ClientSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização do cliente.',
                             status.HTTP_404_NOT_FOUND: 'Cliente não encontrada.'
                         })
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SellerViewSet(CreateAPIView,
                    UpdateAPIView,
                    RetrieveAPIView,
                    ListAPIView,
                    DestroyAPIView,
                    GenericViewSet):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return []

    @swagger_auto_schema(request_body=SellerSerializer,
                         operation_description="Cadastrar um vendedor",
                         responses={
                             status.HTTP_201_CREATED: SellerSerializer,
                             status.HTTP_404_NOT_FOUND: 'Vendedor não encontrado.',
                             status.HTTP_400_BAD_REQUEST: 'Lista de erros.'
                         })
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Lista todos os vendedores.",
                         responses={
                             status.HTTP_200_OK: SellerSerializer(many=True),
                             status.HTTP_404_NOT_FOUND: 'Lista de vendedores vazia.'
                         })
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retorna um vendedor a partir de seu identificador.",
                         responses={
                             status.HTTP_200_OK: SellerSerializer(many=True),
                             status.HTTP_404_NOT_FOUND: 'Vendedor não encontrado.'
                         })
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Apagar um vendedor.",
                         responses={
                             status.HTTP_204_NO_CONTENT: 'Vendedor apagado com sucesso.',
                             status.HTTP_404_NOT_FOUND: 'Vendedor não encontrado.'
                         })
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Atualiza dados de um vendedor a partir de seu identificador.",
                         responses={
                             status.HTTP_202_ACCEPTED: SellerSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização dos dados do vendedor.',
                             status.HTTP_404_NOT_FOUND: 'Vendedor não encontrada.'
                         })
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Atualiza alguns dados do vendedor.",
                         responses={
                             status.HTTP_202_ACCEPTED: SellerSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização dos dados do vendedor.',
                             status.HTTP_404_NOT_FOUND: 'Vendedor não encontrada.'
                         })
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
