from django.urls import path

from backend.apps.interact.views import get_categories, run_model
from backend.apps.interact.csrf import csrf_token

urlpatterns = [
    path("categories/", get_categories),
    path("run_model/", run_model),
    path("csrf/", csrf_token),
]
