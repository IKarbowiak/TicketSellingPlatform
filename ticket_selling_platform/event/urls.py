from django.urls import path

from . import views

urlpatterns = [
    # path('', views.get_events, name='events'),
    path('', views.EventListView.as_view(), name='events')
]