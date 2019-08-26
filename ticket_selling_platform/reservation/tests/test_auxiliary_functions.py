from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..views import remove_expired_reservations
from ..models import Reservation
from event.models import Event


class AdditionalFunctionTest(TestCase):

    def test_remove_expire_reservation(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))

        r1 = Reservation.objects.create(status=Reservation.BOOKED, event=e)
        r1.booked_time = timezone.now() - timedelta(minutes=5)
        r1.save()

        r2 = Reservation.objects.create(status=Reservation.UNPAID, event=e)
        r2.booked_time = timezone.now() - timedelta(minutes=10)
        r2.save()

        r3 = Reservation.objects.create(status=Reservation.PAID, event=e)
        r3.booked_time = timezone.now() - timedelta(days=1)
        r3.save()

        r4 = Reservation.objects.create(status=Reservation.BOOKED, event=e)
        r4.booked_time = timezone.now() - timedelta(minutes=16)
        r4.save()

        r5 = Reservation.objects.create(status=Reservation.UNPAID, event=e)
        r5.booked_time = timezone.now() - timedelta(minutes=20)
        r5.save()


        # WHEN
        remove_expired_reservations()

        # THEN
        self.assertEqual(Reservation.objects.all().count(), 3)
        self.assertSetEqual(set(Reservation.objects.all().values_list('pk', flat=True).distinct()),
                            {r1.pk, r2.pk, r3.pk})