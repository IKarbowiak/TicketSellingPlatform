from django.urls import path

from . import views


urlpatterns = [
    path('<int:reservation_pk>/', views.payment_view, name='payment'),
]