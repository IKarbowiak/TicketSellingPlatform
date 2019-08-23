from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Reservation
from ticket.models import Ticket

@receiver(pre_delete, sender=Reservation)
def user_like_changed(sender, instance, **kwargs):
    instance.tickets.all().update(status=Ticket.FREE)

