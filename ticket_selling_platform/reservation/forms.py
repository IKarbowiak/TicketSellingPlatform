from django import forms

from .models import Reservation
from ticket.models import Ticket


class ReservationForm(forms.Form):
    def __init__(self,*args,**kwargs):
        print(args)
        print(kwargs)
        self.tickets = {ticket['type']: ticket['total'] for ticket in kwargs.pop('free_tickets')}
        print(self.tickets)
        super(ReservationForm, self).__init__(*args,**kwargs)
        self.fields['regular_tickets'] = forms.IntegerField(min_value=0, max_value=self.tickets.get('REGULAR', 0),
                                                                   initial=0)
        self.fields['premium_tickets'] = forms.IntegerField(min_value=0, max_value=self.tickets.get('PREMIUM', 0),
                                                            initial=0)
        self.fields['vip_tickets'] = forms.IntegerField(min_value=0, max_value=self.tickets.get('VIP', 0),
                                                            initial=0)

    regular_tickets = forms.IntegerField(min_value=0, initial=0)
    vip_tickets = forms.IntegerField(min_value=0, initial=0)
    premium_tickets = forms.IntegerField(min_value=0, initial=0)

