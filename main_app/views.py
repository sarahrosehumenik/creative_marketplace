
from platform import java_ver
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Cart, Like
import os
import uuid
import boto3
import stripe


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

@login_required
def add_like(request, product_id, user_id):
    like = Like.objects.create(product_id=product_id, user_id=user_id)
    return redirect('products_index')

@login_required
def assoc_product(request, user_id, product_id):
    cart = Cart.objects.get(user_id=user_id)
    cart.products.add(product_id)
    return redirect('products_index')

@login_required
def unassoc_product(request, user_id, product_id):
    cart = Cart.objects.get(user_id=user_id)
    cart.products.remove(product_id)
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    print(request.user.id)
    cart = Cart.objects.get(user_id=request.user.id)
    products = cart.products.all()
    return render(request, 'cart/detail.html', { 'cart': cart, 'products': products })


#PROTUCT CBVs------------------------------------------------------------------------------
class ProductList(ListView): 
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        products = Product.objects.all()
        user_likes = Like.objects.filter(user_id=self.request.user.id)
        feed = []
        for product in products:
            like_count = product.like_set.all().count()
            user_liked = False
            for user_like in user_likes:
                if user_like.product.id == product.id:
                    user_liked = True
            feed.append({'product': product, 'like_count':like_count, 'user_liked': user_liked})
        #run algo on feed
        context['feed'] = feed
        return context
    
class ProductCreate(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['name','caption', 'description', 'price', 'quantity', 'photo_file']
    

    def form_valid(self, form):
        photo_file = self.request.FILES.get('photo_file', None)
        
        if photo_file:
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                # build the full url string
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                print(f"S3 URL!!!!!!!:\n\n{url}\n\n")
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
        
        form.instance.user = self.request.user
        #reassign photo_file field in the form to the s3 url
        form.instance.photo_file = url

        return super().form_valid(form)


class ProductDetail(DetailView):
    model = Product
    

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['caption', 'description', 'price', 'quantity',] #allowing quantity updates may cause problems later...

class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/products' 

#Stripe Views------------------------------------------------------------------------------

class CreateCheckoutSessionView(View):
    stripe.api_key = os.environ['STRIPE_SECRET_KEY']
    def post(self, request, *args, **kwargs):
        stripe_product = Product.objects.get(stripe_price_id=self.kwargs["pk"])
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': stripe_product.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.BASE_URL + '/payments/success/',
                cancel_url=settings.BASE_URL + '/payments/cancel/',
            )
        except Exception as e:
            print(f'\n\n{e}\n\n')

        return redirect(checkout_session.url)

def payment_success(request):
    return render(request, 'success.html')

def payment_cancel(request):
    return render(request, 'cancel.html')