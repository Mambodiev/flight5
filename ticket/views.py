from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from .utils import get_or_set_order_session
from django.shortcuts import get_object_or_404, reverse, redirect, render

from .models import Ticket
from .forms import TicketForm
from django.views import generic
from .forms import ContactForm, AddToCartForm
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
            return reverse("ticket:ticket-list")
    
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        ticket = self.get_object()

        item_filter = order.items.filter(ticket=ticket)

        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
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


