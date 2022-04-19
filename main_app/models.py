from itertools import product
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length= 100)
    caption = models.CharField(max_length=140)
    description = models.TextField(max_length=2000) 
    price = models.IntegerField(default= 0)
    quantity = models.IntegerField(default= 1)
    likes = models.IntegerField(default= 0)
    photo_file = models.ImageField(upload_to='images/', max_length=300)

    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def get_absolute_url(self):
       return reverse('products_index')

    def __str__(self):
       return self.name

class Cart(models.Model):

   products = models.ManyToManyField(Product)
   
   user = models.ForeignKey(User, on_delete = models.CASCADE)

   
   
class Photo(models.Model):
    url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"S3 Photo url!!!!!!!!!!!: {self.url}"
   



    #many to manyfield for tags/categories

