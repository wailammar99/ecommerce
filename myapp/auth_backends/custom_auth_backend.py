from django.contrib.auth.backends import ModelBackend
from .models import client  # Import your Client model

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = client.objects.get(username=username)
            if user.password:
                return user
        except client.DoesNotExist:
            return None