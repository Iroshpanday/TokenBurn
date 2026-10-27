from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import AIService


class ChatView(APIView):

    def post(self, request):

        message = request.data.get("message")

        if not message:
            return Response(
                {"error": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        answer = AIService.generate_response(message)

        return Response(
            {"response": answer},
            status=status.HTTP_200_OK,
        )