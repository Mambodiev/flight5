from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "depart",
            "destination",
            "date_du_vol",
            "heure_du_vol",
            "places_restantes",
            "prix_ticket",
        ]
        widgets = {
        'date_du_vol': forms.TextInput(attrs={'type': 'date'}),
        'heure_du_vol': forms.TextInput(attrs={'type': 'Time'})

        }



