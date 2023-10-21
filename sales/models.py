from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save
from people.models import Client, Seller
from products.models import Product
from sales.enums import Weekday
from vendor.mixins.model import ModelWithoutIdMixin, ModelMixin


class Sale(ModelWithoutIdMixin):
    invoice = models.BigAutoField(primary_key=True,
                                  blank=False,
                                  null=False,
                                  editable=False,
                                  verbose_name="Código da venda")
    client = models.ForeignKey(Client,
                               verbose_name="Cliente",
                               on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller,
                               verbose_name="Vendedor",
                               on_delete=models.CASCADE)
    date_sale = models.DateTimeField(blank=False,
                                     null=False,
                                     verbose_name="Data/Hora da venda")
    items = models.ManyToManyField(Product,
                                   through="Item",
                                   verbose_name='Itens')

    def __str__(self):
        return f"{str(self.invoice).zfill(8)} - {str(self.date_sale)}"

    class Meta:
        ordering = ['invoice', 'date_sale', 'seller', 'client']
        verbose_name = 'sale'
        verbose_name_plural = 'sales'


class Item(models.Model):
    sale = models.ForeignKey(Sale,
                             on_delete=models.CASCADE,
                             verbose_name='Venda')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Produto/Serviço')
    quantity = models.PositiveIntegerField(blank=False,
                                           null=False,
                                           default=0,
                                           verbose_name='Quantidade')
    unitary_price_commission = models.DecimalField(blank=False,
                                                   null=False,
                                                   default=0.00,
                                                   max_digits=10,
                                                   decimal_places=2,
                                                   verbose_name="Preço unitário com comissão",
                                                   validators=[
                                                        MinValueValidator(0.00),
                                                    ])
    total_product = models.DecimalField(blank=False,
                                        null=False,
                                        default=0.00,
                                        max_digits=10,
                                        decimal_places=2,
                                        verbose_name="Total do produto",
                                        validators=[
                                            MinValueValidator(0.00)
                                        ])
    percentage_commission = models.DecimalField(blank=False,
                                                max_digits=10,
                                                decimal_places=2,
                                                null=False,
                                                default=0,
                                                verbose_name="% de Comissão",
                                                validators=[
                                                    MinValueValidator(0),
                                                    MaxValueValidator(10)
                                                ])
    commission = models.DecimalField(blank=False,
                                     null=False,
                                     default=0.00,
                                     max_digits=10,
                                     decimal_places=2,
                                     verbose_name="Comissão",
                                     validators=[
                                         MinValueValidator(0.00)
                                     ])

    class Meta:
        ordering = ['sale', 'product', 'quantity', 'total_product', 'commission', 'percentage_commission']
        verbose_name = 'item'
        verbose_name_plural = 'items'
        constraints = [
            models.UniqueConstraint(fields=['sale', 'product', ], name='unique_item_sale_product'),
        ]


class Commission(ModelMixin):
    DAYS_WEEK = Weekday.days_week()
    day_week = models.PositiveSmallIntegerField(unique=True,
                                                blank=False,
                                                null=False,
                                                choices=DAYS_WEEK,
                                                verbose_name="Dia da semana",
                                                validators=[
                                                    MinValueValidator(1),
                                                    MaxValueValidator(7)
                                                ])
    min = models.PositiveSmallIntegerField(null=False,
                                           blank=False,
                                           verbose_name="Minímo",
                                           validators=[
                                               MinValueValidator(0),
                                               MaxValueValidator(10)
                                           ])
    max = models.PositiveSmallIntegerField(null=False,
                                           blank=False,
                                           verbose_name="Máximo",
                                           validators=[
                                               MinValueValidator(0),
                                               MaxValueValidator(10)
                                           ])

    def __str__(self):
        return f"{self.day_week} - min -> {self.min}% / max -> {self.max}%"

    class Meta:
        ordering = ['day_week', 'min', 'max']
        verbose_name = 'commission'
        verbose_name_plural = 'commissions'


from sales.signals import update_fields_item

pre_save.connect(update_fields_item, sender=Item)
