from django.db import models

from vendor.mixins.model import ModelWithoutIdMixin


class People(ModelWithoutIdMixin):
    id = models.BigAutoField(primary_key=True,
                             blank=False,
                             null=False,
                             editable=False,
                             verbose_name="Id")
    name = models.CharField(max_length=50,
                            blank=False,
                            null=False,
                            verbose_name="Nome")
    email = models.EmailField(blank=False,
                              null=False,
                              unique=True,
                              verbose_name="Email")
    phone = models.BigIntegerField(max_length=11,
                                   null=False,
                                   blank=False,
                                   unique=True,
                                   verbose_name="Telefone")

    def __str__(self):
        return f"{str(self.id).zfill(3)} - {self.name}"

    class Meta:
        ordering = ['name', 'email', 'phone']
        verbose_name = 'person'
        verbose_name_plural = 'people'


class Seller(People):

    class Meta:
        verbose_name = 'seller'
        verbose_name_plural = 'sellers'


class Client(People):

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'customers'
