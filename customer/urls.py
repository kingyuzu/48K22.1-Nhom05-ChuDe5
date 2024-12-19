from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('ticket/list/', views.ticket_list, name='ticket_list'),
    path('', lambda request: redirect('/products/', permanent=True)),
    path('products/', views.product_list),
]
