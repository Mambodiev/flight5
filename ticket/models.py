from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime    
from django.shortcuts import reverse


User = get_user_model()

# Create your models here.


class Ticket(models.Model):
    depart = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    date_du_vol = models.DateTimeField(default=datetime.now,blank=True)
    heure_du_vol = models.TimeField(auto_now=False, auto_now_add=False)
    places_restantes  = models.IntegerField()
    prix_ticket  = models.IntegerField()
 

    def __str__(self):
        return self.depart
    

    def get_absolute_url(self):
        return reverse("ticket:ticket-detail", kwargs={'pk': self.pk})
    
    # def get_absolute_url(self):
    #     return reverse('ticket-detail', args=[str(self.id)])



class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", related_name='items', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} x {self.ticket.depart}"
    


class Order(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

