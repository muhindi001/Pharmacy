from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError


class UUIDCompatibleBackend(ModelBackend):
    def get_user(self, user_id):
        if not user_id:
            return None

        user_model = get_user_model()
        if isinstance(user_id, int):
            return user_model.objects.filter(pk=user_id).first()

        if isinstance(user_id, str):
            try:
                return user_model.objects.get(pk=user_id)
            except (ValidationError, user_model.DoesNotExist, TypeError, ValueError):
                return None

        try:
            return user_model.objects.get(pk=user_id)
        except (ValidationError, user_model.DoesNotExist, TypeError, ValueError):
            return None
