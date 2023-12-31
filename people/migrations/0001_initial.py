# Generated by Django 3.2.21 on 2023-10-05 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='Telefone')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
                'ordering': ['name', 'email', 'phone'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('people_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='people.people')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'customers',
            },
            bases=('people.people',),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('people_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='people.people')),
            ],
            options={
                'verbose_name': 'seller',
                'verbose_name_plural': 'sellers',
            },
            bases=('people.people',),
        ),
    ]
