# Generated by Django 2.2.8 on 2020-11-04 06:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_order_size_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='size_color',
            new_name='Product_Colors',
        ),
        migrations.AddField(
            model_name='order',
            name='Product_Size',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
    ]
