# Generated by Django 4.2.2 on 2023-06-29 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_rename_timestamp_stock_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='previous_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]