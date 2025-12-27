from django.urls import path

from backend.apps.interact.views import get_categories


urlpatterns = [path("categories/", get_categories)]
