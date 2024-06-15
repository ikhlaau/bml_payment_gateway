from django.urls import path
from . import views

urlpatterns = [
    path('webhook/order-created/', views.order_created, name='order_created'),
    path('checkout/', views.checkout, name='checkout'),
    path('from_bml/', views.from_bml, name='from_bml'),
]