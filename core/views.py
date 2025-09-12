from django.http import HttpResponse
from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import ComputeRequest, ComputeResponse
from .services import compute


def health(_):
    return HttpResponse("ok")


class ComputeView(APIView):
    """
    POST /api/compute
    {
      "numbers": [1, 2, 3.5],
      "op": "avg"  # sum | avg | max | min
    }
    """

    def post(self, request):
        try:
            payload = ComputeRequest.model_validate(request.data)
        except ValidationError as e:
            # Pydantic v2 gir gode feilmeldinger til frontend
            return Response({"detail": e.errors()}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            value = compute(payload.numbers, payload.op)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        resp = ComputeResponse(operation=payload.op, count=len(payload.numbers), result=value)
        return Response(resp.model_dump(), status=status.HTTP_200_OK)
