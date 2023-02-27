from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Ticket, OrderItem

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




class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': _("Your name")
    }), label=_('Name'))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': _("Your e-mail")
    }), label=_('Email'))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': _('Your message')
    }), label=_('Message'))


class AddToCartForm(forms.ModelForm):
    class Meta:
        model =OrderItem
        fields = ['quantity']
