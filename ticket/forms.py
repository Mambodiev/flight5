from django.forms import ModelForm
from allauth.account.forms import SignupForm
from .models import Ticket


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "depart",
            "destination",
            "escale",
            "date_du_vol",
            "heure_du_vol",
            "places_restantes",
            "prix_ticket",
        ]



