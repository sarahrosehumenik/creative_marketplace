from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('products/', views.ProductList.as_view(), name="products_index"),
    path('products/create/', views.ProductCreate.as_view(), name='products_create'),

]