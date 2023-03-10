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


class AddressForm(forms.Form):

    shipping_address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Appartement, Suite, etc'}),
                  max_length=50, required=False)
    shipping_address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Appartement, Suite, etc'}),
                  max_length=50, required=False)
    shipping_zip_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Zip code'}),
                  max_length=50, required=False)
    shipping_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City'}),
                  max_length=50, required=False)

    billing_address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Appartement, Suite, etc'}),
                  max_length=50, required=False)
    billing_address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Appartement, Suite, etc'}),
                  max_length=50, required=False)
    billing_zip_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Zip code'}),
                  max_length=50, required=False)
    billing_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City'}),
                  max_length=50, required=False)

    # selected_shipping_address = forms.ModelChoiceField(
    #     Address.objects.none(), required=False
    # )
    # selected_billing_address = forms.ModelChoiceField(
    #     Address.objects.none(), required=False
    # )

    # def __init__(self, *args, **kwargs):
    #     user_id = kwargs.pop('user_id')
    #     super().__init__(*args, **kwargs)

    #     user = User.objects.get(id=user_id)

    #     shipping_address_qs = Address.objects.filter(
    #         user=user,
    #         address_type='S'
    #     )
    #     billing_address_qs = Address.objects.filter(
    #         user=user,
    #         address_type='B'
    #     )

    #     self.fields['selected_shipping_address'].queryset = shipping_address_qs
    #     self.fields['selected_billing_address'].queryset = billing_address_qs

    # def clean(self):
    #     data = self.cleaned_data

    #     selected_shipping_address = data.get('selected_shipping_address', None)
    #     if selected_shipping_address is None:
    #         if not data.get('shipping_address_line_1', None):
    #             self.add_error("shipping_address_line_1",
    #                            "Please fill in this field")
    #         if not data.get('shipping_address_line_2', None):
    #             self.add_error("shipping_address_line_2",
    #                            "Please fill in this field")
    #         if not data.get('shipping_zip_code', None):
    #             self.add_error("shipping_zip_code",
    #                            "Please fill in this field")
    #         if not data.get('shipping_city', None):
    #             self.add_error("shipping_city", "Please fill in this field")

    #     selected_billing_address = data.get('selected_billing_address', None)
    #     if selected_billing_address is None:
    #         if not data.get('billing_address_line_1', None):
    #             self.add_error("billing_address_line_1",
    #                            "Please fill in this field")
    #         if not data.get('billing_address_line_2', None):
    #             self.add_error("billing_address_line_2",
    #                            "Please fill in this field")
    #         if not data.get('billing_zip_code', None):
    #             self.add_error("billing_zip_code",
    #                            "Please fill in this field")
    #         if not data.get('billing_city', None):
    #             self.add_error("billing_city", "Please fill in this field")