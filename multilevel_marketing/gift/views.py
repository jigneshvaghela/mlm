from functools import reduce
from django.core.paginator import Paginator
import json
import ast
from operator import or_
from django.http import JsonResponse
from django.shortcuts import render
from . import models
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage,BadHeaderError,EmailMultiAlternatives
from django.http import HttpResponse,HttpResponseRedirect
from multilevel_marketing import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.forms import model_to_dict


from medicines import models as medicines_model
from accounts import models as accounts_model
from django.contrib import messages
from django.views.generic import RedirectView
# from .filters import UserFilter  
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse



# Create your views here.
@login_required(login_url="/login")
def category(request):
    # user_ = None
    # wishlisted_list =[]
    # if request.user.is_authenticated:
    #     user=request.user.id
    #     # user_ = get_object_or_404(models.Profile, user_id=user)
    #     wishlisted_list = list(models.User_Wishlist.objects.filter(created_user=request.user).values_list('Product_id',flat=True).order_by('Product'))
    #     wishlist = models.User_Wishlist.objects.filter(created_user=request.user.id)
    #     print(user_.referral_code)
        
    showcartandserch = True
    cart_item_count=None
    all_items=None
    total_price=None
    total_count=0
    if 'cart' in request.session:
        all_items = []
        total_count = 0
        total_price = 0
        
        for prod_id, quantity in request.session['cart'].items():
            total_count += quantity
            
            item = models.Product.objects.get(id=prod_id)
            all_items.append({
                'Product_Name': item.Product_Name,
                'Price': item.Price,
                'quantity': quantity,
                'sub_total': item.Price * quantity,
            })
            total_price += item.Price * quantity
        
    ##################cloths    
    CategloryS=accounts_model.Categlory.objects.all()
    BrandsS=accounts_model.Brands.objects.all()
    Colorss=accounts_model.Colors.objects.all()
    ParentTrue=accounts_model.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=accounts_model.Product_fliters.objects.filter(parent__isnull=False)
    # Sizes=models.Size.objects.all()
       
    #####################filtering
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Type.objects.all()



    #####################gift###########
    giftCategloryS=models.Categlory.objects.all()

    giftParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)   
    giftTypeS=models.Type.objects.all()
            
        
    TypeS=models.Type.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    Products=models.Product.objects.all().order_by('-Price') 
    my_products1=models.Product.objects.all().count() 
    a=models.Product.objects.all().order_by('Price') 
    ProductDescription=models.Product_Description.objects.all()
    ###################end##############
    
    #######medicines###############
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()
    ##########endif###############

    paginator = Paginator(Products, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    context={'type':'gift','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,
    'ParentTrue':ParentTrue,'ParentFalse':ParentFalse,'giftCategloryS':giftCategloryS,
    'giftParentTrue':giftParentTrue,'giftTypeS':giftTypeS,'TypeS':TypeS,'Image_Videos':Image_Videos,
    'ProductDescription':ProductDescription,
    'medicateC':medicateC,'medicateS':medicateS,
    'showcartandserch':showcartandserch,'cart_item_count': total_count,'all_items' : all_items,
    'total_price': total_price,'page_obj':page_obj,
    'a':a,}
    

    
    if request.method == "POST": #os request.GET()
        get_value= request.body
        # Do your logic here coz you got data in `get_value`
        data={}
        # data = self.get_queryset()
        
        data['result'] = serializers.serialize('json', models.Product.objects.filter(Price=1111),fields=('Product_Name'))
        # data['result'] = models.Product.objects.all().order_by('-Price')
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request,'category.html',context)
@login_required(login_url="/login")
def product(request,id):
    Products=models.Product.objects.all()    
    ProductDetails=models.Product.objects.get(id=id)   
    Imageproduct=models.Image_Video.objects.filter(Image_Product=id)
    ProductDescription=models.Product_Description.objects.filter(Product=id)
    CategloryS=models.Categlory.objects.all()
    TypeS=models.Type.objects.all()
    a=models.Product.objects.all().order_by('Price') 
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()

    paginator = Paginator(Products, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'CategloryS':CategloryS,'TypeS':TypeS,'medicateC':medicateC,'medicateS':medicateS,'ProductDescription':ProductDescription,'ProductDetails':ProductDetails,'Imageproduct':Imageproduct,'page_obj':page_obj,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
    return render(request,'product.html',context)

@login_required(login_url="/login")
def Categloryfilter(request,id):  
    showcartandserch = True
    cart_item_count=None
    all_items=None
    total_price=None
    total_count=0
    if 'cart' in request.session:
        all_items = []
        total_count = 0
        total_price = 0
        
        for prod_id, quantity in request.session['cart'].items():
            total_count += quantity
            
            item = models.Product.objects.get(id=prod_id)
            all_items.append({
                'Product_Name': item.Product_Name,
                'Price': item.Price,
                'quantity': quantity,
                'sub_total': item.Price * quantity,
            })
            total_price += item.Price * quantity
        


    ##################cloths    
    CategloryS=accounts_model.Categlory.objects.all()
    BrandsS=accounts_model.Brands.objects.all()
    Colorss=accounts_model.Colors.objects.all()
    ParentTrue=accounts_model.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=accounts_model.Product_fliters.objects.filter(parent__isnull=False)
    # Sizes=models.Size.objects.all()
       
    #####################gift###########
    giftCategloryS=models.Categlory.objects.all()

    giftParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)   
    giftTypeS=models.Type.objects.all()
            
        
    TypeS=models.Type.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    Products=models.Product.objects.filter(Product_Categlory=id) 
    my_products1=models.Product.objects.filter(Product_Categlory=id).count()
    a=models.Product.objects.all().order_by('Price') 
    ProductDescription=models.Product_Description.objects.all()
    ###################end##############
    
    ###################filter###
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Type.objects.all()
    ################end#########



    #######medicines###############
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()
    ##########endif###############

    paginator = Paginator(Products, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    context={'type':'gift','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,
    'ParentTrue':ParentTrue,'ParentFalse':ParentFalse,'giftCategloryS':giftCategloryS,
    'giftParentTrue':giftParentTrue,'giftTypeS':giftTypeS,'TypeS':TypeS,'Image_Videos':Image_Videos,
    'ProductDescription':ProductDescription,
    'medicateC':medicateC,'medicateS':medicateS,
    'showcartandserch':showcartandserch,'cart_item_count': total_count,'all_items' : all_items,
    'total_price': total_price,'page_obj':page_obj,
    'a':a,}
    


    # Products=models.Product.objects.filter(Product_Categlory=id) 
    # ProductDescription=models.Product_Description.objects.all()
    # Image_Videos=models.Image_Video.objects.all()
    # CategloryS=models.Categlory.objects.all()
    # TypeS=models.Type.objects.all()
    
    # a=models.Product.objects.all().order_by('Price') 
    # ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    # ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    # medicateC=medicines_model.Categlory.objects.all()
    # medicateS=medicines_model.SubCateglory.objects.all()

    # paginator = Paginator(Products, 3) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # context={'CategloryS':CategloryS,'TypeS':TypeS,'Image_Videos':Image_Videos,'medicateC':medicateC,'medicateS':medicateS,'ProductDescription':ProductDescription,'page_obj':page_obj,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
      
    return render(request,'category.html',context)

@login_required(login_url="/login")
def Typefilter(request,id): 
    showcartandserch = True
    cart_item_count=None
    all_items=None
    total_price=None
    total_count=0
    if 'cart' in request.session:
        all_items = []
        total_count = 0
        total_price = 0
        
        for prod_id, quantity in request.session['cart'].items():
            total_count += quantity
            
            item = models.Product.objects.get(id=prod_id)
            all_items.append({
                'Product_Name': item.Product_Name,
                'Price': item.Price,
                'quantity': quantity,
                'sub_total': item.Price * quantity,
            })
            total_price += item.Price * quantity
        


    ##################cloths    
    CategloryS=accounts_model.Categlory.objects.all()
    BrandsS=accounts_model.Brands.objects.all()
    Colorss=accounts_model.Colors.objects.all()
    ParentTrue=accounts_model.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=accounts_model.Product_fliters.objects.filter(parent__isnull=False)
    # Sizes=models.Size.objects.all()
       
    #####################gift###########
    giftCategloryS=models.Categlory.objects.all()

    giftParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)   
    giftTypeS=models.Type.objects.all()
            
        
    TypeS=models.Type.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    Products=models.Product.objects.filter(Product_Type=id) 
    my_products1=models.Product.objects.filter(Product_Type=id).count() 
    a=models.Product.objects.all().order_by('Price') 
    ProductDescription=models.Product_Description.objects.all()
    ###################end##############
    
    ###################filter###
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Type.objects.all()
    ################end#########


    #######medicines###############
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()
    ##########endif###############

    paginator = Paginator(Products, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    context={'type':'gift','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,
    'ParentTrue':ParentTrue,'ParentFalse':ParentFalse,'giftCategloryS':giftCategloryS,
    'giftParentTrue':giftParentTrue,'giftTypeS':giftTypeS,'TypeS':TypeS,'Image_Videos':Image_Videos,
    'ProductDescription':ProductDescription,
    'medicateC':medicateC,'medicateS':medicateS,
    'showcartandserch':showcartandserch,'cart_item_count': total_count,'all_items' : all_items,
    'total_price': total_price,'page_obj':page_obj,
    'a':a,}



    # Products=models.Product.objects.filter(Product_Type=id)
    # request.session["Product_Colors"] = id
    # ProductDescription=models.Product_Description.objects.all()
    # Image_Videos=models.Image_Video.objects.all()
    # CategloryS=models.Categlory.objects.all()
    # TypeS=models.Type.objects.all()
    # a=models.Product.objects.all().order_by('Price') 
    # ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    # ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    # medicateC=medicines_model.Categlory.objects.all()
    # medicateS=medicines_model.SubCateglory.objects.all()

    # paginator = Paginator(Products, 10) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # context={'CategloryS':CategloryS,'TypeS':TypeS,'Image_Videos':Image_Videos,'medicateC':medicateC,'medicateS':medicateS,'page_obj':page_obj,'ProductDescription':ProductDescription,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
       
    return render(request,'category.html',context)

@login_required(login_url="/login")
def Stylefilter(request,id):     
    showcartandserch = True
    cart_item_count=None
    all_items=None
    total_price=None
    total_count=0
    if 'cart' in request.session:
        all_items = []
        total_count = 0
        total_price = 0
        
        for prod_id, quantity in request.session['cart'].items():
            total_count += quantity
            
            item = models.Product.objects.get(id=prod_id)
            all_items.append({
                'Product_Name': item.Product_Name,
                'Price': item.Price,
                'quantity': quantity,
                'sub_total': item.Price * quantity,
            })
            total_price += item.Price * quantity
        


    ##################cloths    
    CategloryS=accounts_model.Categlory.objects.all()
    BrandsS=accounts_model.Brands.objects.all()
    Colorss=accounts_model.Colors.objects.all()
    ParentTrue=accounts_model.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=accounts_model.Product_fliters.objects.filter(parent__isnull=False)
    # Sizes=models.Size.objects.all()
       
    #####################gift###########
    giftCategloryS=models.Categlory.objects.all()

    giftParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)   
    giftTypeS=models.Type.objects.all()
            
        
    TypeS=models.Type.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    Products=models.Product.objects.filter(Product_Filter_Name=id)  
    my_products1=models.Product.objects.filter(Product_Filter_Name=id).count()
    print('ffffffffffffffffffffffffffffffffffffffffffffff',my_products1) 
    a=models.Product.objects.all().order_by('Price') 
    ProductDescription=models.Product_Description.objects.all()
    ###################end##############
    
    ###################filter###
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Type.objects.all()
    ################end#########

    #######medicines###############
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()
    ##########endif###############

    paginator = Paginator(Products, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    context={'type':'gift','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,
    'ParentTrue':ParentTrue,'ParentFalse':ParentFalse,'giftCategloryS':giftCategloryS,
    'giftParentTrue':giftParentTrue,'giftTypeS':giftTypeS,'TypeS':TypeS,'Image_Videos':Image_Videos,
    'ProductDescription':ProductDescription,
    'medicateC':medicateC,'medicateS':medicateS,
    'showcartandserch':showcartandserch,'cart_item_count': total_count,'all_items' : all_items,
    'total_price': total_price,'page_obj':page_obj,
    'a':a,}
    





    # Products=models.Product.objects.filter(Product_Filter_Name=id) 
    # ProductDescription=models.Product_Description.objects.all()
    # Image_Videos=models.Image_Video.objects.all()
    # CategloryS=models.Categlory.objects.all()
    # TypeS=models.Type.objects.all()

    # a=models.Product.objects.all().order_by('Price') 
    # ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    # ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    # medicateC=medicines_model.Categlory.objects.all()
    # medicateS=medicines_model.SubCateglory.objects.all()

    # paginator = Paginator(Products, 3) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # context={'CategloryS':CategloryS,'TypeS':TypeS,'Image_Videos':Image_Videos,'medicateC':medicateC,'medicateS':medicateS,'ProductDescription':ProductDescription,'page_obj':page_obj,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
      
    return render(request,'category.html',context)

@login_required(login_url="/login")
def Filter_Product(request):
    giftParentTrue=models.Product_fliters.objects.filter(parent__isnull=True) 
    
    # giftParentTrue1=gift_model.Product.objects.all()
     ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Type.objects.all()
    ##############end

    giftCategloryS=models.Categlory.objects.all()
    giftTypeS=models.Type.objects.all()
   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()
    CategloryS=accounts_model.Categlory.objects.all()
    BrandsS=accounts_model.Brands.objects.all()
    Colorss=accounts_model.Colors.objects.all()
    Sizes=accounts_model.Size.objects.all()
    Products=accounts_model.Product.objects.all().order_by('-Price') 
    Image_Videos=accounts_model.Image_Video.objects.all()
    ParentTrue=accounts_model.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=accounts_model.Product_fliters.objects.filter(parent__isnull=False)

    
    my_products=models.Product.objects.all()
    my_products1=models.Product.objects.all()
    filter_category1=''
    filter_category=''
   
    if 'Categlory' in request.GET:
       filter_category1 = request.GET.getlist('Categlory')       
       my_products = my_products.filter(Product_Categlory__in=filter_category1)
       my_products1 = my_products.filter(Product_Categlory__in=filter_category1).count()
    
    if 'Type' in request.GET:
        filter_category = request.GET.getlist('Type')       
        my_products = my_products.filter(Product_Type__in=filter_category)
        my_products1 = my_products.filter(Product_Categlory__in=filter_category1).count()
    
    # if 'Color' in request.GET:
    #    filter_category2 = request.GET.getlist('Color')       
    #    my_products = my_products.filter(Product_Colors__in=filter_category2)
   
    # if 'Size' in request.GET:
    #    filter_category4 = request.GET.getlist('Size')   
    #    my_products = my_products.filter(Product_Size__in=filter_category4)

    # if 'Product' in request.GET:
    #    filter_category6 = request.GET.getlist('Product')   
    #    my_products = my_products.filter(Product_Filter_Name__in=filter_category6)


    if 'price1' in request.GET or 'price2' in request.GET or 'price3' in request.GET or 'price4' in request.GET:
       price1 = str(request.GET.get('price1'))
       price2 = str(request.GET.get('price2'))
       price3 = str(request.GET.get('price3'))
       price4 = str(request.GET.get('price4'))
       
       a=[]
       if price1 != 'None':
            a+=price1.split('-')
       if price2 != 'None':
            a+=price2.split('-')
       if price3 != 'None':
            a+=price3.split('-')
       if price4 != 'None':
            a+=price4.split('-')
       my_products = my_products.filter(Price__range=(a[0], a[len(a)-1]))
       my_products1 = my_products.filter(Product_Categlory__in=filter_category1).count()
    #    print('===============================================================',my_products)
    paginator = Paginator(my_products, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'gift','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'Image_Videos':Image_Videos,'Sizes':Sizes,'page_obj':page_obj,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
   
    return render(request,'category.html',context)


