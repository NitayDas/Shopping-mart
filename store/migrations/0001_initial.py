# Generated by Django 5.0.6 on 2024-06-03 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(max_length=200, null=True)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('quantity', models.IntegerField(default=10)),
                ('discount', models.FloatField(default=0, max_length=100, null=True)),
                ('discount_price', models.FloatField(default=0, max_length=100, null=True)),
                ('bulk_discount_threshold', models.IntegerField(blank=True, default=0, null=True)),
                ('bulk_discount_free_items', models.IntegerField(blank=True, default=0, null=True)),
                ('free_item_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='free_item', to='store.product')),
            ],
        ),
    ]
