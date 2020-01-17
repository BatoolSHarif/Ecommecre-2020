from django import forms
from django.forms.models import ModelForm
from .models import ItemModel, OrderItemModel,CheckoutModel,UserProfileModel,RefundRequestModel,CommentModel,BillingAddressModel




class ItemForm(ModelForm):
    class Meta ():
        model = ItemModel
        exclude = []


class OrderItemForm(ModelForm):
    class Meta ():
        model = OrderItemModel
        exclude = []


class CommentForm(forms.ModelForm):
    class Meta():
        model = CommentModel
        fields = ('name', 'email', 'body')

class CheckoutForm(forms.ModelForm):
     class Meta():
        model = CheckoutModel
        fields = ()

class UserProfileForm(forms.ModelForm):
     class Meta():
        model = UserProfileModel
        fields = ()

class RefundRequestForm(forms.ModelForm):
    class Meta ():
        model = RefundRequestModel
        fields = ()

# class ItemDetailViewForm(forms.ModelForm):
#     class Meta ():
#         model = ItemDetailView
#         fields = ()




# class CheckoutForm(forms.Form):

#     address = forms.CharField(widget=forms.TextInput(attrs={'class':"custom-select d-block w-100"}))
#     address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Alwakkalat St"}))
#     address2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':"Apartment or suite"}))
#     country = forms.ChoiceField(choices=COUNTRY_CHOICES,widget=forms.Select(attrs={'class':"custom-select d-block w-100"}))
#     city = forms.ChoiceField(choices= CITY_CHOICES,widget=forms.Select(attrs={'class':"custom-select d-block w-100"}))
#     billing_address = forms.BooleanField(required=False)
#     save_info = forms.BooleanField(required=False)
#     phone_number = forms.CharField(max_length=10,required=True,widget=forms.TextInput(attrs={'placeholder':"+962 7XX-XXX-XXX"}))