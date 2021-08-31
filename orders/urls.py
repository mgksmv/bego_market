from django.urls import path

from . import views

urlpatterns = [
    path('', views.orders, name='orders'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-complete/', views.order_complete, name='order_complete')
]
