# Generated by Django 5.1.1 on 2024-10-05 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_alter_flowers_price_new'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categorys'},
        ),
        migrations.AlterModelOptions(
            name='flowers',
            options={'verbose_name': 'Flower', 'verbose_name_plural': 'Flowers'},
        ),
        migrations.AlterModelOptions(
            name='flowerstype',
            options={'verbose_name': 'Flowers Type', 'verbose_name_plural': 'Flowers Types'},
        ),
    ]
