# Generated by Django 5.0.6 on 2024-07-11 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
