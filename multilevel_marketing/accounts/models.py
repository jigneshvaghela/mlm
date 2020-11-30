import uuid
import random, string
from django.db import models
from colorfield.fields import ColorField
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.contrib.auth.models import User
import base64
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import F,Sum

class Profile(models.Model):
    """ Default profile """

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile',on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=300, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    otp=models.CharField(max_length=300, blank=True, null=True,unique=True)
    cart = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to='media/', default='profile.png', null=True)


    def get_absolute_url(self):
        return u'/profile/show/%d' % self.id
    def generate_verification_code(self):
        # Generate user's verification code
        # TODO: Move this to the model
        return uuid.uuid1()

    def save(self, *args, **kwargs):
        """
        If this is a new user, generate code.
        Otherwise leave as is
        """
        if not self.pk:
            self.referral_code = self.generate_verification_code()
        return super(Profile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)

# Create your models here.
class ImageModel(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    image = models.ImageField(blank = False, null = False)

class Categlory(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    CategloryName=models.CharField(max_length=2000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Categlorycreateuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.CategloryName)


class Colors(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    ColorsName=ColorField(default='#FF0000')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Colorscreateuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.ColorsName)


class Brands(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    BrandsName=models.CharField(max_length=2000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Brandscreateuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.BrandsName)

class Material(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    MaterialName=models.CharField(max_length=2000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Materialcreateuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.MaterialName)

class Image_Video(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Image=models.ImageField(upload_to='product_image/', max_length=254)
    Image_Product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='Image_Productss')  
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Image_Video')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.Image)



post_save.connect(create_user_profile, sender=User)

class Product(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Image=models.ImageField(upload_to='product_image/', max_length=254)
    Product_Name=models.CharField(max_length=1000)
    Product_Description=models.CharField(max_length=1000)
    Price=models.IntegerField()
    Discount_Price=models.IntegerField(default=0)
    Availability=models.PositiveIntegerField(default=0)
    New_Arrivals=models.BooleanField(default=0,null=True)
    Deals_of_day=models.BooleanField(default=0,null=True)
    Coming_soon=models.BooleanField(default=0,null=True)
    Courier_charge=models.CharField(max_length=1000,null=True)
    Product_Filter_Name=models.ForeignKey('Product_fliters',on_delete=models.CASCADE,null=True,related_name='Product_Filter_Namesssssss')    
    Product_Material=models.ForeignKey(Material,on_delete=models.CASCADE,related_name='Product_Materialss')
    Product_Categlory=models.ForeignKey(Categlory,on_delete=models.CASCADE,related_name='Product_Categloryuser')
    Product_Brands=models.ForeignKey(Brands,on_delete=models.CASCADE,related_name='Product_Brandsuser')   
    Product_Colors=models.ManyToManyField('Colors',related_name='Product_Colorsuser')
    Product_Size=models.ManyToManyField('Size',related_name='Product_Sizeuser')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Sizecreated_user')
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
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Dcreated_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.Manufacturing)




class Size(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Product_Size=models.CharField(max_length=2000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Sizecreateuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return str(self.Product_Size)


class Product_fliters(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Name=models.CharField(max_length=10000)
    parent = models.ForeignKey("self", null=True, blank="True",on_delete=models.CASCADE,related_name='parentsss')
    Categlory=models.ManyToManyField('Categlory',related_name='Categlory_Colorsuser')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Product_flitersss')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
   
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.Name)

    def children(self):
        return Product_fliters.objects.filter(parent=self)




class User_Wishlist(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Product=models.CharField(max_length=500)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Wishcreated_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


class User_Address(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    landmark=models.CharField(max_length=2500)
    address=models.CharField(max_length=2500)
    country=models.CharField(max_length=250)
    state=models.CharField(max_length=250)
    city=models.CharField(max_length=250)
    pincode=models.CharField(max_length=10, default="43701")
    default=models.BooleanField(default=0)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='UserAddress_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


class member(models.Model):
    parent=models.ForeignKey(User,on_delete=models.CASCADE,related_name='parent_user')
    child=models.ForeignKey(User,on_delete=models.CASCADE,related_name='child_user')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='member_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

class caseback(models.Model):
    no_of_member=models.IntegerField()
    amount=models.FloatField()
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='caseback_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

class caseback_data_member(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='caseback_data_user')
    amount=models.FloatField()
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='casebackdata_user')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

class Faq(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    question=models.CharField(max_length=10000)
    answer=models.CharField(max_length=10000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Faq')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    
class Send_message(models.Model):  
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    name=models.CharField(max_length=10000)
    email = models.EmailField(max_length = 254) 
    message=models.CharField(max_length=10000)    

class Contact_details(models.Model):  
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    phone=models.CharField(max_length=10000)
    phone2=models.CharField(max_length=10000)
    hours=models.CharField(max_length=10000)
    email = models.EmailField(max_length = 254) 
    address=models.CharField(max_length=10000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Contact_details')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)     

class About(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    image = models.ImageField(upload_to='media/', default='profile.png', null=True)
    description=models.CharField(max_length=10000)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='About')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True) 

class Account_address(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    Account_Number=models.CharField(max_length=10000)
    UPI=models.CharField(max_length=10000)
    IFSC=models.CharField(max_length=10000)
    Contact_Number=models.CharField(max_length=1000)
    Created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Account_address')