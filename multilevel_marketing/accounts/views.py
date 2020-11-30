from functools import reduce
from django.core.paginator import Paginator
from itertools import chain
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
from .tokens import account_activation_token
from django.core.mail import EmailMessage,BadHeaderError,EmailMultiAlternatives
from django.http import HttpResponse,HttpResponseRedirect
from multilevel_marketing import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.forms import model_to_dict
from gift import models as gift_model
from medicines import models as medicines_model
from django.contrib import messages
from django.views.generic import RedirectView
from django.core.mail import send_mail,send_mass_mail,mail_admins,mail_managers

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
from gift import models  as gifts
from medicines import models as medicine
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

import random,os
import http.client

def search(request):
    if request.method == 'GET':
        query= request.GET.get('q')
      
        if query is not None:
            lookups= Q(Product_Name__icontains=query) | Q(Product_Categlory=query)| Q(Product_Description__icontains=query)| Q(Price__icontains=query)

            Products1= models.Product.objects.filter(lookups).distinct()
            Products2= gift_model.Product.objects.filter(lookups).distinct()
            Products3= medicines_model.Product.objects.filter(lookups).distinct()
            Products = list(chain(Products1, Products2,Products3))
            CategloryS=models.Categlory.objects.all()
            BrandsS=models.Brands.objects.all()
            Colorss=models.Colors.objects.all()
            Sizes=models.Size.objects.all()
            Image_Videos=models.Image_Video.objects.all()
            print('Productsddddddddddddddd',Products)
            a=models.Product.objects.all().order_by('Price') 
            ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
            ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)
            ProductDescription=models.Product_Description.objects.all()

            giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
            # giftParentTrue1=gift_model.Product.objects.all()
        

            giftCategloryS=gift_model.Categlory.objects.all()
            giftTypeS=gift_model.Type.objects.all()
        
            medicateC=medicines_model.Categlory.objects.all()
            medicateS=medicines_model.SubCateglory.objects.all()


            paginator = Paginator(Products, 30) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context={'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss,'Sizes':Sizes,'page_obj':page_obj,'ProductDescription':ProductDescription,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse,'Image_Videos':Image_Videos}
            
            return render(request, 'filter.html', context)

        else:
            return render(request, 'filter.html')

    else:
        return render(request, 'filter.html')

@csrf_exempt
@login_required(login_url="/login")
def reference(request,id):
    Products=models.Profile.objects.filter(referral_code=id)
    return render(request,'category.html',{'Products':Products})

@csrf_exempt
@login_required(login_url="/login") 
def user_logout(request):
    if 'user' in request.session:
        del request.session['user']
    if 'cart' in request.session:
        del request.session['cart']
    logout(request)
    return redirect('accounts:index')
# Create your views here.
@csrf_exempt
def index(request):

    showcartandserch = True
    wishlisted_list =[]
    
    if request.user.is_authenticated:
        user=request.user.id
       
        
        wishlisted_list = list(models.User_Wishlist.objects.filter(created_user=request.user).values_list('Product',flat=True).order_by('Product'))
        wishlist = models.User_Wishlist.objects.filter(created_user=request.user.id)
       
       
    queryset = models.ImageModel.objects.all()
    clothproductS=models.Product.objects.filter(Deals_of_day=1)
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    q1=models.Product_fliters.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()

    Image_Videos1=models.Image_Video.objects.all()
    ProductDescription1=models.Product_Description.objects.all()

    Image_Videos2=gift_model.Image_Video.objects.all()
    ProductDescription2=gift_model.Product_Description.objects.all()
   
    Image_Videos3=medicines_model.Image_Video.objects.all()
    ProductDescription3=medicines_model.Product_Description.objects.all()

    Image_Videos = list(chain(Image_Videos1, Image_Videos2,Image_Videos3)) 
    ProductDescription = list(chain(ProductDescription1, ProductDescription2,ProductDescription3))

    clothdealC=models.Product.objects.filter(Coming_soon=1)
    giftproductC=gift_model.Product.objects.filter(Coming_soon=1)
    resultC = list(chain(clothdealC, giftproductC)) 
  
    clothdealD=models.Product.objects.filter(Deals_of_day=1)
    giftproductD=gift_model.Product.objects.filter(Deals_of_day=1)
    medicateCd=medicines_model.Product.objects.filter(Deals_of_day=1)
    resultD = list(chain(clothdealD, giftproductD,medicateCd)) 
   

    clothdealS=models.Product.objects.filter(New_Arrivals=1)
    giftproductS=gift_model.Product.objects.filter(New_Arrivals=1)
    medicateCc=medicines_model.Product.objects.filter(New_Arrivals=1)
    results = list(chain(clothdealS, giftproductS,medicateCc)) 
   
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
    giftq1=gift_model.Product_fliters.objects.all()
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()
   
    medicateC=medicines_model.Categlory.objects.all()
    print('fsdddddddddddddddddddddddd',medicateC)
    medicateS=medicines_model.SubCateglory.objects.all()
    # user_=models.Profile.objects.get(user_id=request.user)
    # 'user_':user_,
    context={'queryset' : queryset,'ParentTrue':ParentTrue,'showcartandserch':showcartandserch,'Image_Videos':Image_Videos,'ProductDescription':ProductDescription,'medicateC':medicateC,'medicateS':medicateS,'CategloryS':CategloryS,'wishlisted_list':wishlisted_list,'results':results,'resultC':resultC,'resultD':resultD,'BrandsS':BrandsS,'Colorss':Colorss,'q1':q1,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'giftq1':giftq1}
    
    return render(request,'index.html', context)
@csrf_exempt
def contact(request):
    contact_d=models.Contact_details.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'contact_d':contact_d,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        models.Send_message.objects.create(name=name,email=email,message=message)    
    return render(request,'contact.html',alert)
@csrf_exempt
def about(request):
    about=models.About.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'about':about,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}    
    return render(request,'about.html',alert)

@csrf_exempt
@login_required(login_url="/login")  
def account_addresses(request):    
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    
    u=User.objects.get(username=request.user)
    user_p=models.User_Address.objects.filter(created_user=request.user).count()
    user_ps=models.User_Address.objects.filter(created_user=request.user).values_list('default', flat=True)
    
    
    if request.method == "POST":
        address=request.POST.get('address')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        country=request.POST.get('country')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        default=request.POST.get('default') 
        if default=='on':
            default=True
        else:
            default=False
        models.User_Address.objects.create(address=address,landmark=landmark,default=default,city=city,country=country,state=state,pincode=pincode,created_user=request.user)
    
    user_data=models.User_Address.objects.filter(created_user_id=request.user)        
    context={'user_p':user_p,'user_data':user_data,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}
    return render(request,'account-addresses.html',context)

@csrf_exempt
def edit(request,id):
    user_ps=models.User_Address.objects.filter(created_user=request.user).values_list('id', flat=True)
    a=[]
    for i in user_ps:
        a.append(i)
   
    print('fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',user_ps)
    pro=models.User_Address.objects.get(id=id)
    
    if request.method == "POST":
        address=request.POST.get('address')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        country=request.POST.get('country')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode') 
        default=request.POST.get('default') 
        if default=='on':
            default=True
        else:
            default=False          
        pro.address=address
        pro.landmark=landmark
        pro.city=city
        pro.country=country
        pro.state=state
        pro.pincode=pincode
        pro.default=default
        pro.save()
        if default==True:
            a.remove(pro.id)
            pro=models.User_Address.objects.get(id=a[0])
            pro.default=False
            pro.save()
        return redirect('accounts:account_addresses')
    return render(request,'account-addresses.html',{'pro':pro})


def generate_otp():
	otp=random.randint(1000,9999)
	return otp
	
@csrf_exempt   	
def account_create(request):
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss} 
    request.session['a']=''
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        if User.objects.filter(username = request.POST['username']).exists():
            alert['message'] = "Username already exists"
        elif User.objects.filter(email = request.POST['email']).exists():
            alert['message'] = "email already exists"
        else:
            first=request.POST.get('first_name')
            last=request.POST.get('last_name')
            username=request.POST.get('username')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            password=request.POST.get('password')
            usr=User.objects.create_user(username=username,first_name=first,last_name=last,email=email,is_active = False,password=password)
            userid=User.objects.get(email=email).pk
            a=userid  
            request.set_session['a':a]
            print(request.session['a'])
            request.session['user_id'] = a
            usr11=models.Profile.objects.get(user_id= userid)
            request.session["us"] =usr11.id
            usr11.phone=phone
            usr11.save()
            mobile_no=request.POST.get('phone')
            otp=generate_otp()
            request.session['otp']=int(otp)
            conn = http.client.HTTPConnection("2factor.in")
            payload = ""
            headers = { 'content-type': "application/x-www-form-urlencoded" }
            utl_send="/API/V1/293832-67745-11e5-88de-5600000c6b13/SMS/"+str(mobile_no)+"/"+str(otp)
            conn.request("GET", "/API/V1/96077bae-0adf-11eb-9fa5-0200cd936042/SMS/"+str(mobile_no)+"/"+str(otp), payload, headers)
            res = conn.getresponse()
            data = res.read()
            try:
                mail_subject = 'Activate your account.'
                current_site = get_current_site(request)    
  
                mail_subject = 'Activate your blog account.'
                html_content = render_to_string('acc_active_email.html', {'user': usr,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(usr.pk)),
                        'token':account_activation_token.make_token(usr),})
                to_email = usr.email
                from_email=settings.EMAIL_HOST_USER       
                msg = EmailMultiAlternatives(mail_subject, mail_subject, from_email, to=[to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send() 
                userid=User.objects.get(email=email).pk
                a=userid                                        
            except  BadHeaderError:             
                ins=User.objects.get(email__exact=request.POST.get('email')).delete()              
                alert['message']="email not send"
            return redirect('accounts:EnterOTP')
    return render(request,'account-create.html',alert)

def verify(request):
    print(request.session['a'])
    usr11=models.Profile.objects.get(user_id=request.session['a'])
    user=User.objects.get(id=request.session['a'])
    if request.method=='POST':
        entered_otp=request.POST.get('otp')
        if request.session['otp']==int(entered_otp):
            user.is_active=True
            user.save()
            return HttpResponseRedirect(reverse('accounts:login'))
        else:
            return HttpResponseRedirect(reverse('accounts:EnterOTP'))
    return render(request,'EnterOTP.html',{'usr11':usr11})

@csrf_exempt
@login_required(login_url="/login")  
def personal_details(request):
    u=User.objects.get(username=request.user)
    pro=models.Profile.objects.get(user=request.user)
    about=models.About.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'pro':pro,'about':about,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}
  
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        profile_pic = request.FILES.get('profile_pic')          
        if profile_pic==None:
            profile_pic=pro.profile_pic                      
        pro.phone=phone 
        pro.profile_pic=profile_pic  
        pro.save()
        u.first_name=first_name
        u.last_name=last_name
        u.email=email
        u.save()            
        return redirect('accounts:personal_details')    
    return render(request,'profile-details.html',alert)

@csrf_exempt
@login_required(login_url="/login")  
def account_details(request):
    about=models.About.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    
    user_p=models.Account_address.objects.filter(Created_user=request.user).count()
    print('fffffffffffffff',user_p)
    if user_p == 0:
        if request.method == "POST":
            Account_Number=request.POST.get('Account_Number')
            UPI=request.POST.get('UPI')
            IFSC=request.POST.get('IFSC')
            Contact_Number=request.POST.get('Contact_Number')                   
            models.Account_address.objects.create(Account_Number=Account_Number,UPI=UPI,IFSC=IFSC,Contact_Number=Contact_Number,Created_user=request.user)   
            return redirect('accounts:account_details')

    else:
   
        pro=models.Account_address.objects.get(Created_user=request.user)
        if request.method == "POST":
            Account_Number=request.POST.get('Account_Number')
            UPI=request.POST.get('UPI')
            IFSC=request.POST.get('IFSC')
            Contact_Number=request.POST.get('Contact_Number')                   
            pro.Account_Number=Account_Number 
            pro.UPI=UPI 
            pro.IFSC=IFSC 
            pro.Contact_Number=Contact_Number  
            pro.save()
            return redirect('accounts:account_details')   
    pro=models.Account_address.objects.filter(Created_user=request.user)     
    alert = {'user_p':user_p,'pro':pro,'about':about,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}        
    # user_data= models.Account_address.objects.filter(Created_user=request.user)   
    return render(request,'account-details.html',alert)




@csrf_exempt
@login_required(login_url="/login")
def account_wishlist(request):
    print('====================================================')
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    
  
    wishlist = models.User_Wishlist.objects.filter(created_user=request.user.id).values_list('Product', flat=True)
    bid_count_dict={}
    for i in wishlist:
        if models.Product.objects.filter(id=i).exists():    
            bid_count=models.Product.objects.get(id=i)
            bid_count_dict[i]=bid_count
        elif gifts.Product.objects.filter(id=i).exists():
            bid_count=gifts.Product.objects.get(id=i)
            bid_count_dict[i]=bid_count
        elif medicine.Product.objects.filter(id=i).exists():
            bid_count=medicine.Product.objects.get(id=i)
            bid_count_dict[i]=bid_count
    return render(request, template_name='account-wishlist.html', context={"wishlist": wishlist,'bid_count_dict':bid_count_dict,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss})

def ajax_products_load(request):
    return render(request,'ajax-products-load.html')
def blog(request):
    return render(request,'blog.html')
def blog_fixed_column(request):
    return render(request,'blog-fixed-column.html')
def blog_grid_2(request):
    return render(request,'blog-grid-2.html')
def blog_grid_3(request):
    return render(request,'blog-grid-3.html')
def blog_grid_4(request):
    return render(request,'blog-grid-4.html')

def blog_post(request):
    return render(request,'blog-post.html')
def brands(request):
    return render(request,'brands.html')
def cart(request):
    return render(request,'cart.html')

@csrf_exempt
@login_required(login_url="/login") 
def Categloryfilter(request,id):  
    Products=models.Product.objects.filter(Product_Categlory=id) 
    my_products1=models.Product.objects.filter(Product_Categlory=id).count() 
    ProductDescription=models.Product_Description.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    a=models.Product.objects.all().order_by('Price') 
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()
    ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()


    paginator = Paginator(Products, 3) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'Image_Videos':Image_Videos,'ProductDescription':ProductDescription,'Sizes':Sizes,'page_obj':page_obj,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
      
    return render(request,'category.html',context)
@csrf_exempt
@login_required(login_url="/login") 
def quebookmak1(request,id):    
    Products=models.Product.objects.filter(Product_Brands=id)
    my_products1=models.Product.objects.filter(Product_Brands=id).count()
    ProductDescription=models.Product_Description.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    a=models.Product.objects.all().order_by('Price') 
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)
    ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()
   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()


    paginator = Paginator(Products, 3) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'Image_Videos':Image_Videos,'ProductDescription':ProductDescription,'Sizes':Sizes,'page_obj':page_obj,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
       
    return render(request,'category.html',context)


 ##################
@csrf_exempt
@login_required(login_url="/login") 
def Colorfilter(request,id): 
    Products=models.Product.objects.filter(Product_Colors=id)
    my_products1=models.Product.objects.filter(Product_Colors=id).count()
    request.session["Product_Colors"] = id
    ProductDescription=models.Product_Description.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    a=models.Product.objects.all().order_by('Price') 
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()
    ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()


    paginator = Paginator(Products, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'Image_Videos':Image_Videos,'Sizes':Sizes,'page_obj':page_obj,'ProductDescription':ProductDescription,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
       
    return render(request,'category.html',context)

################
@csrf_exempt
@login_required(login_url="/login") 
def Stylefilter(request,id): 
    Products=models.Product.objects.filter(Product_Filter_Name=id)
    my_products1=models.Product.objects.filter(Product_Filter_Name=id).count()
    ProductDescription=models.Product_Description.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    a=models.Product.objects.all().order_by('Price') 
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()
    ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()


    paginator = Paginator(Products, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'Image_Videos':Image_Videos,'Sizes':Sizes,'page_obj':page_obj,'ProductDescription':ProductDescription,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
       
    return render(request,'category.html',context)

@csrf_exempt
@login_required(login_url="/login") 
def Productcolor(request):  
    print('heeeeeeeeee',helloooo)    
    if request.method=='POST':
        print('heeeeeeeeee',helloooo)
        for i in j:
            Product_Colors1=request.POST.get(str(i.id))       
            print('helllooooooo',Product_Colors1)
    return render(request,'cart.html')


@csrf_exempt
@login_required(login_url="/login") 
def cart_view(request): 
    Products=''
    items_json=''
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()     
    context = {'Products':Products,'items_json':items_json,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}   
    if request.method=='POST':
        items_json = request.POST.get('itemsJson', '')      
        items_json=json.loads(items_json)
        # Product_Colors1=request.POST.get('Product_Colors')       
        print('fffff',items_json)
        
        p=[]
        Products=[]
      
        for i in items_json:
            cloth=''    
            gift=''
            medicin=''
            if models.Product.objects.filter(id=items_json[i][3]).exists():
                cloth=models.Product.objects.filter(id=items_json[i][3])
                Products.append(cloth)
            elif gifts.Product.objects.filter(id=items_json[i][3]).exists():
                gift=gifts.Product.objects.filter(id=items_json[i][3])
                Products.append(gift)
            elif medicine.Product.objects.filter(id=items_json[i][3]).exists():
                medicin=medicine.Product.objects.filter(id=items_json[i][3])
                Products.append(medicin)
            # context={'Products':Products,'items_json':items_json}
               
            
            context = {'Products':Products,'items_json':items_json,'about':about,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}   
    return render(request,'cart.html',context)   
     
    return render(request,'cart.html',context) 


@csrf_exempt
@login_required(login_url="/login") 
def category(request):
    user_ = None
    wishlisted_list =[]
    if request.user.is_authenticated:
        user=request.user.id
        user_ = get_object_or_404(models.Profile, user_id=user)
        wishlisted_list = list(models.User_Wishlist.objects.filter(created_user=request.user).values_list('Product',flat=True).order_by('Product'))
        wishlist = models.User_Wishlist.objects.filter(created_user=request.user.id)
        print(user_)
        
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
        
    CategloryS=models.Categlory.objects.all()
    ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    Products=models.Product.objects.filter(Coming_soon=False).order_by('-Price')
    my_products1=models.Product.objects.filter(Coming_soon=False).count()
    a=models.Product.objects.all().order_by('Price') 
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)
   
    ProductDescription=models.Product_Description.objects.all()

    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
    # giftParentTrue1=gift_model.Product.objects.all()
   

    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()
   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()

    paginator = Paginator(Products, 9) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'user_':user_,'wishlist': wishlist,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'wishlisted_list':wishlisted_list,'showcartandserch':showcartandserch,'cart_item_count': total_count,'all_items' : all_items,'total_price': total_price,'BrandsS':BrandsS,'Colorss':Colorss,'Sizes':Sizes,'page_obj':page_obj,'ProductDescription':ProductDescription,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse,'Image_Videos':Image_Videos}
    

    
    if request.method == "POST": #os request.GET()
        get_value= request.body
        # Do your logic here coz you got data in `get_value`
        data={}
        # data = self.get_queryset()
        
        data['result'] = serializers.serialize('json', models.Product.objects.filter(Price=1111),fields=('Product_Name'))
        # data['result'] = models.Product.objects.all().order_by('-Price')
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request,'category.html',context)

@csrf_exempt
@login_required(login_url="/login") 
def category_sort_price_high_to_low(request):
    ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    Products=models.Product.objects.all().order_by('-Price') 
    my_products1=models.Product.objects.all().count()
    ProductDescription=models.Product_Description.objects.all()
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)
    paginator = Paginator(Products, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'Sizes':Sizes,'page_obj':page_obj,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse,'ProductDescription':ProductDescription,'Image_Videos':Image_Videos}
    return render(request,'category.html',context)

@csrf_exempt
@login_required(login_url="/login") 
def category_sort_price_low_to_high(request):
    ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    Image_Videos=models.Image_Video.objects.all()
    Products=models.Product.objects.all().order_by('Price')
    my_products1=models.Product.objects.all().count()
    ProductDescription=models.Product_Description.objects.all()
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)
    paginator = Paginator(Products, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'ParentTrue':ParentTrue,'Sizes':Sizes,'page_obj':page_obj,'ParentFalse':ParentFalse,'ProductDescription':ProductDescription,'Image_Videos':Image_Videos}
    return render(request,'category.html',context)

@csrf_exempt
@login_required(login_url="/login") 
def Filter_Product(request): 
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)
    # giftParentTrue1=gift_model.Product.objects.all()
     ###########filtering#######
    CategloryFS=models.Categlory.objects.all()
    TypeFS=models.Brands.objects.all()
    ##############end

    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()
   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    Products=models.Product.objects.all().order_by('-Price') 
    Image_Videos=models.Image_Video.objects.all()
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    
    my_products=models.Product.objects.all()
    my_products1=models.Product.objects.all()
    filter_category1=''
    filter_category=''
    filter_category2=''
    filter_category4=''
    filter_category5=''
    filter_category6=''

    if 'Categlory' in request.GET:
       filter_category1 = request.GET.getlist('Categlory')       
       my_products = my_products.filter(Product_Categlory__in=filter_category1)
       my_products1 = my_products.filter(Product_Categlory__in=filter_category1).count()
    
    if 'Brand' in request.GET:
        filter_category = request.GET.getlist('Brand')       
        my_products = my_products.filter(Product_Brands__in=filter_category)
        my_products1 = my_products.filter(Product_Brands__in=filter_category).count()
    
    if 'Color' in request.GET:
       filter_category2 = request.GET.getlist('Color')       
       my_products = my_products.filter(Product_Colors__in=filter_category2)
       my_products1 = my_products.filter(Product_Colors__in=filter_category2).count()
   
    if 'Size' in request.GET:
       filter_category4 = request.GET.getlist('Size')   
       my_products = my_products.filter(Product_Size__in=filter_category4)
       my_products1 = my_products.filter(Product_Size__in=filter_category4).count()

    if 'Product' in request.GET:
       filter_category6 = request.GET.getlist('Product')   
       my_products = my_products.filter(Product_Filter_Name__in=filter_category6)
       my_products1 = my_products.filter(Product_Filter_Name__in=filter_category6).count()

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
       my_products1 = my_products.filter(Price__range=(a[0], a[len(a)-1])).count()
    #    print('===============================================================',my_products)
    paginator = Paginator(my_products, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'type':'cloth','my_products1':my_products1,'TypeFS':TypeFS,'CategloryFS':CategloryFS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'Image_Videos':Image_Videos,'Sizes':Sizes,'page_obj':page_obj,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
   
    return render(request,'category.html',context)


@csrf_exempt
@login_required(login_url="/login") 
def post(request):
    if request.method == "POST": #os request.GET()
        get_value= request.body
        # Do your logic here coz you got data in `get_value`
        data = {}
        data['result'] = 'you made a request'
        return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login") 
def dropdown(request):
    if request.method == "POST": #os request.GET()
        get_value= request.body
        # Do your logic here coz you got data in `get_value`
        data = {}
        data['result'] = 'you made a request'
        return HttpResponse(json.dumps(data), content_type="application/json")
     
    return render(request,'dropdown.html')

@csrf_exempt
def sorting(request):
    a=models.Product.objects.all().order_by('-Price') 
    context={'a':a}
    return render(request,'category.html',context)

@csrf_exempt
def productfilter(request):
    Products=models.Product.objects.all()
    user_filter = UserFilter(request.GET, queryset=Products)
    context={'filter': user_filter,'type':'choth'}
    if request.method == "POST": #os request.GET()
        get_value= request.body
        # Do your logic here coz you got data in `get_value`
        data = {}
        data['result'] = models.Product.objects.all().order_by('-Price') 
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request,'category.html',context)



def category_empty(request):
    return render(request,'category-empty.html')

def category_no_filters(request):
    return render(request,'category-no-filters.html')
def category_right_column(request):
    return render(request,'category-right-column.html')
def category_with_description(request):
    return render(request,'category-with-description.html')


# def member(request):
    
#     if request.method=='POST':
#         referral=request.POST.get('referral')
        
#         ref=''
#         user=''
#         ref_count=''
#         if referral=='':
#             user=User.objects.filter(is_active=1,is_staff=0,is_superuser=0)[0]
#             ref=models.Profile.objects.get(user=User.objects.get(id=user.id))
#             ref_count=models.member.objects.filter(parent_id=user.id).count()
#         else:
#             print('rrrrr---------------------rrrrrrrrrrrrrrrrrrrrrr',referral)
#             ref=models.Profile.objects.get(referral_code=referral)
#             user=models.User.objects.get(id=ref.user_id)
#             ref_count=models.member.objects.filter(parent_id=ref.user_id).count()
#         if ref_count==10:
#             child=models.member.objects.filter(parent=ref.user_id).values_list('child_id')
#             for i in child:
#                 ref_count=models.member.objects.filter(parent=i[0]).count() 
#                 if ref_count==10:
#                     child=models.member.objects.filter(parent=ref.id).values_list('child_id')
#                     for i in child:
#                         ref_count=models.member.objects.filter(parent=i[0]).count()
#                         if ref_count==10:
#                             child=models.member.objects.filter(parent=ref.id).values_list('child_id')
#                             for i in child:
#                                 ref_count=models.member.objects.filter(parent=i[0]).count()
#                                 if ref_count==10:
#                                     child=models.member.objects.filter(parent=ref.id).values_list('child_id')
#                                     for i in child:
#                                         ref_count=models.member.objects.filter(parent=i[0]).count()
#                                 else:
#                                     models.member.objects.create(parent=models.User.objects.get(id=i[0]),child=request.user,created_user_id=request.user.id)
#                                     ref_count=models.member.objects.filter(parent=models.User.objects.get(id=i[0])).count()
#                                     if ref_count==10:
#                                         caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
#                                         models.caseback_data_member.objects.create(user=models.User.objects.get(id=i[0]),amount=caseback_amount.amount,created_user_id=request.user.id)
#                                     return redirect('payment:paytm') 
#                         else:
#                             models.member.objects.create(parent=models.User.objects.get(id=i[0]),child=request.user,created_user_id=request.user.id)
#                             ref_count=models.member.objects.filter(parent=models.User.objects.get(id=i[0])).count()
#                             if ref_count==10:
#                                 caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
#                                 models.caseback_data_member.objects.create(user=models.User.objects.get(id=i[0]),amount=caseback_amount.amount,created_user_id=request.user.id)
#                             return redirect('payment:paytm') 
#                 else:
#                     models.member.objects.create(parent=models.User.objects.get(id=i[0]),child=request.user,created_user_id=request.user.id)
#                     ref_count=models.member.objects.filter(parent=models.User.objects.get(id=i[0])).count()
#                     if ref_count==10:
#                         caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
#                         models.caseback_data_member.objects.create(user=models.User.objects.get(id=i[0]),amount=caseback_amount.amount,created_user_id=request.user.id)
#                     return redirect('payment:paytm')
#         else:
#             models.member.objects.create(parent=models.User.objects.get(id=ref.user_id),child=request.user,created_user_id=request.user.id)
#             ref_count=models.member.objects.filter(parent=models.User.objects.get(id=ref.user_id)).count()
#             if ref_count==10:
#                 caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
#                 models.caseback_data_member.objects.create(user=models.User.objects.get(id=ref.user_id),amount=caseback_amount.amount,created_user_id=request.user.id)
#             return redirect('payment:paytm')   
@csrf_exempt  
@login_required(login_url="/login")
def checkout(request): 
    if request.method=='POST':
        products11 = request.POST.get('id_get')      
        items_json=json.loads(products11)    
        # Product_Color=request.POST.get('products') 
        pro1={}    
        for i in items_json:          
            Product_Colors1=request.POST.get(items_json[i][3])
            Product_Size1=request.POST.get('Size'+items_json[i][3])
            pro1[items_json[i][3]]=Product_Colors1,Product_Size1
            print('items_json',Product_Colors1)
        print('items_jsonhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh',pro1)
        request.session['pro1']=pro1     
        
    user=User.objects.get(username=request.user)
    user_data=models.User_Address.objects.get(default=1,created_user_id=user.id)
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'user':user,'user_data':user_data,'about':about,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}    
    
    return render(request,'checkout.html',alert)


def collections(request):
    return render(request,'collections.html')
def coming_soon(request):
    return render(request,'coming-soon.html')
def coming_soon_without_bg(request):
    return render(request,'coming-soon-without-bg.html')
def compare(request):
    return render(request,'compare.html')
@csrf_exempt
def faq(request):
    faqs=models.Faq.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'about':about,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}    

    return render(request,'faq.html',alert)


def gallery(request):
    return render(request,'gallery.html')
def gallery_2(request):
    return render(request,'gallery-2.html')

@csrf_exempt
def add_item(request, product_id, amount):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    if product_id in request.session['cart']:
        request.session['cart'][product_id] += amount
    else:
        request.session['cart'][product_id] = amount

    request.session.modified = True

    return JsonResponse(
    {
        'items_in_cart': sum(request.session['cart'].values()),
    })




@csrf_exempt
def login_user(request):
    print('----------user login-----------------------')
    contact_d=models.Contact_details.objects.all()
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    context = {'contact_d':contact_d,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}
    if request.method == 'POST':
        email = request.POST.get('emailaddress')
        password = request.POST.get('password')
        username = get_user(email)
        user = authenticate(username=username, password=password)
        
            
        if user:
            if user.is_active:
                login(request,user)
                return redirect('accounts:index')
                if user in request.session:
                    context['user'] = User.objects.get(id=request.session['user'])

                if cart in request.session:
                    context['cart_item_count'] = sum(request.session['cart'].values())
                else:
                    context['cart_item_count'] = 0
            else:
                return redirect('accounts:index')
        else:
            return redirect('accounts:index')
    else:
        return render(request,'login.html',context)


def page404(request):
    return render(request,'page404.html')
def privacy_policy(request):
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}    

    return render(request,'privacy-policy.html',alert)





def product(request,id):
    resultp=''
    Imageproduct=''
    ProductDescription=''
  
    if models.Product.objects.filter(id=id).exists():    
        resultp=models.Product.objects.get(id=id)
        Imageproduct=models.Image_Video.objects.filter(Image_Product=id)
        ProductDescription=models.Product_Description.objects.filter(Product=id)
    elif gifts.Product.objects.filter(id=id).exists():
        resultp=gifts.Product.objects.get(id=id)
        Imageproduct=gifts.Image_Video.objects.filter(Image_Product=id)
        ProductDescription=gifts.Product_Description.objects.filter(Product=id)
    elif medicine.Product.objects.filter(id=id).exists():
        resultp=medicine.Product.objects.get(id=id)
        Imageproduct=medicine.Image_Video.objects.filter(Image_Product=id)
        ProductDescription=medicine.Product_Description.objects.filter(Product=id)

    Imageproduct=models.Image_Video.objects.filter(Image_Product=id)
    ProductDescription=models.Product_Description.objects.filter(Product=id)

      
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    

    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()
    Sizes=models.Size.objects.all()
    a=models.Product.objects.all().order_by('Price') 
    ParentTrue=models.Product_fliters.objects.filter(parent__isnull=True)
    ParentFalse=models.Product_fliters.objects.filter(parent__isnull=False)

    
    context={'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'CategloryS':CategloryS,'BrandsS':BrandsS,'Colorss':Colorss,'Sizes':Sizes,'ProductDescription':ProductDescription,'resultp':resultp,'Imageproduct':Imageproduct,'a':a,'ParentTrue':ParentTrue,'ParentFalse':ParentFalse}
    return render(request,'product.html',context)


def reviews(request):
    return render(request,'reviews.html')

def terms_of_use(request):
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gift_model.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gift_model.Categlory.objects.all()
    giftTypeS=gift_model.Type.objects.all()   
    medicateC=medicines_model.Categlory.objects.all()
    medicateS=medicines_model.SubCateglory.objects.all()   
    alert = {'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}    

    return render(request,'terms-of-use.html',alert)

def test_header_mobile_1(request):
    return render(request,'test-header-mobile-1.html')
def test_header_mobile_1_nosticky(request):
    return render(request,'test-header-mobile-1-nosticky.html')
def test_header_nosticky(request):
    return render(request,'test-header-nosticky.html')
def test_mobile_menu_accordion(request):
    return render(request,'test-mobile-menu-accordion.html')
def test_product_preview_equal_height(request):
    return render(request,'test-product-preview-equal-height.html')
def test_product_preview_style2(request):
    return render(request,'test-product-preview-style2.html')
def typography(request):
    return render(request,'typography 03.html')






def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

def bookmarkdlt(request,id):
    a=models.User_Wishlist.objects.get(Product=id)
    a.delete()
    # print('=============upload file2 ==photo=======================================',a)
    return redirect('accounts:account_wishlist')
@csrf_exempt
@login_required(login_url="/login")  
def add_to_wishlist(request):
    if request.is_ajax() and request.POST and 'attr_id' in request.POST:
      
        if request.user.is_authenticated:          
            data =  models.User_Wishlist.objects.filter(created_user_id = request.user.id,Product = request.POST['attr_id'])
            if data.exists():
                data.delete()
            else:
                models.User_Wishlist.objects.create(created_user_id = request.user.id,Product = request.POST['attr_id'])
    else:
        print("No Product is Found")

    return redirect("accounts:contact")


def update_cart(cart, product, Price = 0, quantity=1):   
    if type(cart) is dict:
        if product in cart['products'] and quantity * -1 >= cart['products'][product]['quantity']:
            cart['num_products'] -= cart['products'][product]['quantity']
            cart['total'] -= cart['products'][product]['Price'] * cart['products'][product]['quantity']
            del cart['products'][product]
            return cart
        if product in cart['products']:
            cart['products'][product]['quantity'] += quantity
        else:
            cart['products'][product] = {'quantity': quantity, 'Price': price}
        cart['num_products'] += quantity
        cart['total'] += cart['products'][product]['Price'] * quantity
        return cart


def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            u = User.objects.get(id=request.session['user']['id'])
            if not check_password(form.cleaned_data['password'], u.password):
                return render(request, 'checkout.html', {'const': CONSTANTS, 'OrderForm': OrderForm()})
            products = request.session['cart']['products']
            orderDate = datetime.datetime.now()
            for p in products:
                o = Order(quantity=products[p]['quantity'], date=orderDate,
                          subtotal=products[p]['quantity'] * products[p]['price'],
                          address=form.cleaned_data['address'], product_id=Product.objects.get(name=p).id,
                          user_id=request.session['user']['id'], telephone=form.cleaned_data['telephone'])
                o.save()
            del request.session['cart']
            request.session['user']['cart'] = None
            u = User.objects.get(id=request.session['user']['id'])
            u.cart = None
            u.save()
            messages.add_message(request, messages.INFO, "ordered", extra_tags='ordered')
            return redirect('redir')
        else:
            return checkout(request)
    else:
        return checkout(request)


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None
    
def tree_view(request):
    child=models.member.objects.filter(parent=request.user.id)
    sub_child=models.member.objects.all()
    print(request.user.id)
    return render(request,'treeview.html',{'lists':child,'child':sub_child})