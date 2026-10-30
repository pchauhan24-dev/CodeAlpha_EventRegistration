
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Event, Registration


class EventRegistrationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.event = Event.objects.create(
            name="Test Event",
            description="An event for automated testing",
            date=timezone.now() + timedelta(days=30),
            location="Raipur",
            capacity=2,
        )

        self.registration_data = {
            "event": self.event.pk,
            "attendee_name": "Test User",
            "attendee_email": "testuser@example.com",
        }

    def test_event_list_returns_200(self):
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_can_be_created(self):
        data = {
            "name": "New Test Event",
            "description": "Testing event creation",
            "date": (
                timezone.now() + timedelta(days=45)
            ).isoformat(),
            "location": "Raipur",
            "capacity": 10,
        }

        response = self.client.post(
            "/api/events/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Event.objects.filter(name="New Test Event").exists()
        )

    def test_registration_can_be_created(self):
        response = self.client.post(
            "/api/registrations/",
            self.registration_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Registration.objects.count(), 1)

    def test_duplicate_registration_is_rejected(self):
        Registration.objects.create(
            event=self.event,
            attendee_name="Test User",
            attendee_email="testuser@example.com",
        )

        response = self.client.post(
            "/api/registrations/",
            self.registration_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_email_is_rejected(self):
        data = {
            **self.registration_data,
            "attendee_email": "not-an-email",
        }

        response = self.client.post(
            "/api/registrations/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn(b"attendee_email", response.content)

    def test_full_event_rejects_registration(self):
        self.event.capacity = 1
        self.event.save()

        Registration.objects.create(
            event=self.event,
            attendee_name="First Attendee",
            attendee_email="first@example.com",
        )

        data = {
            **self.registration_data,
            "attendee_email": "second@example.com",
        }

        response = self.client.post(
            "/api/registrations/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
