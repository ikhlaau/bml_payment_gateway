from django.contrib import admin
from intergration.models import *

# Register your models here.



class Shopify_admin(admin.ModelAdmin):
	list_display = [field.name for field in Shopify._meta.fields if field.name != "id"]
admin.site.register(Shopify,Shopify_admin)



class ShopifyOrder_admin(admin.ModelAdmin):
	list_display = [field.name for field in ShopifyOrder._meta.fields if field.name != "id"]
admin.site.register(ShopifyOrder,ShopifyOrder_admin)
