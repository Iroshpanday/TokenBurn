from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Project
from .services import AIService


class ChatView(APIView):

    def post(self, request):

        message = request.data.get("message")
        project_id = request.data.get("project_id")
        organization_id = request.data.get("organization_id")

        if not message or not project_id or not organization_id:
            return Response(
                {"error": "message, project_id and organization_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project = get_object_or_404(Project, id=project_id)

        result = AIService.generate_response(message, project, organization_id)

        return Response(result, status=status.HTTP_200_OK)
