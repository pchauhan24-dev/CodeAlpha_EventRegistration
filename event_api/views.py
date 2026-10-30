
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


# ------------------------------------------
# EVENT LIST AND CREATE
# ------------------------------------------

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("date")
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Reset the event form after successful browser submission.
        if request.accepted_renderer.format == "api":
            return redirect("/api/events/")

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


# ------------------------------------------
# EVENT DETAILS, UPDATE AND DELETE
# ------------------------------------------

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# ------------------------------------------
# REGISTRATION LIST AND CREATE
# ------------------------------------------

class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Registration.objects.select_related("event").all()
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        queryset = Registration.objects.select_related("event").all()

        event_id = self.request.query_params.get("event")

        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset.order_by("-registered_at")

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        # Keep the previously selected event in the fresh form.
        if self.request.method == "GET":
            event_id = self.request.query_params.get("event")

            if event_id:
                serializer.fields["event"].initial = event_id

        return serializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event")

        if not event_id:
            return Response(
                {"error": "An event ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event = get_object_or_404(
            Event.objects.select_for_update(),
            pk=event_id,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check event capacity.
        if event.registrations.count() >= event.capacity:
            return Response(
                {
                    "error": (
                        "This event has reached its maximum capacity."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["attendee_email"]

        # Prevent duplicate registrations for the same event.
        if event.registrations.filter(
            attendee_email__iexact=email
        ).exists():
            return Response(
                {
                    "error": (
                        "This email is already registered for this event."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)

        # Return to the same event's registration form.
        # Attendee name and email will be cleared.
        if request.accepted_renderer.format == "api":
            return redirect(
                f"/api/registrations/?event={event.pk}"
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# ------------------------------------------
# REGISTRATION DETAILS AND CANCELLATION
# ------------------------------------------

class RegistrationCancelView(generics.RetrieveDestroyAPIView):
    queryset = Registration.objects.select_related("event").all()
    serializer_class = RegistrationSerializer
