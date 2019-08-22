from string import ascii_uppercase

from django.db import models

from reservation.models import Reservation
from event.models import Event


class TicketType(models.Model):
    REGULAR = 'REGULAR'
    PREMIUM = 'PREMIUM'
    VIP = 'VIP'
    TICKET_TYPES = [
        (REGULAR, 'regular'),
        (PREMIUM, 'premium'),
        (VIP, 'VIP'),
    ]

    type = models.CharField(max_length=20, choices=TICKET_TYPES)
    price = models.PositiveIntegerField()
    seats_number = models.PositiveIntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')

    def create_tickets(self):
        for seat in range(1, self.seats_number + 1):
            Ticket.objects.create(seat_identifier='{}{}'.format(self.type[0], seat), type=self)

    def __str__(self):
        return '{}, {} seats'.format(self.type, self.seats_number)


class Ticket(models.Model):
    seat_identifier = models.CharField(max_length=10)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, related_name='tickets')
    type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return 'SEAT: {}'.format(self.seat_identifier)
