# Generated by Django 4.2.2 on 2023-06-29 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_alter_stock_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]
