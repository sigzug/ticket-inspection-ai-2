# CSRF helper endpoint: sets 'csrftoken' cookie and returns the token
from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf_token(request):
    token = get_token(request)  # ensures CSRF cookie is set
    return JsonResponse({"csrfToken": token})
