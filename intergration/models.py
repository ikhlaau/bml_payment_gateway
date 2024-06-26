from django.db import models

# Create your models here.


class Shopify(models.Model):
    name = models.CharField(max_length=250,null=False,blank=False)
    webhook_secret = models.CharField(max_length=250,null=False,blank=False)
    api_key = models.CharField(max_length=250,null=False,blank=False)
    shop_name = models.CharField(max_length=250,null=True)
    password = models.CharField(max_length=250,null=True)
    bml_key = models.CharField(max_length=500,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.shop_name) 

class ShopifyOrder(models.Model):
    order_id = models.CharField(max_length=200,null=False,blank=False)
    shop_id = models.CharField(max_length=200,null=False,blank=False)
    checkout_id = models.CharField(max_length=200,null=True,blank=True)
    cart_token = models.CharField(max_length=200,null=True,blank=True)
    checkout_token = models.CharField(max_length=200,null=True,blank=True)
    confirmation_number = models.CharField(max_length=200,null=True,blank=True)
    order_number = models.CharField(max_length=200,null=True,blank=True)
    order_status_url = models.CharField(max_length=250,null=True,blank=True)
    token = models.CharField(max_length=200,null=True,blank=True)
    reference = models.CharField(max_length=200,null=True,blank=True)
    total_price = models.CharField(max_length=200,null=False,blank=False)
    presentment_currency = models.CharField(max_length=200,null=False,blank=False)
    payment_url = models.CharField(max_length=200,null=True,blank=True)
    payment_status = models.CharField(max_length=200,null=False,blank=False)
    gateway_id = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.order_id) + " " + str(self.order_number)