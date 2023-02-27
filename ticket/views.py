from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from .models import Ticket
from .forms import TicketForm
from django.views import generic
from .forms import ContactForm
# CRUD - create, retrieve, update, delete, list


app_name =  'ticket'


class TicketListView(generic.ListView):
    template_name = "ticket/ticket_list.html"
    queryset = Ticket.objects.all()
    

# class TicketDetailView(generic.DetailView):
#     template_name = 'ticket/ticket_detail.html'
#     model = Ticket

class TicketDetailView(generic.DetailView):
    model = Ticket


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


