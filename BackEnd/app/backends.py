import hashlib
import hmac

from django.contrib.auth.backends import BaseBackend
from .models import User
from django.contrib.auth.hashers import check_password
from .exceptions.exceptions import Unauthorized
import bcrypt

from .secret import SECRET_KEY


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username_or_email, password=None):

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                if self.check_password(password, user.password_hash):
                    return user
                else:
                    raise Unauthorized("Invalid Password")
            except User.DoesNotExist:
                pass
        else:
            try:
                # print(username)
                user = User.objects.get(username=username_or_email)
                if self.check_password(password, user.password_hash):  # and user.is_account_verified
                    return user
                else:
                    raise Unauthorized("Invalid Password")
            except User.DoesNotExist:
                pass

    def get_user(self, user_id):
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None

    def check_password(self, password, hashed_password):

        h = hmac.new(SECRET_KEY.encode(), digestmod=hashlib.sha256)
        h.update(password.encode())
        return hashed_password == h.hexdigest()
