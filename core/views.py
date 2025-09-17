from django.http import HttpResponse
from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import UseModelRequest
from .services import run_model


def health(_):
    return HttpResponse("ok")


class UseModelView(APIView):
    def get(self, request):
        try:
            payload = UseModelRequest.model_validate(request.data)
        except ValidationError as e:
            return Response({"detail": e.errors()}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        value = run_model(payload)
        return Response(value.model_dump(), status=status.HTTP_200_OK)