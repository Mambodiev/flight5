from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from .utils import get_or_set_order_session
from django.shortcuts import get_object_or_404, reverse, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Ticket, OrderItem
from .forms import TicketForm
from django.views import generic
from .forms import ContactForm, AddToCartForm, AddressForm
# CRUD - create, retrieve, update, delete, list


app_name =  'ticket'


class TicketListView(generic.ListView):
    template_name = "ticket/ticket_list.html"
    queryset = Ticket.objects.all()
    

# class TicketDetailView(generic.DetailView):
#     template_name = 'ticket/ticket_detail.html'
#     model = Ticket

class TicketDetailView(generic.FormView):
    template_name = 'ticket/ticket_detail.html'
    model = Ticket
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Ticket, pk=self.kwargs["pk"])

    def get_success_url(self):
            return reverse("ticket:summary")
    
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        ticket = self.get_object()

        item_filter = order.items.filter(ticket=ticket)

        if item_filter.exists():
            item = item_filter.first()
            item.quantity = int(form.cleaned_data['quantity'])
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.ticket = ticket
            new_item.order = order
            new_item.save()

        return super(TicketDetailView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['ticket'] = self.get_object()
        return context


class HomeView(generic.TemplateView):
    template_name = "tickets.html"

# def ticket_list(request):
#     tickets = Ticket.objects.all()
#     context = {
#         "tickets": tickets
#     }
#     return render(request, "tickets.html", context)


class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'

    def get_success_url(self):
        return reverse("contact")

    def form_valid(self, form):
        messages.info(
            self.request, "Thanks for getting in touch. We have received your message.")
        name = form.cleaned_data.get(_('name'))
        email = form.cleaned_data.get(_('email'))
        message = form.cleaned_data.get(_('message'))

        full_message = f"""
            Received message below from {name}, {email}
            ________________________


            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        return super(ContactView, self).form_valid(form)



class TicketView(generic.TemplateView):
    template_name = "ticket/ticket_view.html"

    def get_context_data(self, **kwargs):
        context = super(TicketView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context


class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("ticket:summary")


class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("ticket:summary")


class RemoveFromTicketView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("ticket:summary")


class CheckoutView(generic.FormView):
    template_name = 'ticket/checkout.html'
    form_class = AddressForm

    # def get_success_url(self):
    #     return reverse("cart:payment")

    # def form_valid(self, form):
    #     order = get_or_set_order_session(self.request)
    #     selected_shipping_address = form.cleaned_data.get(
    #         'selected_shipping_address')
    #     selected_billing_address = form.cleaned_data.get(
    #         'selected_billing_address')

    #     if selected_shipping_address:
    #         order.shipping_address = selected_shipping_address
    #     else:
    #         address = Address.objects.create(
    #             address_type='S',
    #             user=self.request.user,
    #             address_line_1=form.cleaned_data['shipping_address_line_1'],
    #             address_line_2=form.cleaned_data['shipping_address_line_2'],
    #             zip_code=form.cleaned_data['shipping_zip_code'],
    #             city=form.cleaned_data['shipping_city'],
    #         )
    #         order.shipping_address = address

    #     if selected_billing_address:
    #         order.billing_address = selected_billing_address
    #     else:
    #         address = Address.objects.create(
    #             address_type='B',
    #             user=self.request.user,
    #             address_line_1=form.cleaned_data['billing_address_line_1'],
    #             address_line_2=form.cleaned_data['billing_address_line_2'],
    #             zip_code=form.cleaned_data['billing_zip_code'],
    #             city=form.cleaned_data['billing_city'],
    #         )
    #         order.billing_address = address

    #     order.save()
    #     messages.info(
    #         self.request, "You have successfully added your addresses")
    #     return super(CheckoutView, self).form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = super(CheckoutView, self).get_form_kwargs()
    #     kwargs["user_id"] = self.request.user.id
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super(CheckoutView, self).get_context_data(**kwargs)
    #     context["order"] = get_or_set_order_session(self.request)
    #     return context

















def ticket_retrieve(request, pk):
    ticket = Ticket.objects.get(id=pk)
    context = {
        "ticket": ticket
    }
    return render(request, "ticket.html", context)


def ticket_create(request):
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {
        "form": form
    }
    return render(request, "ticket_create.html", context)


def ticket_update(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)

    if request.method == "POST":
        form = TicketForm(request.POST, files = request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {
        "form": form
    }
    return render(request, "ticket_update.html", context)


def ticket_delete(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.delete()
    return redirect("/")


