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
    path('products/<int:product_id>/like/<int:user_id>/', views.add_like, name='add_like'),
    path('products/<int:product_id>/add_comment/<int:user_id>/', views.add_comment, name='add_comment'),
    #CART URL PATHS--------------------------------------------------------------------------
    path('cart/<int:user_id>/assoc_product/<int:product_id>/', views.assoc_product, name='assoc_product'),
    path('cart/<int:user_id>/unassoc_product/<int:product_id>/', views.unassoc_product, name='unassoc_product'),
    path('cart/', views.cart_detail, name='cart_detail'),
    #PROFILE URL PATHS------------------------------------------------------------------------
    path('profile/', views.profile_likes, name='profile_likes'),
    #STRIPE URL PATHS------------------------------------------------------------------------
    path('payments/create-checkout-session/<pk>/', views.CreateCheckoutSessionView.as_view(), name='create-stripe-checkout-session'),
    path('payments/cancel/', views.payment_cancel, name='cancel-stripe-payment'),
    path('payments/success/', views.payment_success, name='success-stripe-payment'),
    #CATCH-ALL PATH FOR NOT FOUND
    #path('*/', views.not_found, name='url-not-found'),
]