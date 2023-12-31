# Generated by Django 3.2.21 on 2023-10-06 19:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='uuid')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('day_week', models.PositiveSmallIntegerField(choices=[(1, 'Segunda-feira'), (2, 'Terça-feira'), (3, 'Quarta-feira'), (4, 'Quinta-feira'), (5, 'Sexta-feira'), (6, 'Sábado'), (7, 'Domingo')], unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)], verbose_name='Dia da semana')),
                ('min', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Minímo')),
                ('max', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Máximo')),
            ],
            options={
                'verbose_name': 'commission',
                'verbose_name_plural': 'commissions',
                'ordering': ['day_week', 'min', 'max'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantidade')),
                ('unitary_price_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Preço unitário com comissão')),
                ('total_product', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Total do produto')),
                ('percentage_commission', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='% de Comissão')),
                ('commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Comissão')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Produto/Serviço')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ['sale', 'product', 'quantity', 'total_product', 'commission', 'percentage_commission'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('invoice', models.BigAutoField(editable=False, primary_key=True, serialize=False, verbose_name='Código da venda')),
                ('date_sale', models.DateTimeField(verbose_name='Data/Hora da venda')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.client', verbose_name='Cliente')),
                ('items', models.ManyToManyField(through='sales.Item', to='products.Product', verbose_name='Itens')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.seller', verbose_name='Vendedor')),
            ],
            options={
                'verbose_name': 'sale',
                'verbose_name_plural': 'sales',
                'ordering': ['invoice', 'date_sale', 'seller', 'client'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sale', verbose_name='Venda'),
        ),
        migrations.AddConstraint(
            model_name='item',
            constraint=models.UniqueConstraint(fields=('sale', 'product'), name='unique_item_sale_product'),
        ),
    ]
