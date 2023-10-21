from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from sales.models import Sale, Item


class ItemsToEditSerializer(Serializer):
    id = serializers.IntegerField(help_text="ID do item")
    label = serializers.CharField(help_text="Produto/Serviço")
    quantity = serializers.IntegerField(help_text="Quantidade")
    price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Preço unitário")
    total = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total do Produto")


class ItemsSalesSerializer(Serializer):
    id = serializers.IntegerField(help_text="ID do item")
    product_id = serializers.IntegerField(help_text="ID do Produto")
    product_name = serializers.CharField(help_text="Produto/Serviço")
    quantity = serializers.IntegerField(help_text="Quantidade")
    unitary_price_commission = serializers.DecimalField(max_digits=10,
                                                        decimal_places=2,
                                                        help_text="Preço Unitário com comissão")
    total_product = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total do Produto")
    commission = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Comissão")
    percentage_commission = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="% de Comissão")


class ReportSalesCartSerializer(Serializer):
    items = ItemsSalesSerializer(many=True)
    total_sale = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total de Venda")
    total_commission = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total do Comissão")


class EditSalesSerializer(Serializer):
    invoice = serializers.IntegerField(help_text="Nota Fiscal")
    seller = serializers.IntegerField(help_text="Vendedor")
    client = serializers.IntegerField(help_text="Cliente")
    date = serializers.DateTimeField(help_text="Data da venda")
    total_sale = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Valor Total")
    items = ItemsToEditSerializer(many=True)


class ReportSalesSerializer(Serializer):
    invoice = serializers.IntegerField(help_text="Nota Fiscal")
    invoice_label = serializers.CharField(help_text="Nota Fiscal (mask)")
    seller = serializers.CharField(help_text="Vendedor")
    client = serializers.CharField(help_text="Cliente")
    date = serializers.DateTimeField(help_text="Data da venda")
    total_sale = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Valor Total")
    cart = ReportSalesCartSerializer()


class FilterDatesSerializer(Serializer):
    date_start = serializers.DateField(help_text='Data inicial')
    date_end = serializers.DateField(help_text='Data final')


class ReportCommissionSerializer(Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50, allow_blank=False, allow_null=False, help_text='Nome do vendedor')
    total_sales = serializers.IntegerField(help_text='Total de vendas')
    total_commission = serializers.DecimalField(max_digits=10, decimal_places=2, help_text='Total de comissão')


class ItemCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = ['product', 'quantity']


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        exclude = ('sale', )


class SaleSerializer(ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'


class SaleCreateUpdateSerializer(ModelSerializer):
    items = ItemCreateUpdateSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['invoice', 'client', 'seller', 'date_sale', 'items', 'created_at']

    def create(self, validated_data):
        items = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        for item in items:
            dict_item = dict(item)
            Item.objects.create(sale=sale, **dict_item)
        return sale

    def update(self, instance, validated_data):
        items = validated_data.pop('items')
        for item in validated_data:
            if Sale._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        for item in items:
            dict_item = dict(item)
            item = Item.objects.filter(sale=instance, product=dict_item['product']).first()
            Item.objects.filter(pk=item.pk).update(**dict_item)
        instance.save()
        return instance
