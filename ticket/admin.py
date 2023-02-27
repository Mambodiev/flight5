from django.contrib import admin
from .models import Ticket, OrderItem, Order


admin.site.register(Ticket)
admin.site.register(OrderItem)
admin.site.register(Order)
