# Generated by Django 5.1.4 on 2024-12-09 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_cartitem_cart_alter_cartitem_options_and_more'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='sessions.session'),
        ),
    ]