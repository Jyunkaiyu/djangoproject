# Generated by Django 4.0.6 on 2022-08-17 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0005_rename_count_shopping_cart_counts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopping_cart',
            name='counts',
            field=models.IntegerField(default=1),
        ),
    ]
