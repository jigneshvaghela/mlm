
from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Categlory)
admin.site.register(models.Type)

admin.site.register(models.Product)
admin.site.register(models.Product_fliters)
admin.site.register(models.Image_Video)
admin.site.register(models.Product_Description)