from django.db import models


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
