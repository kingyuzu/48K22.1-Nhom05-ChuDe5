from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('contact/', views.contact_view, name='admin-contact'),
    path('contact/<str:contact_id>/', views.contact_detail_view,
         name='admin-contact-detail'),
    path('contacts/export/', views.export_contacts_csv,
         name='export_contacts_csv'),

    # Product pages config
    path('product/', views.product_view, name='admin-product'),
    path('product/<str:product_id>/', views.product_detail_view,
         name='admin-product-detail'),

    path('order/', views.order_view, name='admin-order'),
    path('order/<str:order_id>/', views.order_detail_view,
         name='admin-order-detail'),
    path('ticket/', views.ticket_view, name='admin-ticket'),
    path('ticket-detail/<str:ticket_id>/',
         views.ticket_detail_view, name='admin-ticket-detail'),
    path('campaign/', views.campaign_view, name='admin-campaign'),
    path('campaign-detail/<str:campaign_id>/',
         views.campaign_detail_view, name='admin-campaign-detail'),
    path('campaign/update/<str:campaign_id>/',
         views.update_campaign_email, name='update_campaign_email'),
    path('', lambda request: redirect('contact/')),
]
