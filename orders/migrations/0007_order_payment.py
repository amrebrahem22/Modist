# Generated by Django 3.0 on 2019-12-15 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0005_remove_address_payment'),
        ('orders', '0006_auto_20191214_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='addresses.Payment'),
        ),
    ]
