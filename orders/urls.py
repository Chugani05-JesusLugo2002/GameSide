from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:order_pk>/', views.order_detail, name='order-detail'),
    path('<int:order_pk>/confirm/', views.confirm_order, name='confirm-order'),
    path('<int:order_pk>/cancel/', views.cancel_order, name='cancel-order'),
    path('<int:order_pk>/pay/', views.pay_order, name='pay-order'),
]
