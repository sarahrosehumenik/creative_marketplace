from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Cart

# VIEW FUNCTIONS----------------------------------------------------------------------------
def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # cart = Cart.objects.create()
            #automatically log in any newly created user
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid signup, try agian'
    #If we click signup, thats a GET req, so we hit this code
    #If we hit submit (that's POST) and the form isn't valid, we hit this code and show another empty form         
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def assoc_product(request, user_id, product_id):
    cart = Cart.objects.get(user_id=user_id)
    cart.products.add(product_id)
    return redirect('products_index')

#PROTUCT CBVs------------------------------------------------------------------------------
class ProductList(ListView): 
    model = Product
    
class ProductCreate(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['name','caption', 'description', 'price', 'quantity']

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


class ProductDetail(DetailView):
    model = Product

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['caption', 'description', 'price', 'quantity'] #allowing quantity updates may cause problems later...

class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/products' 

#CART CBVs------------------------------------------------------------------------------

class CartList(LoginRequiredMixin, ListView):
    model = Cart
