from django import template 
from .models import Order
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def cart_item_count():
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            return qs[0].items.count()

    return 0