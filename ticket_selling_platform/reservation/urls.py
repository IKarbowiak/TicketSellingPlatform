from django.urls import path

from . import views

urlpatterns = [
    path('buy-tickets/<int:event_pk>', views.choose_tickets_panel, name='buy_tickets'),
    path('<int:reservation_pk>', views.reservation_confirm, name='reservation'),
    path('reservation-confirmation/<int:reservation_pk>', views.reservation_confirmation,
         name='reservation_confirmation'),
    path('client-reservations/<int:client_id>', views.get_client_reservations, name='client_reservations'),
    path('reservation-canceled/<int:reservation_pk>', views.reservation_canceled, name='reservation_canceled'),
    path('reservation-check', views.reservation_check, name='reservation_check'),
]
