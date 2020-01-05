from django.contrib import admin
from .models import models
from .models import Comment

# Register your models here.
from mainapp.models import Item
admin.site.register(Item)

from mainapp.models import Order 
admin.site.register(Order)

from mainapp.models import OrderItem
admin.site.register(OrderItem)

from mainapp.models import Comment
admin.site.register(Comment)
