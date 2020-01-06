from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,ListView,DeleteView,DetailView,View
from .models import Item, Order , OrderItem , Comment
from .forms import CommentForm
from django.utils import timezone
from django.contrib import messages


def item_list (request):
    context = {'items':Item.objects.all()}
    return render (request,'index.html',context)

class CheckoutListView (ListView):
    model = Item
    template_name = 'checkout-page.html'



# def product (request):
#     context = {}
#     return render (request,'product-page.html',context)

class HomeView(ListView):
    model = Item
    template_name = 'index.html'
    paginate_by = 10
    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        context ['items'] = Item.objects.all()
        # context ['item_id'] = Item.objects.get(id=id)
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'
    
   

def add_to_cart(request,pk):
        item_id = Item.objects.get(pk=pk)
        order_item, created = OrderItem.objects.get_or_create(
            item=item_id,
            ordered=False)
        order_qs = Order.objects.filter(ordered=False)
        if order_qs.exists():
            order = order_qs [0]
            if order.items.filter (item__id = item_id.id).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request,"This item quantity was updated to your cart")
                return redirect('product-url',pk=pk)
            else :
                messages.info(request,"This item was added to your cart")
                order.items.add(order_item)
                return redirect('product-url',pk=pk)
        else :
            order_date = timezone.now()
            order = Order.objects.create(ordered_date=order_date)
            order.items.add(order_item)
            messages.info(request,"This item was added to your cart")
            return redirect('product-url',pk=pk)


def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
                form.save()
    else:
            form = CommentForm ()
    context = {'form':form}
    context ['comment'] = Comment.objects.all()
    context ['items'] = Item.objects.all()
    return render (request,'product-page.html',context=context)



def remove_from_cart(request, pk):
    item_id = Item.objects.get(pk=pk)
    order_qs = Order.objects.filter(ordered=False)
    if order_qs.exists():
        order = order_qs [0]
        #check if the order item is in the order
        if order.items.filter (item__pk = item_id.pk).exists():
            order_item = OrderItem.objects.filter(
                                        item=item_id,
                                        ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart")
            return redirect('summary-url')

        else:
            messages.info(request,"This item is not in your cart")
            return redirect('product-url',pk=pk)
    else:
        #add a message that the user dosent have order
        messages.info(request,"you dont have an active order")
        return redirect('product-url',pk=pk)
    return redirect('product-url',pk=pk)



def remove_singel_item_from_cart(request, pk):
    item_id = Item.objects.get(pk=pk)
    order_qs = Order.objects.filter(ordered=False)

    if order_qs.exists():
        order = order_qs [0]
        #check if the order item is in the order
        if order.items.filter (item__pk = item_id.pk).exists():
            order_item = OrderItem.objects.filter(
                                        item=item_id,
                                        ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
               order.items.remove(order_item) 
            messages.info(request,"This item quantity was updated to your cart")
            return redirect('summary-url')
            

        else:
            messages.info(request,"This item is not in your cart")
            return redirect('summary-url')
    else:
        #add a message that the user dosent have order
        messages.info(request,"you dont have an active order")
        return redirect('summary-url')
    return redirect('summary-url')
    



class OrderSummaryDetailView(View):
    
    def get(self,*kargs,**kwargs):
        order = Order.objects.get(ordered=False)
        context = {
                'object': order
                            }
        return render(self.request, 'order_summary.html', context=context)




class list(ListView):
    model = Item
    template_name = 'list.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(list, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['items2'] = Item.objects.all()
        return context


class detail(DetailView):
    model = Item
    template_name = 'dlist.html'
    def detail_view_pk(request,pk):
        quant = Item.objects.get(pk=pk)
        context ['Dlist'] = Item.objects.filter(title=quant)
        context ['k'] = Item.objects.all()
        return context

    # def get_context_data(self,**kwargs):       
    #     d=self.get(id=id)
    #     context = super(Item,self).get_context_data(**kwargs)
    #     
    #     return context

# slug_field = self.get_slug_field()
#         context ['Dlist'] = OrderItem.filter(**{slug_field: slug})
























# def detail(request,id):
#     d=Item.objects.get(id=id)
#     context = {}
#     context ['Dlist'] = OrderItem.objects.filter(item=d)
#     return render(request,'product-page.html',context=context)

# def get(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     context = self.get_context_data(object=self.object)
#     return self.render_to_response(context)

# models.SlugField (
#     verbose_name = "Slug",
#     allow_unicode = True,
#     unique=True)

# def list (request):
#     model = Item
    
#     context = {}
#     context['items2'] = Item.objects.all()
#     return render(request,'list.html',context=context)