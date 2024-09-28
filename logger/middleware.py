from .models import LogEntry
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ip = (
            request.META.get("HTTP_X_FORWARDED_FOR").split(",")[-1].strip()
            if request.META.get("HTTP_X_FORWARDED_FOR")
            else request.META.get("REMOTE_ADDR")
        )
        user = None
        message = ""

        if request.path == "/jwt/login/" and request.method == "POST":

            try:
                if response.status_code != 200:
                    raise ValueError("Fail Request")

                user = User.objects.get(username=request.POST.get("username"))
                message = (
                    f"Status Code: {response.status_code} - {response.status_text}"
                )

            except:
                message = f"Status Code: {response.status_code} - {response.status_text}\nData: {response.data}"

        elif request.path == "/jwt/token/refresh/" and request.method == "POST":
            try:
                token = RefreshToken(response.data.get("refresh"))
                user_id = token["user_id"]
                user = User.objects.get(id=user_id)
                message = (
                    f"Status Code: {response.status_code} - {response.status_text}"
                )

            except:
                message = f"Status Code: {response.status_code} - {response.status_text}\nData: {response.data}"

        elif request.path.startswith("/document/") and request.method == "GET":
            split_path = request.path.split("/")
            clean_split_path = [item for item in split_path if item]
            document_id = clean_split_path[1]

            try:
                auth_header = request.META.get("HTTP_AUTHORIZATION")
                if not auth_header:
                    raise ValueError("do not have token")

                token = auth_header.split(" ")[1]
                token = AccessToken(token)
                user_id = token["user_id"]
                user = User.objects.get(id=user_id)
                message = f"Status Code: {response.status_code} - {response.status_text}\nDocument ID: {document_id}"

            except:
                message = f"Status Code: {response.status_code} - {response.status_text}\nDocument ID: {document_id}\nData: {response.data}"

        if message:
            LogEntry.objects.create(
                path=request.path,
                method=request.method,
                user=user,
                ip_address=f"{ip}",
                message=message,
            )

        return response
