from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from django.views.generic import ListView

from .models import Event


class EventListView(ListView):
    queryset = Event.objects.filter(datetime__gte=timezone.now() - timedelta(days=5)) \
        .annotate(available_tickets=Count('ticket_types__tickets', distinct=True,
                                          filter=Q(ticket_types__tickets__reservation__isnull=True)))
    context_object_name = 'events'
    paginate_by = 4
    template_name = 'event/events_list.html'


