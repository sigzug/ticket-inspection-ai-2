from django.urls import path

from .views import ComputeView, health

urlpatterns = [
    path("health/", health, name="health"),
    path("compute/", ComputeView.as_view(), name="compute"),
]
