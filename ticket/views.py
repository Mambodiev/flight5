from django.shortcuts import render, redirect
from .models import Ticket
from .forms import TicketForm

# CRUD - create, retrieve, update, delete, list


def ticket_list(request):
    tickets = Ticket.objects.all()
    context = {
        "tickets": tickets
    }
    return render(request, "tickets.html", context)


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


