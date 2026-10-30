
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def home(request):
    return JsonResponse({
        "message": "Welcome to the Event Registration System API!",
        "endpoints": {
            "events": "/api/events/",
            "registrations": "/api/registrations/",
            "admin": "/admin/"
        }
    })


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("event_api.urls")),
]
