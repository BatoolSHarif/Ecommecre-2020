# from django.conf import settings
from django.db import models 
from django.shortcuts import reverse
# Create your models here.
# class UserInfo(models.Model):
#     from_date = models.DateField(default=datetime.now())
#     to_date =  models.DateField(default=datetime.now()) 
#     customer = models.ForeignKey(to='UserInfo',on_delete=models.PROTECT)
#     def __str__(self):
#         return self.first_name
# STATUS_CHOICES = (
#     (1, _("Jordan")),
#     (2, _("Lebanon")),
#     (3, _("Palistien")),
#     (4, _("Iraq")),
#     (5, _("Kwiut")),
#     (6, _("Qatar")),
#     (7, _("Syria")),
# )

CATIGORY_CHOICES = (
    ('S', 'Shirts'),
    ('SW', "Sport wear"),
    ('O', "Outwear"),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', "secondary"),
    ('D', "danger"),
)

class Item (models.Model):
    title = models.CharField (max_length=100)
    price = models.FloatField(default=0.0)
    catigory = models.CharField (choices= CATIGORY_CHOICES, max_length = 2, default="S")
    label = models.CharField (choices= LABEL_CHOICES, max_length = 2, default="P")
    
    def get_absolute_url(self):
        return reverse('product-url', kwargs={'pk': self.pk})
 
    def get_add_to_cart_url(self):
        return reverse('add-to-cart-url', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse('remove-url', kwargs={'pk': self.pk})    
        
    def __str__(self):
        return self.title
    
class OrderItem (models.Model):
    item = models.ForeignKey(to='Item',on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order (models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

class Comment(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.name

