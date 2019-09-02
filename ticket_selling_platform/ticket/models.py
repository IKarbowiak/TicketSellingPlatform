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

    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    price = models.PositiveIntegerField()

    def create_tickets(self, event, ticket_amount):
        for seat in range(1, ticket_amount + 1):
            Ticket.objects.create(seat_identifier='{}{}'.format(self.type[0], seat), type=self, event=event)

    def __str__(self):
        return '{}, {} price'.format(self.type, self.price)


class Ticket(models.Model):
    seat_identifier = models.CharField(max_length=10)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True,
                                    related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return 'SEAT: {}'.format(self.seat_identifier)
