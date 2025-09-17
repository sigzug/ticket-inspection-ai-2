from django.urls import path

from .views import UseModelView, health

urlpatterns = [
    path("health/", health, name="health"),
    path("use-model/", UseModelView.as_view(), name="use_model"),
]
