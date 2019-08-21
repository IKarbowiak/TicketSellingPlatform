from django import forms
from django.core.exceptions import ValidationError


class ReservationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(ReservationForm, self).__init__(*args, **kwargs)

    chosen_seats = forms.CharField(label='Chosen seats', max_length=100)

    def clean_chosen_seats(self):
        chosen_seats = self.cleaned_data['chosen_seats']
        chosen_seats_set = set(chosen_seats.split(', '))
        available_tickets = set(self.event.get_all_tickets().filter(reservation__isnull=True)\
            .values_list('seat_identifier', flat=True).distinct())

        booked_tickets = chosen_seats_set.difference(available_tickets)
        if booked_tickets:
            return ValidationError('Some seats are already booked: {}'.format(', '.join(booked_tickets)))
        return chosen_seats
