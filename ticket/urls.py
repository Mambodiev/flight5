
from django.contrib import admin
from django.urls import path

from ticket import views

app_name = 'ticket'

from ticket.views import (
    # ticket_list,
    ticket_retrieve,
    ticket_create,
    ticket_update,
    ticket_delete
)

urlpatterns = [
    # path('', ticket_list),
    path('',views.HomeView.as_view(), name='home'),
    path('ticket-list/',views.TicketListView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('tickets/<pk>/', ticket_retrieve),
    path('tickets/<pk>/edit/', ticket_update),
    path('tickets/<pk>/delete/', ticket_delete),
    path('add-ticket/', ticket_create),
] 