# Generated by Django 2.2.8 on 2020-10-20 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Courier',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
