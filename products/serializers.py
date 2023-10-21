from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from products.models import Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ListItemsSerializer(Serializer):
    id = serializers.IntegerField(help_text='Id do produto')
    product = serializers.CharField(help_text="Produto")
    value = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Valor unitário")
