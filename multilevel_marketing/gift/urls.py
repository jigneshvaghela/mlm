
from django.urls import path,re_path
from django.conf.urls import url
from . import views
app_name='gift'
urlpatterns = [
   

   
  
    path('category',views.category,name='category'),
    # path('category-sort-price-high-to-low',views.category_sort_price_high_to_low,name='category_sort_price_high_to_low'),
    # path('category-sort-price-low-to-high',views.category_sort_price_low_to_high,name='category_sort_price_low_to_high'),
    path('Categloryfilter/<slug:id>', views.Categloryfilter, name='Categloryfilter'),
    path('Typefilter/<slug:id>', views.Typefilter, name='Typefilter'),
    path('Subfilter/<slug:id>', views.Stylefilter, name='Subfilter'),
    path('Filter_Product',views.Filter_Product,name='Filter_Product'),
   

    ##############cart3#####################
    # path('add_item/<str:product_id>/<int:amount>', views.add_item),
    
    
    # re_path(r'^cart/$', views.cart, name="cart"),
    # re_path(r'^order/$', views.order, name="order"),

    
    # path('product/<slug:id>',views.product,name='product1'),

    path('product',views.product,name='product'),

]
