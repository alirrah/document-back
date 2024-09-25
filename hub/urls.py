from django.urls import path
from .views import DocumentDetail

urlpatterns = [path("<int:pk>/", DocumentDetail.as_view(), name="document-detail")]
