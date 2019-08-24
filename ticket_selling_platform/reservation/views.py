import re
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q, F, Sum
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from event.models import Event
from .forms import ReservationForm, check_seats_availability, ReservationCheckForm, ClientForm
from .models import Reservation, Client
from ticket.models import Ticket

row_length = 10


# TODO: exclude reservation which have status PAID => remove others
def remove_expired_reservations():
    Reservation.objects.filter(booked_time__lte=timezone.now() - timedelta(minutes=15),
                               status=Reservation.BOOKED).delete()


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
    remove_expired_reservations()
    event = get_object_or_404(Event, pk=event_pk)
    if 'new_reservation' in request.session.keys():
        old_reservation = Reservation.objects.filter(pk=request.session['new_reservation']).first()
        if old_reservation:
            old_reservation.delete()
        del request.session['new_reservation']
        
    if request.method == 'POST':
        form = ReservationForm(request.POST, event=event)
        if form.is_valid():
            cd = form.cleaned_data
            # double check if seats are still free
            taken_seats = check_seats_availability(cd, event)
            if not taken_seats:
                reservation = Reservation.objects.create(event=event)
                seats_identifiers = cd['chosen_seats'].split(', ')
                Ticket.objects.filter(seat_identifier__in=seats_identifiers)\
                    .update(reservation=reservation)
                request.session['new_reservation'] = reservation.pk
                return HttpResponseRedirect('/reservation/{}'.format(reservation.pk))
            # TODO: return some Error ?
    else:
        form = ReservationForm(event=event)
    free_tickets = event.ticket_types.all().values('type', 'price') \
        .annotate(total=Count('tickets', distinct=True, filter=Q(tickets__reservation__isnull=True)))

    ticket_types_data = prepare_seats_rows(event.ticket_types.all())
    print(form)
    return render(request, 'reservation/buy_tickets.html', {'event': event, 'free_tickets': free_tickets,
                                                            'form': form, 'tickets': ticket_types_data})


def reservation_confirm(request, reservation_pk):
    reservation = Reservation.objects.filter(pk=reservation_pk).first()
    if not reservation:
        return HttpResponseRedirect('/')
    if reservation.status == Reservation.PAID:
        return HttpResponseRedirect('/reservation-confirmation/{}'.format(reservation.id))
    if reservation.status == Reservation.UNPAID:
        request.session['reservation_id'] = reservation.pk
        return redirect(reverse('payment:process'))

    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            client, _ = Client.objects.get_or_create(email=cd['email'])
            client.first_name = cd['first_name']
            client.last_name = cd['last_name']
            client.save()

            reservation.client = client
            reservation.status = Reservation.UNPAID
            reservation.save()
            request.session['reservation_id'] = reservation.pk
            del request.session['new_reservation']
            return redirect(reverse('payment:process'))

    reservation_time = timezone.now() - reservation.booked_time
    if reservation_time >= timedelta(minutes=15):
        reservation.delete()
        return HttpResponseRedirect('/reservation-canceled/{}'.format(reservation.pk))

    print(form)
    left_time = re.match(r'\d+:(\d\d:\d\d).\d+', str(timedelta(minutes=15) - reservation_time)).group(1)
    tickets, total_price = reservation.get_reservation_details()

    return render(request, 'reservation/reservation_confirm.html', {'reservation': reservation,
                                                                    'left_time': left_time,
                                                                    'tickets': tickets,
                                                                    'total_price': total_price,
                                                                    'form': form})


def reservation_confirmation(request, reservation_pk):
    reservation = Reservation.objects.filter(pk=reservation_pk).first()
    if not reservation:
        return HttpResponseRedirect('/')
    if reservation.status != Reservation.PAID:
        return HttpResponseRedirect('/reservation/{}'.format(reservation.pk))
    details, total_price = reservation.get_reservation_details()
    event = reservation.event
    return render(request, 'reservation/reservation_confirmation.html', {'details': details,
                                                                         'total_price': total_price,
                                                                         'reservation_number': reservation.pk,
                                                                         'event': event})


def reservation_canceled(request, reservation_pk):
    reservation = Reservation.objects.filter(pk=reservation_pk).first()
    if not reservation:
        return HttpResponseRedirect('/')
    if reservation.status == Reservation.PAID:
        return HttpResponseRedirect('/reservation-confirmation/{}'.format(reservation_pk))
    reservation_pk = reservation.pk
    reservation.delete()
    reservation.save()
    return render(request, 'reservation/reservation_canceled.html', {'reservation_pk': reservation_pk})


def reservation_check(request):
    form = ReservationCheckForm()
    if request.method == 'POST':
        form = ReservationCheckForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            reservation_pk = cd['reservation_id']
            email = cd['email']
            if not reservation_pk:
                client = Client.objects.get(email=email)
                return HttpResponseRedirect('/client-reservations/{}'.format(client.pk))
            return HttpResponseRedirect('/reservation-confirmation/{}'.format(reservation_pk))
    return render(request, 'reservation/reservation_check.html', {'form': form})


def get_client_reservations(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    reservations = client.reservations.all().order_by('-event__datetime', 'pk')
    return render(request, 'reservation/client_reservations.html', {'reservations': reservations})

