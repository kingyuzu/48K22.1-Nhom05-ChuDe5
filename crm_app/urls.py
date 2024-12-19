"""
URL configuration for crm_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from admin_manager.views import (
    TicketAPIView,
    CampaignAPIView,
    MailTrackAPIView,
    SendCampaignEmailAPIView,
    AddEmailsToCampaignAPIView,
    ContactAPIView,
    track_click,
    track_open_email,
    track_unsubscribe,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("customer.urls")),  # Include app URLs
    path("system-admin/", include("admin_manager.urls"), name="system-admin"),

    # Ticket APIs
    path("api/tickets/", TicketAPIView.as_view(),
         name="tickets"),  # List and Create
    path(
        "api/tickets/<str:ticket_id>/", TicketAPIView.as_view(), name="ticket"
    ),  # Retrieve, Update, Delete
    # Campaign APIs
    path(
        "api/campaigns/", CampaignAPIView.as_view(), name="campaigns"
    ),  # List and Create
    path(
        "api/campaigns/<str:campaign_id>/", CampaignAPIView.as_view(), name="campaigns"
    ),  # Retrieve, Update, Delete
    path(
        "api/campaigns/<str:campaign_id>/add-emails", AddEmailsToCampaignAPIView.as_view(), name="campaign_emails"
    ),
    # Add emails to Campaign
    # api/campaigns/33/send-emails
    path(
        "api/campaigns/<str:campaign_id>/send-emails",
        SendCampaignEmailAPIView.as_view(),
        name="send_campaign_emails",
    ),
    # MailTrack APIs
    path(
        "api/mail-tracks/", MailTrackAPIView.as_view(), name="mailtracks"
    ),  # List and Create
    path(
        "api/mail-tracks/<str:track_id>/", MailTrackAPIView.as_view(), name="mailtracks"
    ),  # Retrieve, Update, Delete
    # Track email events
    path("email/open/<str:track_id>/", track_open_email, name="track_open_email"),
    path(
        "email/unsubscribe/<str:track_id>/", track_unsubscribe, name="track_unsubscribe"
    ),
    path("email/click/<str:track_id>/", track_click, name="track_click"),

    # Contacts APIs
    path(
        "api/contacts/", ContactAPIView.as_view(), name="contacts"
    ),  # List and Create
    path(
        "api/contacts/<str:contact_id>/", ContactAPIView.as_view(), name="contacts"
    ),  # Retrieve, Update, Delete
]
