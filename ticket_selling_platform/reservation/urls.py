from django.urls import path

from . import views

urlpatterns = [
    path('buy-tickets/<int:event_pk>', views.choose_tickets_panel, name='buy_tickets'),
    path('reservation/<int:reservation_pk>', views.reservation_payment, name='payment'),
    path('reservation-confirmation/<int:reservation_pk>', views.reservation_confirm, name='reservation_confirmation'),
    path('reservation-canceled/<int:reservation_pk>', views.reservation_canceled, name='reservation_canceled'),
    path('reservation-check', views.reservation_check, name='reservation_check')
]