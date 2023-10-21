from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sales.controllers import get_report_sales, get_report_commission, get_sale_by_pk
from sales.models import Sale
from sales.serializers import (SaleSerializer, SaleCreateUpdateSerializer,
                               FilterDatesSerializer, ReportCommissionSerializer, ReportSalesSerializer,
                               EditSalesSerializer)


class SaleViewSet(CreateAPIView,
                  UpdateAPIView,
                  ListAPIView,
                  RetrieveAPIView,
                  DestroyAPIView,
                  GenericViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all().order_by('-created_at')

    @swagger_auto_schema(request_body=SaleCreateUpdateSerializer,
                         operation_description="Criação de uma nova venda.",
                         responses={
                             status.HTTP_201_CREATED: SaleSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Lista de erros relacionado a criação de uma venda'
                         })
    def create(self, request, *args, **kwargs):
        try:
            serializer = SaleCreateUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except (TypeError, IntegrityError) as _error:
            return Response({'error': str(_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Relatório de vendas",
                         responses={status.HTTP_200_OK: SaleSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Lista de todos as vendas",
                         responses={status.HTTP_200_OK: ReportSalesSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path="report")
    def report_sales(self, request, *args, **kwargs):
        queryset = get_report_sales()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReportSalesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReportSalesSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Retorna um venda a partir de seu ID.",
                         responses={
                             status.HTTP_200_OK: SaleSerializer(many=True),
                             status.HTTP_404_NOT_FOUND: 'Venda não encontrado.'
                         })
    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        instance = get_sale_by_pk(instance)
        serializer = EditSalesSerializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Apagar uma venda.",
                         responses={
                             status.HTTP_204_NO_CONTENT: 'Venda apagada com sucesso.',
                             status.HTTP_404_NOT_FOUND: 'Venda não encontrado.'
                         })
    def destroy(self, request, pk):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=SaleCreateUpdateSerializer,
                         operation_description="Atualiza uma venda a partir de seu ID.",
                         responses={
                             status.HTTP_202_ACCEPTED: SaleCreateUpdateSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização do imóvel.',
                             status.HTTP_404_NOT_FOUND: 'Venda não encontrada.'
                         })
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SaleCreateUpdateSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(operation_description="Atualiza apenas alguns campos da venda.",
                         responses={
                             status.HTTP_202_ACCEPTED: SaleCreateUpdateSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização da venda.',
                             status.HTTP_404_NOT_FOUND: 'Venda não encontrada.'
                         })
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(operation_description="Retorna uma lista da quantidade de vendas e comissão por vendedor.",
                         query_serializer=FilterDatesSerializer(many=True),
                         responses={status.HTTP_200_OK: ReportCommissionSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path="report/commission")
    def report_commission(self, request, *args, **kwargs):
        date_start = self.request.query_params.get('dateStart')
        date_end = self.request.query_params.get('dateEnd')
        queryset = get_report_commission(date_start, date_end)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReportCommissionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReportCommissionSerializer(queryset, many=True)
        return Response(serializer.data)
