from django import forms
from django.forms.models import ModelForm
from .models import Item, OrderItem,Comment

class ItemForm(ModelForm):
    class Meta ():
        model = Item
        exclude = []

class OrderItemForm(ModelForm):
    class Meta ():
        model = OrderItem
        exclude = []

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')