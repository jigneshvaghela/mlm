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
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Categlorygiftcreateuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.CategloryName)




class Type(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    BrandsName=models.CharField(max_length=2000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Brandsgiftcreateuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.BrandsName)



class Image_Video(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Image=models.ImageField(upload_to='product_image/', max_length=254)
    Image_Product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='giftImage_Productss')  
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='giftImage_Video')
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
    Coming_soon=models.BooleanField(default=0,null=True)
    Courier_charge=models.CharField(max_length=1000,null=True)
    Product_Filter_Name=models.ForeignKey('Product_fliters',on_delete=models.CASCADE,null=True,related_name='Product_Filter_Namesssssss')    
    Product_Categlory=models.ForeignKey(Categlory,on_delete=models.CASCADE,related_name='giftProduct_Categloryuser')
    Product_Type=models.ForeignKey(Type,on_delete=models.CASCADE,related_name='giftProduct_Brandsuser')   
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='giftSizecreated_user')
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
    Product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='ProductDes')
    Matrial_detail=models.CharField(max_length=10000) 
    Proof=models.CharField(max_length=100)
    Samples=models.CharField(max_length=10000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='giftDcreated_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.Manufacturing)





class Product_fliters(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Name=models.CharField(max_length=10000)
    parent = models.ForeignKey("self", null=True, blank="True",on_delete=models.CASCADE,related_name='giftparentsss')
    Categlory=models.ManyToManyField('Categlory',related_name='giftCateglory_Colorsuser')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='giftProduct_flitersss')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
   
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.Name)

    def children(self):
        return Product_fliters.objects.filter(parent=self)


