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

urlpatterns =[
    path('admin/', admin.site.urls),
    path('',views.HomeView.as_view(), name='item-list-url'),
    path('product/<int:pk>',views.ItemDetailView.as_view(), name="product-url"),
    path('checkout',views.CheckoutListView.as_view(),name = 'checkout-url'),
    path('comment',views.add_comment,name = 'comment-url'),
    path('add-to-cart/<int:pk>',views.add_to_cart, name = "add-to-cart-url"),
    path('remove-from-cart/<int:pk>',views.remove_from_cart, name = "remove-url"),

    path('list',views.list.as_view(),name = 'list'),
    path('list/<int:pk>',views.detail.as_view(),name = 's_details'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)