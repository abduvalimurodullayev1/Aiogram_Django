# Generated by Django 5.1.3 on 2024-12-04 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_category_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='d_latitude',
            new_name='delivery_latitude',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='d_longitude',
            new_name='delivery_longitude',
        ),
    ]