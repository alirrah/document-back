from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import Document
from .views import DocumentDetail
from django.contrib.auth import get_user_model

User = get_user_model()


class DocumentDetailTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.document = Document.objects.create(
            title="Test Document", content="This is a test document."
        )

    def test_get_document_success(self):
        request = self.factory.get("/document/" + str(self.document.pk) + "/")
        force_authenticate(request, user=self.user)
        response = DocumentDetail.as_view()(request, pk=self.document.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.document.title)
        self.assertEqual(response.data["content"], self.document.content)

    def test_get_document_not_found(self):
        pk_not_exist = 999
        request = self.factory.get("/document/" + str(pk_not_exist) + "/")
        force_authenticate(request, user=self.user)
        response = DocumentDetail.as_view()(request, pk=pk_not_exist)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Document not found")

    def test_get_document_unauthenticated(self):
        request = self.factory.get("/document/" + str(self.document.pk) + "/")
        response = DocumentDetail.as_view()(request, pk=self.document.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
