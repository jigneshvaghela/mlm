# Generated by Django 2.2.8 on 2020-10-15 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categlory',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('CategloryName', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_user', models.PositiveIntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_user', models.PositiveIntegerField(blank=True, null=True)),
                ('deleted', models.DateTimeField(auto_now=True, null=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jjj', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('Image', models.ImageField(max_length=254, upload_to='product_image/')),
                ('Product_Name', models.CharField(max_length=1000)),
                ('Product_Description', models.CharField(max_length=1000)),
                ('Price', models.IntegerField()),
                ('Discount_Price', models.IntegerField(default=0)),
                ('Availability', models.PositiveIntegerField(default=0)),
                ('New_Arrivals', models.BooleanField(default=0, null=True)),
                ('Deals_of_day', models.BooleanField(default=0, null=True)),
                ('Courier_charge', models.CharField(max_length=1000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_user', models.PositiveIntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('Product_Categlory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMesddd', to='medicines.Categlory')),
            ],
        ),
        migrations.CreateModel(
            name='SubCateglory',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('SubCategloryName', models.CharField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_user', models.PositiveIntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_user', models.PositiveIntegerField(blank=True, null=True)),
                ('deleted', models.DateTimeField(auto_now=True, null=True)),
                ('CategloryName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Prff', to='medicines.Categlory')),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMesddf', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Description',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('Product_Description', models.CharField(max_length=10000)),
                ('Manufacturing', models.CharField(max_length=10000)),
                ('Weight', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_user', models.PositiveIntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMes', to='medicines.Product')),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMesDcreated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='Product_SubCateglory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMeshg', to='medicines.SubCateglory'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMesscreated_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Image_Video',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('Image', models.ImageField(max_length=254, upload_to='product_image/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_user', models.PositiveIntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_user', models.PositiveIntegerField(blank=True, null=True)),
                ('deleted', models.DateTimeField(auto_now=True, null=True)),
                ('Image_Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMesddffffwww', to='medicines.Product')),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductMesddffff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
