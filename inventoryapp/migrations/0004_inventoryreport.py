# Generated by Django 5.1.2 on 2024-10-31 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0003_rename_product_id_inventory_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_data', models.JSONField()),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
