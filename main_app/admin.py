from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Product, Cart, Like, Comment

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Like)
admin.site.register(Comment)