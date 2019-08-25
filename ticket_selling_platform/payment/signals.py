from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from reservation.models import Reservation


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    print(ipn_obj.payment_status)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # payment finished with success
        reservation = get_object_or_404(Reservation, id=ipn_obj.invoice)
        reservation.status = Reservation.PAID
        reservation.save()

valid_ipn_received.connect(payment_notification)