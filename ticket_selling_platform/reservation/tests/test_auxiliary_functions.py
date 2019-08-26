from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..views import remove_expired_reservations, get_reservation_left_time, prepare_seats_rows
from ..models import Reservation
from event.models import Event
from ticket.models import Ticket, TicketType


class RemoveExpireReservationsTest(TestCase):

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


class ReservationLeftTimeTet(TestCase):

    def test_calculate_reservation_left_time_for_active_reservation(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.BOOKED, event=e)

        r.booked_time = timezone.now() - timedelta(minutes=12)
        r.save()

        # WHEN
        left_time = get_reservation_left_time(r)

        # THEN
        self.assertTrue(int(left_time.split(':')[0]) > 0)

    def test_calculate_reservation_left_time_fo_passed_reservation(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.BOOKED, event=e)

        r.booked_time = timezone.now() - timedelta(minutes=20)
        r.save()

        # WHEN
        left_time = get_reservation_left_time(r)

        # THEN
        self.assertFalse(left_time)

class PrepareSeatsRowTest(TestCase):

    def test_prepare_seats_row_for_event(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        vip_type = TicketType.objects.create(type=TicketType.VIP, price=10)
        t1 = Ticket.objects.create(seat_identifier='TestIdentifier1', type=vip_type, event=e)
        t2 = Ticket.objects.create(seat_identifier='TestIdentifier2', type=vip_type, event=e)

        regular_type = TicketType.objects.create(type=TicketType.REGULAR, price=10)
        t3 = Ticket.objects.create(seat_identifier='TestIdentifier3', type=regular_type, event=e)
        t4 = Ticket.objects.create(seat_identifier='TestIdentifier4', type=regular_type, event=e)

        # WHEN
        ticket_types_data = prepare_seats_rows(e)

        # THEN
        self.assertListEqual(ticket_types_data, [{'type': 'VIP', 'price': 10, 'tickets': [[t1, t2]]},
                                                 {'type': 'REGULAR', 'price': 10, 'tickets': [[t3, t4]]}])

    def test_prepare_seats_row_for_event_without_tickets(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))

        # WHEN
        ticket_types_data = prepare_seats_rows(e)

        # THEN
        self.assertFalse(ticket_types_data)
