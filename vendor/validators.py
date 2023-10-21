from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def not_date_past(date):
    if date < date.today():
        raise ValidationError("A data não pode ser inferior a data atual")
    return date


def validate_phone(phone):
    if len(str(phone)) < 10 or len(str(phone)) > 11:
        raise serializers.ValidationError('Número de telefone inválido')
    return phone
