# Generated by Django 4.2 on 2023-11-23 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_stock_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]