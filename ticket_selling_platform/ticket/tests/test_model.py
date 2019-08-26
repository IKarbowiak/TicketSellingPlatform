from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..models import TicketType
from event.models import Event


class TicketTypeModelTest(TestCase):

    def test_create_tickets(self):
        # GIVEN
        ticket_type = TicketType.objects.create(price=10, type=TicketType.REGULAR)
        event = Event.objects.create(name='TestEvent', description='TestDescription',
                                     datetime=timezone.now() + timedelta(days=2))

        # WHEN
        ticket_type.create_tickets(event, 10)

        # THEN
        self.assertEqual(event.tickets.all().count(), 10)
