from django.contrib import admin
from django.contrib.auth.models import User
from . import models
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','date','subtotal']
    list_filter = ('quantity',)
    search_fields = ('product','user','quantity','date','subtotal')
    ordering = ['product','user','quantity','date','subtotal']

admin.site.register(models.Order,OrderAdmin)