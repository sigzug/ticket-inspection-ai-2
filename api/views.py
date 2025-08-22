from django.http import HttpResponse


def index(request):
    return HTTPResponse("Hello, world! This is the API index page.")
