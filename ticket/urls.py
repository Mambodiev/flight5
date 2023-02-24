
from django.contrib import admin
from django.urls import path

from ticket.views import (
    ticket_list,
    ticket_retrieve,
    ticket_create,
    ticket_update,
    ticket_delete
)

urlpatterns = [
    path('', ticket_list),
    path('tickets/<pk>/', ticket_retrieve),
    path('tickets/<pk>/edit/', ticket_update),
    path('tickets/<pk>/delete/', ticket_delete),
    path('add-ticket/', ticket_create),
] 