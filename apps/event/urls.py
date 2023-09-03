from . import views

from django.urls import path

urlpatterns = [
    # Create operation
    path("event/add/", views.AddEvent.as_view(), name="add_event"),
    # Read operations for all events
    path("event/", views.EventList.as_view(), name="event_list"),
    # Read, Delete, Update operations for a specific event
    path("event/<int:eventId>/", views.EventDetail.as_view(), name="event_detail"),
]
