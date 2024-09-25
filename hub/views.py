from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Document
from .serializers import DocumentSerializer


class DocumentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND
            )
