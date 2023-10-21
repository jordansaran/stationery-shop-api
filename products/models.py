from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from vendor.mixins.model import ModelWithoutIdMixin


class Product(ModelWithoutIdMixin):

    id = models.BigAutoField(primary_key=True,
                             null=False,
                             blank=False,
                             editable=False,
                             verbose_name="Código de barra")
    product = models.CharField(max_length=255,
                               blank=False,
                               null=False,
                               unique=True,
                               verbose_name="Produto/Serviço")
    unitary_price = models.DecimalField(blank=False,
                                        null=False,
                                        default=0.00,
                                        verbose_name="Preço unitário",
                                        max_digits=10,
                                        decimal_places=2,
                                        validators=[
                                           MinValueValidator(0.00)
                                       ])
    commission = models.SmallIntegerField(blank=False,
                                          null=False,
                                          default=0,
                                          verbose_name="Comissão",
                                          validators=[
                                              MinValueValidator(0),
                                              MaxValueValidator(10)
                                          ])

    class Meta:
        ordering = ['product', 'unitary_price', 'commission']
        verbose_name = "product"
        verbose_name_plural = "products"
