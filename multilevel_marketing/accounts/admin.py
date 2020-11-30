from django.contrib import admin
from django.contrib.auth.models import User
from . import models
# Register your models here.



# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'author', 'publish', 'status')
#     list_filter = ('status', 'created', 'publish', 'author')
#     search_fields = ('title', 'body')
#     raw_id_fields = ('author')
#     date_hierarchy = ('publish')
#     ordering = ['status', 'publish']

class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['image']
    search_fields = ('image',)
    ordering = ['image',]
    # list_display_links = ('created_user',)
    # list_editable = ('description',)

class CategloryAdmin(admin.ModelAdmin):
    list_display = ['CategloryName','created_user']
    list_filter = ('created_user', 'CategloryName')
    search_fields = ('CategloryName',)
    ordering = ['CategloryName']
    list_display_links = ('created_user',)
    list_editable = ('CategloryName',)

class BrandsAdmin(admin.ModelAdmin):
    list_display = ['BrandsName','created_user']
    list_filter = ('created_user', 'BrandsName')
    search_fields = ('BrandsName',)
    ordering = ['BrandsName']
    list_display_links = ('created_user',)
    list_editable = ('BrandsName',)

class ColorsAdmin(admin.ModelAdmin):
    list_display = ['ColorsName','created_user']
    list_filter = ('created_user', 'ColorsName')
    search_fields = ('ColorsName',)
    ordering = ['ColorsName']
    list_display_links = ('created_user',)
    list_editable = ('ColorsName',) 

class ProductAdmin(admin.ModelAdmin):
    list_display = ['Product_Name','Price','Discount_Price','Availability','Product_Categlory','Product_Brands']
    list_filter = ('Product_Categlory', 'Product_Brands')
    search_fields = ('Product_Name','Product_Categlory','Product_Brands','Availability')
    ordering = ['Availability','Discount_Price','Price']
    list_display_links = ('Product_Name',) 
    list_editable = ('Discount_Price','Price','Availability',)

class SizeAdmin(admin.ModelAdmin):
    list_display = ['created_user','Product_Size',]
    list_filter = ('created_user', 'Product_Size')
    search_fields = ('Product_Size',)
    ordering = ['Product_Size']
    # list_display_links = ('ColorsName',) 
    list_editable = ('Product_Size',)

class Product_flitersAdmin(admin.ModelAdmin):
    list_display = ['Name','parent','created_user']
    list_filter = ('Name','Categlory')
    search_fields = ('Categlory','Name','parent')
    ordering = ['parent','Categlory']
    list_display_links = ('created_user',) 
    list_editable = ('parent','Name')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['MaterialName','created_user']
    list_filter = ('created_user', 'MaterialName')
    search_fields = ('MaterialName',)
    ordering = ['MaterialName']
    list_display_links = ('created_user',)  
    list_editable = ('MaterialName',) 

class Image_VideoAdmin(admin.ModelAdmin):
    list_display = ['Image','Image_Product','created_user']
    list_filter = ('created_user',)
    search_fields = ('Image_Product',)
    ordering = ['Image_Product']
    list_display_links = ('created_user',)  
    list_editable = ('Image_Product',) 


class Product_DescriptionAdmin(admin.ModelAdmin):
    list_display = ['Product','Manufacturing','Weight']
    list_filter = ('Manufacturing',)
    search_fields = ('Manufacturing','Product')
    ordering = ['Manufacturing','Product']
    list_display_links = ('Weight',)  
    list_editable = ('Manufacturing',) 


class memberAdmin(admin.ModelAdmin):
    list_display = ['parent','child','created_user']
    list_filter = ('parent', 'child')
    search_fields = ('parent','child',)
    ordering = ['parent','child',]
    


class casebackAdmin(admin.ModelAdmin):
    list_display = ['no_of_member','amount','created_user']
    list_filter = ('created_user', 'no_of_member')
    search_fields = ('no_of_member','amount')
    ordering = ['no_of_member','amount']
    

class caseback_data_memberAdmin(admin.ModelAdmin):
    list_display = ['user','amount','created_user']
    list_filter = ('created_user', 'amount')
    search_fields = ('user','amount',)
    ordering = ['user','amount',]
    list_display_links = ('created_user',)  
    
class Contact_detailsAdmin(admin.ModelAdmin):
    list_display = ['phone','hours','address','email','created_user']
    list_filter = ('created_user',)
    search_fields = ('address',)
    ordering = ['hours','phone']
    list_display_links = ('created_user',)  
    list_editable = ('phone','hours','address','email',) 

class FaqAdmin(admin.ModelAdmin):
    list_display = ['question','answer','created_user']
    list_filter = ('created_user',)
    search_fields = ('question','answer',)
    ordering = ['question','answer']
    list_display_links = ('created_user',)  
    list_editable = ('question','answer',) 

class AboutAdmin(admin.ModelAdmin):
    list_display = ['image','description','created_user']
    list_filter = ('created_user',)
    search_fields = ('description','created_user')
    ordering = ['image','description']
    list_display_links = ('created_user',)  
    list_editable = ('image','description',) 


class Send_messageAdmin(admin.ModelAdmin):
    list_display = ['name','email','message']
    list_filter = ('email',)
    search_fields = ('name','email','message')
    ordering = ['email','message']
     

class User_AddressAdmin(admin.ModelAdmin):
    list_display = ['landmark','country','city','state','default','pincode']
    list_filter = ('country','city','state')
    search_fields = ('landmark','country','city','state','default','pincode')
    ordering = ['landmark','country','city','state','default','pincode']
   

class User_WishlistAdmin(admin.ModelAdmin):
    list_display = ['Product','created_user']
    list_filter = ('created_user',)
    search_fields = ('description','Product')
    ordering = ['Product','created_user']
    
   


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','referral_code','otp','cart']
    list_filter = ('cart',)
    search_fields = ('user','referral_code','otp','cart')
    ordering = ['user','referral_code','otp','cart']
         


admin.site.register(models.ImageModel,ImageModelAdmin)
admin.site.register(models.Categlory, CategloryAdmin)
admin.site.register(models.Brands,BrandsAdmin)
admin.site.register(models.Colors,ColorsAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Size,SizeAdmin)
admin.site.register(models.Product_fliters,Product_flitersAdmin)
admin.site.register(models.Material,MaterialAdmin)
admin.site.register(models.Image_Video,Image_VideoAdmin)
admin.site.register(models.Product_Description,Product_DescriptionAdmin)
admin.site.register(models.member,memberAdmin)
admin.site.register(models.caseback,casebackAdmin)
admin.site.register(models.caseback_data_member,caseback_data_memberAdmin)
admin.site.register(models.Contact_details,Contact_detailsAdmin)
admin.site.register(models.Faq,FaqAdmin)
admin.site.register(models.About,AboutAdmin)

admin.site.register(models.Send_message,Send_messageAdmin)
admin.site.register(models.User_Address,User_AddressAdmin)
admin.site.register(models.User_Wishlist,User_WishlistAdmin)

admin.site.register(models.Profile,ProfileAdmin)





