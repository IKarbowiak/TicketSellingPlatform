from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from reservation.models import Reservation


def payment_view(request, reservation_pk):
    reservation_obj = Reservation.objects.filter(pk=reservation_pk).first()
    if not reservation_obj:
        return HttpResponseRedirect('/')
    return render(request, 'payment/payment.html', {'reservation_obj': reservation_obj})
