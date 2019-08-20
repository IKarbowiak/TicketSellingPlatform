from django.urls import path

from . import views

urlpatterns = [
    path('buy-tickets/<int:event_pk>', views.choose_tickets_panel, name='buy_tickets')
]