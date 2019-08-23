from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation


def check_seats_availability(cleaned_data, event):
    chosen_seats = cleaned_data['chosen_seats']
    chosen_seats_set = set(chosen_seats.split(', '))
    available_tickets = set(event.get_all_tickets().filter(reservation__isnull=True) \
                            .values_list('seat_identifier', flat=True).distinct())

    already_taken_tickets = chosen_seats_set.difference(available_tickets)
    return already_taken_tickets


class ReservationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(ReservationForm, self).__init__(*args, **kwargs)

    chosen_seats = forms.CharField(label='Chosen seats', max_length=100,
                                   widget=forms.Textarea(attrs={'rows': 2, 'readonly': True}))
    email = forms.EmailField()

    def clean_chosen_seats(self):
        chosen_seats = self.cleaned_data['chosen_seats']
        booked_tickets = check_seats_availability(self.cleaned_data, self.event)
        if booked_tickets:
            raise ValidationError('Some seats are already booked: {}'.format(', '.join(booked_tickets)))
        return chosen_seats


class ReservationCheckForm(forms.Form):
    reservation_id = forms.IntegerField(min_value=0, error_messages={'empty': 'Fill this field'})

    def clean_reservation_id(self):
        reservation_id = self.cleaned_data['reservation_id']
        print(reservation_id)
        if not Reservation.objects.filter(pk=reservation_id).exists():
            raise ValidationError('Reservation does not exist')
        return reservation_id

