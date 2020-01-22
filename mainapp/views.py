from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,ListView,DeleteView,DetailView,View
from .models import ItemModel, OrderModel , OrderItemModel , CommentModel , BillingAddressModel,CheckoutModel,UserProfileModel,RefundRequestModel
from .forms import CommentForm,UserProfileForm,OrderItemForm
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import random
import string
from django.db.models import Q





def track(request):
    context = {}
    context['order_num'] = OrderModel.objects.filter(user=request.user)
    return render (request,'track_order.html',context)  

def testproductpage(request):
    context = {}
    return render (request,'product-pageTest.html',context)  

def CreateOrderNumber():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=20))

def item_list (request):
    context = {'items':ItemModel.objects.all()}
    return render (request,'index.html',context)

#--------------------------------------------------------------------------------
#Checkout ListView :

class CheckoutListView(CreateView):
    model = CheckoutModel
    template_name = 'checkout-page.html'
    success_url = reverse_lazy('Thankyou-url')
    fields = '__all__'

    def get_context_data(self,**kwargs):
        context = super(CheckoutListView,self).get_context_data(**kwargs)
        order = OrderModel.objects.get(user=self.request.user,ordered=False)
        context['order'] = order
        return context
 
#--------------------------------------------------------------------------------
#ThankYou/Pay on Delivery Method :

def Tankyou(request):
    # deliverd = OrderItemModel.objects.get(user=request.user,ordered=False)
    order = OrderModel.objects.get(user=request.user,ordered=False)
    order_items = order.items.all()
    order_items.update(ordered=True)

    for item in order_items :
        item.save()
    
    order.ordered = True
    order.being_deliverd = True
    order.order_number = CreateOrderNumber()
    order.save()
    # order_items.update(ordered=True)
    # for item in order_items:
    #     item.save()
    return render (request,'Thankyou.html')

#--------------------------------------------------------------------------------
#HoemPage ListView :

class HomeView(ListView):
    model = ItemModel
    template_name = 'index.html'
    paginate_by = 10

    def get(self,request):

        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return redirect('employer_url')
            return super().get(request)
            messages.info(self.request,"Sorry Your are not allowed to visit this page")
    
        else:
            return super().get(request)
        
    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        context ['items'] = ItemModel.objects.all()
        context['profile'] = UserProfileModel.objects.all()
        return context

    def get_queryset(self):
        return super().get_queryset()[:5]
      


#--------------------------------------------------------------------------------
#Check On User Auth. Method :   -Data Filling

class check_on_user(CreateView):
    model = ItemModel
    template_name = 'Employer_Data_Page.html'
    success_url = reverse_lazy('item-list-url')
    fields = '__all__'

    def get_context_data(self,**kwargs):
        context = super(check_on_user,self).get_context_data(**kwargs)
        order = OrderModel.objects.all()
        context['order'] = order
        return context
    

#--------------------------------------------------------------------------------
#Product Page Method :

class ItemDetailView(DetailView):
    model = ItemModel
    template_name = 'product-page.html'
    def get_context_data(self,**kwargs):
        context = super(ItemDetailView,self).get_context_data(**kwargs)
        context['obj'] = ItemModel.objects.all()
        context ['comment'] = CommentModel.objects.all()
        return context
    
    
   
#--------------------------------------------------------------------------------
# Add To Cart Method :

def add_to_cart(request,pk):
        if request.method == 'POST':
                form = OrderItemForm(request.POST)
                item_id = ItemModel.objects.get(pk=pk)
                order_item, created = OrderItemModel.objects.get_or_create(
                    user=request.user,
                    item=item_id,
                    ordered=False)
                order_qs = OrderModel.objects.filter(user=request.user,ordered=False)
                if order_qs.exists():
                    order = order_qs [0]
                    if order.items.filter (item__id = item_id.id).exists():
                        order_item.quantity += 1
                        order_item.save()
                        messages.info(request,"This item quantity was updated to your cart")
                        return redirect('summary-url')
                    else :
                        messages.info(request,"This item was added to your cart")
                        order.items.add(order_item)
                        return redirect('summary-url')
                else :
                    order_date = timezone.now()
                    order = OrderModel.objects.create(user=request.user,ordered_date=order_date)
                    order.items.add(order_item)
                    messages.info(request,"This item was added to your cart")
                    return redirect('summary-url')
        else:
            form = OrderItemForm ()
        context = {'form':form}
        return render (request,'order_summary.html',context=context)
#--------------------------------------------------------------------------------
#Comment Method :

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
                form.save()
    else:
            form = CommentForm ()
    context = {'form':form}
    context ['comment'] = CommentModel.objects.all()
    context ['items'] = ItemModel.objects.all()
    return render (request,'comments.html',context=context)

#--------------------------------------------------------------------------------
# Remove From Cart Method :

def remove_from_cart(request, pk):
        if request.method == 'POST':
            form = OrderItemForm(request.POST)
            item_id = ItemModel.objects.get(pk=pk)
            order_qs = OrderModel.objects.filter(user=request.user,ordered=False)
            if order_qs.exists():
                order = order_qs [0]
                #check if the order item is in the order
                if order.items.filter (item__pk = item_id.pk).exists():
                    order_item = OrderItemModel.objects.filter(
                                                user=request.user,
                                                item=item_id,
                                                ordered=False)[0]
                    order.items.remove(order_item)
                    messages.info(request,"This item was removed from your cart")
                    return redirect('summary-url')

                else:
                    messages.info(request,"This item is not in your cart")
                    return redirect('summary-url')
            else:
                #add a message that the user dosent have order
                messages.info(request,"you dont have an active order")
        else:
            form = OrderItemForm ()
        context = {'form':form}
        context['item'] = OrderItemModel.objects.all() 
        return render (request,'order_summary.html',context=context)
        

            # return HttpResponseRedirect(reverse_lazy('product-url'))
            # return redirect('product-url',pk=pk)

#--------------------------------------------------------------------------------
#RemoveSingleItemFromCart Method :

def remove_singel_item_from_cart(request, pk):
    if request.method == 'POST':
            form = OrderItemForm(request.POST)
            item_id = ItemModel.objects.get(pk=pk)
            order_qs = OrderModel.objects.filter(user=request.user,ordered=False)
            if order_qs.exists():
                order = order_qs [0]
                #check if the order item is in the order
                if order.items.filter (item__pk = item_id.pk).exists():
                    order_item = OrderItemModel.objects.filter(
                                                user=request.user,
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
    else:
            form = OrderItemForm ()
        
    
#--------------------------------------------------------------------------------
#Order DetailViwe :

class OrderSummaryDetailView(View):
    
    def get(self,*kargs,**kwargs):
        try:
            order = OrderModel.objects.get(user=self.request.user,ordered=False)
            context = {
                    'object': order
                                }
            return render(self.request, 'order_summary.html', context=context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You dont have an active order")
            return redirect('/')


def cart_item_count(request):
    if user.is_authenticated:
        qs=OrderModel.objects.filter(user=self.request.user,ordered=False)
        if qs.exists():
            return qs[0].items.count()

    return 0


#---------------------------------------------------------------------------------------------
# Refund system :

class RefundRequest(CreateView):
    model = RefundRequestModel
    template_name = "refund_req_form.html"
    success_url = reverse_lazy('item-list-url')
    fields = '__all__'


    # def get_context_data(self,**kwargs):
        # context = super(RefundRequest,self).get_context_data(**kwargs)
        # order1 = OrderModel.objects.filter(user=self.request.user)
        # refund_req = order.objects.all()
        # refund_req.update(refund_request=True)
        # refund_req.save()
        # return context
 

#--------------------------------------------------------------------------------
#Profile ListViwe :
class ProfileListView(ListView):
    model = UserProfileModel
    template_name = 'profile.html'
    def get_context_data(self,**kwargs):
        context = super(ProfileListView,self).get_context_data(**kwargs)
        context['order_num'] = OrderModel.objects.filter(user=self.request.user)
        context['data'] = CheckoutModel.objects.all()
        return context

#--------------------------------------------------------------------------------
#ALLProduct ListViwe :

class ProductList(ListView):
    model = ItemModel
    template_name = "product_catigory.html"

    def get_queryset(self):
       queryset = super().get_queryset()
       query = self.request.GET.get("q")
       if query:
        queryset = self.model.objects.filter(title__icontains=query)
       return queryset

#--------------------------------------------------------------------------------
#About/Contact ListViwe :

class Contact(ListView):
    model = ItemModel
    template_name = "contact.html"


class AboutList(ListView):
    model = ItemModel
    template_name = "about.html"


#--------------------------------------------------------------------------------
#Beds ListViwe :

class BedsList(ListView):
    model = ItemModel
    template_name = "Beds.html"
    def get_context_data(self,**kwargs):
        context = super(BedsList,self).get_context_data(**kwargs) 
        context['bed_cat'] = self.model.objects.filter(catigory="B")
        return context    



#--------------------------------------------------------------------------------
#Desks ListViwe :

class DesksList(ListView):
    model = ItemModel
    template_name = "Desks.html" 
    def get_context_data(self,**kwargs):
            context = super(DesksList,self).get_context_data(**kwargs) 
            context['desk_cat'] = self.model.objects.filter(catigory="D")
            return context      
    

#--------------------------------------------------------------------------------
#Lamps ListViwe : 

class LigthingList(ListView):
    model = ItemModel
    template_name = "Lighting.html"
    def get_context_data(self,**kwargs):
            context = super(LigthingList,self).get_context_data(**kwargs) 
            context['ligting_cat'] = self.model.objects.filter(catigory="L")
            return context  


class ServicesListView(ListView):
    model = ItemModel
    template_name = "services.html"




# def rating 
# class SearchListView(ListView):
#     model = ItemModel
#     template_name = "search_results.html"

#     def get_queryset(self):
#        queryset = super().get_queryset().filter(title=True)
#        query = self.request.GET.get("q")
#        if query:
#         queryset = queryset.filter(title__icontains=query)
#        return queryset

#     def get_context_data(self, **kwargs):
#        context = super(SearchListView, self).get_context_data(**kwargs)
#        context['queryset'] = self.get_queryset()
#        context['category'] = ItemModel.objects.all()
#        return context




















    # def get_context_data(self,**kwargs):       
    #     d=self.get(id=id)
    #     context = super(Item,self).get_context_data(**kwargs)
    #     
    #     return context

# slug_field = self.get_slug_field()
#         context ['Dlist'] = OrderItem.filter(**{slug_field: slug})





class list(ListView):
    model = ItemModel
    template_name = 'list.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(list, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['items2'] = ItemModel.objects.all()
        return context


class detail(DetailView):
    model = ItemModel
    template_name = 'dlist.html'
    def detail_view_pk(request,pk):
        quant = ItemModel.objects.get(pk=pk)
        context ['Dlist'] = ItemModel.objects.filter(title=quant)
        context ['k'] = ItemModel.objects.all()
        return context










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