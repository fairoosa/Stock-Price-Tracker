# Generated by Django 4.2.2 on 2023-06-28 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_rename_current_price_stock_current_pric'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='current_pric',
            new_name='current_price',
        ),
    ]