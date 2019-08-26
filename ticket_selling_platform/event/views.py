from django.utils import timezone
from django.db.models import Count, Q
from django.views.generic import ListView

from .models import Event
from reservation.views import remove_expired_reservations


class EventListView(ListView):
    context_object_name = 'events'
    paginate_by = 4
    template_name = 'event/events_list.html'

    def get_queryset(self):
        remove_expired_reservations()
        queryset = Event.objects.filter(datetime__gte=timezone.now()) \
            .annotate(available_tickets=Count('tickets', distinct=True,
                                              filter=Q(tickets__reservation__isnull=True)))\
            .order_by('datetime')
        return queryset
