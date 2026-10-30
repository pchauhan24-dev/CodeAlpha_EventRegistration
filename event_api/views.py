
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("date")
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Registration.objects.select_related("event").all()
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        queryset = Registration.objects.select_related("event").all()
        event_id = self.request.GET.get("event")

        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset.order_by("-registered_at")

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

        if event.registrations.count() >= event.capacity:
            return Response(
                {"error": "This event has reached its maximum capacity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["attendee_email"]

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

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RegistrationCancelView(APIView):
    def delete(self, request, pk):
        registration = get_object_or_404(Registration, pk=pk)
        registration.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
