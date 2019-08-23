from decimal import Decimal

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from reservation.models import Reservation


def payment_process(request):
    reservation_id = request.session.get('reservation_id')
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    host = request.get_host()

    paypal_dict = {
        'buisness': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(reservation.get_total_price()).quantize(Decimal('0.01')),
        'item_id': 'Reservation {}'.format(reservation_id),               # Reservation id
        'invoice': str(reservation_id),                                   # Bill identifier
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),  # where to sent IPN request
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'reservation': reservation, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
