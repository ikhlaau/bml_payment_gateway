from django.urls import path
from . import views

urlpatterns = [
    path('webhook/order-created/', views.order_created, name='order_created'),
    path('test/', views.hello, name='test'),
]