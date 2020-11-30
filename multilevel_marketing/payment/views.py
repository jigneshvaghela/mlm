from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse
import json
import simplejson as json
from django.db.models import Count
from multilevel_marketing import settings
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.db.models import Sum,F,FloatField
from itertools import chain
# Create your views here.
from . import Checksum
from django.contrib.auth.decorators import login_required
MERCHANT_KEY='dRqXXn5!k6v&EA6f'
from .import models as pay
from accounts import models 
from gift import models  as gifts
from medicines import models as medicine
import json
from django.contrib.auth.models import User

@login_required
@ensure_csrf_cookie
def paytm(request):
    pro2=request.session['pro1']
    
    if request.method=='POST':
        items_json = request.POST.get('itemsJson1', '')   
        items_json=json.loads(items_json)    
       
        referral=request.POST.get('referral')
        checkbox1=request.POST.get('address')
        fname=''
        lname=''
        country=''
        state=''
        city=''
        postal=''
        address=''
        landmark=''
        if checkbox1==2:

            fname=request.POST.get('fname2')
            lname=request.POST.get('lname2')
            country=request.POST.get('country2')
            state=request.POST.get('state2')
            city=request.POST.get('city2')
            postal=request.POST.get('postal2')
            address=request.POST.get('address2')
            landmark=request.POST.get('landmark2')
        else:
            add=models.User_Address.objects.get(default=1,created_user_id=request.user)
            fname=request.user.first_name
            lname=request.user.last_name
            country=add.country
            state=add.state
            city=add.city
            postal=add.pincode
            address=add.address
            landmark=add.landmark
            # Product_Size=add.Product_Size
            # Product_Colors=add.Product_Colors
        total=0
        
       
        user = request.user
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        MERCHANT_ID = settings.PAYTM_MERCHANT_ID
        CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL+'/'
        P_URL = 'https://securegw-stage.paytm.in/theia/processTransaction'
        CUST_ID = user.email
        order_id = Checksum.__id_generator__()
        for i in items_json:
            size=''
            color=''
            
            if items_json[i][3] in pro2:
                color=pro2[str(items_json[i][3])][0]
                size=pro2[str(items_json[i][3])][1]
            total+=items_json[i][0]*items_json[i][2]+items_json[i][5]
            print(size,color)
            pay.Order.objects.create(product =items_json[i][3] ,user = request.user,quantity = items_json[i][0],Courier=items_json[i][5],Product_Size=size,Product_Colors=color, subtotal = items_json[i][0]*items_json[i][2],first_name=fname,last_name=lname,country=country,state=state,city=city,zipcode=postal,Address=address,Landmark=landmark,order_id=order_id)
        bill_amount =total
        request.session['amount']=bill_amount
        request.session['order_id']=order_id
        if bill_amount:
            data_dict = {
                        'MID':MERCHANT_ID,
                        'ORDER_ID':order_id,
                        'TXN_AMOUNT': str(bill_amount),
                        'CUST_ID': CUST_ID,
                        'INDUSTRY_TYPE_ID':'Retail',
                        'WEBSITE': settings.PAYTM_WEBSITE,
                        'CHANNEL_ID':'WEB',
                        'CALLBACK_URL':'http://192.168.1.9:1111/payment/response',
                    }
            param_dict = data_dict   
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
            referral=request.POST.get('referral')
            ref=''
            user=''
            ref_count=''
            if referral=='':
                user=User.objects.filter(is_active=1,is_staff=0,is_superuser=1)[0]
                ref=models.Profile.objects.get(user=User.objects.get(id=user.id))
                ref_count=models.member.objects.filter(parent_id=user.id).count()
            else:
                ref=models.Profile.objects.get(referral_code=referral)
                user=models.User.objects.get(id=ref.user_id)
                ref_count=models.member.objects.filter(parent_id=ref.user_id).count()
            if ref_count==10:
                child=models.member.objects.filter(parent=ref.user_id).values_list('child_id')
                for i in child:
                    ref_count=models.member.objects.filter(parent=i[0]).count() 
                    if ref_count==10:
                        child=models.member.objects.filter(parent=ref.id).values_list('child_id')
                        for i in child:
                            ref_count=models.member.objects.filter(parent=i[0]).count()
                            if ref_count==10:
                                child=models.member.objects.filter(parent=ref.id).values_list('child_id')
                                for i in child:
                                    ref_count=models.member.objects.filter(parent=i[0]).count()
                                    if ref_count==10:
                                        child=models.member.objects.filter(parent=ref.id).values_list('child_id')
                                        for i in child:
                                            ref_count=models.member.objects.filter(parent=i[0]).count()
                                    else:
                                        models.member.objects.create(parent=models.User.objects.get(id=i[0]),child=request.user,created_user_id=request.user.id)
                                        ref_count=models.member.objects.filter(parent=models.User.objects.get(id=i[0])).count()
                                        if ref_count==10:
                                            caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
                                            models.caseback_data_member.objects.create(user=models.User.objects.get(id=i[0]),amount=caseback_amount.amount,created_user_id=request.user.id)
                                        return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'paytmurl' :P_URL, 'title': 'Paytm'})
                            else:
                                models.member.objects.create(parent=models.User.objects.get(id=i[0]),child=request.user,created_user_id=request.user.id)
                                ref_count=models.member.objects.filter(parent=models.User.objects.get(id=i[0])).count()
                                if ref_count==10:
                                    caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
                                    models.caseback_data_member.objects.create(user=models.User.objects.get(id=i[0]),amount=caseback_amount.amount,created_user_id=request.user.id)
                                return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'paytmurl' :P_URL, 'title': 'Paytm'})
                    else:
                        models.member.objects.create(parent=models.User.objects.get(id=i[0]),child=request.user,created_user_id=request.user.id)
                        ref_count=models.member.objects.filter(parent=models.User.objects.get(id=i[0])).count()
                        if ref_count==10:
                            caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
                            models.caseback_data_member.objects.create(user=models.User.objects.get(id=i[0]),amount=caseback_amount.amount,created_user_id=request.user.id)
                        return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'paytmurl' :P_URL, 'title': 'Paytm'})
            else:
                models.member.objects.create(parent=models.User.objects.get(id=ref.user_id),child=request.user,created_user_id=request.user.id)
                ref_count=models.member.objects.filter(parent=models.User.objects.get(id=ref.user_id)).count()
                if ref_count==10:
                    caseback_amount=models.caseback.objects.get(no_of_member=ref_count)
                    models.caseback_data_member.objects.create(user=models.User.objects.get(id=ref.user_id),amount=caseback_amount.amount,created_user_id=request.user.id)
                return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'paytmurl' :P_URL, 'title': 'Paytm'}) 
            return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'paytmurl' :P_URL, 'title': 'Paytm'})
        return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def recipt(request):
    if request.method == "POST":
        user=request.user
        data_dict = {}      
        data_dict = dict(request.POST.items())
        data_dict['PLANPRICE']=request.session['amount']
        data_dict['GST']=0
        print(data_dict)
        pay.Paytm_history.objects.create(user=request.user, **data_dict)
    
    status = 'TXN_FAILURE' 
    for key,value in data_dict.items():
        if key == 'STATUS':
            # user.user_details.status = value
            # user.user_details.save()
            # if value == 'TXN_SUCCESS':
            status = value
    order=pay.Order.objects.filter(order_id=data_dict['ORDERID'])
    a=[]
    for j in order:
        a.append(j.quantity)
    print(a)
    
    # total=pay.Order.objects.filter(order_id=data_dict['ORDERID']).aggregate(Sum('subtotal'))
    order2 = pay.Order.objects.values('order_id').annotate(Count('subtotal'),total_price1=Sum('subtotal'),total_price2=Sum('Courier')).filter(order_id=data_dict['ORDERID'])
    
    total3={}
    for item in order2:
        abc=item['order_id']
        totalCost = item['total_price1']+ item['total_price2'] 
        total3[abc]=totalCost
    print('ggggg',total3)



    p=[]
    Products=''
    for i in order:
        cloth=''
        gift=''
        medicin=''
        if models.Product.objects.filter(id=i.product).exists():
            cloth=models.Product.objects.filter(id=i.product)
            cloth1=models.Product.objects.get(id=i.product)        
            cloth1.Availability= cloth1.Availability-a[0] 
            cloth1.save()
            p.append(cloth)
                   
        elif gifts.Product.objects.filter(id=i.product).exists():
            gift=gifts.Product.objects.filter(id=i.product) 
            gift1=gifts.Product.objects.get(id=i.product)          
            gift1.Availability= gift1.Availability-a[0] 
            gift1.save()
            p.append(gift)

        elif medicine.Product.objects.filter(id=i.product).exists():
            medicin=medicine.Product.objects.filter(id=i.product)  
            medicin1=medicine.Product.objects.get(id=i.product)           
            medicin1.Availability= medicin1.Availability-a[0] 
            medicin1.save()
            p.append(medicin)

    return render(request, "payments/invoice.html", {'total3':total3,'orders':order,'Products':p,"payment": data_dict, 'title': 'Recipt', "status": status})



@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        data_dict = dict(request.POST.items())

        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            for key in request.POST:
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            # models.Paytm_history.objects.create(user=settings.USER, **data_dict)
            return render(request, "payments/response.html", {"paytm":data_dict, 'title': 'Confirm'})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)


@login_required(login_url="/login") 
def account_history(request):
    # (Sum(F('field1')*F('field2')))   
    # cloth=models.Product.objects.annotate(total_price=Sum(F('Discount_Price') * F('Courier_charge')))
    # total_group=Sum(F('Discount_Price')*F('Courier_charge'), output_field=FloatField())
    # print('gg',total_group)    
    order = pay.Order.objects.values('order_id','date').annotate(Count('date'),total_price=Sum('subtotal')).filter(user_id=request.user)
   
    order5={}
    for i in order:
        print(i)
    print(order5)
    CategloryS=models.Categlory.objects.all()
    BrandsS=models.Brands.objects.all()
    Colorss=models.Colors.objects.all()  
    giftParentTrue=gifts.Product_fliters.objects.filter(parent__isnull=True)  
    giftCategloryS=gifts.Categlory.objects.all()
    giftTypeS=gifts.Type.objects.all()   
    medicateC=medicine.Categlory.objects.all()
    medicateS=medicine.SubCateglory.objects.all()     
    context = {'orders':order,'order5':order5,'CategloryS':CategloryS,'giftParentTrue':giftParentTrue,'giftCategloryS':giftCategloryS,'giftTypeS':giftTypeS,'medicateC':medicateC,'medicateS':medicateS,'BrandsS':BrandsS,'Colorss':Colorss}
    return render(request,'account-history.html',context)


@login_required(login_url="/login")  
def invoice(request,order_id):
    # totalCost = 0
    payment=pay.Paytm_history.objects.get(ORDERID=order_id)
    order=pay.Order.objects.filter(order_id=order_id)
    order1 = pay.Order.objects.values('order_id','Courier').annotate(Count('subtotal'),total_price=Sum('subtotal')).filter(user_id=request.user)
    total=pay.Order.objects.filter(order_id=order_id).aggregate(Sum('subtotal'))
    order2 = pay.Order.objects.values('order_id').annotate(Count('subtotal'),total_price1=Sum('subtotal'),total_price2=Sum('Courier')).filter(user_id=request.user)
    
    total3={}
    for item in order2:
        abc=item['order_id']
        totalCost = item['total_price1']+ item['total_price2'] 
        total3[abc]=totalCost
    print('ggggg',total3)


    # total1=pay.Order.objects.all().annotate(total_price=Sum(F('Courier', FloatField()) * F('subtotal', FloatField())))
    # for t in total1:
    #     print(t.total_price)
    p=[]
    Products=''
    print(order)
    for i in order:
        cloth=''
        gift=''
        medicin=''
    
        if models.Product.objects.filter(id=i.product).exists():
            cloth=models.Product.objects.filter(id=i.product)
            p.append(cloth)
           

           
        elif gifts.Product.objects.filter(id=i.product).exists():
            gift=gifts.Product.objects.filter(id=i.product)
            p.append(gift)
        elif medicine.Product.objects.filter(id=i.product).exists():
            medicin=medicine.Product.objects.filter(id=i.product)
            p.append(medicin)
    #     Products = list(chain(cloth, gift,medicin))
    # p.append(Products)
    context={'total3':total3,'order2':order2,'orders':order,'Products':p,'total':total['subtotal__sum'],'payment':payment}
    return render(request,'payments/invoice2.html',context)

