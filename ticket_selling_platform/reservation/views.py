import re
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.utils import timezone

from event.models import Event
from .forms import ReservationForm
from reservation.models import Reservation

row_length = 10


def prepare_seats_rows(ticket_types):
    ticket_types_data = []
    for ticket_type in ticket_types.order_by('-price'):
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
    return ticket_types_data


def choose_tickets_panel(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, event=event)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            booked_tickets = cd['chosen_seats'].split(', ')
            available_tickets = event.get_all_tickets().filter(reservation__isnull=True)
            r = Reservation.objects.create()
            # TODO: Handle ticket Reservation
            return HttpResponseRedirect('/reservation/{}'.format(r.pk))
    else:
        form = ReservationForm(event=event)
    free_tickets = event.ticket_types.all().values('type', 'price') \
        .annotate(total=Count('tickets', distinct=True, filter=Q(tickets__reservation__isnull=True)))

    ticket_types_data = prepare_seats_rows(event.ticket_types.all())

    return render(request, 'reservation/buy_tickets.html', {'event': event, 'free_tickets': free_tickets,
                                                            'form': form, 'tickets': ticket_types_data})


def reservation_payment(request, reservation_pk):
    reservation = get_object_or_404(Reservation, pk=reservation_pk)
    if reservation.status == Reservation.PAID:
        return HttpResponseRedirect('/reservation-confirm/')
    reservation_time = timezone.now() - reservation.booked_time
    if reservation_time >= timedelta(minutes=15):
        reservation.delete()
        return HttpResponseRedirect('/reservation-canceled/')
    left_time = re.match(r'\d+:(\d\d:\d\d).\d+', str(timedelta(minutes=15) - reservation_time)).group(1)
    return render(request, 'reservation/payment.html', {'reservation': reservation,
                                                        'left_time': left_time})




