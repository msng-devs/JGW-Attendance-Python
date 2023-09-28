from . import views

from django.urls import path

urlpatterns = [
    # Create, Read operations for all events
    path("", views.EventList.as_view(), name="event_list"),
    # Read, Delete, Update operations for a specific event
    path("<int:eventId>/", views.EventDetail.as_view(), name="event_detail"),
]
