# Generated by Django 2.2.8 on 2020-10-31 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gift', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Product_Size',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
