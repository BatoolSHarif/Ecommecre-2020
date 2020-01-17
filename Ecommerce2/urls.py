"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


app_name = "mainapp"

urlpatterns =[
# Admin/HomePage/Account URLS
    path('admin/', admin.site.urls),
    path('',views.HomeView.as_view(), name='item-list-url'),
    path('accounts/', include('allauth.urls')),

# Product/Checkout/OrderSummary URLS
    path('product/<int:pk>',views.ItemDetailView.as_view(), name="product-url"),
    path('checkout',views.CheckoutListView.as_view(),name = 'checkout-url'),
    path('order-summary',views.OrderSummaryDetailView.as_view(),name="summary-url"),

# Comment
    path('/product/1',views.add_comment,name = 'comment-url'),
    
# Add/Remove from cart URLS
    path('add-to-cart/<int:pk>',views.add_to_cart,name = "add-to-cart-url"),
    path('remove-from-cart/<int:pk>',views.remove_from_cart, name = "remove-url"),
    path('remove-singel-item/<int:pk>',views.remove_singel_item_from_cart,name = 'remove-singel-item-url'),

# Tankyou/Cash on delv.
    path('Thankyou',views.Tankyou,name="Thankyou-url"),

# DataFilling URL
    path('DataFilling',views.check_on_user.as_view(),name='employer_url'),

# Profile URL
    path('profile',views.ProfileListView.as_view(),name="profile_url"),

# CAtigories URL
    path('product_cat',views.ProductList.as_view(),name="prodct_catigory_url"),
    
# About/Contact URLS
    path('About_Us',views.AboutList.as_view(),name='about_url'),
    path('Contact Us',views.Contact.as_view(),name='contact_url'),
    
# Beds Section URLS
   path('Beds_Products_list',views.BedsList.as_view(),name="bed_list_url"),
   
# Desks Section URLS
    path('Desks_Products_list',views.DesksList.as_view(),name="desk_list_url"),

# Lamps Section URLS    
    path('Lighting_Products_list',views.LigthingList.as_view(),name="ligthing_list_url"),


# TESTS
    path('list',views.list.as_view(),name = 'list'),
    path('list/<int:pk>',views.detail.as_view(),name = 's_details'),

# Refund RequestForm
    path('refund_request',views.RefundRequest.as_view(),name="refund_req_url"),

# Search 
    path('our_services',views.ServicesListView.as_view(),name="services_url"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
