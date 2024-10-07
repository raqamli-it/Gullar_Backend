# Generated by Django 5.1.1 on 2024-10-05 12:59

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlowersType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_type/')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flowers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price_old', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_new', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_time', models.CharField(blank=True, max_length=50, null=True)),
                ('delivery_price', models.CharField(blank=True, max_length=50, null=True)),
                ('product_composition', models.CharField(blank=True, max_length=150, null=True)),
                ('discount', models.BooleanField(default=False)),
                ('discount_percent', models.IntegerField(blank=True, null=True)),
                ('desc', models.TextField(blank=True, default='', null=True)),
                ('ready', models.BooleanField(default=False)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='data.category')),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='market', to=settings.AUTH_USER_MODEL)),
                ('flowers_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flowers_type', to='data.flowerstype')),
            ],
        ),
    ]
