from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    description = models.TextField()

    def get_all_tickets(self):
        types = self.ticket_types.all()
        tickets = types[0].tickets.all()
        for ticket_type in types:
            tickets = tickets | ticket_type.tickets.all()
        return tickets.distinct()
