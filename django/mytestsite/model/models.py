from operator import mod
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Test(models.Model):
  name=models.CharField(max_length=20)
  gender=models.CharField(max_length=10)

class discount(models.Model):
  name=models.CharField(max_length=20)
  Discount=models.IntegerField(default=1)
class product(models.Model):
  product_name=models.CharField(max_length=30)
  category=models.CharField(max_length=30)
  describe=models.CharField(max_length=10000)
  price=models.IntegerField(default=0)
  dsc=models.ForeignKey(discount,on_delete=models.CASCADE,related_name='discountOf',default='',blank=True,null=True)
  number_of_purchases=models.IntegerField(default=0)
  Details=models.CharField(default='',max_length=1000)
class shopping_cart(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='usernameOf')
  product_name=models.ForeignKey(product,on_delete=models.SET_NULL,null = True,related_name='product_nameOf')
  created=models.DateTimeField(auto_now_add=True)
  counts=models.IntegerField(default=1)
class purchase_record_model(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pr_usernameOf')
  product_name=models.ForeignKey(product,on_delete=models.SET_NULL,null = True,related_name='pr_product_nameOf')
  created=models.DateTimeField(auto_now_add=True)
