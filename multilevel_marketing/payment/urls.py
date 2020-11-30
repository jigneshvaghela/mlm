from . import views
from django.urls import path
from django.conf.urls import url
app_name='payment'
urlpatterns = [
    
    
    # path('pagecheckout_bynow/<int:mid>',views.pagecheckout_bynow,name='pagecheckout_bynow'),
    # path('paymentpage',views.paymentpage,name='paymentpage'),
    path('invoice/<slug:order_id>', views.invoice, name='invoice'),
    path('paytm', views.paytm, name='paytm'),
    path('response', views.response, name='response'),
    path('recipt', views.recipt, name='recipt'),
    # path('payments_home', views.payments_home, name='payments_home'),
    path('account_history',views.account_history,name='account_history'),
    

]