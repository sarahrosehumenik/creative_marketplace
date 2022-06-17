from itertools import product
from unittest.util import _MIN_COMMON_LEN
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
   hashtag = models.CharField(max_length=50) 

   def __str__(self):
    return self.hashtag
   
class Product(models.Model):
    name = models.CharField(max_length= 100)
    caption = models.CharField(max_length=140)
    description = models.TextField(max_length=2000) 
    price = models.IntegerField(default= 0)
    tags = models.ManyToManyField(Tag)
    quantity = models.IntegerField(default= 1)
    photo_file = models.ImageField(upload_to='images/', max_length=300)
    #stripe fields
    stripe_product_id = models.CharField(max_length=100, blank=True, default='')
    stripe_price_id = models.CharField(max_length=100, blank=True, default='')
    #product creator field
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def get_absolute_url(self):
       return reverse('products_index')

    def __str__(self):
       return self.name

class Comment(models.Model):
   product = models.ForeignKey(Product, on_delete= models.CASCADE)
   user = models.ForeignKey(User, on_delete= models.CASCADE)
   text = models.TextField(max_length=300)
   
class Like(models.Model):
   product = models.ForeignKey(Product, on_delete= models.CASCADE)
   user = models.ForeignKey(User, on_delete= models.CASCADE)


class Cart(models.Model):
   products = models.ManyToManyField(Product)
   user = models.ForeignKey(User, on_delete = models.CASCADE)

   

   
   


    #many to manyfield for tags/categories

