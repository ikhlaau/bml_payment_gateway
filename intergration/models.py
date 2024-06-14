from django.db import models

# Create your models here.


class Shopify(models.Model):
    number = models.CharField(max_length=10,null=False,blank=False)
    secret = models.CharField(max_length=10,null=False,blank=False)
    rateplan = models.CharField(max_length=10,null=False,blank=False)
    name = models.CharField(max_length=250,null=True)
    sex = models.CharField(max_length=6,null=True)
    dob = models.DateField(null=True)
    # user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.number) + " " + str(self.name)

class ShopifyOrder(models.Model):
    order_id = models.CharField(max_length=200,null=False,blank=False)
    checkout_id = models.CharField(max_length=200,null=False,blank=False)
    cart_token = models.CharField(max_length=200,null=False,blank=False)
    checkout_token = models.CharField(max_length=200,null=False,blank=False)
    confirmation_number = models.CharField(max_length=200,null=False,blank=False)
    order_number = models.CharField(max_length=200,null=False,blank=False)
    order_status_url = models.CharField(max_length=250,null=False,blank=False)
    token = models.CharField(max_length=200,null=False,blank=False)
    total_price = models.CharField(max_length=200,null=False,blank=False)
    presentment_currency = models.CharField(max_length=200,null=False,blank=False)
    payment_url = models.CharField(max_length=200,null=True,blank=True)
    payment_status = models.CharField(max_length=200,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.number) + " " + str(self.name)