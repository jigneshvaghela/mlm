import uuid
import random, string
from django.db import models
from colorfield.fields import ColorField
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.contrib.auth.models import User
import base64
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Categlory(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    CategloryName=models.CharField(max_length=2000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='jjj')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.CategloryName)


class SubCateglory(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    SubCategloryName=models.CharField(max_length=2000)
    CategloryName=models.ForeignKey('Categlory',on_delete=models.CASCADE,related_name='Prff')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ProductMesddf')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.CategloryName)



class Image_Video(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Image=models.ImageField(upload_to='product_image/', max_length=254)
    Image_Product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='ProductMesddffffwww')  
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ProductMesddffff')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.Image)



class Product(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Image=models.ImageField(upload_to='product_image/', max_length=254)
    Product_Name=models.CharField(max_length=1000)
    Product_Description=models.CharField(max_length=1000)
    Price=models.IntegerField()
    Discount_Price=models.IntegerField(default=0)
    Product_Size=models.PositiveIntegerField(default=0)
    Product_Colors=models.PositiveIntegerField(default=0)
    Availability=models.PositiveIntegerField(default=0)
    New_Arrivals=models.BooleanField(default=0,null=True)
    Deals_of_day=models.BooleanField(default=0,null=True)
    Courier_charge=models.CharField(max_length=1000,null=True)
    # Coming_soon=models.BooleanField(default=0,null=True)
    Product_Categlory=models.ForeignKey(Categlory,on_delete=models.CASCADE,related_name='ProductMesddd')
    Product_SubCateglory=models.ForeignKey(SubCateglory,on_delete=models.CASCADE,related_name='ProductMeshg')   
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ProductMesscreated_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.Product_Name)



class Product_Description(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Product_Description=models.CharField(max_length=10000) 
    Manufacturing=models.CharField(max_length=10000) ######we can also put dropdown all country ##############  
    Weight=models.FloatField() 
    Product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='ProductMes')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ProductMesDcreated_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.Manufacturing)

