from django.db import models

from reservation.models import Reservation
from event.models import Event


class Ticket(models.Model):
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
    ticket_identifier = models.CharField(max_length=10)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return '{} ticket {}'.format(self.type, self.ticket_identifier)
