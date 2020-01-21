from django.db import models 
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.
CATIGORY_CHOICES = (
    ('B', 'Beds'),
    ('D', "Desks"),
    ('L', "Lighting"),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', "secondary"),
    ('D', "danger"),
)

CITY_CHOICES = (
(None, 'Choose...'),
('A','Amman'),
('Z','Zarqa'),
('I','Irbid'),
('J', 'Jerash'),
('AJ','Ajloun'),
('K','Karak'),
('AQ','Aqaba'),
('O','Other',)
)

COUNTRY_CHOICES = (    
(None, 'Choose...'),
('J','Jordan'),)

TYPE_CHOICES = (
('D','Double'),
('S','Single'),
('C','Children'),
('O', 'Office'),
('CO','Computer'),
('CH','Chair_desk'),
('F','Floor'),
('CI','Cieling',),
('T','Tabel',)
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class ItemModel (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField (max_length=100)
    price = models.FloatField(default=0.0)
    catigory = models.CharField (choices= CATIGORY_CHOICES, max_length = 2, default="S")
    label = models.CharField (choices= LABEL_CHOICES, max_length = 2, default="P")
    image = models.ImageField(blank=True,null=True)
    descrption = models.CharField(max_length=200,blank=True,null=True)
    item_type =  models.CharField (choices= TYPE_CHOICES, max_length = 2, default="S")
    def get_absolute_url(self):
        return reverse('product-url', kwargs={'pk': self.pk})
 
    def get_add_to_cart_url(self):
        return reverse('add-to-cart-url', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse('remove-url', kwargs={'pk': self.pk})    

    
    def __str__(self):
        return self.title
    
class OrderItemModel (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    item = models.ForeignKey(to='ItemModel',on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def total_item_price(self):
        return self.quantity * self.item.price
        
        
    

class OrderModel(models.Model):
    
    # item = models.ForeignKey(to='ItemModel',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    items = models.ManyToManyField(OrderItemModel)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(to="BillingAddressModel",on_delete=models.SET_NULL,blank=True,null=True)
    being_deliverd = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    order_number = models.CharField(max_length=20,blank=True,null=True)
    
    def final_price(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.total_item_price()
        return total
    
    def get_singel_item_remove_from_cart_url(self):
        return reverse('remove-singel-item-url', kwargs={'pk': self.pk}) 
    
    def get_add_to_cart_url(self):
        return reverse('add-to-cart-url', kwargs={'pk': self.pk})

class CommentModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.name

class BillingAddressModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    ddress = models.CharField(max_length=100,blank=True,null=True)
    address2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=1,blank=True,null=True)
    phone_number = models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return  self.user.username


class CheckoutModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)    
    address = models.CharField(max_length=50,blank=True,null=True)
    address2 = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(choices=COUNTRY_CHOICES,max_length=50,blank=True,null=True)
    city = models.CharField(choices=CITY_CHOICES,max_length=50,blank=True,null=True)
    phone_number = models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return  self.user.username

class UserProfileModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)    
    profile_item  = models.ForeignKey(to="OrderModel",on_delete=models.SET_NULL,blank=True,null=True)

class RefundRequestModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(to="OrderModel",on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20,blank=True,null=True)
    Name = models.CharField(max_length=20,blank=True,null=True)
    message =  models.CharField(max_length=100,blank=True,null=True)
    email =  models.EmailField(max_length=100,blank=True,null=True)
    accpted =  models.BooleanField(default=False)
    def __str__(self):
        return  f"{self.order.title}" 


class Rating(models.Model):

    RATING_CHOICES = (
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent')    
    )
    productID = models.ForeignKey(OrderItemModel, on_delete=models.CASCADE)
    indRating = models.IntegerField(choices=RATING_CHOICES)



class Tag(models.Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag


class ProductTags(models.Model):
    tag_name = models.ManyToManyField(to='Tag')
    tag_product = models.ForeignKey(to='ItemModel', on_delete=models.CASCADE, null=True, blank=True, unique=True)
    def __str__(self):
        return  self.tag_product


# class product(models.Model):
#     pass
# class Tag(models.Model):
#     name = models.CharField(max_length=255)

# class ProductTag(models.Model):
#     tag = models.ManyToManyField(to='Tag')
#     product = models.ManyToManyField(to='Product')

#     @classmethod
#     def   