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