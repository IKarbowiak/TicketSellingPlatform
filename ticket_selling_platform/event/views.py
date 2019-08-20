from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from django.views.generic import ListView

from .models import Event


class EventListView(ListView):
    queryset = Event.objects.filter(datetime__gte=timezone.now() - timedelta(days=1)) \
        .annotate(available_tickets=Count('tickets', distinct=True, filter=Q(tickets__reservation__isnull=True)))
    context_object_name = 'events'
    paginate_by = 4
    template_name = 'event/events_list.html'

