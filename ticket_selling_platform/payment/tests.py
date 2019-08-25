from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from reservation.models import Reservation, Client
from event.models import Event


class PaymentProcessTest(TestCase):

    def test_payment_process_response(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)

        session = self.client.session
        session['reservation_id'] = r.pk
        session.save()

        # WHEN
        response = self.client.get(reverse('payment:process'))

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['reservation'], r)
        self.assertTemplateUsed('payment/canceled.htmll')

    def test_payment_process_404_response(self):
        # GIVEN
        session = self.client.session
        session['reservation_id'] = 1
        session.save()

        # WHEN
        response = self.client.get(reverse('payment:process'))

        # THEN
        self.assertEqual(response.status_code, 404)


class PaymentDoneViewTest(TestCase):

    def test_status_status_code(self):
        # WHEN
        response = self.client.get(reverse('payment:done'))

        # THEN
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        # WHEN
        response = self.client.get(reverse('payment:done'))

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('payment/done.html')


class PaymentCanceledViewTest(TestCase):

    def test_payment_canceled(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)

        session = self.client.session
        session['reservation_id'] = r.pk
        session.save()

        # WHEN
        response = self.client.get(reverse('payment:canceled'))

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('payment/canceled.html')
        self.assertEqual(response.context['reservation_id'], r.pk)
