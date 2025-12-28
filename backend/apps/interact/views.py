from urllib.request import Request

from django.http import JsonResponse

from backend.apps.interact import services


# Create your views here.
def get_categories(request: Request) -> JsonResponse:
    # Logic to get categories
    categories = services.load_in_model_categories()
    serialized_categories = {name: cat.categories.to_list() for name, cat in categories.items()}
    return JsonResponse({"categories": serialized_categories})


def run_model(request: Request) -> JsonResponse:
    return JsonResponse({"res": "yes"})
