from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    #PRODUCTS URL PATHS----------------------------------------------------------------------
    path('products/', views.ProductList.as_view(), name="products_index"),
    path('products/create/', views.ProductCreate.as_view(), name='products_create'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='products_detail'),
    path('products/<int:pk>/update', views.ProductUpdate.as_view(), name='products_update'),
    path('products/<int:pk>/delete', views.ProductDelete.as_view(), name='products_delete'),
    #CART URL PATHS--------------------------------------------------------------------------
    path('cart/<int:user_id>/assoc_product/<int:product_id>/', views.assoc_product, name='assoc_product'),
    path('cart/<int:user_id>/unassoc_product/<int:product_id>/', views.unassoc_product, name='unassoc_product'),
    path('cart/', views.cart_detail, name='cart_detail'),
]