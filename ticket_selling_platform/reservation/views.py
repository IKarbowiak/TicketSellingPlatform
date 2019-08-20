from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from event.models import Event
from .forms import ReservationForm

def choose_tickets_panel(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    free_tickets = event.tickets.all().filter(reservation__isnull=True).values('type', 'price').annotate(total=Count('pk'))
    form = ReservationForm(free_tickets=list(free_tickets))
    return render(request, 'reservation/buy_tickets.html', {'event': event, 'free_tickets': free_tickets,
                                                            'form': form})
