from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q

from event.models import Event
from .forms import ReservationForm

def choose_tickets_panel(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    free_tickets = event.ticket_types.all().values('type', 'price') \
        .annotate(total=Count('tickets', distinct=True, filter=Q(tickets__reservation__isnull=True)))
    form = ReservationForm(free_tickets=list(free_tickets))
    return render(request, 'reservation/buy_tickets.html', {'event': event, 'free_tickets': free_tickets,
                                                            'form': form})
