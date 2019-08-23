from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation, Client


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
                                   widget=forms.Textarea(attrs={'rows': 2, 'readonly': True,
                                                                'style': 'width:100%'}))

    def clean_chosen_seats(self):
        chosen_seats = self.cleaned_data['chosen_seats']
        booked_tickets = check_seats_availability(self.cleaned_data, self.event)
        if booked_tickets:
            raise ValidationError('Some seats are already booked: {}'.format(', '.join(booked_tickets)))
        return chosen_seats


class ReservationCheckForm(forms.Form):
    reservation_id = forms.IntegerField(min_value=0, error_messages={'empty': 'Fill this field'}, required=False)
    email = forms.EmailField(required=False)

    @staticmethod
    def check_reservation_id(reservation_id):
        if not Reservation.objects.filter(pk=reservation_id).exists():
            raise ValidationError('Reservation with number {} does not exist'.format(reservation_id))

    @staticmethod
    def check_email(email):
        if not Client.objects.filter(email=email, reservation__isnull=False).exists():
            raise ValidationError('Reservation for {} email address does not exist'.format(email))

    @staticmethod
    def check_both(reservation_id, email):
        if not Client.objects.filter(reservation__pk=reservation_id, email=email).exists():
            raise ValidationError('Reservation for {} address with {} number does not exist'
                                  .format(reservation_id, email))

    def clean(self):
        cleaned_data = super().clean()
        res_id = cleaned_data['reservation_id']
        email = cleaned_data['email']

        if not res_id and not email:
            raise ValidationError("Fill at least one field")
        elif res_id and not email:
            self.check_reservation_id(res_id)
        elif email and not res_id:
            self.check_email(email)
        else:
            self.check_both(res_id, email)

        return cleaned_data


class ClientForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
