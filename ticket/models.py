from django.db import models
from datetime import datetime    

# Create your models here.


class Ticket(models.Model):
    depart = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    date_du_vol = models.DateTimeField(default=datetime.now,blank=True)
    heure_du_vol = models.TimeField(auto_now=False, auto_now_add=False)
    places_restantes  = models.IntegerField()
    prix_ticket  = models.IntegerField()
 

    def __str__(self):
        return self.destination
