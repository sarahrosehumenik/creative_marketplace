
from platform import java_ver
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Cart, Photo
from PIL import Image
import os
import uuid
import boto3
import asyncio


# VIEW FUNCTIONS----------------------------------------------------------------------------
def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f'USER ID!!! {user.id}')
            cart = Cart.objects.create(user_id=user.id)
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

def add_photo(request, product_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            print(f"S3 URL!!!!!!!: {url}")
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, product_id=product_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('products_index')

@login_required
def assoc_product(request, user_id, product_id):
    cart = Cart.objects.get(user_id=user_id)
    cart.products.add(product_id)
    return redirect('products_index')

@login_required
def cart_detail(request):
    print(request.user.id)
    cart = Cart.objects.get(user_id=request.user.id)
    products = cart.products.all()
    return render(request, 'cart/detail.html', { 'cart': cart, 'products': products })

#PROTUCT CBVs------------------------------------------------------------------------------
class ProductList(ListView): 
    model = Product
    
class ProductCreate(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['name','caption', 'description', 'price', 'quantity', 'photo_file']
    

    def form_valid(self, form):
        print(f"This is our request!!!!!!!!!!!:\n\n{self.request.FILES.get('photo_file', None)}\n\n")
        photo_file = self.request.FILES.get('photo_file', None)
        
        print(f'\n\n the photo file\n{photo_file}')
        if photo_file:
            # print(f'\n\n1My image file is closed: \n\n {photo_file.closed}')
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            # print(f'\n\n2My image file is closed: \n\n {photo_file.closed}')
            # just in case something goes wrong
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                # print(f'\n\n3My image file is closed: \n\n {photo_file.closed}')
                # build the full url string
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                print(f"S3 URL!!!!!!!:\n\n{url}\n\n")
                # we can assign to cat_id or cat (if you have a cat object)
                #Photo.objects.create(url=url, product_id=product_id)
                # print(f'\n\n4My image file is closed: \n\n {photo_file.closed}')
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
        
        form.instance.user = self.request.user
        # print('\n\ncode is working here\n\n')
        # open_photo_file = self.request.FILES.get('photo_file', None)
        # print(f'\n\n5My re-gotten image file is closed: \n {open_photo_file.closed}')
        
        
        form.instance.photo_file = url
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

# class CartList(LoginRequiredMixin, ListView):
#     model = Cart

