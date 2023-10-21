from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer
from people.models import Client, Seller
from vendor.validators import validate_phone


class ClientSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    phone = IntegerField(validators=[validate_phone])

    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone']


class SellerSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    phone = IntegerField(validators=[validate_phone])

    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'phone']
