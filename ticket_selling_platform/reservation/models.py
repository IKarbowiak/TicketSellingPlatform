from django.db import models
from django.db.models import Count, Q, F, Sum
from functools import reduce


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)


class Reservation(models.Model):
    PAID = 'PAID'
    UNPAID = 'UNPAID'
    BOOKED = 'BOOKED'
    RESERVATION_STATUS_CHOICES = [
        (PAID, 'paid'),
        (UNPAID, 'unpaid'),
        (BOOKED, 'ongoing'),
    ]

    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default=BOOKED)
    booked_time = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE, related_name='reservation')

    def get_reservation_details(self):
        reservation_details = self.tickets.all() \
                .values(ticket_type=F('type__type'), price=F('type__price')) \
                .annotate(amount=Count('ticket_type'), total_price=Sum('price'))
        total_price = reduce(lambda x, y: x + y, [element['total_price'] for element in reservation_details])
        return reservation_details, total_price
