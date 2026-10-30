
from django.urls import path

from .views import (
    EventListCreateView,
    EventDetailView,
    RegistrationListCreateView,
    RegistrationCancelView,
)

urlpatterns = [
    path("events/", EventListCreateView.as_view(), name="event-list-create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path(
        "registrations/",
        RegistrationListCreateView.as_view(),
        name="registration-list-create",
    ),
    path(
        "registrations/<int:pk>/",
        RegistrationCancelView.as_view(),
        name="registration-cancel",
    ),
]
