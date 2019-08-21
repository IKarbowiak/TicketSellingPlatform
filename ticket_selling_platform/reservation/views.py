from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q

from event.models import Event
from .forms import ReservationForm

def choose_tickets_panel(request, event_pk):
    row_length = 10
    event = get_object_or_404(Event, pk=event_pk)
    free_tickets = event.ticket_types.all().values('type', 'price') \
        .annotate(total=Count('tickets', distinct=True, filter=Q(tickets__reservation__isnull=True)))
    ticket_types_data = []
    for ticket_type in event.ticket_types.all().order_by('-price'):
        counter = 0
        ticket_data = []
        row = []
        for ticket in ticket_type.tickets.all():
            if counter == row_length:
                counter = 0
                ticket_data.append(row)
                row = []
            row.append(ticket)
            counter += 1
        ticket_data.append(row)
        ticket_types_data.append({'type': ticket_type.type, 'price': ticket_type.price, 'tickets': ticket_data})
    form = ReservationForm(free_tickets=list(free_tickets))
    return render(request, 'reservation/buy_tickets.html', {'event': event, 'free_tickets': free_tickets,
                                                            'form': form, 'tickets': ticket_types_data})
