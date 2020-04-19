# Generated by Django 3.0.4 on 2020-04-19 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0011_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=10),
        ),
    ]