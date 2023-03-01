from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime    
from django.shortcuts import reverse


User = get_user_model()

# Create your models here.


class Ticket(models.Model):

    VILLE_DE_DEPART = (
        ('Bunia', 'Bunia'),
        ('Kisangani', 'Kisangani'),
        ('Aru', 'Aru'),
        ('Mahagi', 'Mahagi'),
        ('Beni', 'Beni'),
         ('Goma', 'Goma'),
    )


    VILLE_DE_ARRIVEE = (  
        ('Bunia', 'Bunia'),
        ('Kisangani', 'Kisangani'),
        ('Aru', 'Aru'),
        ('Mahagi', 'Mahagi'),
        ('Beni', 'Beni'),
         ('Goma', 'Goma'),
    )


    depart = models.CharField(max_length=150, choices=VILLE_DE_DEPART, default='New')
    destination = models.CharField(max_length=150, choices=VILLE_DE_ARRIVEE, default='New')
    date_du_vol = models.DateTimeField(default=datetime.now, blank=True,  null=True )
    heure_du_vol = models.TimeField(auto_now=False, auto_now_add=False)
    places_restantes  = models.IntegerField()
    prix_ticket  = models.IntegerField(default=0)
 

    def __str__(self):
        return self.depart
    

    def get_absolute_url(self):
        return reverse("ticket:ticket-detail", kwargs={'pk': self.pk})
    
    # def get_absolute_url(self):
    #     return reverse('ticket-detail', args=[str(self.id)])

    def get_price(self):
        return "{:.2f}".format(self.prix_ticket / 100)



class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", related_name='items', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} x {self.ticket.depart}"
    
    def get_raw_total_item_price(self):
        return self.quantity * self.ticket.prix_ticket

    def get_total_item_price(self):
        price = self.get_raw_total_item_price()  # 1000
        return "{:.2f}".format(price / 100)
    


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
    
    def get_raw_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_raw_total_item_price()
        return total
    
    def get_subtotal(self):
        subtotal = self.get_raw_subtotal()
        return "{:.2f}".format(subtotal / 100)

    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()
        # add tax, add delivery, subtract discounts
        # total = subtotal - discounts + tax + delivery
        return subtotal

    def get_total(self):
        total = self.get_raw_total()
        return "{:.2f}".format(total / 100)

