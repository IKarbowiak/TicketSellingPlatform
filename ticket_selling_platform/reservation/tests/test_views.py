from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..models import Client, Reservation
from event.models import Event
from ticket.models import Ticket, TicketType


class ReservationConfirmationTest(TestCase):

    def test_reservation_confirmation_correct_template(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)
        vip_type = TicketType.objects.create(type=TicketType.VIP, price=10)
        t1 = Ticket.objects.create(seat_identifier='TestIdentifier1', type=vip_type, event=e, reservation=r)
        t2 = Ticket.objects.create(seat_identifier='TestIdentifier2', type=vip_type, event=e, reservation=r)
        t3 = Ticket.objects.create(seat_identifier='TestIdentifier3', type=vip_type, event=e)

        # WHEN
        response = self.client.get('/reservation/reservation-confirmation/{}'.format(r.pk))

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation/reservation_confirmation.html')
        self.assertEqual(len(response.context['tickets']), 1)
        self.assertDictEqual(response.context['tickets'][0],
                             {'ticket_type': 'VIP', 'price': 10, 'amount': 2, 'total_price': 20})
        self.assertEqual(response.context['total_price'], 20)
        self.assertEqual(response.context['reservation_number'], r.pk)
        self.assertEqual(response.context['seats'], '{}, {}'.format(t1.seat_identifier, t2.seat_identifier))
        self.assertEqual(response.context['event'], e)

    def test_reservation_confirmation_for_unpaid_reservation(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.UNPAID, client=c, event=e)
        res_pk = r.pk

        # WHEN
        response = self.client.get('/reservation/reservation-confirmation/{}'.format(r.pk))

        # THEN
        self.assertTrue(response.status_code, 302)
        self.assertEqual(response.url, '/reservation/{}'.format(res_pk))

    def test_reservation_confirmation_for_not_existing_reservation(self):
        # WHEN
        response = self.client.get('/reservation/reservation-confirmation/{}'.format(0xDEAD))

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('event:events'))


class ReservationCanceledViewTest(TestCase):

    def test_reservation_canceled_correct_template(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.UNPAID, client=c, event=e)
        res_pk = r.pk

        # WHEN
        response = self.client.get('/reservation/reservation-canceled/{}'.format(r.pk))

        # THEN
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation/reservation_canceled.html')
        self.assertFalse(Reservation.objects.filter(pk=res_pk))
        self.assertEqual(response.context['reservation_pk'], r.pk)

    def test_reservation_canceled_for_paid_reservation(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)
        res_pk = r.pk

        # WHEN
        response = self.client.get('/reservation/reservation-canceled/{}'.format(r.pk))

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reservation/reservation-confirmation/{}'.format(res_pk))
        self.assertTrue(Reservation.objects.filter(pk=res_pk))

    def test_reservation_canceled_for_not_existing_reservation(self):
        # WHEN
        response = self.client.get('/reservation/reservation-canceled/{}'.format(1))

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('event:events'))


class ReservationCheckViewTest(TestCase):

    def test_response_code_for_get_method(self):
        # WHEN
        response = self.client.get(reverse('reservation:reservation_check'))

        # THEM
        self.assertEqual(response.status_code, 200)

    def test_response_for_post_method_with_reservation_id(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)

        # WHEN
        response = self.client.post(reverse('reservation:reservation_check'), {'reservation_id': r.pk, 'email': ''})

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reservation/reservation-confirmation/{}'.format(r.pk))

    def test_response_for_post_method_without(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)

        # WHEN
        response = self.client.post(reverse('reservation:reservation_check'), {'reservation_id': '',
                                                                               'email': 'test@email.com'})

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reservation/client-reservations/{}'.format(c.pk))

    def test_response_for_post_method_without_valid_form(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)

        # WHEN
        response = self.client.post(reverse('reservation:reservation_check'), {'reservation_id': '',
                                                                               'email': 'test@test.com'})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('reservation/reservation_check.html')

    def test_response_for_post_method_with_email_and_res_pk(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)

        # WHEN
        response = self.client.post(reverse('reservation:reservation_check'), {'reservation_id': r.pk,
                                                                               'email': 'test@email.com'})

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reservation/reservation-confirmation/{}'.format(r.pk))


class ClientReservationsTest(TestCase):

    def test_status_code(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        Reservation.objects.bulk_create([
            Reservation(status=Reservation.UNPAID, client=c, event=e),
            Reservation(status=Reservation.PAID, client=c, event=e),
            Reservation(status=Reservation.UNPAID, event=e),
        ])

        # WHEN
        response = self.client.get('/reservation/client-reservations/{}'.format(c.pk))

        # THEN
        self.assertEqual(response.status_code, 200)

    def test_response_content(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        Reservation.objects.bulk_create([
            Reservation(status=Reservation.UNPAID, client=c, event=e),
            Reservation(status=Reservation.PAID, client=c, event=e),
            Reservation(status=Reservation.UNPAID, event=e),
        ])

        # WHEN
        response = self.client.get('/reservation/client-reservations/{}'.format(c.pk))

        # THEN
        reservations = response.context['reservations']
        self.assertEqual(len(reservations), 2)
        self.assertSetEqual({res.pk for res in reservations}, {res.pk for res in c.reservations.all()})

    def test_response_code_no_client(self):
        # WHEN
        response = self.client.get('/reservation/client-reservations/{}'.format(2))

        # THEN
        self.assertEqual(response.status_code, 404)


class ReservationConfirmViewTest(TestCase):

    def test_reservation_confirm_with_no_reservation(self):
        # GIVEN
        reservation_pk = 1

        # WHEN
        response = self.client.get('/reservation/{}'.format(reservation_pk))

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('event:events'))

    def test_reservation_confirm_for_paid_reservation(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.PAID, client=c, event=e)

        # WHEN
        response = self.client.get('/reservation/{}'.format(r.pk))

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reservation/reservation-confirmation/{}'.format(r.pk))

    def test_reservation_confirm_for_unpaid_reservation(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.UNPAID, client=c, event=e)

        # WHEN
        response = self.client.get('/reservation/{}'.format(r.pk))

        # THEN
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payment:process'))

    def test_get_method_reservation_confirm_with_booked_reservation(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.BOOKED, event=e)
        ticket_type = TicketType.objects.create(type=TicketType.VIP, price=10)
        t1 = Ticket.objects.create(seat_identifier='TestIdentifier1', reservation=r, type=ticket_type, event=e)
        t2 = Ticket.objects.create(seat_identifier='TestIdentifier2', reservation=r, type=ticket_type, event=e)


        session = self.client.session
        session['new_reservation'] = r.pk
        session.save()

        # WHEN
        response = self.client.get('/reservation/{}'.format(r.pk))

        # THEN
        reservation = Reservation.objects.get(pk=r.pk)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session.get('reservation_id'))
        self.assertTrue(self.client.session.get('new_reservation'))
        self.assertEqual(reservation.status, Reservation.BOOKED)
        self.assertFalse(reservation.client)
        self.assertListEqual(list(response.context['tickets']),
                             [{'ticket_type': 'VIP', 'price': 10, 'amount': 2, 'total_price': 20}])
        self.assertEqual(response.context['total_price'], 20)
        self.assertEqual(response.context['reservation'].pk, r.pk)


    def test_post_method_reservation_confirm_with_booked_reservation_valid_form(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.BOOKED, event=e)

        session = self.client.session
        session['new_reservation'] = r.pk
        session.save()

        # WHEN
        response = self.client.post('/reservation/{}'.format(r.pk), {'email': 'test@email.com',
                                                                     'first_name': 'TestName',
                                                                     'last_name': 'TestLastName'})

        # THEN
        reservation = Reservation.objects.get(pk=r.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['reservation_id'], r.pk)
        self.assertFalse(self.client.session.get('new_reservation'))
        self.assertEqual(reservation.status, Reservation.UNPAID)
        self.assertTrue(reservation.client)

    def test_post_method_reservation_confirm_with_booked_reservation_valid_form_existing_client(self):
        # GIVEN
        c = Client.objects.create(first_name='TestClientName', last_name='TestClientLastName', email='test@email.com')
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.BOOKED, client=c, event=e)

        session = self.client.session
        session['new_reservation'] = r.pk
        session.save()

        post_data = {'email': 'test@email.com',
                     'first_name': 'TestName',
                     'last_name': 'TestLastName'}

        # WHEN
        response = self.client.post('/reservation/{}'.format(r.pk), post_data)

        # THEN
        reservation = Reservation.objects.get(pk=r.pk)
        client = reservation.client
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['reservation_id'], r.pk)
        self.assertFalse(self.client.session.get('new_reservation'))
        self.assertEqual(reservation.status, Reservation.UNPAID)
        self.assertTrue(client)
        self.assertEqual(client.first_name, post_data['first_name'])
        self.assertEqual(client.last_name, post_data['last_name'])
        self.assertEqual(client.email, post_data['email'])


    def test_post_method_reservation_confirm_with_booked_reservation_not_valid_form(self):
        # GIVEN
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))
        r = Reservation.objects.create(status=Reservation.BOOKED, event=e)
        ticket_type = TicketType.objects.create(type=TicketType.VIP, price=10)
        t1 = Ticket.objects.create(seat_identifier='TestIdentifier1', reservation=r, type=ticket_type, event=e)
        t2 = Ticket.objects.create(seat_identifier='TestIdentifier2', reservation=r, type=ticket_type, event=e)


        session = self.client.session
        session['new_reservation'] = r.pk
        session.save()

        # WHEN
        response = self.client.post('/reservation/{}'.format(r.pk), {'email': 'test',
                                                                     'first_name': 'TestName',
                                                                     'last_name': 'TestLastName'})

        # THEN
        reservation = Reservation.objects.get(pk=r.pk)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session.get('reservation_id'))
        self.assertTrue(self.client.session.get('new_reservation'))
        self.assertEqual(reservation.status, Reservation.BOOKED)
        self.assertFalse(reservation.client)
        self.assertListEqual(list(response.context['tickets']),
                             [{'ticket_type': 'VIP', 'price': 10, 'amount': 2, 'total_price': 20}])
        self.assertEqual(response.context['total_price'], 20)
        self.assertEqual(response.context['reservation'].pk, r.pk)
        self.assertTrue(int(response.context['left_time'].split(':')[0]) > 0)


class ChooseTicketPanelViewTest(TestCase):

    def test_get_method_for_choose_ticket_panel(self):
        # GIVEN
        seats_number = 10
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))

        r1 = Reservation.objects.create(status=Reservation.PAID, event=e)
        r2 = Reservation.objects.create(status=Reservation.BOOKED, event=e)
        regular = TicketType.objects.create(price=10, type=TicketType.REGULAR)
        premium = TicketType.objects.create(price=20, type=TicketType.PREMIUM)
        vip = TicketType.objects.create(price=30, type=TicketType.VIP)

        for ticket_type in [regular, premium, vip]:
            ticket_type.create_tickets(e, seats_number)

        regular_ticket = regular.tickets.first()
        regular_ticket.reservation = r1
        regular_ticket.save()

        vip_ticket = vip.tickets.first()
        vip_ticket.reservation = r1
        vip_ticket.save()


        session = self.client.session
        session['new_reservation'] = r2.pk
        session.save()

        # WHEN
        response = self.client.get('/reservation/buy-tickets/{}'.format(e.pk))

        # THEN
        self.assertFalse(self.client.session.get('new_reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], e)

        free_tickets = {data['type__type']: {'price': data['type__price'], 'total': data['total']}
                        for data in response.context['free_tickets']}
        self.assertEqual(free_tickets, {'PREMIUM': {'price': 20, 'total': 10},
                                        'REGULAR': {'price': 10, 'total': 9},
                                        'VIP': {'price': 30, 'total': 9}})

    def test_get_post_for_choose_ticket_panel(self):
        # GIVEN
        seats_number = 10
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))

        regular = TicketType.objects.create(price=10, type=TicketType.REGULAR)
        premium = TicketType.objects.create(price=20, type=TicketType.PREMIUM)
        vip = TicketType.objects.create(price=30, type=TicketType.VIP)

        for ticket_type in [regular, premium, vip]:
            ticket_type.create_tickets(e, seats_number)


        # WHEN
        response = self.client.post('/reservation/buy-tickets/{}'.format(e.pk),
                                    {'chosen_seats': ', '.join([regular.tickets.first().seat_identifier,
                                                                premium.tickets.first().seat_identifier,
                                                                vip.tickets.first().seat_identifier,])})

        # THEN
        reservation = Reservation.objects.all().first()
        self.assertTrue(reservation)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reservation/{}'.format(reservation.pk))

    def test_get_post_for_already_taken_seat(self):
        seats_number = 10
        e = Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))

        r1 = Reservation.objects.create(status=Reservation.PAID, event=e)
        r2 = Reservation.objects.create(status=Reservation.BOOKED, event=e)
        regular = TicketType.objects.create(price=10, type=TicketType.REGULAR)
        premium = TicketType.objects.create(price=20, type=TicketType.PREMIUM)
        vip = TicketType.objects.create(price=30, type=TicketType.VIP)

        for ticket_type in [regular, premium, vip]:
            ticket_type.create_tickets(e,  seats_number)

        regular_ticket = regular.tickets.first()
        regular_ticket.reservation = r1
        regular_ticket.save()

        vip_ticket = vip.tickets.first()
        vip_ticket.reservation = r1
        vip_ticket.save()

        # WHEN
        response = self.client.post('/reservation/buy-tickets/{}'.format(e.pk),
                                    {'chosen_seats': ', '.join([regular_ticket.seat_identifier,
                                                                premium.tickets.first().seat_identifier,
                                                                vip.tickets.last().seat_identifier,])})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation/buy_tickets.html')

    def test_404_response(self):
        # WHEN
        response = self.client.get('/reservation/buy-tickets/1')

        # THEN
        self.assertEqual(response.status_code, 404)
