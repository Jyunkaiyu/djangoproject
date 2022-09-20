# Generated by Django 4.0.6 on 2022-08-12 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='shopping_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product_name', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_nameOf', to='model.test')),
                ('username', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='usernameOf', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]