# Generated by Django 5.1.2 on 2024-10-30 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0002_rename_product_inventory_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='product_id',
            new_name='product',
        ),
    ]