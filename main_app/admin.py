from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Product, Cart, Like, Comment, Tag

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Tag)

from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})