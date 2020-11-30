from django.urls import path,re_path
from django.conf.urls import url
from . import views
app_name='accounts'
urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('account_addresses',views.account_addresses,name='account_addresses'),
    path('edit/<slug:id>', views.edit, name='edit'),
    path('account_create',views.account_create,name='account_create'),
    path('personal_details',views.personal_details,name='personal_details'),
    path('account_details',views.account_details,name='account_details'),
    
    # path('account_details',views.account_details,name='account_details'),
    # path('member',views.member,name='member'),
    path('account_wishlist/',views.account_wishlist,name='account_wishlist'),


    path('ajax_products_load',views.ajax_products_load,name='ajax_products_load'),
    path('blog',views.blog,name='blog'),
    path('blog_fixed_column',views.blog_fixed_column,name='blog_fixed_column'),
    path('blog_grid_2',views.blog_grid_2,name='blog_grid_2'),
    path('blog_grid_3',views.blog_grid_3,name='blog_grid_3'),
    path('blog_grid_4',views.blog_grid_4,name='blog_grid_4'),
    path('blog_post',views.blog_post,name='blog_post'),
    path('brands',views.brands,name='brands'),
    path('cart',views.cart,name='cart'),
    path('category',views.category,name='category'),
    path('category-sort-price-high-to-low',views.category_sort_price_high_to_low,name='category_sort_price_high_to_low'),
    path('category-sort-price-low-to-high',views.category_sort_price_low_to_high,name='category_sort_price_low_to_high'),
    path('Categloryfilter/<slug:id>', views.Categloryfilter, name='Categloryfilter'),
    path('Colorfilter/<slug:id>', views.Colorfilter, name='Colorfilter'),
    path('Stylefilter/<slug:id>', views.Stylefilter, name='Stylefilter'),
    path('quebookmak1/<slug:id>', views.quebookmak1, name='quebookmak1'),

    path('category_empty',views.category_empty,name='category_empty'),
    path('category_no_filters',views.category_no_filters,name='category_no_filters'),
    path('category_right_column',views.category_right_column,name='category_right_column'),
    path('category_with_description',views.category_with_description,name='category_with_description'),
    path('checkout',views.checkout,name='checkout'),
    path('collections',views.collections,name='collections'),
    path('coming_soon',views.coming_soon,name='coming_soon'),
    path('coming_soon_without_bg',views.coming_soon_without_bg,name='coming_soon_without_bg'),
    path('compare',views.compare,name='compare'),
    path('faq',views.faq,name='faq'),
    path('gallery',views.gallery,name='gallery'),
    path('gallery_2',views.gallery_2,name='gallery_2'),
    path('login/',views.login_user,name='login'),
    path('page404',views.page404,name='page404'),
    path('privacy_policy',views.privacy_policy,name='privacy_policy'),

    path('verify',views.verify,name='EnterOTP'),

    ##################search######
     path('search/', views.search, name='Search'),
    ################wishlist################
    
    path('bookmarkdlt/<slug:id>/',views.bookmarkdlt,name='bookmarkdlt'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'), # For add to wishlist

    ##############cart3#####################
    path('add_item/<str:product_id>/<int:amount>', views.add_item),
    
   

    path('reference/referralcode=<slug:id>', views.reference,name='reference'),
    path('Filter_Product',views.Filter_Product,name='Filter_Product'),
    path('product/<slug:id>',views.product,name='product1'),

    path('product',views.product,name='product'),

    
    path('reviews',views.reviews,name='reviews'),
    path('terms_of_use',views.terms_of_use,name='terms_of_use'),
    path('test_header_mobile_1',views.test_header_mobile_1,name='test_header_mobile_1'),
    path('test_header_mobile_1_nosticky',views.test_header_mobile_1_nosticky,name='test_header_mobile_1_nosticky'),
    path('test_header_nosticky',views.test_header_nosticky,name='test_header_nosticky'),
    path('test_mobile_menu_accordion',views.test_mobile_menu_accordion,name='test_mobile_menu_accordion'),
    path('test_product_preview_equal_height',views.test_product_preview_equal_height,name='test_product_preview_equal_height'),
    path('test_product_preview_style2',views.test_product_preview_style2,name='test_product_preview_style2'),
    path('typography',views.typography,name='typography'),
    path('productfilter',views.productfilter,name='productfilter'),
    path('sorting',views.sorting,name='sorting'),
    url(r'^user_logout/$',views.user_logout,name='user_logout'),
    ###################dropdown#########
    path('dropdown',views.dropdown,name='dropdown'),
    ##############endfor#########
    # path('member',views.member,name='member'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('Productcolor',views.Productcolor,name='Productcolor'),
    
    
    ################filteringgggggggggggggggggggggg#################################
    path('tree_view',views.tree_view,name='tree_view')


]
