from django.contrib import admin
from .models import models
from .models import CommentModel,BillingAddressModel,ProductTags,Tag



class OrderAdmin (admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_deliverd',
                    'received',
                    'refund_request',
                    'refund_granted',
                    'order_number']

    list_filter = [ 'ordered',
                    'being_deliverd',
                    'received',
                    'refund_request',
                    'refund_granted']

# Register your models here.
from mainapp.models import ItemModel
admin.site.register(ItemModel)

from mainapp.models import OrderModel
admin.site.register(OrderModel,OrderAdmin)

from mainapp.models import OrderItemModel
admin.site.register(OrderItemModel)

from mainapp.models import CommentModel
admin.site.register(CommentModel)

from mainapp.models import BillingAddressModel
admin.site.register(BillingAddressModel)


from mainapp.models import CheckoutModel
admin.site.register(CheckoutModel)

from mainapp.models import RefundRequestModel
admin.site.register(RefundRequestModel)

from mainapp.models import Tag
admin.site.register(Tag)

from mainapp.models import ProductTags
admin.site.register(ProductTags)