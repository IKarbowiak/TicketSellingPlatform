from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Event


class EventListViewTest(TestCase):

    def test_response_status_code(self):
        # GIVEN
        Event.objects.create(name='TestEvent', description='TestDescription',
                                 datetime=timezone.now() + timedelta(days=2))

        # WHEN
        response = self.client.get(reverse('event:events'))

        # THEN
        self.assertEqual(response.status_code, 200)

    def test_response_content(self):
        # GIVEN
        Event.objects.bulk_create([
            Event(name='TestEvent1', description='TestDescription',datetime=timezone.now() + timedelta(days=2)),
            Event(name='TestEvent2', description='TestDescription',datetime=timezone.now() + timedelta(days=3)),
            Event(name='TestEvent3', description='TestDescription', datetime=timezone.now() - timedelta(days=3))
        ])

        # WHEN
        response = self.client.get(reverse('event:events'))

        # THEN
        events = response.context['events']
        self.assertEqual(len(events), 2)
        self.assertSetEqual({event.name for event in events}, {'TestEvent1', 'TestEvent2'})


